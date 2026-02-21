from board import TakBoard


def verify_refactor():
    print("Initializing board...")
    board = TakBoard(size=5)

    # 1. Test Initial State
    print("Testing initial state...")
    assert board.get_winner() is None
    assert board.is_terminal() is False

    # 2. Test Next Turn
    print("Testing next_turn()...")
    prev_ply = board.ply_count
    prev_player = board.current_player
    ret = board.next_turn()

    assert ret is None  # Should not return string anymore
    assert board.ply_count == prev_ply + 1
    assert board.current_player != prev_player

    # 3. Test Road Win Detection
    print("Testing Road Win detection...")
    # Setup a horizontal road for white
    board.board = [[[] for _ in range(5)] for _ in range(5)]  # Clear board
    for c in range(5):
        board.board[0][c].append(("white", "F"))

    # Verify winner
    winner = board.get_winner()
    print(f"Winner detected: {winner}")
    assert winner == "white"
    assert board.is_terminal() is True

    # 4. Test Flat Win Detection
    print("Testing Flat Win detection...")
    # Fill board with white flats
    board.board = [[[] for _ in range(5)] for _ in range(5)]
    for r in range(5):
        for c in range(5):
            board.board[r][c].append(("white", "F"))

    # Modify one to be black to avoid road win (actually fully filled is usually road win check first)
    # But lets just check if flat win logic triggers when road win is false.
    # We need to make sure no road exists.
    # 5x5 filled with white IS a road win.
    # Let's make a checkerboard pattern
    board.board = [[[] for _ in range(5)] for _ in range(5)]
    count = 0
    for r in range(5):
        for c in range(5):
            color = "white" if (r + c) % 2 == 0 else "black"
            board.board[r][c].append((color, "F"))

    # White has 13, Black has 12
    # This might have accidental roads, let's just trust logic if get_winner returns something
    winner = board.get_winner()
    print(f"Checkerboard Winner: {winner}")
    # Winner should be white (13 vs 12)
    assert winner == "white"
    assert board.is_terminal() is True

    print("SUCCESS: Refactoring verified.")


if __name__ == "__main__":
    verify_refactor()
