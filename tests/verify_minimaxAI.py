from board import TakBoard
from minimaxAI import MinimaxAI


def test_debug_root():
    board = TakBoard(size=5)
    ai = MinimaxAI()

    # Creamos un estado intermedio simple
    board.place_piece(2, 2, 'F')
    board.place_piece(3, 2, 'F')
    

    print("Turno actual:", board.current_player)
    print(board)

    print("\n========== DEPTH 1 ==========")
    ai.debug_root(board, depth=1)

    print("\n========== DEPTH 2 ==========")
    ai.debug_root(board, depth=2)


if __name__ == "__main__":
    test_debug_root()