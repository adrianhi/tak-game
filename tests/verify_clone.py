from board import TakBoard


def verify_clone():
    board = TakBoard(size=5)
    print("Initial:")
    print(f"Original Ply: {board.ply_count}")
    print(f"Original Pieces: {board.pieces['white']['flat']}")

    # Clone
    clone = board.clone()
    print("Clone created.")

    # Modify clone
    print("Modifying clone...")
    clone.place_piece(0, 0, "F", "white")

    # Verify clone changes
    print(f"Clone Ply: {clone.ply_count}")
    print(f"Clone Pieces: {clone.pieces['white']['flat']}")
    assert clone.ply_count == 1
    assert clone.pieces["white"]["flat"] == board._get_initial_pieces(5) - 1

    # Verify original unchanged
    print("Verifying original unchanged...")
    print(f"Original Ply: {board.ply_count}")
    print(f"Original Pieces: {board.pieces['white']['flat']}")

    assert board.ply_count == 0
    assert board.pieces["white"]["flat"] == board._get_initial_pieces(5)
    assert board.board[0][0] == []

    print("SUCCESS: Clone modification did not affect original board.")


if __name__ == "__main__":
    verify_clone()
