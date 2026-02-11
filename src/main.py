from bienvenida import bienvenida
from Menu_Tak import pedir_nombres, menu_principal, jugar_nuevamente
from board import TakBoard
import time

def main():
    #bienvenida()
    
    # 2. Solicitar nombres de jugadores
    jugador1, jugador2 = pedir_nombres()
    
    
    
    while True:
        # 3. Menú Principal
        opcion = menu_principal()
        
        if opcion == 1: # Jugar
            # Solicitar tamaño del tablero
            print(f"\n¡Comenzando el juego entre {jugador1} y {jugador2} en un tablero de 5x5!\n")
            
            # Inicializar tablero
            board = TakBoard(size=5)
            
            game_running = True
            while game_running:
                board.display_board()
                print(f"Turno de: {'Blancas ⬛' if board.current_player == 'white' else 'Negras ⬜'}")
                
                # MENÚ DE ACCIONES
                print("\n¿Qué acción deseas realizar?")
                print("  1. Colocar una nueva pieza")
                print("  2. Mover una pila existente")
                print("  0. Salir al menú principal")
                
                action = input("\nElige una opción: ").strip()
                
                if action == '0':
                    game_running = False
                    continue
                
                elif action == '1':
                    # COLOCAR PIEZA NUEVA
                    print("\nEscribe la posición donde quieres colocar (fila,columna)")
                    move = input("Posición: ").strip()
                    
                    try:
                        r, c = map(int, move.split(','))
                        
                        if 1 <= r <= 5 and 1 <= c <= 5:
                            row_idx = 5 - r
                            col_idx = c - 1
                            
                            piece_type_user = board.get_piece_type()
                            
                            if board.place_piece(row_idx, col_idx, piece_type_user):
                                print("✅ Pieza colocada.")
                                if board.winner:
                                    board.display_board()
                                    print(f"\n¡JUEGO TERMINADO! Ganador: {board.winner} ({jugador1 if board.winner == 'white' else jugador2})")
                                    game_running = False
                            else:
                                print("❌ No se pudo colocar la pieza.")
                        else:
                            print("❌ Coordenadas fuera de rango (1-5).")
                            
                    except ValueError:
                        print("❌ Entrada inválida. Usa formato: fila,columna")
                
                elif action == '2':
                    # MOVER PILA EXISTENTE
                    
                    # Paso 1: Obtener pila a mover
                    result = board.get_stack_to_move()
                    
                    if result is None:
                        print("Movimiento cancelado.")
                        continue
                    
                    start_row, start_col = result
                    print(f"✅ Pila seleccionada en ({board.size - start_row},{start_col + 1})")
                    
                    # Paso 2: Obtener dirección
                    direction = board.get_move_direction()
                    
                    if direction is None:
                        print("Movimiento cancelado.")
                        continue
                    
                    print(f"✅ Dirección seleccionada: {direction}")
                    
                    # Paso 3: Obtener distribución de fichas
                    drops = board.get_drops_distribution(start_row, start_col)
                    
                    if drops is None:
                        print("Movimiento cancelado.")
                        continue
                    
                    print(f"✅ Distribución: {drops}")
                    
                    # Paso 4: Ejecutar movimiento
                    if board.move_stack(start_row, start_col, direction, drops):
                        print("✅ Movimiento realizado exitosamente.")
                        
                        # Verificar si hay ganador
                        if board.winner:
                            board.display_board()
                            print(f"\n¡JUEGO TERMINADO! Ganador: {board.winner} ({jugador1 if board.winner == 'white' else jugador2})")
                            game_running = False
                    else:
                        print("❌ No se pudo realizar el movimiento.")
            

            
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