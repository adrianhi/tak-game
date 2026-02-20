import numpy as np

import board


class MinimaxAI:
    def choose_move(self, board, depth=3):
        """
        Retorna el mejor movimiento para el jugador actual del tablero.
        """

        ai_player = board.current_player
        best_score = -np.inf
        best_move = None

        moves = board.get_available_decisions()

        if not moves:
            return None

        for move in moves:
            clone = board.clone()
            clone.apply_move(move)

            score = self._minimax(
                clone, depth - 1, maximizing=False, ai_player=ai_player
            )

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _minimax(self, board, depth, maximizing, ai_player):
        """
        Implementación recursiva del algoritmo Minimax.
        """
        # Caso base
        if depth == 0 or board.is_terminal():
            return board.evaluate(ai_player)

        moves = board.get_available_decisions()

        if not moves:
            return board.evaluate(ai_player)

        if maximizing:
            max_eval = -np.inf

            for move in moves:
                clone = board.clone()
                clone.apply_move(move)

                eval_score = self._minimax(
                    clone, depth - 1, maximizing=False, ai_player=ai_player
                )

                max_eval = max(max_eval, eval_score)

            return max_eval

        else:
            min_eval = np.inf

            for move in moves:
                clone = board.clone()
                clone.apply_move(move)

                eval_score = self._minimax(
                    clone, depth - 1, maximizing=True, ai_player=ai_player
                )

                min_eval = min(min_eval, eval_score)

            return min_eval

    def debug_root(self, board, depth=2):
        """
        Evalúa todos los movimientos en el nivel raíz e imprime sus scores.
        """
        ai_player = board.current_player
        moves = board.get_available_decisions()

        print(f"\n--- Debug Minimax (depth={depth}) ---")
        print("Jugador IA:", ai_player)
        print("Movimientos disponibles:", len(moves))
        print()

        best_score = -np.inf
        best_move = None

        for move in moves:
            clone = board.clone()
            clone.apply_move(move)

            score = self._minimax(
                clone, depth - 1, maximizing=False, ai_player=ai_player
            )

            print("Movimiento:", move)
            print("Score:", score)
            print("-------------------------")

            if score > best_score:
                best_score = score
                best_move = move

        print("\n>>> Mejor movimiento:", best_move)
        print(">>> Mejor score:", best_score)
        print("---------------------------------\n")

        return best_move
