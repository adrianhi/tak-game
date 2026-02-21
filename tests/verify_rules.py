
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'src'))
from board import TakBoard

def test_placement():
    print("--- Test Placement ---")
    board = TakBoard(3)
    # Valid
    assert board.place_piece(0, 0, 'F') == True
    assert board.board[0][0][-1] == ('white', 'F')
    # Invalid (Occupied)
    assert board.place_piece(0, 0, 'F') == False
    # Next player
    assert board.current_player == 'black' # Was updated by place_piece? Wait, place_piece updates player?
    # Yes, lines 166 (commented out in my edit but wait... I need to check if I uncommented it or if it was there)
    # The code I replaced in step 140 had:
    # # self.current_player = 'black' if self.current_player == 'white' else 'white'
    # commented out!
    # Wait, check board.py content. logic was:
    # # Cambio de turno (ahora manejado por next_turn, pero mantenemos simple por ahora)
    # # self.current_player = ...
    
    # If I uncomment it, place_piece changes turn. If I use next_turn, I should check that.
    # In my plan, turn management is separate. 
    # But for a simple place_piece call, does it auto-switch?
    # verify_flow.py worked, so main.py using place_piece must be working.
    # In main.py: 
    # if board.place_piece(...):
    #    ...
    # It doesn't call next_turn explicitly in the loop I wrote in main.py step 41.
    # But verify_flow worked?
    # Step 41 main.py code:
    #                     if board.place_piece(row_idx, col_idx, 'F'):
    #                         print("Pieza colocada.")
    # It just prints. It loops.
    # verify_flow inputs: "3,3", then "salir".
    # It didn't check whose turn it was properly or it didn't matter.
    
    # ISSUE: place_piece logic in board.py (Step 140) has the turn switch COMMENTED OUT.
    # So current_player NEVER CHANGES in the current code!
    # I need to fix `place_piece` and `move_stack` to use `next_turn` or uncomment the switch.
    # AND I need `next_turn` to be called.
    
    # Let's check `board.py` again.
    
    print("Placement test validation pending check of board.py Turn switching logic.")

def test_stack_movement():
    print("--- Test Stack Movement ---")
    board = TakBoard(5)
    board.board[2][2] = [('white', 'F')]
    board.current_player = 'white'
    
    # Move 1 Right
    assert board.move_stack(2, 2, 'R', [1]) == True
    assert board.board[2][2] == []
    assert board.board[2][3] == [('white', 'F')]
    
    # Move back (invalid, no piece)
    assert board.move_stack(2, 2, 'R', [1]) == False
    
    # Move Opponent stack (invalid)
    board.current_player = 'black'
    assert board.move_stack(2, 3, 'L', [1]) == False

def test_wall_blocking():
    print("--- Test Wall Blocking ---")
    board = TakBoard(5)
    board.board[2][3] = [('black', 'S')] # Wall
    board.board[2][2] = [('white', 'F')]
    board.current_player = 'white'
    
    # Try to move onto wall with Flat
    assert board.move_stack(2, 2, 'R', [1]) == False

def test_capstone_flatten():
    print("--- Test Capstone Flattening ---")
    board = TakBoard(5)
    board.board[2][3] = [('black', 'S')] # Wall
    board.board[2][2] = [('white', 'C')] # Capstone
    board.current_player = 'white'
    
    # Flatten
    assert board.move_stack(2, 2, 'R', [1]) == True
    # Stack should be [('black', 'F'), ('white', 'C')]
    assert board.board[2][3][0] == ('black', 'F') # Flattened wall
    assert board.board[2][3][-1] == ('white', 'C') # Capstone on top

def test_road_win():
    print("--- Test Road Win ---")
    board = TakBoard(5)
    # Create path 0,0 to 0,4
    for c in range(5):
        board.board[0][c] = [('white', 'F')]
    
    assert board.check_road_win() == 'white'

if __name__ == "__main__":
    try:
        test_placement()
        test_stack_movement()
        test_wall_blocking()
        test_capstone_flatten()
        test_road_win()
        print("ALL TESTS PASSED")
    except AssertionError as e:
        print(f"TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
