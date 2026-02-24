import numpy as np
import time


class MinimaxAI:
    def __init__(self, num_heuristics=5, weight_config=1):
        self.nodes_explored = (
            0  # Mantengo este para compatibilidad retrospectiva si es necesario
        )
        self.nodes_last_move = 0
        self.nodes_total = 0
        self.all_heuristics = [
            self.h_flats,
            self.h_connected_group,
            self.h_reserves,
            self.h_center_control,
            self.h_mobility,
        ]
        self.active_heuristics = self.all_heuristics[:num_heuristics]

        if weight_config == 1:
            self.weights = {
                "flats": 2,
                "connected": 5,
                "reserves": 1,
                "center": 2,
                "mobility": 1,
            }
        else:
            self.weights = {
                "flats": 4,
                "connected": 3,
                "reserves": 2,
                "center": 4,
                "mobility": 2,
            }

    def choose_move(self, board, max_depth=3, max_time=5):
        """
        Retorna el mejor movimiento para el jugador actual del tablero
        utilizando Iterative Deepening Search (IDS) sobre Minimax con poda Alpha-Beta
        y con un límite de tiempo configurable.
        """
        self.nodes_explored = 0
        self.nodes_last_move = 0
        self.start_time = time.time()
        self.max_time = max_time
        self.time_up = False

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

                # Si el tiempo se agotó mientras exploraba, ignoramos este avance parcial
                if self.time_up:
                    break

                if score > best_score:
                    best_score = score
                    best_move_this_iteration = move

                # Actualizamos alpha en la raíz
                alpha = max(alpha, best_score)

            if self.time_up:
                print(f"-> ¡Tiempo agotado! (Cortando búsqueda en profundidad {depth})")
                break

            # Guardamos el mejor movimiento de esta profundidad de forma segura
            # (solo si completó el nivel sin ser cortado por tiempo o si es el primero)
            if best_move_this_iteration is not None:
                overall_best_move = best_move_this_iteration

            print(
                f"-> Profundidad actual: {depth} | Score: {best_score} | Nodos acumulados (iteración): {self.nodes_last_move}"
            )

        self.nodes_total += self.nodes_last_move

        print(f"\n=> Búsqueda IDS completada hasta profundidad {max_depth}.")
        print(
            f"=> Total de nodos evaluados (IDS + Alpha-Beta): {self.nodes_last_move}\n"
        )

        return overall_best_move

    def _alphabeta(self, board, depth, alpha, beta, maximizing, ai_player):
        """
        Implementación recursiva del algoritmo Minimax con poda Alpha-Beta.
        """
        # Chequeo de tiempo
        if time.time() - self.start_time >= self.max_time:
            self.time_up = True
            return self.evaluate(board, ai_player)

        self.nodes_explored += 1
        self.nodes_last_move += 1

        # Caso base
        if depth == 0 or board.is_terminal():
            return self.evaluate(board, ai_player)

        moves = board.get_available_decisions()

        if not moves:
            return self.evaluate(board, ai_player)

        if maximizing:
            max_eval = -np.inf

            for move in moves:
                clone = board.clone()
                clone.apply_move(move)

                eval_score = self._alphabeta(
                    clone, depth - 1, alpha, beta, False, ai_player
                )

                if self.time_up:
                    break

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

                if self.time_up:
                    break

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
        self.nodes_last_move = 0
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
        print(">>> Nodos evaluados en total:", self.nodes_last_move)
        print("---------------------------------\n")

        return best_move

    def evaluate(self, board, player):
        opponent = "black" if player == "white" else "white"

        # Caso terminal
        if board.is_terminal():
            winner = board.get_winner()
            if winner == player:
                return 100000
            elif winner == opponent:
                return -100000
            else:
                return 0

        score = 0
        if self.h_flats in self.active_heuristics:
            score += self.weights["flats"] * self.h_flats(board, player)
        if self.h_connected_group in self.active_heuristics:
            score += self.weights["connected"] * self.h_connected_group(board, player)
        if self.h_reserves in self.active_heuristics:
            score += self.weights["reserves"] * self.h_reserves(board, player)
        if self.h_center_control in self.active_heuristics:
            score += self.weights["center"] * self.h_center_control(board, player)
        if self.h_mobility in self.active_heuristics:
            score += self.weights["mobility"] * self.h_mobility(board, player)

        return score

    # Heuristics
    def h_flats(self, board, player):
        """
        Heurística que cuenta las piezas planas del jugador y las del oponente.
        """
        opponent = "black" if player == "white" else "white"
        my_flats = board._count_visible_flats(player)
        opp_flats = board._count_visible_flats(opponent)
        return my_flats - opp_flats

    def h_connected_group(self, board, player):
        """
        Heurística que cuenta el tamaño del grupo conectado más grande del jugador y del oponente.
        """
        opponent = "black" if player == "white" else "white"
        my_group = board._largest_connected_group(player)
        opp_group = board._largest_connected_group(opponent)
        return my_group - opp_group

    def h_reserves(self, board, player):
        """
        Heurística que cuenta las piezas de reserva del jugador y las del oponente.
        """
        opponent = "black" if player == "white" else "white"
        my_reserve = sum(board.pieces[player].values())
        opp_reserve = sum(board.pieces[opponent].values())
        return my_reserve - opp_reserve

    def h_center_control(self, board, player):
        """
        Heurística que cuenta el control del centro del tablero por parte del jugador y del oponente.
        """
        center = board.size // 2
        score = 0
        for r in range(board.size):
            for c in range(board.size):
                stack = board.board[r][c]
                if stack:
                    owner = stack[-1][0]
                    dist = abs(r - center) + abs(c - center)
                    val = max(0, 2 - dist)
                    if owner == player:
                        score += val
                    else:
                        score -= val
        return score

    def h_mobility(self, board, player):
        """
        Heurística que cuenta la movilidad del jugador y del oponente.
        """
        my_stacks = 0
        opp_stacks = 0
        for r in range(board.size):
            for c in range(board.size):
                stack = board.board[r][c]
                if stack:
                    if stack[-1][0] == player:
                        my_stacks += 1
                    else:
                        opp_stacks += 1
        return my_stacks - opp_stacks
