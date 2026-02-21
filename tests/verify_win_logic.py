
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'src'))
from board import TakBoard

def test_win_integration():
    print("--- Test Win Integration ---")
    board = TakBoard(3)
    
    # Simulate a road win
    # 0,0 'F' (White)
    # 0,1 'F' (White)
    # 0,2 'F' (White)
    
    board.place_piece(0, 0, 'F') # White
    board.place_piece(1, 0, 'F') # Black
    board.place_piece(0, 1, 'F') # White
    board.place_piece(1, 1, 'F') # Black
    board.place_piece(0, 2, 'F') # White wins!
    
    if board.winner == 'white':
        print("SUCCESS: Road Win detected and board.winner set to 'white'")
    else:
        print(f"FAILURE: Expected board.winner='white', got '{board.winner}'")
        
    # Test Flat Win (simulated by filling board)
    print("\n--- Test Flat Win ---")
    board2 = TakBoard(3)
    # Fill board
    # Row 0: W B W
    # Row 1: B W B
    # Row 2: W B W
    # Flats: W=5, B=4
    
    moves = [
        (0,0), (0,1), (0,2),
        (1,0), (1,1), (1,2),
        (2,0), (2,1), (2,2)
    ]
    
    for r, c in moves:
        board2.place_piece(r, c, 'F')
        if board2.winner:
            print(f"Winner found early at {r},{c}: {board2.winner}")
            break
            
    if board2.winner == 'white':
        print("SUCCESS: Flat Win detected and board.winner set to 'white'")
    else:
        print(f"FAILURE: Expected board.winner='white', got '{board2.winner}'")

if __name__ == "__main__":
    test_win_integration()
