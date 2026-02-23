import sys
from unittest.mock import patch
from game_ai_vs_ai import jugar_ai_vs_ai
import io

inputs = [
    '1', '1', '1',  # AI 1: Minimax, depth 1, heuristics 1
    '2',             # AI 2: Random
]

def mock_input(*args, **kwargs):
    if inputs:
        return inputs.pop(0)
    return '1'

with patch('builtins.input', side_effect=mock_input):
    with patch('time.sleep', return_value=None):
        try:
            jugar_ai_vs_ai()
        except:
            pass
