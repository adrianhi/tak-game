import time
from core.board import TakBoard
from controllers.controller import TakController
from ia.minimaxAI import MinimaxAI
from ia.randomAI import RandomAI
from ia.greedyAI import GreedyAI
from ia.worstAI import WorstAI
from ui.ui_manager import TakTerminalUI


def jugar_ai_vs_ai(jugador1_nombre="IA Blancas", jugador2_nombre="IA Negras"):
    """
    Función principal que ejecuta el bucle de juego IA vs IA.
    Permite configurar ambas IAs de forma independiente y las enfrenta.
    """
    print("=== Tak 5x5: Modo IA vs IA ===")

    board = TakBoard(size=5)
    ui = TakTerminalUI(board)
    controller = TakController(board)

    print(f"\n--- Configuración para {jugador1_nombre} (Blancas) ---")
    print("Tipo de IA:")
    print("  1. Minimax")
    print("  2. Random")
    print("  3. Greedy")
    print("  4. Worst")
    ai_w_type = input("Opción (1, 2, 3 o 4) [por defecto 1]: ").strip()

    if ai_w_type == "2":
        ai_white = RandomAI()
        depth_w, time_w = 0, 0
    elif ai_w_type == "3":
        # Necesitamos instanciar un dummy Minimax solo para sacar su eval, o usar la lógica
        # Como GreedyAI pide `evaluation_function`, le pasamos el `evaluate` de Minimax
        dummy_minimax = MinimaxAI()
        ai_white = GreedyAI(dummy_minimax.evaluate)
        depth_w, time_w = 0, 0
    elif ai_w_type == "4":
        dummy_minimax = MinimaxAI()
        ai_white = WorstAI(dummy_minimax.evaluate)
        depth_w, time_w = 0, 0
    else:
        depth_w_str = input("Elige la profundidad (ej. 2, 3) [por defecto 2]: ").strip()
        depth_w = int(depth_w_str) if depth_w_str.isdigit() else 2
        time_w = controller.get_ai_time_limit()
        heuristics_w = controller.get_number_of_heuristics()
        config_w = controller.get_weight_config()
        ai_white = MinimaxAI(num_heuristics=heuristics_w, weight_config=config_w)

    print(f"\n--- Configuración para {jugador2_nombre} (Negras) ---")
    print("Tipo de IA:")
    print("  1. Minimax")
    print("  2. Random")
    print("  3. Greedy")
    print("  4. Worst")
    ai_b_type = input("Opción (1, 2, 3 o 4) [por defecto 1]: ").strip()

    if ai_b_type == "2":
        ai_black = RandomAI()
        depth_b, time_b = 0, 0
    elif ai_b_type == "3":
        dummy_minimax = MinimaxAI()
        ai_black = GreedyAI(dummy_minimax.evaluate)
        depth_b, time_b = 0, 0
    elif ai_b_type == "4":
        dummy_minimax = MinimaxAI()
        ai_black = WorstAI(dummy_minimax.evaluate)
        depth_b, time_b = 0, 0
    else:
        depth_b_str = input("Elige la profundidad (ej. 2, 3) [por defecto 2]: ").strip()
        depth_b = int(depth_b_str) if depth_b_str.isdigit() else 2
        time_b = controller.get_ai_time_limit()
        heuristics_b = controller.get_number_of_heuristics()
        config_b = controller.get_weight_config()
        ai_black = MinimaxAI(num_heuristics=heuristics_b, weight_config=config_b)

    print("\n¡Comienza el duelo de inteligencias artificiales!\n")

    # Bucle del juego
    while not board.is_terminal():
        ui.display_board()

        current_player = board.current_player

        if current_player == "white":
            print(f"--- Turno de {jugador1_nombre} (Blancas) ---")
            print(f"{jugador1_nombre} está pensando su próximo movimiento...")

            start_time = time.time()
            move = ai_white.choose_move(board, max_depth=depth_w, max_time=time_w)
            end_time = time.time()

            if move is None:
                print(
                    f"{jugador1_nombre} no ha podido encontrar movimientos válidos. ¡Fin inesperado!"
                )
                break

            elapsed_time = end_time - start_time
            print(f"-> Tiempo de respuesta: {elapsed_time:.3f} segundos")

        else:
            print(f"--- Turno de {jugador2_nombre} (Negras) ---")
            print(f"{jugador2_nombre} está pensando su próximo movimiento...")

            start_time = time.time()
            move = ai_black.choose_move(board, max_depth=depth_b, max_time=time_b)
            end_time = time.time()

            if move is None:
                print(
                    f"{jugador2_nombre} no ha podido encontrar movimientos válidos. ¡Fin inesperado!"
                )
                break

            elapsed_time = end_time - start_time
            print(f"-> Tiempo de respuesta: {elapsed_time:.3f} segundos")

        board.apply_move(move)
        time.sleep(1)  # Espera para visualización

    # Resultado Final
    ui.display_board()
    print("\n" + "=" * 30)
    print("       FIN DE LA PARTIDA")
    print("=" * 30)

    winner = board.get_winner()
    if winner:
        ganador_nombre = jugador1_nombre if winner == "white" else jugador2_nombre
        print(f"¡El ganador es {ganador_nombre} ({winner.upper()})!")
    else:
        print("El juego ha terminado en empate o finalizado sin ganador definido.")

    print("\nEstadísticas finales:")
    if isinstance(ai_white, MinimaxAI):
        print(f"- {jugador1_nombre} (IA Blancas):")
        print(
            f"   Nodos totales expandidos: {getattr(ai_white, 'nodes_total', ai_white.nodes_explored)}"
        )
    else:
        print(f"- {jugador1_nombre}: No aplica (no usa Minimax).")

    if isinstance(ai_black, MinimaxAI):
        print(f"- {jugador2_nombre} (IA Negras):")
        print(
            f"   Nodos totales expandidos: {getattr(ai_black, 'nodes_total', ai_black.nodes_explored)}"
        )
    else:
        print(f"- {jugador2_nombre}: No aplica (no usa Minimax).")


if __name__ == "__main__":
    jugar_ai_vs_ai()
