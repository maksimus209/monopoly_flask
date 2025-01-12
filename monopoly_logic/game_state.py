from monopoly_logic.player import Player

class GameState:
    def __init__(self, board, num_players=5):
        self.board = board
        self.players = [
            Player(name=str(i + 1), color=color)
            for i, color in enumerate(["red", "blue", "green", "yellow", "purple"][:num_players])
        ]
        self.active_player_index = 0  # Pierwszy gracz zaczyna

    def get_players(self):
        return self.players

    def move_active_player(self, steps):
        active_player = self.players[self.active_player_index]
        new_position = active_player.move(steps)
        current_field = self.board.get_field_by_position(new_position)  # Pobierz dane pola
        self.next_turn()  # Przejdź do następnego gracza
        return active_player, current_field["name"]  # Zwróć nazwę pola

    def next_turn(self):
        self.active_player_index = (self.active_player_index + 1) % len(self.players)

    def check_game_over(self):
        active_players = [player for player in self.players if player.balance > 0]
        return len(active_players) == 1  # Gra kończy się, gdy zostaje jeden gracz
