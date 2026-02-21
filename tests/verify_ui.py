from src.board import TakBoard
from src.ui_manager import TakTerminalUI


def verify_ui():
    board = TakBoard(5)
    ui = TakTerminalUI(board)

    # Just call display_board once
    ui.display_board()


if __name__ == "__main__":
    verify_ui()
