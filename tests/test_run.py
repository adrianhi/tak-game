import sys
from unittest.mock import patch
from game_ai_vs_ai import jugar_ai_vs_ai
import io

with patch('builtins.input', side_effect=['1', '1', '1', '1', '1']):
    with patch('time.sleep', return_value=None): # skip sleep
        jugar_ai_vs_ai()
