import time
from board import TakBoard
from controller import TakController
from minimaxAI import MinimaxAI
from ui_manager import TakTerminalUI


def play_vs_ai_test():
    """
    Función principal que ejecuta el bucle de juego Humano vs MinimaxIA.
    Reutiliza el TakController para gestionar todas las entradas del humano.
    """
    print("=== Tak 5x5: Prueba de IA Minimax con TakController ===")

    # Elegir color
    human_color = ""
    while human_color not in ["white", "black"]:
        human_color = (
            input("Elige tu color (white/black) [por defecto white]: ").strip().lower()
        )
        if not human_color:
            human_color = "white"

    ai_color = "black" if human_color == "white" else "white"

    # Configurar profundidad
    depth_str = input(
        "Elige la profundidad de la IA (ej. 2, 3) [por defecto 2]: "
    ).strip()
    depth = 2
    if depth_str.isdigit():
        depth = int(depth_str)

    print(f"\n¡Comienza el juego! Eres el jugador {human_color}.")
    print(f"La IA ('{ai_color}') jugará con profundidad Minimax {depth}.\n")

    # Inicializar el estado del juego y los componentes MVC de consola
    board = TakBoard(size=5)
    ui = TakTerminalUI(board)
    controller = TakController(board)

    num_heuristics = controller.get_number_of_heuristics()
    ai = MinimaxAI(num_heuristics=num_heuristics)

    # Configurar límite de tiempo después de tener el controlador
    max_time = controller.get_ai_time_limit()
    print(f"La IA no tomará más de {max_time} segundos por turno.\n")

    # Bucle del juego
    while not board.is_terminal():
        ui.display_board()

        current_player = board.current_player

        if current_player == human_color:
            print(f"--- Turno HUMANO ({human_color}) ---")

            # Reutilizamos el controlador principal de Tak
            action = controller.get_game_action()

            if action == "0":
                print("Has abandonado la partida.")
                break

            try:
                if action == "1":
                    pos = controller.get_placement_position()
                    if not pos:
                        continue

                    row, col = pos
                    piece_type = controller.get_piece_type()

                    if piece_type:
                        if board.can_place_piece(row, col, piece_type):
                            board.place_piece(row, col, piece_type)
                            print(f"-> Has colocado {piece_type} en ({row}, {col}).")
                        else:
                            print(
                                "Movimiento inválido: No puedes colocar esa pieza ahí (ocupado o reglas rotas)."
                            )
                            continue
                    else:
                        continue

                elif action == "2":
                    pos = controller.get_stack_to_move()
                    if not pos:
                        continue

                    start_row, start_col = pos
                    direction = controller.get_move_direction()

                    if not direction:
                        continue

                    drops = controller.get_drops_distribution(start_row, start_col)

                    if not drops:
                        continue

                    # Validamos usando _validate_stack_move dentro de move_stack y manejamos sus errores
                    try:
                        board.move_stack(start_row, start_col, direction, drops)
                        print(
                            f"-> Has movido la pila en ({start_row}, {start_col}) hacia {direction} distribuyendo {drops}."
                        )
                    except ValueError as e:
                        print(f"Error al mover la pila: {e}")
                        continue

            except Exception as e:
                print(f"Error inesperado procesando el turno: {e}")
                continue

        else:
            print(f"--- Turno IA ({ai_color}) ---")
            print("La IA está pensando su próximo movimiento...")

            start_time = time.time()
            move = ai.choose_move(board, max_depth=depth, max_time=max_time)
            end_time = time.time()

            if move is None:
                print(
                    "La IA no ha podido encontrar movimientos válidos. ¡Fin inesperado!"
                )
                break

            elapsed_time = end_time - start_time
            print(f"-> La IA ha aplicado el movimiento: {move}")
            print(f"-> Tiempo de respuesta de la IA: {elapsed_time:.3f} segundos")

            board.apply_move(move)

    # Resultado Final
    ui.display_board()
    print("\n" + "=" * 30)
    print("       FIN DE LA PRUEBA")
    print("=" * 30)

    winner = board.get_winner()
    if winner in ("white", "black"):
        print(f"¡El ganador es el jugador {winner.upper()}!")
        if winner == human_color:
            print("¡Felicidades, ganaste contra la IA!")
        else:
            print("La IA ha ganado. ¡Mejor suerte la próxima!")
    elif winner == "tie":
        print("La partida terminó en empate.")
    else:
        print("Juego finalizado sin resultado válido.")


if __name__ == "__main__":
    play_vs_ai_test()
