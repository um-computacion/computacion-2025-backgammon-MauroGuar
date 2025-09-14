from itertools import combinations


class Board:
    """Representa un tablero de juego.

    Permite la creación y gestión del tablero de juego.

    Por default, se divide en seis triángulos (o casillas)
    en la parte superior (top) y seis en la inferior (bot/bottom).

    Los triángulos son representados por una lista, por ejemplo "[5, 2, "●"]".
    En donde 5 es la cantidad de fichas normales ("●" o "○"),
    "●" es el tipo de ficha en sí (que también puede ser un espacio en blanco " ")
    y 2 es el tipo de símbolo de selección:
    (0 = Ninguno; 1 = Resaltador de ficha seleccionada; 2 = Posible movimiento).
    Entonces, en este ejemplo, se representan 5 fichas blancas
    con un posible movimiento sobre ellas.

    La clase se encarga de mediar toda clase de cambios
    en el tablero (ej.: movimiento de fichas).

    Attributes:
        __top_board_triangles__: Una lista que contiene los triángulos superiores.
        __bot_board_triangles__: Una lista que contiene los triángulos inferiores.
        __bar__: Una lista que contiene la cantidad de fichas en la barra.
                [fichas blancas, fichas negras]
    """

    def __init__(self):
        """Inicializa una instancia de tablero de juego por defecto."""
        self.__top_board_triangles__ = []
        self.__bot_board_triangles__ = []
        self.__bar__ = []
        self.new_game_board()

    @property
    def top_board_triangles(self) -> list:
        """Obtiene los triángulos superiores del tablero."""
        return self.__top_board_triangles__

    @property
    def bot_board_triangles(self) -> list:
        """Obtiene los triángulos inferiores del tablero."""
        return self.__bot_board_triangles__

    def new_game_board(self):
        """Resetea el tablero de juego a un estado inicial por defecto."""
        self.__top_board_triangles__ = [[5, 0, "●"], [0, 0, " "], [0, 0, " "], [0, 0, " "], [3, 0, "○"], [0, 0, " "],
                                        [5, 0, "○"], [0, 0, " "], [0, 0, " "], [0, 0, " "], [0, 0, " "], [2, 0, "●"]]

        self.__bot_board_triangles__ = [[5, 0, "○"], [0, 0, " "], [0, 0, " "], [0, 0, " "], [3, 0, "●"], [0, 0, " "],
                                        [5, 0, "●"], [0, 0, " "], [0, 0, " "], [0, 0, " "], [0, 0, " "], [2, 0, "○"]]

        self.__bar__ = [0, 0]

    @staticmethod
    def map_normal_index(normal_index: int, uses_white_checkers: bool) -> tuple[bool, int]:
        """Mapea la entrada de índice normal a un índice compatible con las listas de triángulos.

        Args:
            normal_index: El índice normal (1-24).
            uses_white_checkers: Indica si el jugador usa fichas blancas.
        Returns:
            Una tupla que contiene un booleano que indica
            si el triángulo está en la parte superior o no
            y el índice correspondiente en la lista de triángulos.
        """
        # Si el jugador usa fichas blancas, los triángulos 1-12
        # están en la parte superior y los triángulos 13-24
        # están en la parte inferior.
        if uses_white_checkers:
            if 1 <= normal_index <= 12:
                return True, 12 - normal_index
            if 13 <= normal_index <= 24:
                return False, normal_index - 13

        # Si el jugador usa fichas negras, los triángulos 1-12
        # están en la parte inferior y los triángulos 13-24
        # están en la parte superior.
        else:
            if 1 <= normal_index <= 12:
                return False, 12 - normal_index
            if 13 <= normal_index <= 24:
                return True, normal_index - 13

    def replace_triangle(self, normal_index: int, uses_white_checkers: bool, new_triangle: list):
        """Reemplaza un triángulo en el tablero de juego.

        Args:
            normal_index: El ínidce normal (1-24).
            uses_white_checkers: Indica si el jugador usa fichas blancas.
            new_triangle: El nuevo triángulo que reemplazará al existente.
        """
        is_top, index = self.map_normal_index(normal_index, uses_white_checkers)
        if is_top:
            self.__top_board_triangles__[index] = new_triangle
        else:
            self.__bot_board_triangles__[index] = new_triangle

    def replace_multiple_triangles(self, replacements: list, uses_white_checkers: bool):
        """Reemplaza múltiples triángulos en el tablero de juego.

        Args:
            replacements: Una lista de tuplas, cada una conteniendo
                        el índice normal (1-24) y el nuevo triángulo.
                        Ejemplo: [(1, [3, 0, "●"]), (13, [2, 0, "○"])]
            uses_white_checkers: Indica si el jugador usa fichas blancas.
        """
        for normal_index, new_triangle in replacements:
            self.replace_triangle(normal_index, uses_white_checkers, new_triangle)

    def verify_checker_placement(self, normal_index: int, uses_white_checkers: bool) -> bool:
        """Verifica si una ficha puede ser colocada en un triángulo específico.

        Args:
            normal_index: El índice normal (1-24).
            uses_white_checkers: Indica si el jugador usa fichas blancas.
        Returns:
            True si la ficha puede ser colocada, False en caso contrario.
        """
        # Mapea el índice normal al índice de la lista correspondiente
        is_top, index = self.map_normal_index(normal_index, uses_white_checkers)
        # Obtiene el triángulo a verificar
        if is_top:
            verify_triangle = self.__top_board_triangles__[index]
        else:
            verify_triangle = self.__bot_board_triangles__[index]

        # Si el triángulo está vacío, se puede colocar la ficha
        if verify_triangle[0] == 0:
            return True

        if verify_triangle[0] > 0:
            # Si el triángulo tiene fichas del mismo color, se puede colocar la ficha
            if ((uses_white_checkers and verify_triangle[2] == "●") or
                    (not uses_white_checkers and verify_triangle[2] == "○")):
                return True

            # Si el triángulo tiene una sola ficha del color opuesto, se puede colocar la ficha
            elif verify_triangle[0] == 1:
                return True

        # Si ninguna de las condiciones anteriores se cumple, no se puede colocar la ficha
        return False

    def verify_movable_checker(self, normal_index: int, uses_white_checkers: bool) -> bool:
        """Verifica si una ficha en un triángulo específico puede ser movida.

        Args:
            normal_index: El índice normal (1-24).
            uses_white_checkers: Indica si el jugador usa fichas blancas.
        Returns:
            True si la ficha puede ser movida, False en caso contrario.
        """
        # Mapea el índice normal al índice de la lista correspondiente
        is_top, index = self.map_normal_index(normal_index, uses_white_checkers)
        if is_top:
            verify_triangle = self.__top_board_triangles__[index]
        else:
            verify_triangle = self.__bot_board_triangles__[index]

        # Si el triángulo tiene fichas del mismo color, se puede mover la ficha
        if verify_triangle[0] > 0 and ((uses_white_checkers and verify_triangle[2] == "●") or (
                not uses_white_checkers and verify_triangle[2] == "○")):
            return True
        # En caso contrario, no se puede mover la ficha
        return False

    def move_checker(self, normal_origin: int, normal_dest: int, uses_white_checkers: bool) -> bool:
        """Mueve una ficha de un triángulo a otro.

        No realiza ninguna verificación de validez del movimiento.
        Ya debe haberse verificado previamente.

        Args:
            normal_origin: El índice normal (1-24) del triángulo de origen.
            normal_dest: El índice normal (1-24) del triángulo de destino.
            uses_white_checkers: Indica si el jugador usa fichas blancas.
        Returns:
            True si una ficha fue comida durante el movimiento, False en caso contrario.
        """
        # Mapea los índices normales a los índices de las listas correspondientes
        org_is_top, org_index = self.map_normal_index(normal_origin, uses_white_checkers)
        if org_is_top:
            origin_triangle = self.__top_board_triangles__[org_index]
        else:
            origin_triangle = self.__bot_board_triangles__[org_index]
        dest_is_top, dest_index = self.map_normal_index(normal_dest, uses_white_checkers)
        if dest_is_top:
            dest_triangle = self.__top_board_triangles__[dest_index]
        else:
            dest_triangle = self.__bot_board_triangles__[dest_index]

        # Realiza el movimiento
        # Disminuye el conteo en el triángulo de origen
        # y actualiza el símbolo si es necesario
        origin_triangle[0] -= 1
        if origin_triangle[0] == 0:
            origin_triangle[2] = " "

        # Si el triángulo de destino tiene una sola ficha del color opuesto,
        # la ficha es comida y se actualiza la barra
        eaten_checker = False
        if dest_triangle[0] == 1 and ((uses_white_checkers and dest_triangle[2] == "○") or
                                      (not uses_white_checkers and dest_triangle[2] == "●")):
            if uses_white_checkers:
                self.__bar__[1] += 1
                dest_triangle = [1, 0, "●"]
            else:
                self.__bar__[0] += 1
                dest_triangle = [1, 0, "○"]
            eaten_checker = True

        # Si el triángulo de destino está vacío o tiene fichas del mismo color,
        # simplemente se aumenta el conteo y se actualiza el símbolo si es necesario
        else:
            dest_triangle[0] += 1
            if uses_white_checkers:
                dest_triangle[2] = "●"
            else:
                dest_triangle[2] = "○"

        self.replace_multiple_triangles([(normal_origin, origin_triangle), (normal_dest, dest_triangle)],
                                        uses_white_checkers)
        return eaten_checker

    @staticmethod
    def get_possible_sums_tuple(numbers: tuple[int, ...]) -> tuple[int, ...]:
        """Calcula todas las sumas posibles de
        combinaciones de números positivos en una tupla.
        Sin repeticiones y ordenadas de menor a mayor.

        Args:
            numbers: Una tupla de números enteros.
        Returns:
            Una tupla ordenada de todas las sumas posibles de combinaciones.
        """
        # Filtra solo los números positivos
        positive_numbers = [num for num in numbers if num > 0]

        # Hace un set para evitar sumas repetidas
        possible_sums = set()

        # Calcula todas las combinaciones posibles
        for i in range(1, len(positive_numbers) + 1):
            for combo in combinations(positive_numbers, i):
                possible_sums.add(sum(combo))

        # Retorna una tupla ordenada de las sumas posibles
        return tuple(sorted(list(possible_sums)))

    def get_possible_moves(self, selected_checker_normal: int,
                           uses_white_checkers: bool, dice_numbers: tuple[int, ...]) -> tuple[int, ...]:
        """Calcula y devuelve todos los movimientos posibles para una ficha seleccionada.

        Args:
            selected_checker_normal: El índice normal (1-24) de la ficha seleccionada.
            uses_white_checkers: Indica si el jugador usa fichas blancas.
            dice_numbers: Una tupla de números representando los dados lanzados.
        Returns:
            Una tupla de índices normales (1-24) a los que la ficha puede moverse.
            Incluye 25 si la ficha puede ser retirada.
        """
        movements_possible = []
        # Obtiene todas las sumas posibles de los números de los dados
        movements_to_check = self.get_possible_sums_tuple(dice_numbers)

        # Verifica cada movimiento posible
        for move in movements_to_check:
            objective_triangle_normal = selected_checker_normal + move
            # Si el movimiento está dentro del rango del tablero lo verifica
            if objective_triangle_normal <= 24:
                if self.verify_checker_placement(objective_triangle_normal, uses_white_checkers):
                    movements_possible.append(objective_triangle_normal)
            # Si el movimiento excede el rango del tablero,
            # significa que la ficha puede ser retirada
            elif objective_triangle_normal == 25:
                movements_possible.append(25)

        # Retorna una tupla de movimientos posibles
        return tuple(movements_possible)
