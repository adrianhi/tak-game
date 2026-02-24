import random


class RandomAI:
    def __init__(self):
        self.nodes_explored = 0

    def choose_move(self, board, max_depth=3, max_time=5):
        """
        Retorna un movimiento aleatorio válido para el jugador actual.
        La firma coincide con MinimaxAI para permitir intercambiabilidad.
        """
        self.nodes_explored = 1
        moves = board.get_available_decisions()
        if not moves:
            return None

        move = random.choice(moves)
        return move
