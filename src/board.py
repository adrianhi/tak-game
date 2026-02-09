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
                symbol = "⬜"  # Piedra plana blanca
            elif piece_type == 'S':
                symbol = "🔲"  # Piedra de pie blanca
            else:  # 'C'
                symbol = "◇"   # Capstone blanco
        else:  # black
            if piece_type == 'F':
                symbol = "⬛"  # Piedra plana negra
            elif piece_type == 'S':
                symbol = "🔳"  # Piedra de pie negra
            else:  # 'C'
                symbol = "◆"   # Capstone negro
        
        # Mostrar altura de la pila si hay más de una pieza
        height = len(stack)
        if height > 1:
            return f"{symbol} {height}  "
        else:
            return f"{symbol}   "
    
    def _display_game_info(self):
        """Muestra información adicional del juego"""
        print("─" * (self.size * 8 + 1))
        print(f"Turno actual: {'Blancas ⬜' if self.current_player == 'white' else 'Negras ⬛'}")
        print(f"\nPiezas disponibles:")
        print(f"  Blancas: {self.pieces['white']['flat']} planas, {self.pieces['white']['capstones']} capstones")
        print(f"  Negras:  {self.pieces['black']['flat']} planas, {self.pieces['black']['capstones']} capstones")
        print("=" * (self.size * 8 + 1))
        print("\nLeyenda:")
        print("  ⬜/⬛ = Piedra plana    🔲/🔳 = Piedra de pie    ◇/◆ = Capstone")
        print("  Número al lado de la pieza indica altura de la pila")
    
    def place_piece(self, row, col, piece_type='F'):
        """
        Coloca una pieza en el tablero
        row, col: posición (0-indexed)
        piece_type: 'F' = flat, 'S' = standing, 'C' = capstone
        """
        if not self.board[row][col]:  # Solo si la celda está vacía
            self.board[row][col].append((self.current_player, piece_type))
            
            # Actualizar piezas disponibles
            if piece_type == 'C':
                self.pieces[self.current_player]['capstones'] -= 1
            else:
                self.pieces[self.current_player]['flat'] -= 1
            
            self.current_player = 'black' if self.current_player == 'white' else 'white'
            return True
        return False
    
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


if __name__ == "__main__":
    main()
