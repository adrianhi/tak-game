"""
Módulo de Reglas del Juego (Move Generation Rules).
Este módulo implementa el patrón Estrategia para la generación de movimientos,
permitiendo separar las reglas de apertura de las reglas normales de juego,
siguiendo el Principio de Responsabilidad Única (SRP) y facilitando la extensión.
"""

from abc import ABC, abstractmethod


class MoveGenerator(ABC):
    """
    Interfaz abstracta para generadores de movimientos.
    Define el contrato que deben seguir las diferentes estrategias de reglas.
    """

    @abstractmethod
    def get_moves(self, board):
        """
        Genera una lista de movimientos válidos dado el estado actual del tablero.
        Args:
            board (TakBoard): La instancia del tablero actual.
        Returns:
            list: Lista de diccionarios representando los movimientos válidos.
        """
        pass

    @abstractmethod
    def get_turn_color(self, board):
        """
        Retorna el color de la pieza que se debe colocar en este turno.
        Normalmente es el color del jugador actual, pero en la apertura es el opuesto.
        Args:
            board (TakBoard): La instancia del tablero actual.
        Returns:
            str: 'white' o 'black'
        """
        pass


class OpeningMoveGenerator(MoveGenerator):
    """
    Estrategia para los primeros turnos del juego (Apertura).
    Reglas:
    - Turno 1 (Blancas): Debe colocar una pieza del oponente (Negra).
    - Turno 2 (Negras): Debe colocar una pieza del oponente (Blanca).
    - Solo se permiten Piedras Planas ('F').
    - No se permiten movimientos de pila ni colocar Capstones/Muros.
    """

    def get_turn_color(self, board):
        """En la apertura, se juega con el color del oponente."""
        return "black" if board.current_player == "white" else "white"

    def get_moves(self, board):
        """Genera solo colocaciones de Flats del color opuesto."""
        options = []
        # Determinar el color de la pieza a colocar (color del oponente)
        piece_color = self.get_turn_color(board)

        # Iterar sobre todas las celdas del tablero
        for r in range(board.size):
            for c in range(board.size):
                # Solo se puede colocar en celdas vacías
                if not board.board[r][c]:
                    # Verificar si el color objetivo tiene piezas disponibles
                    if board.pieces[piece_color]["flat"] > 0:
                        options.append(
                            {
                                "type": "place",
                                "pos": (r, c),
                                "piece": "F",
                                "color": piece_color,  # Color forzado al oponente
                            }
                        )
        return options


class StandardMoveGenerator(MoveGenerator):
    """
    Estrategia para el juego normal (después de la apertura).
    Reglas:
    - Se pueden colocar Piedras Planas, Muros o Capstones (si hay disponibles).
    - Se pueden mover pilas controladas por el jugador actual.
    - Las piezas colocadas son del color del jugador actual.
    """

    def get_turn_color(self, board):
        """En juego estándar, se juega con el color propio."""
        return board.current_player

    def get_moves(self, board):
        """Genera todos los movimientos normales de colocación y de pila."""
        options = []
        current_color = self.get_turn_color(board)

        # 1. Movimientos de Colocación (Place)
        for r in range(board.size):
            for c in range(board.size):
                if not board.board[r][c]:  # Solo celdas vacías
                    # Verificar disponibilidad de piedras planas (para F y S)
                    if board.pieces[current_color]["flat"] > 0:
                        options.append(
                            {
                                "type": "place",
                                "pos": (r, c),
                                "piece": "F",
                                "color": current_color,
                            }
                        )
                        options.append(
                            {
                                "type": "place",
                                "pos": (r, c),
                                "piece": "S",
                                "color": current_color,
                            }
                        )

                    # Verificar disponibilidad de Capstones
                    if board.pieces[current_color]["capstones"] > 0:
                        options.append(
                            {
                                "type": "place",
                                "pos": (r, c),
                                "piece": "C",
                                "color": current_color,
                            }
                        )

        # 2. Movimientos de Pila (Stack Move)
        deltas = ["U", "D", "L", "R"]
        for r in range(board.size):
            for c in range(board.size):
                if board.can_move_stack(r, c):
                    stack_len = len(board.board[r][c])
                    max_pickup = min(stack_len, board.size)

                    for pickup in range(1, max_pickup + 1):
                        compositions = board._get_compositions(pickup)
                        for drops in compositions:
                            for direction in deltas:
                                allowed, _ = board._validate_stack_move(
                                    r, c, direction, drops
                                )
                                if allowed:
                                    options.append(
                                        {
                                            "type": "move",
                                            "pos": (r, c),
                                            "dir": direction,
                                            "drops": drops,
                                        }
                                    )
        return options


class TakRuleEngine:
    """
    Fachada que decide qué estrategia de reglas usar basándose en el estado del juego.
    Delega en OpeningMoveGenerator para los primeros 2 turnos (ply 0 y 1),
    y en StandardMoveGenerator para el resto de la partida.
    """

    def __init__(self):
        # Instanciar las dos estrategias disponibles
        self.opening_rules = OpeningMoveGenerator()
        self.standard_rules = StandardMoveGenerator()

    def _get_strategy(self, board):
        """Selecciona la estrategia correcta según el número de turno (ply)."""
        if board.ply_count < 2:
            return self.opening_rules
        return self.standard_rules

    def get_moves(self, board):
        """
        Delega la generación de movimientos a la estrategia adecuada.
        Args:
            board (TakBoard): Tablero con estado actual (incluyendo ply_count).
        Returns:
            list: Lista de movimientos válidos para el turno actual.
        """
        return self._get_strategy(board).get_moves(board)

    def get_turn_color(self, board):
        """
        Retorna el color de la pieza que debe colocarse en el turno actual.
        Args:
            board (TakBoard): Tablero con estado actual.
        Returns:
            str: 'white' o 'black'
        """
        return self._get_strategy(board).get_turn_color(board)
