
import unittest
from unittest.mock import patch
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from board import TakBoard
from ui_manager import TakTerminalUI
from controller import TakController

class TestTakRefactor(unittest.TestCase):
    def setUp(self):
        self.board = TakBoard(size=5)
        self.ui = TakTerminalUI(self.board)
        self.controller = TakController(self.board)

    @patch('builtins.input', side_effect=['1']) # Select Flat
    def test_get_piece_type(self, mock_input):
        piece_type = self.controller.get_piece_type()
        self.assertEqual(piece_type, 'F')

    @patch('builtins.input', side_effect=['3,3', '0']) # Select 3,3 then cancel
    def test_get_stack_to_move(self, mock_input):
        # We need a piece at 3,3 (index 2,2 for 5x5 board? logic uses 5-row, col-1)
        # 3,3 -> row_idx = 5-3=2, col_idx=3-1=2.
        self.board.board[2][2] = [('white', 'F')]
        self.board.current_player = 'white'
        
        pos = self.controller.get_stack_to_move()
        self.assertEqual(pos, (2, 2))

    @patch('builtins.input', side_effect=['1']) # Up
    def test_get_move_direction(self, mock_input):
        direction = self.controller.get_move_direction()
        self.assertEqual(direction, 'U')

    @patch('builtins.input', side_effect=['1', '1']) # Pickup 1, Drop 1
    def test_get_drops_distribution(self, mock_input):
        # Setup stack
        self.board.board[2][2] = [('white', 'F')]
        drops = self.controller.get_drops_distribution(2, 2)
        self.assertEqual(drops, [1])

if __name__ == '__main__':
    unittest.main()
