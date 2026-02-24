import sys
import os

# Agregar src al path para importar módulos del juego
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from board import TakBoard


def test_opening_rules():
    print("=== Iniciando Pruebas de Reglas de Apertura ===")
    board = TakBoard(size=5)

    # --- Turno 1: Blancas (Ply 0) ---
    # Regla: Blancas deben colocar una Flat del color Negras
    print(f"\n[Ply {board.ply_count}] Jugador actual: {board.current_player}")
    moves = board.get_available_decisions()

    assert len(moves) > 0, "Debería haber movimientos disponibles"

    for m in moves:
        assert (
            m["type"] == "place"
        ), f"En turno 1 solo se permite place. Encontrado: {m['type']}"
        assert (
            m["piece"] == "F"
        ), f"En turno 1 solo se permite Flat (F). Encontrado: {m['piece']}"
        assert (
            m["color"] == "black"
        ), f"En turno 1 Blancas debe poner Negra. Encontrado: {m['color']}"

    print("✅ Turno 1 validado: Blancas solo puede colocar Flats Negras.")

    # Ejecutar movimiento de Blancas sin pasar color explícito
    # El tablero debe deducirlo automáticamente de las reglas de apertura
    move = moves[0]
    success, msg = board.place_piece(move["pos"][0], move["pos"][1], move["piece"])
    assert success, f"Debería poder colocar la pieza: {msg}"

    # Verificar que en el tablero hay una pieza negra (aunque era turno de Blancas)
    top = board._top_piece(move["pos"][0], move["pos"][1])
    assert top == ("black", "F"), f"La pieza debería ser Black Flat. Encontrado: {top}"

    # --- Turno 2: Negras (Ply 1) ---
    # Regla: Negras deben colocar una Flat del color Blancas
    print(f"\n[Ply {board.ply_count}] Jugador actual: {board.current_player}")
    assert board.current_player == "black", "Debería ser turno de Negras"

    moves = board.get_available_decisions()

    for m in moves:
        assert (
            m["type"] == "place"
        ), f"En turno 2 solo se permite place. Encontrado: {m['type']}"
        assert (
            m["piece"] == "F"
        ), f"En turno 2 solo se permite Flat (F). Encontrado: {m['piece']}"
        assert (
            m["color"] == "white"
        ), f"En turno 2 Negras debe poner Blanca. Encontrado: {m['color']}"

    print("✅ Turno 2 validado: Negras solo puede colocar Flats Blancas.")

    # Ejecutar movimiento de Negras sin pasar color explícito
    # Buscar una posición vacía (la primera que no esté ocupada)
    move = next(m for m in moves if not board.board[m["pos"][0]][m["pos"][1]])
    success, msg = board.place_piece(move["pos"][0], move["pos"][1], move["piece"])
    assert success, f"Debería poder colocar la pieza: {msg}"

    # Verificar que en el tablero hay una pieza blanca (aunque era turno de Negras)
    top = board._top_piece(move["pos"][0], move["pos"][1])
    assert top == ("white", "F"), f"La pieza debería ser White Flat. Encontrado: {top}"

    # --- Turno 3: Blancas (Ply 2) - Juego Normal ---
    # Regla: A partir de aquí, cada jugador coloca sus propias piezas
    print(f"\n[Ply {board.ply_count}] Jugador actual: {board.current_player}")
    assert board.current_player == "white", "Debería ser turno de Blancas"

    moves = board.get_available_decisions()

    # Verificar que se permiten todos los tipos de pieza y el color es el propio
    found_F = False
    found_S = False
    found_C = False

    for m in moves:
        if m["type"] == "place":
            assert (
                m["color"] == "white"
            ), f"Ahora Blancas debe poner Blancas. Encontrado: {m['color']}"
            if m["piece"] == "F":
                found_F = True
            if m["piece"] == "S":
                found_S = True
            if m["piece"] == "C":
                found_C = True

    assert (
        found_F and found_S and found_C
    ), "En turno 3 deberían estar disponibles F, S y C"
    print("✅ Turno 3 validado: Juego normal (F, S, C disponibles para Blancas).")

    print("\n🎉 Todas las pruebas pasaron exitosamente.")


if __name__ == "__main__":
    test_opening_rules()
