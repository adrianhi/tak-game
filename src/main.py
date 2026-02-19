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

        if opcion == 1:  # Jugar
            # Solicitar tamao del tablero
            print(
                f"\nComenzando el juego entre {jugador1} y {jugador2} en un tablero de 5x5!\n"
            )

            # Inicializar tablero, UI y controlador
            board = TakBoard(size=5)
            ui = TakTerminalUI(board)
            controller = TakController(board)

            game_running = True
            while game_running:
                ui.display_board()

                # MENÚ DE ACCIONES
                action = controller.get_game_action()

                if action == "0":
                    game_running = False
                    continue

                elif action == "1":
                    # COLOCAR PIEZA NUEVA
                    pos = controller.get_placement_position()

                    if pos:
                        row_idx, col_idx = pos
                        piece_type_user = controller.get_piece_type()

                        success, message = board.place_piece(
                            row_idx, col_idx, piece_type_user
                        )

                        if success:
                            print(f" {message}")
                            print(f" {message}")
                            winner = board.get_winner()
                            if winner:
                                ui.display_board()
                                print(
                                    f"\nJUEGO TERMINADO! Ganador: {winner} ({jugador1 if winner == 'white' else jugador2})"
                                )
                                game_running = False
                        else:
                            print(f" {message}")

                elif action == "2":
                    # MOVER PILA EXISTENTE

                    # Paso 1: Obtener pila a mover
                    result = controller.get_stack_to_move()

                    if result is None:
                        print("Movimiento cancelado.")
                        continue

                    start_row, start_col = result
                    print(
                        f" Pila seleccionada en ({board.size - start_row},{start_col + 1})"
                    )

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
                    success, message = board.move_stack(
                        start_row, start_col, direction, drops
                    )

                    if success:
                        print(f" {message}")

                        # Verificar si hay ganador
                        winner = board.get_winner()
                        if winner:
                            ui.display_board()
                            print(
                                f"\nJUEGO TERMINADO! Ganador: {winner} ({jugador1 if winner == 'white' else jugador2})"
                            )
                            game_running = False
                    else:
                        print(f" {message}")

        elif opcion == 2:  # Salir
            print("Gracias por jugar. Hasta luego!")
            break

        elif opcion == 3:  # Cambiar Nombres
            print("\n--- Cambiando nombres de jugadores ---")
            jugador1, jugador2 = pedir_nombres()
            continue


if __name__ == "__main__":
    main()
