import random
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "super_secret_key"

# ----------------------------------------------------
# Ustawienia GRY
# ----------------------------------------------------
NUM_PLAYERS = 4
BOARD_SIZE = 40
HOME_LENGTH = 4
MAX_6_ROLLS = 3

START_FIELDS = [0, 10, 20, 30]
PLAYER_COLORS = ["czerwony", "niebieski", "zielony", "żółty"]

def roll_dice():
    return random.randint(1, 6)

def next_player(current):
    return (current + 1) % NUM_PLAYERS

def init_game_state():
    positions = []
    for _ in range(NUM_PLAYERS):
        positions.append([None, None, None, None])
    return {
        'positions': positions,
        'current_player': 0,
        'rolls_in_a_row': 0,
        'last_roll': 0,
        'nickname': ["Gracz", "AI1", "AI2", "AI3"],
        'colors': PLAYER_COLORS,
        'winner': None
    }

def is_ai_player(p):
    return p != 0

def get_start_field(p):
    return START_FIELDS[p]

def get_home_range(p):
    start_home = 40 + p * HOME_LENGTH
    end_home = start_home + HOME_LENGTH - 1
    return (start_home, end_home)

def do_capture_if_any(state, p, new_pos):
    if not (0 <= new_pos < BOARD_SIZE):
        return
    positions = state['positions']
    for other in range(NUM_PLAYERS):
        if other == p:
            continue
        for i in range(4):
            if positions[other][i] == new_pos:
                positions[other][i] = None

def move_pawn(state, p, pawn_idx, steps):
    positions = state['positions']
    current_pos = positions[p][pawn_idx]

    if current_pos is None:
        if steps == 6:
            start_pos = get_start_field(p)
            do_capture_if_any(state, p, start_pos)
            positions[p][pawn_idx] = start_pos
        else:
            return
    elif isinstance(current_pos, int) and 0 <= current_pos < BOARD_SIZE:
        home_start, home_end = get_home_range(p)
        distance_to_home = (get_start_field(p) - current_pos) % BOARD_SIZE
        if steps > distance_to_home:
            leftover = steps - distance_to_home
            home_pos = home_start + (leftover - 1)
            if home_pos > home_end:
                positions[p][pawn_idx] = 'in_dome'
            else:
                positions[p][pawn_idx] = home_pos
        else:
            new_pos = (current_pos + steps) % BOARD_SIZE
            do_capture_if_any(state, p, new_pos)
            positions[p][pawn_idx] = new_pos
    elif isinstance(current_pos, int) and 40 <= current_pos <= 55:
        home_start, home_end = get_home_range(p)
        new_home_pos = current_pos + steps
        if new_home_pos > home_end:
            positions[p][pawn_idx] = 'in_dome'
        else:
            positions[p][pawn_idx] = new_home_pos
    else:
        pass

def check_winner(state):
    positions = state['positions']
    for p in range(NUM_PLAYERS):
        in_dome_count = sum(1 for pos in positions[p] if pos == 'in_dome')
        if in_dome_count == 4:
            return p
    return None

def all_pawns_blocked_or_in_dome(state, p):
    positions = state['positions'][p]
    roll = state['last_roll']
    can_out = (roll == 6)
    for pos in positions:
        if pos is None:
            if can_out:
                return False
        elif pos != 'in_dome':
            return False
    return True

def calc_final_position(state, p, pawn_idx, steps):
    pos = state['positions'][p][pawn_idx]
    if pos is None:
        return get_start_field(p)
    elif isinstance(pos, int) and 0 <= pos < BOARD_SIZE:
        home_start, home_end = get_home_range(p)
        distance_to_home = (get_start_field(p) - pos) % BOARD_SIZE
        if steps > distance_to_home:
            leftover = steps - distance_to_home
            home_pos = home_start + (leftover - 1)
            if home_pos > home_end:
                return 9999
            else:
                return home_pos
        else:
            return (pos + steps) % BOARD_SIZE
    elif isinstance(pos, int) and 40 <= pos <= 55:
        home_start, home_end = get_home_range(p)
        new_home = pos + steps
        if new_home > home_end:
            return 9999
        else:
            return new_home
    else:
        return pos

