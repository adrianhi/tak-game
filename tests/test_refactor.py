import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from board import TakBoard

def test_board_returns():
    print("Testing Board Refactoring...")
    board = TakBoard(5)
    
    # Test place_piece success
    success, msg = board.place_piece(0, 0, 'F')
    assert success is True
    assert isinstance(msg, str)
    print(f"Place Piece Success: OK ({msg})")
    
    # Test place_piece failure (occupied)
    success, msg = board.place_piece(0, 0, 'F')
    assert success is False
    assert isinstance(msg, str)
    print(f"Place Piece Failure: OK ({msg})")
    
    # Test move_stack
    # First place some pieces
    board.place_piece(0, 1, 'F')
    # Try to move invalid
    success, msg = board.move_stack(0, 1, 'R', [1]) # 0,1 to 0,2
    # It might fail if not my turn (turn changed after valid place)
    # Turn 1: White places (0,0). Turn 2: Black places (failure 0,0). Turn 2: Black places (0,1).
    # Turn 3: White moves (0,1)? No, (0,1) is Black's.
    
    print(f"Move Stack Result: valid? {success}, msg: {msg}")
    
    print("All checks passed!")

if __name__ == "__main__":
    test_board_returns()
