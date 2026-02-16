from bienvenida import bienvenida
from Menu_Tak import pedir_nombres, menu_principal, jugar_nuevamente
from board import TakBoard
from ui_manager import TakTerminalUI
from controller import TakController
import time

def main():
    """Función principal del juego Tak. Orquesta la lógica, UI y controlador."""
   # bienvenida()
    
    # 2. Solicitar nombres de jugadores
    jugador1, jugador2 = pedir_nombres()
    
    
    
    while True:
        # 3. Men Principal
        opcion = menu_principal()
        
        if opcion == 1: # Jugar 
            # Solicitar tamao del tablero
            print(f"\nComenzando el juego entre {jugador1} y {jugador2} en un tablero de 5x5!\n")
            
            # Inicializar tablero, UI y controlador
            board = TakBoard(size=5)
            ui = TakTerminalUI(board)
            controller = TakController(board)
            
            game_running = True
            while game_running:
                ui.display_board()
                
                # MEN DE ACCIONES
                print("\nQué acción deseas realizar?")
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
                            
                            piece_type_user = controller.get_piece_type()
                            
                            if board.place_piece(row_idx, col_idx, piece_type_user):
                                print(" Pieza colocada.")
                                if board.winner:
                                    ui.display_board()
                                    print(f"\nJUEGO TERMINADO! Ganador: {board.winner} ({jugador1 if board.winner == 'white' else jugador2})")
                                    game_running = False
                            else:
                                print(" No se pudo colocar la pieza.")
                        else:
                            print(" Coordenadas fuera de rango (1-5).")
                            
                    except ValueError:
                        print(" Entrada invlida. Usa formato: fila,columna")
                
                elif action == '2':
                    # MOVER PILA EXISTENTE
                    
                    # Paso 1: Obtener pila a mover
                    result = controller.get_stack_to_move()
                    
                    if result is None:
                        print("Movimiento cancelado.")
                        continue
                    
                    start_row, start_col = result
                    print(f" Pila seleccionada en ({board.size - start_row},{start_col + 1})")
                    
                    # Paso 2: Obtener direccin
                    direction = controller.get_move_direction()
                    
                    if direction is None:
                        print("Movimiento cancelado.")
                        continue
                    
                    print(f" Dirección seleccionada: {direction}")
                    
                    # Paso 3: Obtener distribución de fichas
                    drops = controller.get_drops_distribution(start_row, start_col)
                    
                    if drops is None:
                        print("Movimiento cancelado.")
                        continue
                    
                    print(f" Distribución: {drops}")
                    
                    # Paso 4: Ejecutar movimiento
                    if board.move_stack(start_row, start_col, direction, drops):
                        print(" Movimiento realizado exitosamente.")
                        
                        # Verificar si hay ganador
                        if board.winner:
                            ui.display_board()
                            print(f"\nJUEGO TERMINADO! Ganador: {board.winner} ({jugador1 if board.winner == 'white' else jugador2})")
                            game_running = False
                    else:
                        print(" No se pudo realizar el movimiento.")
            

            
        elif opcion == 2: # Salir
            print("Gracias por jugar. Hasta luego!")
            break
            
        elif opcion == 3: # Cambiar Nombres
            print("\n--- Cambiando nombres de jugadores ---")
            jugador1, jugador2 = pedir_nombres()
            continue

if __name__ == "__main__":
    main()