def do_ai_move(state):
    cp = state['current_player']
    roll = state['last_roll']
    pos_arr = state['positions'][cp]

    possible_moves = []
    for i in range(4):
        if pos_arr[i] == 'in_dome':
            continue
        if pos_arr[i] is None:
            if roll == 6:
                possible_moves.append((i, get_start_field(cp)))
        else:
            finalp = calc_final_position(state, cp, i, roll)
            possible_moves.append((i, finalp))

    if not possible_moves:
        return

    # 1) zbijanie
    capture_moves = []
    for i, finalp in possible_moves:
        if 0 <= finalp < BOARD_SIZE:
            for other in range(NUM_PLAYERS):
                if other == cp:
                    continue
                for j in range(4):
                    if state['positions'][other][j] == finalp:
                        capture_moves.append((i, finalp))
                        break
    if capture_moves:
        i, _ = capture_moves[0]
        move_pawn(state, cp, i, roll)
        return

    # 2) z bazy
    out_of_base = []
    for i, finalp in possible_moves:
        if pos_arr[i] is None:
            out_of_base.append((i, finalp))
    if out_of_base:
        i, _ = out_of_base[0]
        move_pawn(state, cp, i, roll)
        return

    # 3) pionek najdalej od startu
    best_dist = -1
    best_i = None
    for i, finalp in possible_moves:
        cpos = pos_arr[i]
        if isinstance(cpos, int) and 0 <= cpos < BOARD_SIZE:
            startf = get_start_field(cp)
            dist = (cpos - startf) % BOARD_SIZE
            if dist > best_dist:
                best_dist = dist
                best_i = i
    if best_i is not None:
        move_pawn(state, cp, best_i, roll)
        return

    # 4) pierwszy
    i, _ = possible_moves[0]
    move_pawn(state, cp, i, roll)


# ----------------------------------------------------
# Widoki Flask
# ----------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_game', methods=['GET','POST'])
def new_game():
    """
    Widok do wyboru trybu:
    - Po wybraniu 'computer', przekierowujemy do configure_player
    - w config_player user poda nickname, color i wtedy tworzymy stan gry
    """
    if request.method == 'POST':
        mode = request.form.get('mode')
        if mode == 'computer':
            return redirect(url_for('configure_player'))
        else:
            return "Inne tryby w budowie!"
    return render_template('new_game.html')

@app.route('/configure_player', methods=['GET','POST'])
def configure_player():
    """
    User podaje nickname i color
    Po wysłaniu formularza -> tworzymy stan gry, ustawiamy session i redirect do /game
    """
    if request.method == 'POST':
        # Tworzymy stan gry
        state = init_game_state()

        nickname = request.form.get('nickname', 'Gracz1')
        color = request.form.get('color', 'czerwony')
        state['nickname'][0] = nickname
        state['colors'][0] = color

        session['game_state'] = state
        return redirect(url_for('game'))

    return render_template('configure_player.html')

@app.route('/load_game')
def load_game():
    return "Funkcja wczytania gry w budowie."

@app.route('/results')
def results():
    return "Tu możesz docelowo wyświetlać listę wyników."

@app.route('/instructions')
def instructions():
    return "Instrukcja: Chińczyk z 4 graczami (1 ludzki + 3 AI)."

@app.route('/game', methods=['GET','POST'])
def game():
    if 'game_state' not in session:
        return redirect(url_for('new_game'))

    state = session['game_state']
    if state['winner'] is not None:
        return render_template('game.html', game_state=state)

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'roll':
            val = roll_dice()
            state['last_roll'] = val
            state['rolls_in_a_row'] += 1
            if val != 6:
                state['rolls_in_a_row'] = 0

        elif action.startswith('move_'):
            i = int(action.split('_')[1])
            cp = state['current_player']
            val = state['last_roll']
            move_pawn(state, cp, i, val)

            w = check_winner(state)
            if w is not None:
                state['winner'] = w
            else:
                if val == 6 and state['rolls_in_a_row'] < MAX_6_ROLLS:
                    pass
                else:
                    state['current_player'] = next_player(cp)
                    state['last_roll'] = 0
                    state['rolls_in_a_row'] = 0

        session['game_state'] = state
        return redirect(url_for('game'))

    # GET -> sprawdzamy, czy AI ma ruch
    cp = state['current_player']
    if is_ai_player(cp):
        if state['last_roll'] == 0:
            val = roll_dice()
            state['last_roll'] = val
            state['rolls_in_a_row'] += 1
            if val != 6:
                state['rolls_in_a_row'] = 0
            session['game_state'] = state
            return redirect(url_for('game'))

        if not all_pawns_blocked_or_in_dome(state, cp):
            do_ai_move(state)
            w = check_winner(state)
            if w is not None:
                state['winner'] = w
            else:
                if state['last_roll'] == 6 and state['rolls_in_a_row'] < MAX_6_ROLLS:
                    state['last_roll'] = 0
                else:
                    state['current_player'] = next_player(cp)
                    state['last_roll'] = 0
                    state['rolls_in_a_row'] = 0
        else:
            state['current_player'] = next_player(cp)
            state['last_roll'] = 0
            state['rolls_in_a_row'] = 0

        session['game_state'] = state
        return redirect(url_for('game'))

    return render_template('game.html', game_state=state)


if __name__ == '__main__':
    app.run(debug=True)
