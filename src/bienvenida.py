import time

def pausa(segundos=1):
    time.sleep(segundos)

def imprimir_lento(texto, velocidad=0.02):
    for letra in texto:
        print(letra, end="", flush=True)
        time.sleep(velocidad)
    print()


def bienvenida():
    print("=" * 70)
    imprimir_lento("🎮 BIENVENIDO AL JUEGO: TAK 🎮")
    imprimir_lento("Un juego de estrategia abstracta creado por James Ernest")
    print("=" * 70)
    pausa(1)

    imprimir_lento("\n📜 REGLAS OFICIALES DEL JUEGO TAK 📜")
    print("-" * 70)

    reglas = [
        "1. TABLERO: Se juega en un tablero cuadrado (3x3, 4x4, 5x5).",
        "2. PIEZAS: Cada jugador tiene piezas planas, muros (de pie) y una pieza especial llamada Capstone.",
        "3. OBJETIVO PRINCIPAL: Formar un camino continuo desde un borde del tablero al borde opuesto.",
        "4. TURNOS: En cada turno puedes hacer UNA de estas acciones:",
        "   a) Colocar una pieza en una casilla vacía.",
        "   b) Mover una pila de piezas propias (puedes dejar piezas en casillas intermedias).",
        "5. APILAMIENTO: Las piezas se pueden apilar formando torres. Solo la pieza superior controla la casilla.",
        "6. MUROS: Los muros bloquean caminos, pero pueden ser aplastados por una Capstone.",
        "7. CAPSTONE: Puede aplastar un muro al moverse sobre él, convirtiéndolo en pieza plana.",
        "8. CONTROL: Solo las piezas planas y Capstones cuentan para formar caminos.",
        "9. FINAL DEL JUEGO: El juego termina cuando:",
        "   - Un jugador completa un camino (Road Win).",
        "   - Se llenan todas las casillas o se acaban las piezas (Flat Win).",
        "10. FLAT WIN: Si no hay camino, gana quien tenga más piezas planas visibles.",
    ]

    for regla in reglas:
        imprimir_lento(regla)
        pausa(0.3)

    print("-" * 70)
    pausa(1)

    imprimir_lento("\n🎯 OBJETIVO DEL JUEGO 🎯")
    imprimir_lento("Conectar dos lados opuestos del tablero con tus piezas planas o Capstone.")

    pausa(1)
    imprimir_lento("\n🚀 ¡Que comience la estrategia! 🚀")
    print("=" * 70)

