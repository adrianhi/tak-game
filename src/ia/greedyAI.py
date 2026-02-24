import time
import numpy as np


class GreedyAI:
    def __init__(self, evaluation_function):
        """
        Inicializa la IA Greedy con la función de evaluación heurística.
        """
        self.nodes_explored = 0
        self.evaluate = evaluation_function

    def choose_move(self, board, max_depth=None, max_time=None):
        """
        Retorna el movimiento que maximice el valor inmediato en el tablero,
        usando la función de evaluación.
        """
        self.nodes_explored = 0
        ai_player = board.current_player

        moves = board.get_available_decisions()
        if not moves:
            return None

        best_score = -np.inf
        best_move = None

        for move in moves:
            clone = board.clone()
            clone.apply_move(move)

            self.nodes_explored += 1

            # evaluate value for current player
            score = self.evaluate(clone, ai_player)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move
