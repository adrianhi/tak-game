"""
Juego Tak - Diseño del tablero en consola
"""

class TakBoard:
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
            'white': {'flat': self._get_initial_pieces(size), 'capstones': self._get_capstones(size)},
            'black': {'flat': self._get_initial_pieces(size), 'capstones': self._get_capstones(size)}
        }
        
        self.current_player = 'white'
        self.winner = None
    
    def _get_initial_pieces(self, size):
        """Retorna el número de piedras planas según el tamaño del tablero"""
        pieces_map = {3: 10, 4: 15, 5: 21, 6: 30, 8: 50}
        return pieces_map.get(size, 21)
    
    def _get_capstones(self, size):
        """Retorna el número de capstones según el tamaño del tablero"""
        capstones_map = {3: 0, 4: 0, 5: 1, 6: 1, 8: 2}
        return capstones_map.get(size, 1)
    
    def display_board(self):
        """Muestra el tablero en consola con un diseño limpio"""
        print("\n" + "=" * (self.size * 8 + 1))
        print(f"   TABLERO TAK {self.size}x{self.size}")
        print("=" * (self.size * 8 + 1))
        
        # Encabezado con letras de columnas
        print("    ", end="")
        for col in range(self.size):
            print(f"   {chr(65 + col)}   ", end="")
        print()
        
        # Línea superior
        print("   ┌" + "───────┬" * (self.size - 1) + "───────┐")
        
        # Filas del tablero
        for row in range(self.size):
            # Número de fila
            print(f" {self.size - row} │", end="")
            
            # Contenido de cada celda
            for col in range(self.size):
                cell_content = self._format_cell(row, col)
                print(f" {cell_content} │", end="")
            print(f" {self.size - row}")
            
            # Línea separadora (excepto después de la última fila)
            if row < self.size - 1:
                print("   ├" + "───────┼" * (self.size - 1) + "───────┤")
        
        # Línea inferior
        print("   └" + "───────┴" * (self.size - 1) + "───────┘")
        
        # Encabezado inferior con letras
        print("    ", end="")
        for col in range(self.size):
            print(f"   {chr(65 + col)}   ", end="")
        print("\n")
        
        # Información del juego
        self._display_game_info()
    
    def _format_cell(self, row, col):
        """Formatea el contenido de una celda para mostrar"""
        stack = self.board[row][col]
        
        if not stack:
            return "     "  # Celda vacía
        
        # Mostrar la pieza superior
        top_piece = stack[-1]
        player, piece_type = top_piece
        
        # Símbolos para las piezas
        if player == 'white':
            if piece_type == 'F':
                symbol = "⬛"  # Piedra plana blanca (ahora negra visualmente)
            elif piece_type == 'S':
                symbol = "�"  # Piedra de pie blanca
            else:  # 'C'
                symbol = "◆"   # Capstone blanco
        else:  # black
            if piece_type == 'F':
                symbol = "⬜"  # Piedra plana negra (ahora blanca visualmente)
            elif piece_type == 'S':
                symbol = "�"  # Piedra de pie negra
            else:  # 'C'
                symbol = "◇"   # Capstone negro
        
        # Mostrar altura de la pila si hay más de una pieza
        height = len(stack)
        if height > 1:
            return f"{symbol} {height}  "
        else:
            return f"{symbol}   "
    
    def _display_game_info(self):
        """Muestra información adicional del juego"""
        print("─" * (self.size * 8 + 1))
        print(f"Turno actual: {'Blancas ⬛' if self.current_player == 'white' else 'Negras ⬜'}")
        print(f"\nPiezas disponibles:")
        print(f"  Blancas: {self.pieces['white']['flat']} planas, {self.pieces['white']['capstones']} capstones")
        print(f"  Negras:  {self.pieces['black']['flat']} planas, {self.pieces['black']['capstones']} capstones")
        print("=" * (self.size * 8 + 1))
        print("\nLeyenda:")
        print("  ⬛/⬜ = Piedra plana    �/� = Piedra de pie    ◆/◇ = Capstone")
        print("  Número al lado de la pieza indica altura de la pila")
    
    def can_place_piece(self, row, col, piece_type='F'):
        """
        Valida si se puede colocar una pieza en la posición dada
        """
        # Validar límites
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False, "Posición fuera del tablero."
            
        # Validar celda vacía
        if self.board[row][col]:
            return False, "La casilla ya está ocupada."
            
        # Validar disponibilidad de piezas
        pieces = self.pieces[self.current_player]
        if piece_type == 'C':
            if pieces['capstones'] <= 0:
                return False, "No te quedan Capstones."
        else:
            if pieces['flat'] <= 0:
                return False, "No te quedan piedras planas."
                
        return True, ""

    def place_piece(self, row, col, piece_type='F'):
        """
        Coloca una pieza en el tablero
        row, col: posición (0-indexed)
        piece_type: 'F' = flat, 'S' = standing, 'C' = capstone
        """
        allowed, message = self.can_place_piece(row, col, piece_type)
        if not allowed:
            print(f"Movimiento inválido: {message}")
            return False

        self.board[row][col].append((self.current_player, piece_type))
            
        # Actualizar piezas disponibles
        if piece_type == 'C':
            self.pieces[self.current_player]['capstones'] -= 1
        else:
            self.pieces[self.current_player]['flat'] -= 1
            
        # Cambio de turno
        self.next_turn()
        return True

    def can_move_stack(self, row, col):
        """Valida si el jugador actual controla la pila en (row, col)"""
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False
        stack = self.board[row][col]
        if not stack:
            return False
        # El dueño de la pieza superior controla la pila
        return stack[-1][0] == self.current_player

    def move_stack(self, start_row, start_col, direction, drops):
        """
        Mueve una pila de piezas.
        direction: 'U', 'D', 'L', 'R'
        drops: lista de enteros indicando cuántas piezas dejar en cada paso
        """
        # 1. Validar control de la pila
        if not self.can_move_stack(start_row, start_col):
            print("No controlas esta pila.")
            return False

        stack = self.board[start_row][start_col]
        picked_up_count = sum(drops)
        
        # 2. Validar límite de carga (carry limit = board size)
        if picked_up_count > self.size:
             print(f"No puedes cargar más de {self.size} piezas.")
             return False
             
        # 3. Validar que hay suficientes piezas en la pila
        if picked_up_count > len(stack):
            print("No hay suficientes piezas en la pila.")
            return False

        # Tomar las piezas (las de arriba)
        # stack[-N:] son las N piezas de arriba.
        moving_stack = stack[-picked_up_count:]
        left_stack = stack[:-picked_up_count]
        
        # 4. Simular movimiento y validar ruta
        deltas = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
        dr, dc = deltas.get(direction.upper(), (0, 0))
        
        if dr == 0 and dc == 0:
            print("Dirección inválida.")
            return False
            
        current_r, current_c = start_row, start_col
        pieces_dropped_so_far = 0
        
        # Para restaurar en caso de fallo (aunque aquí solo validaremos antes de modificar si es posible o coping)
        # Haremos validación paso a paso
        
        # Validar ruta
        for drop_count in drops:
            current_r += dr
            current_c += dc
            
            # Limites
            if not (0 <= current_r < self.size and 0 <= current_c < self.size):
                print("El movimiento sale del tablero.")
                return False
                
            target_stack = self.board[current_r][current_c]
            
            # Bloqueo por muros y Capstone
            if target_stack:
                top_piece = target_stack[-1]
                top_type = top_piece[1]
                
                if top_type == 'S': # Standing Stone
                    # Solo puede ser aplastada por Capstone si es el final del movimiento y viene sola (el capstone es la unica pieza)
                    # La pieza que va a aterrizar aqui es la ULTIMA de las que se sueltan en este paso.
                    # El grupo que aterriza es moving_stack[pieces_dropped_so_far : pieces_dropped_so_far + drop_count]
                    
                    # Regla Capstone: 
                    # "Capstone can flatten a standing stone... if it moves onto it."
                    # "The Capstone must be moving by itself onto the standing stone?" -> Rules say Capstone must be the piece engaging/flattening.
                    # Usually implemented as: The piece *impacting* the wall must be a Capstone.
                    # And check if it's the LAST step involving the wall?
                    # Generally: A wall blocks movement checking unless it is flattened.
                    # Flattening happens if a Capstone lands on it.
                    
                    # Simplified verification for MVP:
                    # Logic: Is the piece colliding a Capstone?
                    # The leading piece of the substack being dropped is the bottom-most of that substack? No, stacks stay ordered.
                    # Moving stack: [Bottom ... Top]. 
                    # If we have stack [A, B, C] and drop 1 (C), C lands.
                    # If we drop 2 (B, C), B lands on target, then C on B. So B hits the existing stack first.
                    
                    # Verification: The BOTTOM piece of the dropped substack hits the target top.
                    substack = moving_stack[pieces_dropped_so_far : pieces_dropped_so_far + drop_count]
                    striking_piece = substack[0] # The one at the bottom of the held stack segment
                    
                    is_last_step = (pieces_dropped_so_far + drop_count == picked_up_count)
                    
                    if striking_piece[1] == 'C' and is_last_step and drop_count == 1:
                        # Valid flatten move (Capstone lands alone on Wall at end of move)
                        # (Some rules allow carry, but standard is typically Capstone acting alone or top of stack? 
                        # Actually: Capstone needs to be the one hitting. If carried stack is [F, C] (C on top), F hits. Capstone not effective.
                        # So Striking Piece must be C.
                        pass 
                    else:
                        print(f"Camino bloqueado por un muro en {current_r}, {current_c}.")
                        return False
                
                elif top_type == 'C': # Capstone
                     print(f"Camino bloqueado por una Capstone en {current_r}, {current_c}.")
                     return False
            
            pieces_dropped_so_far += drop_count

        # Si todo es válido, ejecutar movimiento
        self.board[start_row][start_col] = left_stack # Remove moved pieces
        
        current_r, current_c = start_row, start_col
        pieces_dropped_so_far = 0
        
        for drop_count in drops:
            current_r += dr
            current_c += dc
            
            substack = moving_stack[pieces_dropped_so_far : pieces_dropped_so_far + drop_count]
            target_stack = self.board[current_r][current_c]
            
            # Check flatten again to apply data change
            if target_stack:
                if target_stack[-1][1] == 'S': # We checked validity above
                     # Flatten: Change 'S' to 'F'
                     owner, _ = target_stack.pop()
                     target_stack.append((owner, 'F'))
            
            # Extend target stack
            target_stack.extend(substack)
            pieces_dropped_so_far += drop_count
            
        self.next_turn()
        return True

    def check_road_win(self):
        """
        Verifica si hay un camino ganador (Road Win).
        Retorna 'white', 'black' o None.
        """
        for player in ['white', 'black']:
            # Buscar camino Oeste-Este (Izquierda-Derecha)
            starts_we = []
            for r in range(self.size):
                cell = self.board[r][0] # Columna 0
                if cell and cell[-1][0] == player and cell[-1][1] in ['F', 'C']:
                    starts_we.append((r, 0))
            
            if self._has_path(player, starts_we, lambda r, c: c == self.size - 1):
                return player

            # Buscar camino Norte-Sur (Arriba-Abajo)
            starts_ns = []
            for c in range(self.size):
                cell = self.board[0][c] # Fila 0
                if cell and cell[-1][0] == player and cell[-1][1] in ['F', 'C']:
                    starts_ns.append((0, c))
            
            if self._has_path(player, starts_ns, lambda r, c: r == self.size - 1):
                return player
                
        return None

    def _has_path(self, player, start_nodes, is_goal):
        """BFS para encontrar camino"""
        queue = list(start_nodes)
        visited = set(start_nodes)
        
        while queue:
            r, c = queue.pop(0)
            
            if is_goal(r, c):
                return True
                
            # Vecinos ortogonales
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    if (nr, nc) not in visited:
                        cell = self.board[nr][nc]
                        if cell and cell[-1][0] == player and cell[-1][1] in ['F', 'C']:
                            visited.add((nr, nc))
                            queue.append((nr, nc))
        return False

    def check_flat_win(self):
        """
        Verifica victoria por puntos (Flat Win) si el tablero está lleno o sin piezas.
        Retorna 'white', 'black', 'tie' o None si no ha terminado.
        """
        # Chequear condiciones de fin: tablero lleno o jugador sin piezas
        is_full = True
        empty_count = 0
        for r in range(self.size):
            for c in range(self.size):
                if not self.board[r][c]:
                    is_full = False
                    empty_count += 1
        
        pieces_out = (self.pieces['white']['flat'] == 0 and self.pieces['white']['capstones'] == 0) or \
                     (self.pieces['black']['flat'] == 0 and self.pieces['black']['capstones'] == 0)

        if is_full or pieces_out:
            # Contar flats (solo cuentan piedras planas 'F')
            white_score = 0
            black_score = 0
            
            for r in range(self.size):
                for c in range(self.size):
                    stack = self.board[r][c]
                    if stack:
                        top = stack[-1]
                        if top[1] == 'F':
                            if top[0] == 'white':
                                white_score += 1
                            else:
                                black_score += 1
            
            if white_score > black_score:
                return 'white'
            elif black_score > white_score:
                return 'black'
            else:
                return 'tie'
        
        return None

    def next_turn(self):
        """Cambia el turno y verifica victoria"""
        # Verificar victoria por camino primero (puede ocurrir en turno propio)
        winner = self.check_road_win()
        if winner:
            self.winner = winner
            return f"Ganador por Camino: {winner}"
            
        # Verificar victoria por flats (full board, etc)
        flat_winner = self.check_flat_win()
        if flat_winner:
            self.winner = flat_winner
            return f"Ganador por Puntos: {flat_winner}"

        self.current_player = 'black' if self.current_player == 'white' else 'white'
        return None

    def add_demo_pieces(self):
        """Añade algunas piezas de demostración al tablero"""
        # Algunos ejemplos de colocación
        self.current_player = 'white'
        self.place_piece(2, 2, 'F')  # Centro - piedra plana blanca
        
        self.place_piece(1, 2, 'F')  # Piedra plana negra
        self.place_piece(3, 2, 'S')  # Piedra de pie blanca
        self.place_piece(2, 1, 'F')  # Piedra plana negra
        
        if self.size >= 5:
            self.place_piece(0, 0, 'C')  # Capstone blanco
            self.place_piece(4, 4, 'C')  # Capstone negro
            self.place_piece(2, 3, 'F')  # Piedra plana blanca
            
        # Simular una pila
        if self.size >= 5:
            self.board[1][1] = [('white', 'F'), ('black', 'F'), ('white', 'F')]


def main():
    """Función principal para demostrar el tablero"""
    print("\n BIENVENIDO A TAK \n")
    
    # Crear tablero de 5x5 (el tamaño estándar)
    board = TakBoard(size=5)
    
    # Añadir piezas de demostración
    board.add_demo_pieces()
    
    # Mostrar el tablero
    board.display_board()
    
    print("\n Ejemplo de juego mostrado arriba con piezas de demostración")
    print("   - Las pilas muestran su altura con un número")
    print("   - El tablero muestra coordenadas (A-E, 1-5)")
    print("   - Se pueden colocar piedras planas, de pie, o capstones\n")

