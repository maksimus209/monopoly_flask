from flask import Flask, render_template, jsonify
from monopoly_logic.board import Board
from monopoly_logic.game_state import GameState

# Inicjalizacja aplikacji Flask
app = Flask(
    __name__,
    template_folder='templates',  # Lokalizacja plików HTML
    static_folder='static'        # Lokalizacja plików CSS/JS
)

# Inicjalizacja planszy i stanu gry
board = Board()
game_state = GameState(board)

# Strona główna
@app.route('/')
def index():
    return render_template('index.html')

# Strona gry
@app.route('/game')
def game():
    fields = board.get_fields()  # Pobierz pola planszy
    players = game_state.get_players()  # Pobierz graczy
    return render_template('game.html', fields=fields, players=players, board=board)  # Przekaż dane do szablonu

# API do rzutu kostką
@app.route('/roll-dice')
def roll_dice():
    import random
    dice_roll = random.randint(1, 6) + random.randint(1, 6)  # Rzut dwiema kostkami
    active_player, new_position = game_state.move_active_player(dice_roll)
    return jsonify({
        "player": active_player.name,  # Imię aktywnego gracza
        "new_position": new_position,  # Nowa pozycja na planszy
        "dice_roll": dice_roll         # Wynik rzutu kostkami
    })

# Uruchomienie aplikacji
if __name__ == '__main__':
    app.run(debug=True)
