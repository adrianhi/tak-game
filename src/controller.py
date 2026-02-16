"""
Módulo de Controlador para Tak.
Maneja la entrada del usuario y la interacción para solicitar movimientos y datos.
"""

class TakController:
    """
    Clase encargada de gestionar la entrada del usuario para el juego Tak.
    Solicita datos como tipo de pieza, movimientos de pila, direcciones, etc.
    """
    def __init__(self, board):
        """
        Inicializa el controlador con una referencia al tablero.
        board: Instancia de TakBoard (necesaria para validaciones de estado)
        """
        self.board = board

    def get_piece_type(self):
        """
        Pregunta al usuario qué tipo de pieza quiere colocar.
        Retorna: 'F' (flat), 'S' (standing), o 'C' (capstone)
        """
        while True:
            print("\n¿Qué tipo de pieza deseas colocar?")
            print("  1. Piedra Plana (horizontal)")
            print("  2. Piedra de Pie (vertical/muro)")

            # Solo mostrar Piedras angulares si tiene disponibles
            if self.board.pieces[self.board.current_player]['capstones'] > 0:
                print("  3. Piedra Angular (Capstone)")
                valid_options = ['1', '2', '3']
            else:
                valid_options = ['1', '2']

            choice = input("\nElige una opción: ").strip()

            if choice not in valid_options:
                print("❌ Opción inválida. Intenta de nuevo.")
                continue
            
            if choice == '1':
                return 'F'
            elif choice == '2':
                return 'S'
            elif choice == '3':
                return 'C'

    def get_stack_to_move(self):
        """
        Pregunta al usuario qué pila quiere mover.
        Retorna: (row, col) o None si cancela
        """
        while True:
            print("\n¿Qué pila quieres mover?")
            print("Formato: fila,columna (ejemplo: 3,2)")
            print("Escribe '0' para volver")
            
            position = input("Posición: ").strip().lower()
            
            if position == '0':
                return None
            
            # Validar formato
            if ',' not in position:
                print("❌ Formato inválido. Usa: fila,columna (ejemplo: 3,2)")
                continue
            
            try:
                parts = position.split(',')
                row = int(parts[0].strip())
                col = int(parts[1].strip())
                
                # Convertir de coordenadas visuales (1-size) a índices (0-size-1)
                row_idx = self.board.size - row
                col_idx = col - 1
                
                # Validar límites
                if not (1 <= row <= self.board.size and 1 <= col <= self.board.size):
                    print(f"❌ Posición fuera del tablero. Usa números entre 1 y {self.board.size}")
                    continue
                
                # Validar que haya una pila
                if not self.board.board[row_idx][col_idx]:
                    print("❌ No hay fichas en esa posición.")
                    continue
                
                # Validar que el jugador actual controle la pila
                if not self.board.can_move_stack(row_idx, col_idx):
                    print("❌ No controlas esa pila. Solo puedes mover pilas donde tu ficha esté arriba.")
                    continue
                
                # Todo válido
                return (row_idx, col_idx)
                
            except (ValueError, IndexError):
                print("❌ Formato inválido. Usa números separados por coma (ejemplo: 3,2)")
                continue

    def get_move_direction(self):
        """
        Pregunta al usuario hacia qué dirección quiere mover la pila.
        Retorna: 'U', 'D', 'L', 'R' o None si cancela
        """
        while True:
            print("\n¿Hacia qué dirección quieres mover?")
            print("  1. Arriba (↑)")
            print("  2. Abajo (↓)")
            print("  3. Izquierda (←)")
            print("  4. Derecha (→)")
            print("Escribe '0' para volver")
            
            choice = input("\nElige una opción: ").strip().lower()
            
            if choice == '0':
                return None
            
            if choice == '1':
                return 'U'  # Up
            elif choice == '2':
                return 'D'  # Down
            elif choice == '3':
                return 'L'  # Left
            elif choice == '4':
                return 'R'  # Right
            else:
                print("❌ Opción inválida. Intenta de nuevo.")
                continue

    def get_drops_distribution(self, start_row, start_col):
        """
        Pregunta al usuario cómo quiere distribuir las fichas al moverlas.
        Retorna: lista de enteros [drop1, drop2, ...] o None si cancela
        """
        stack = self.board.board[start_row][start_col]
        total_pieces = len(stack)
        
        print(f"\nLa pila tiene {total_pieces} ficha(s).")
        print(f"Puedes levantar máximo {min(total_pieces, self.board.size)} ficha(s) (límite de carga: {self.board.size})")
        
        while True:
            print("\n¿Cuántas fichas quieres levantar?")
            print("Escribe '0' para volver")
            
            pickup_input = input("Cantidad: ").strip().lower()
            
            if pickup_input == '0':
                return None
            
            try:
                pickup_count = int(pickup_input)
                
                # Validar cantidad
                if pickup_count < 1:
                    print("❌ Debes levantar al menos 1 ficha.")
                    continue
                
                if pickup_count > total_pieces:
                    print(f"❌ La pila solo tiene {total_pieces} ficha(s).")
                    continue
                
                if pickup_count > self.board.size:
                    print(f"❌ No puedes cargar más de {self.board.size} ficha(s).")
                    continue
                
                # Todo válido, ahora pedir distribución
                break
                
            except ValueError:
                print("❌ Debes ingresar un número.")
                continue
        
        # Ahora pedir cómo distribuir las fichas
        print(f"\nVas a mover {pickup_count} ficha(s).")
        print("Indica cuántas fichas dejar en cada casilla.")
        print(f"Ejemplo: Si mueves 3 fichas, puedes distribuir: 1,2 (dejas 1 en la primera casilla, 2 en la segunda)")
        print(f"O simplemente: {pickup_count} (dejas todas en la última casilla)")
        
        while True:
            print("\nEscribe '0' para volver")
            distribution_input = input("Distribución: ").strip().lower()
            
            if distribution_input == '0':
                return None
            
            try:
                # Parsear la distribución
                drops = [int(x.strip()) for x in distribution_input.split(',')]
                
                # Validar que sumen lo correcto
                if sum(drops) != pickup_count:
                    print(f"❌ La suma debe ser {pickup_count}. Tú sumaste: {sum(drops)}")
                    continue
                
                # Validar que todos sean positivos
                if any(d <= 0 for d in drops):
                    print("❌ Todos los números deben ser mayores a 0.")
                    continue
                
                # Todo válido
                print(f"✅ Distribución: {drops}")
                return drops
                
            except ValueError:
                print("❌ Formato inválido. Usa números separados por comas (ej: 1,2 o 3)")
                continue
