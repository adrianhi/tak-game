import numpy as np

import board


class MinimaxAI:
    def __init__(self):
        self.nodes_explored = 0

    def choose_move(self, board, max_depth=3):
        """
        Retorna el mejor movimiento para el jugador actual del tablero
        utilizando Iterative Deepening Search (IDS) sobre Minimax con poda Alpha-Beta.
        """
        self.nodes_explored = 0
        ai_player = board.current_player

        overall_best_move = None

        moves = board.get_available_decisions()
        if not moves:
            return None

        # Iterative Deepening Loop
        for depth in range(1, max_depth + 1):
            best_score = -np.inf
            best_move_this_iteration = None
            alpha = -np.inf
            beta = np.inf

            # Simple Move Ordering: probar el mejor movimiento de la iteración anterior primero
            if overall_best_move in moves:
                moves.remove(overall_best_move)
                moves.insert(0, overall_best_move)

            for move in moves:
                clone = board.clone()
                clone.apply_move(move)

                score = self._alphabeta(clone, depth - 1, alpha, beta, False, ai_player)

                if score > best_score:
                    best_score = score
                    best_move_this_iteration = move

                # Actualizamos alpha en la raíz
                alpha = max(alpha, best_score)

            # Guardamos el mejor movimiento de esta profundidad
            overall_best_move = best_move_this_iteration

            print(
                f"-> Profundidad actual: {depth} | Score: {best_score} | Nodos acumulados: {self.nodes_explored}"
            )

        print(f"\n=> Búsqueda IDS completada hasta profundidad {max_depth}.")
        print(
            f"=> Total de nodos evaluados (IDS + Alpha-Beta): {self.nodes_explored}\n"
        )

        return overall_best_move

    def _alphabeta(self, board, depth, alpha, beta, maximizing, ai_player):
        """
        Implementación recursiva del algoritmo Minimax con poda Alpha-Beta.
        """
        self.nodes_explored += 1

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

                eval_score = self._alphabeta(
                    clone, depth - 1, alpha, beta, False, ai_player
                )

                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)

                # Poda Alpha-Beta
                if beta <= alpha:
                    break

            return max_eval

        else:
            min_eval = np.inf

            for move in moves:
                clone = board.clone()
                clone.apply_move(move)

                eval_score = self._alphabeta(
                    clone, depth - 1, alpha, beta, True, ai_player
                )

                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)

                # Poda Alpha-Beta
                if beta <= alpha:
                    break

            return min_eval

    def debug_root(self, board, depth=2):
        """
        Evalúa todos los movimientos en el nivel raíz e imprime sus scores.
        Incluye poda al nivel raíz.
        """
        self.nodes_explored = 0
        ai_player = board.current_player
        moves = board.get_available_decisions()

        print(f"\n--- Debug Alpha-Beta (depth={depth}) ---")
        print("Jugador IA:", ai_player)
        print("Movimientos disponibles en raíz:", len(moves))
        print()

        best_score = -np.inf
        best_move = None
        alpha = -np.inf
        beta = np.inf

        for move in moves:
            clone = board.clone()
            clone.apply_move(move)

            score = self._alphabeta(clone, depth - 1, alpha, beta, False, ai_player)

            print("Movimiento:", move)
            print("Score:", score)
            print("-------------------------")

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)

        print("\n>>> Mejor movimiento:", best_move)
        print(">>> Mejor score:", best_score)
        print(">>> Nodos evaluados en total:", self.nodes_explored)
        print("---------------------------------\n")

        return best_move
