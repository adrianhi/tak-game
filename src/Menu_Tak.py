def pedir_nombres():
    print("Bienvenidos a Tak!")
    jugador1 = input("Ingresa el nombre del Jugador 1: ").strip()
    while jugador1 == "":
        jugador1 = input("El nombre no puede estar vacío. Ingresa el nombre del Jugador 1: ").strip()
    
    jugador2 = input("Ingresa el nombre del Jugador 2: ").strip()
    while jugador2 == "" or jugador2 == jugador1:
        jugador2 = input("El nombre no puede estar vacío ni ser igual al Jugador 1. Ingresa el nombre del Jugador 2: ").strip()
    
    return jugador1, jugador2


def menu_principal():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Jugar")
        print("2. Salir")
        print("3. Cambiar Nombres")
        
        opcion = input("Selecciona una opción: ").strip()
        
        # Validación: solo números 1, 2 o 3
        if opcion not in ["1", "2", "3"]:
            print("Opción inválida. Por favor ingresa 1, 2 o 3.")
            continue
        
        return int(opcion)

def jugar_nuevamente():
    while True:
        respuesta = input("¿Desean jugar otra partida? (S/N): ").strip().upper()
        if respuesta in ["S", "N"]:
            return respuesta == "S"
        else:
            print("Respuesta inválida. Ingresa S para sí o N para no.")
