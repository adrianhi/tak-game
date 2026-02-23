from collections import deque
from copy import deepcopy
from core.rules import TakRuleEngine


class TakBoard:
    """
    Clase que representa el tablero de Tak y contiene la lógica de negocio.
    Mantiene el estado de las celdas, las piezas y los turnos.
    """

    def __init__(self, size=5):
        """
        Inicializa el tablero de Tak
        size: tamaño del tablero (típicamente 3, 4, 5, 6, o 8)
        """
        self.size = size
        # El tablero es una matriz donde cada celda puede contener una pila de piezas
        # Cada celda es una lista: [] vacío, o lista de tuplas (jugador, tipo)
        # tipo: 'F' = piedra plana, 'S' = piedra de pie, 'C' = capstone
        self.board = [[[] for _ in range(size)] for _ in range(size)]

        # Piezas disponibles para cada jugador
        self.pieces = {
            "white": {
                "flat": self._get_initial_pieces(size),
                "capstones": self._get_capstones(size),
            },
            "black": {
                "flat": self._get_initial_pieces(size),
                "capstones": self._get_capstones(size),
            },
        }

        self.current_player = "white"

        # Contador de "plies" (medios turnos).
        # 0 = Turno 1 Blancas, 1 = Turno 1 Negras, 2 = Turno 2 Blancas (Normal)...
        self.ply_count = 0

        # Motor de reglas
        self.rules = TakRuleEngine()

    def clone(self):
        """
        Creates a deep copy of the board for simulation (Minimax).
        Returns a new TakBoard instance with identical state.
        """
        return deepcopy(self)

    def _get_initial_pieces(self, size):
        """Retorna el número de piedras planas según el tamaño del tablero"""
        pieces_map = {3: 10, 4: 15, 5: 21, 6: 30, 8: 50}
        return pieces_map.get(size, 21)

    def _get_capstones(self, size):
        """Retorna el número de piedras angulares (capstones) según el tamaño del tablero"""
        capstones_map = {3: 0, 4: 0, 5: 1, 6: 1, 8: 2}
        return capstones_map.get(size, 1)

    def _is_inside(self, row, col):
        """Retorna True si (row, col) está dentro del tablero."""
        return 0 <= row < self.size and 0 <= col < self.size

    def _top_piece(self, row, col):
        """Retorna la pieza superior de una celda o None si está vacía."""
        stack = self.board[row][col]
        return stack[-1] if stack else None

    def _is_road_piece(self, row, col, player):
        """Retorna True si la pieza superior pertenece al jugador y cuenta para camino."""
        top_piece = self._top_piece(row, col)
        return bool(top_piece and top_piece[0] == player and top_piece[1] in ["F", "C"])

    def can_place_piece(self, row, col, piece_type="F"):
        """
        Valida si se puede colocar una pieza en la posición dada
        """
        # Validar límites
        if not self._is_inside(row, col):
            return False, "Posición fuera del tablero."

        # Validar celda vacía
        if self.board[row][col]:
            return False, "La casilla ya está ocupada."

        # Validar disponibilidad de piezas
        pieces = self.pieces[self.current_player]
        if piece_type == "C":
            if pieces["capstones"] <= 0:
                return False, "No te quedan Piedras angulares."
        else:
            if pieces["flat"] <= 0:
                return False, "No te quedan piedras planas."

        return True, ""

    def place_piece(self, row, col, piece_type="F", color=None):
        """
        Coloca una pieza en el tablero
        row, col: posición (0-indexed)
        piece_type: 'F' = flat, 'S' = standing, 'C' = capstone
        """
        allowed, message = self.can_place_piece(row, col, piece_type)
        if not allowed:
            return False, message

        # Si no se especifica color, delegar a las reglas para determinarlo
        piece_color = color if color else self.rules.get_turn_color(self)

        self.board[row][col].append((piece_color, piece_type))

        # Actualizar piezas disponibles (del color de la pieza, no necesariamente del jugador actual)
        if piece_type == "C":
            self.pieces[piece_color]["capstones"] -= 1
        else:
            self.pieces[piece_color]["flat"] -= 1

        # Cambio de turno
        self.next_turn()
        return True, "Pieza colocada."

    def can_move_stack(self, row, col):
        """Valida si el jugador actual controla la pila en (row, col)"""
        if not self._is_inside(row, col):
            return False
        top_piece = self._top_piece(row, col)
        if not top_piece:
            return False
        # El dueño de la pieza superior controla la pila
        return top_piece[0] == self.current_player

    def move_stack(self, start_row, start_col, direction, drops):
        """
        Mueve una pila de piezas.
        direction: 'U', 'D', 'L', 'R'
        drops: lista de enteros indicando cuántas piezas dejar en cada paso
        """
        # 1️⃣ Validar movimiento
        allowed, message = self._validate_stack_move(
            start_row, start_col, direction, drops
        )
        if not allowed:
            return False, message

        # 2️⃣ Preparar datos del movimiento
        stack = self.board[start_row][start_col]
        picked_up_count = sum(drops)

        # Tomar piezas desde arriba (orden correcto)
        moving_stack = stack[-picked_up_count:]
        left_stack = stack[:-picked_up_count]

        # Actualizar pila original
        self.board[start_row][start_col] = left_stack

        # Dirección
        deltas = {
            "U": (-1, 0),
            "D": (1, 0),
            "L": (0, -1),
            "R": (0, 1),
        }
        dr, dc = deltas[direction.upper()]

        current_r, current_c = start_row, start_col
        pieces_dropped_so_far = 0

        # 3️⃣ Ejecutar distribución
        for drop_count in drops:
            current_r += dr
            current_c += dc

            substack = moving_stack[
                pieces_dropped_so_far : pieces_dropped_so_far + drop_count
            ]
            target_stack = self.board[current_r][current_c]

            # Aplastar muro si corresponde (ya validado)
            if target_stack and target_stack[-1][1] == "S":
                owner, _ = target_stack.pop()
                target_stack.append((owner, "F"))

            # Colocar piezas
            target_stack.extend(substack)
            pieces_dropped_so_far += drop_count

        # 4️⃣ Cambiar turno
        self.next_turn()
        return True, "Movimiento realizado exitosamente."

    def apply_move(self, move):
        """
        Aplica un movimiento genérico al tablero.
        El movimiento debe venir en el formato generado por get_available_decisions().

        move: dict con estructura:
            - Place:
                {
                    "type": "place",
                    "pos": (r, c),
                    "piece": "F" | "S" | "C",
                    "color": "white" | "black"
                }
            - Move:
                {
                    "type": "move",
                    "pos": (r, c),
                    "dir": "U" | "D" | "L" | "R",
                    "drops": [int, int, ...]
                }
        """

        if move["type"] == "place":
            row, col = move["pos"]
            piece = move["piece"]
            color = move.get("color")  # Puede venir forzado en apertura

            return self.place_piece(row, col, piece, color)

        elif move["type"] == "move":
            row, col = move["pos"]
            direction = move["dir"]
            drops = move["drops"]

            return self.move_stack(row, col, direction, drops)

        else:
            return False, "Tipo de movimiento desconocido."

    def _validate_stack_move(self, start_row, start_col, direction, drops):
        """Helper to validate stack move without executing it."""
        # 1. Validar control de la pila
        if not self.can_move_stack(start_row, start_col):
            return False, "No controlas esta pila."

        stack = self.board[start_row][start_col]
        picked_up_count = sum(drops)

        # 2. Validar límite de carga (carry limit = board size)
        if picked_up_count > self.size:
            return False, f"No puedes cargar más de {self.size} piezas."

        # 3. Validar que hay suficientes piezas en la pila
        if picked_up_count > len(stack):
            return False, "No hay suficientes piezas en la pila."

        # Tomar las piezas (las de arriba)
        moving_stack = stack[-picked_up_count:]

        # 4. Simular movimiento y validar ruta
        deltas = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
        dr, dc = deltas.get(direction.upper(), (0, 0))

        if dr == 0 and dc == 0:
            return False, "Dirección inválida."

        current_r, current_c = start_row, start_col
        pieces_dropped_so_far = 0

        # Validar ruta
        for drop_count in drops:
            current_r += dr
            current_c += dc

            # Limites
            if not self._is_inside(current_r, current_c):
                return False, "El movimiento sale del tablero."

            target_stack = self.board[current_r][current_c]

            # Bloqueo por muros y Capstone
            if target_stack:
                top_piece = target_stack[-1]
                top_type = top_piece[1]

                if top_type == "S":  # Standing Stone
                    substack = moving_stack[
                        pieces_dropped_so_far : pieces_dropped_so_far + drop_count
                    ]
                    striking_piece = substack[0]

                    is_last_step = pieces_dropped_so_far + drop_count == picked_up_count

                    if striking_piece[1] == "C" and is_last_step and drop_count == 1:
                        pass
                    else:
                        return (
                            False,
                            f"Camino bloqueado por un muro en {current_r}, {current_c}.",
                        )

                elif top_type == "C":  # Capstone
                    return (
                        False,
                        f"Camino bloqueado por una Piedra angular en {current_r}, {current_c}.",
                    )

            pieces_dropped_so_far += drop_count

        return True, ""

    def get_available_decisions(self):
        """
        Retorna una lista de movimientos válidos para el turno actual,
        delegando la lógica al motor de reglas (TakRuleEngine).
        """
        return self.rules.get_moves(self)

    @staticmethod
    def _get_compositions(n):
        """Genera todas las composiciones de n (formas de soltar piezas)."""
        if n == 1:
            return [[1]]
        result = []
        for k in range(1, n + 1):
            if k == n:
                result.append([n])
            else:
                for rest in TakBoard._get_compositions(n - k):
                    result.append([k] + rest)
        return result

    def check_road_win(self):
        """
        Verifica si hay un camino ganador (Road Win).
        Retorna 'white', 'black' o None.
        """
        for player in ["white", "black"]:
            # Buscar camino Oeste-Este (Izquierda-Derecha)
            starts_we = []
            for r in range(self.size):
                if self._is_road_piece(r, 0, player):
                    starts_we.append((r, 0))

            if self._has_path(player, starts_we, lambda r, c: c == self.size - 1):
                return player

            # Buscar camino Norte-Sur (Arriba-Abajo)
            starts_ns = []
            for c in range(self.size):
                if self._is_road_piece(0, c, player):
                    starts_ns.append((0, c))

            if self._has_path(player, starts_ns, lambda r, c: r == self.size - 1):
                return player

        return None

    def _has_path(self, player, start_nodes, is_goal):
        """BFS para encontrar camino"""
        queue = deque(start_nodes)
        visited = set(start_nodes)

        while queue:
            r, c = queue.popleft()

            if is_goal(r, c):
                return True

            # Vecinos ortogonales
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if self._is_inside(nr, nc):
                    if (nr, nc) not in visited:
                        if self._is_road_piece(nr, nc, player):
                            visited.add((nr, nc))
                            queue.append((nr, nc))
        return False

    def check_flat_win(self):
        """
        Verifica victoria por puntos (Flat Win) si el tablero está lleno o sin piezas.
        Retorna 'white', 'black', 'tie' o None si no ha terminado.
        """
        # Chequear condiciones de fin: tablero lleno o jugador sin piezas
        is_full = all(
            self.board[r][c] for r in range(self.size) for c in range(self.size)
        )

        pieces_out = (
            self.pieces["white"]["flat"] == 0 and self.pieces["white"]["capstones"] == 0
        ) or (
            self.pieces["black"]["flat"] == 0 and self.pieces["black"]["capstones"] == 0
        )

        if is_full or pieces_out:
            # Contar flats (solo cuentan piedras planas 'F')
            white_score = 0
            black_score = 0

            for r in range(self.size):
                for c in range(self.size):
                    top = self._top_piece(r, c)
                    if top and top[1] == "F":
                        if top[0] == "white":
                            white_score += 1
                        else:
                            black_score += 1

            if white_score > black_score:
                return "white"
            elif black_score > white_score:
                return "black"
            else:
                return "tie"

        return None

    def next_turn(self):
        """Cambia el turno e incrementa el contador de ply."""
        self.current_player = "black" if self.current_player == "white" else "white"
        self.ply_count += 1

    def get_winner(self):
        """
        Retorna el ganador del juego si existe, o None.
        Prioridad: Road Win > Flat Win.
        """
        # 1. Road Win
        road_winner = self.check_road_win()
        if road_winner:
            return road_winner

        # 2. Flat Win (only if board full or pieces out)
        flat_winner = self.check_flat_win()
        if flat_winner:
            return flat_winner

        return None

    def is_terminal(self):
        """Retorna True si el juego ha terminado."""
        return self.get_winner() is not None

    # LO ULTIMO AGREGADO

    def evaluate(self, player):
        """
        Evaluación simple del tablero desde la perspectiva de 'player'.
        Retorna un valor positivo si la posición es buena para 'player',
        negativo si es mala.
        """

        opponent = "black" if player == "white" else "white"

        # Caso terminal
        if self.is_terminal():
            winner = self.get_winner()
            if winner == player:
                return 100000
            elif winner == opponent:
                return -100000
            else:
                return 0

        score = 0

        # 1️⃣ Flats visibles (solo top y no standing)
        my_flats = self._count_visible_flats(player)
        opp_flats = self._count_visible_flats(opponent)
        score += 2 * (my_flats - opp_flats)

        # 2️⃣ Conectividad
        my_group = self._largest_connected_group(player)
        opp_group = self._largest_connected_group(opponent)
        score += 5 * (my_group - opp_group)

        # 3️⃣ Piezas restantes
        my_reserve = sum(self.pieces[player].values())
        opp_reserve = sum(self.pieces[opponent].values())
        score += 1 * (my_reserve - opp_reserve)

        return score

    def _count_visible_flats(self, player):
        count = 0
        for r in range(self.size):
            for c in range(self.size):
                stack = self.board[r][c]
                if stack:
                    owner, piece_type = stack[-1]
                    if owner == player and piece_type != "S":
                        count += 1
        return count

    def _largest_connected_group(self, player):
        visited = set()
        max_group = 0

        for r in range(self.size):
            for c in range(self.size):
                if (r, c) in visited:
                    continue

                stack = self.board[r][c]
                if stack and stack[-1][0] == player and stack[-1][1] != "S":
                    size = self._bfs_group_size(r, c, player, visited)
                    max_group = max(max_group, size)

        return max_group

    def _bfs_group_size(self, start_r, start_c, player, visited):
        from collections import deque

        queue = deque()
        queue.append((start_r, start_c))
        visited.add((start_r, start_c))

        size = 0

        while queue:
            r, c = queue.popleft()
            size += 1

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    if (nr, nc) not in visited:
                        stack = self.board[nr][nc]
                        if stack and stack[-1][0] == player and stack[-1][1] != "S":
                            visited.add((nr, nc))
                            queue.append((nr, nc))

        return size
