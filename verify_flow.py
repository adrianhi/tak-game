
import sys
import os
from unittest.mock import patch, MagicMock

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from main import main

def run_verification():
    print("Verifying game flow...")
    
    # Inputs to simulate:
    # 1. Player 1 Name
    # 2. Player 2 Name
    # 3. Menu Option 1 (Play)
    # 4. Move "2,2"
    # 5. Move "salir" (back to menu)
    # 6. Menu Option 3 (Change Names)
    # 7. New P1
    # 8. New P2
    # 9. Menu Option 2 (Exit)
    
    inputs = [
        "JugadorUno", "JugadorDos", # Names
        "1",                        # Play
        # Main.py does NOT ask for board size anymore, it hardcodes 5
        "2",                        # Action: Move Stack (will prompt for position)
        "0",                        # Position: '0' to Cancel (Testing our change)
        "0",                        # Action: Exit Game Loop
        "2"                         # Menu: Exit
    ]
    
    try:
        with patch('builtins.input', side_effect=inputs) as mock_input:
            with patch('builtins.print') as mock_print: # Suppress spam
                with patch('time.sleep'): # Skip delays
                    main()
        print("SUCCESS: Game flow execution completed without error.")
    except StopIteration:
        print("ERROR: Ran out of inputs!")
    except Exception as e:
        print(f"ERROR: Exception occurred: {e}")
                
if __name__ == "__main__":
    run_verification()
