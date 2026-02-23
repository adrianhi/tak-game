import time
import numpy as np


class WorstAI:
    def __init__(self, evaluation_function):
        """
        Inicializa la IA Worst con la función de evaluación heurística.
        """
        self.nodes_explored = 0
        self.evaluate = evaluation_function

    def choose_move(self, board, max_depth=None, max_time=None):
        """
        Retorna el movimiento que minimice el valor inmediato en el tablero,
        usando la función de evaluación.
        """
        self.nodes_explored = 0
        ai_player = board.current_player

        moves = board.get_available_decisions()
        if not moves:
            return None

        worst_score = float("inf")
        worst_move = None

        for move in moves:
            clone = board.clone()
            clone.apply_move(move)

            self.nodes_explored += 1

            # evaluate value for current player
            score = self.evaluate(clone, ai_player)

            if score < worst_score:
                worst_score = score
                worst_move = move

        return worst_move
