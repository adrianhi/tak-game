from bienvenida import bienvenida
from Menu_Tak import pedir_nombres, menu_principal, jugar_nuevamente, pedir_tamano
from board import TakBoard
import time

def main():
    # 1. Mensaje de bienvenida
    bienvenida()
    
    # 2. Solicitar nombres de jugadores
    jugador1, jugador2 = pedir_nombres()

    while True:
        # 3. Menú Principal
        opcion = menu_principal()
        
        if opcion == 1: # Jugar
            # Solicitar tamaño del tablero
            tamano = pedir_tamano()
            print(f"\n¡Comenzando el juego entre {jugador1} y {jugador2} en un tablero de {tamano}x{tamano}!\n")
            
            # Inicializar tablero
            board = TakBoard(size=tamano)
            
            # Loop simple de demostración del juego
            game_running = True
            while game_running:
                board.display_board()
                print(f"Turno de: {'Blancas ({jugador1})' if board.current_player == 'white' else 'Negras ({jugador2})'}")
                print("Escribe una posición (fila,columna) para colocar una piedra plana (ej. 2,2) o 'salir' para volver al menú.")
                
                move = input("Movimiento: ").strip().lower()
                
                if move == 'salir':
                    game_running = False
                    continue
                
                try:
                    r, c = map(int, move.split(','))
                    # Ajustar a índice 0 (User input 1-5 -> 0-4) si se prefiere, pero board.py ya maneja indices?
                    # Board display shows 5 at top, 1 at bottom. display_board uses:
                    # print(f" {self.size - row} │", end="")
                    # So row 0 is printed as 5. Row 4 is printed as 1.
                    # Let's assume input is coordinate system matchin visual (row, col) but let's just do direct mapping first for simplicity or stick to the board logic.
                    # Wait, the board logic in add_demo_pieces uses 0-indexed.
                    # Let's map user input (1-5) to (4-0) for rows?
                    # Visual:
                    # Row 0 -> Label 5
                    # Row 4 -> Label 1
                    # So user inputs 5 -> index 0. user inputs 1 -> index 4.
                    # Index = Size - UserRow
                    
                    if 1 <= r <= 5 and 1 <= c <= 5:
                         row_idx = 5 - r
                         col_idx = c - 1
                         if board.place_piece(row_idx, col_idx, 'F'):
                             print("Pieza colocada.")
                         else:
                             print("Casilla ocupada.")
                    else:
                        print("Coordenadas fuera de rango (1-5).")
                        
                except ValueError:
                     print("Entrada inválida. Usa formato: fila,columna")

            
        elif opcion == 2: # Salir
            print("Gracias por jugar. ¡Hasta luego!")
            break
            
        elif opcion == 3: # Cambiar Nombres
            print("\n--- Cambiando nombres de jugadores ---")
            jugador1, jugador2 = pedir_nombres()
            continue

        # Preguntar si jugar nuevamente después de una partida (si el loop de juego termina)
        # En este diseño, 'volver al menú' es parte del flujo natural.
        # Pero si termina la partida (game_running = False), volvemos al menu.
        # Check explicit 'salir' from the game loop returns us here.
        # If we want a generic "Play Again" prompt only when actually finishing a game (win condition),
        # we would put it inside the game logic. 
        # For now, following the structure, we just loop back to menu.

if __name__ == "__main__":
    main()