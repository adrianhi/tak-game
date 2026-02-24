"""
Módulo de Interfaz de Usuario para Tak.
Responsable de toda la salida visual del juego en la consola.
"""


class TakTerminalUI:
    """
    Clase encargada de renderizar el estado del juego Tak en la terminal.
    Proporciona métodos visuales para el tablero y mensajes de información.
    """

    def __init__(self, board):
        """
        Inicializa la UI con una referencia al tablero.
        board: Instancia de TakBoard
        """
        self.board = board

    def display_board(self):
        """Muestra el tablero en consola con un diseño limpio"""
        size = self.board.size
        print("\n" + "=" * (size * 8 + 1))
        print(f"   TABLERO TAK {size}x{size}")
        print("=" * (size * 8 + 1))

        print("    ", end="")
        for col in range(size):
            # Imprime 1, 2, 3... con el espaciado adecuado
            print(f"   {col + 1}   ", end="")
        print()

        # Línea superior
        print("   ┌" + "───────┬" * (size - 1) + "───────┐")

        # Filas del tablero
        for row in range(size):
            # Número de fila
            print(f" {size - row} │", end="")

            # Contenido de cada celda
            for col in range(size):
                cell_content = self._format_cell(row, col)
                print(f" {cell_content} │", end="")
            print(f" {size - row}")

            # Línea separadora (excepto después de la última fila)
            if row < size - 1:
                print("   ├" + "───────┼" * (size - 1) + "───────┤")

        # Línea inferior
        print("   └" + "───────┴" * (size - 1) + "───────┘")

        print("    ", end="")
        for col in range(size):
            print(f"   {col + 1}   ", end="")
        print("\n")

        # Información del juego
        self._display_game_info()

    def _format_cell(self, row, col):
        """Formatea el contenido de una celda para mostrar"""
        stack = self.board.board[row][col]

        if not stack:
            return "     "  # Celda vacía

        # Mostrar la pieza superior
        top_piece = stack[-1]
        player, piece_type = top_piece

        # Símbolos para las piezas
        if player == "white":
            if piece_type == "F":
                symbol = "⬛"
            elif piece_type == "S":
                symbol = "🏳️"
            else:  # 'C'
                symbol = "⚪"
        else:  # black
            if piece_type == "F":
                symbol = "⬜"
            elif piece_type == "S":
                symbol = "🏴"
            else:  # 'C'
                symbol = "⚫"

        # Mostrar altura de la pila si hay más de una pieza
        height = len(stack)
        if height > 1:
            return f"{symbol} {height}  "
        else:
            return f"{symbol}   "

    def _display_game_info(self):
        """Muestra información adicional del juego"""
        size = self.board.size
        print("─" * (size * 8 + 1))
        print(
            f"Turno actual: {'Blancas ⬛' if self.board.current_player == 'white' else 'Negras ⬜'}"
        )

        valid_decisions = self.board.get_available_decisions()
        print(f"Movimientos válidos disponibles: {len(valid_decisions)}")

        print(f"\nPiezas disponibles:")
        print(
            f"  Blancas: {self.board.pieces['white']['flat']} piezas, {self.board.pieces['white']['capstones']} piedra angular"
        )
        print(
            f"  Negras:  {self.board.pieces['black']['flat']} piezas, {self.board.pieces['black']['capstones']} piedra angular"
        )
        print("=" * (size * 8 + 1))
        print("\nLeyenda:")
        print(
            "  ⬛/⬜ = Piedra plana    🏴/🏳️ = Piedra de pie    ⚫/⚪ = Piedra Angular "
        )
        print("  Número al lado de la pieza indica altura de la pila")
