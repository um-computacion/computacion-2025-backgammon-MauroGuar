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
        __num_checkers_board_player__: Una lista con la cantidad total de fichas en el tablero por jugador.
                [fichas blancas, fichas negras]
        __num_checkers_total__: La cantidad total de fichas por jugador (15).
        __selected_checker__: El índice normal (1-24) de la ficha seleccionada actualmente, o None si ninguna.
        __board_bar__: Una lista que contiene la cantidad de fichas en la barra.
                [fichas blancas, fichas negras]
        __checkers_off__: Una lista que contiene la cantidad de fichas retiradas del tablero.
                [fichas blancas, fichas negras]
        __is_bar_empty__: Una lista de booleanos que indica si la barra de cada jugador está vacía.
                [fichas blancas, fichas negras]
        __off_tray_posible_move__: Una lista que indica si el jugador puede mover una ficha al área de retiro.
                [fichas blancas, fichas negras]
    """

    def __init__(self):
        """Inicializa una instancia de tablero de juego por defecto."""
        self.__top_board_triangles__ = []
        self.__bot_board_triangles__ = []
        self.__num_checkers_board_player__ = []
        self.__num_checkers_total__ = 15
        self.__selected_checker__ = None
        self.__board_bar__ = []
        self.__checkers_off__ = []
        self.__is_bar_empty__ = []
        self.__off_tray_posible_move__ = []
        self.new_game_board()

    @property
    def top_board_triangles(self) -> list:
        """Triángulos superiores del tablero."""
        return self.__top_board_triangles__

    @property
    def bot_board_triangles(self) -> list:
        """Triángulos inferiores del tablero."""
        return self.__bot_board_triangles__

    @property
    def selected_checker(self) -> int | None:
        """Índice normal de la ficha seleccionada actualmente."""
        return self.__selected_checker__

    @property
    def board_bar(self) -> list:
        """Cantidad de fichas en la barra del tablero.

        [fichas blancas, fichas negras]
        """
        return self.__board_bar__

    @property
    def is_bar_empty(self) -> list:
        """Indica si la barra de cada jugador está vacía.

        [fichas blancas, fichas negras]
        """
        return self.__is_bar_empty__

    @property
    def checkers_off(self) -> list:
        """Cantidad de fichas retiradas del tablero.

        [fichas blancas, fichas negras]
        """
        return self.__checkers_off__

    @property
    def off_tray_posible_move(self) -> list:
        """Indica si el jugador puede mover una ficha al área de retiro.

        [fichas blancas, fichas negras]
        """
        return self.__off_tray_posible_move__

    def new_game_board(self):
        """Resetea el tablero de juego a un estado inicial por defecto."""
        self.__top_board_triangles__ = [[5, 0, "●"], [0, 0, " "], [0, 0, " "], [0, 0, " "], [3, 0, "○"], [0, 0, " "],
                                        [5, 0, "○"], [0, 0, " "], [0, 0, " "], [0, 0, " "], [0, 0, " "], [2, 0, "●"]]

        self.__bot_board_triangles__ = [[5, 0, "○"], [0, 0, " "], [0, 0, " "], [0, 0, " "], [3, 0, "●"], [0, 0, " "],
                                        [5, 0, "●"], [0, 0, " "], [0, 0, " "], [0, 0, " "], [0, 0, " "], [2, 0, "○"]]
        self.__num_checkers_board_player__ = [15, 15]
        self.__selected_checker__ = None
        self.__board_bar__ = [0, 0]
        self.__checkers_off__ = [0, 0]
        self.__is_bar_empty__ = [True, True]
        self.__can_take_out__ = [False, False]
        self.__off_tray_posible_move__ = [False, False]

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

    def get_triangle_from_normal(self, normal_index: int, uses_white_checker: bool) -> list:
        """Obiene el triángulo correspondiente a un índice normal.

        Args:
            normal_index: El índice normal (1-24).
            uses_white_checkers: Indica si el jugador usa fichas blancas.
        Returns:
            list: El triángulo del tablero.
        """
        is_top, index = self.map_normal_index(normal_index, uses_white_checker)
        if is_top:
            return self.__top_board_triangles__[index]
        else:
            return self.__bot_board_triangles__[index]

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
        # Obtiene el triángulo a verificar
        verify_triangle = self.get_triangle_from_normal(normal_index, uses_white_checkers)

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
        # Obtiene el triángulo a verificar
        verify_triangle = self.get_triangle_from_normal(normal_index, uses_white_checkers)

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
        # Obtiene los triángulos de origen y destino
        origin_triangle = self.get_triangle_from_normal(normal_origin, uses_white_checkers)
        dest_triangle = self.get_triangle_from_normal(normal_dest, uses_white_checkers)

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
                self.add_checker_to_bar(uses_white_checkers)
                dest_triangle = [1, 0, "●"]
            else:
                self.add_checker_to_bar(uses_white_checkers)
                dest_triangle = [1, 0, "○"]
            eaten_checker = True

        # Si el triángulo de destino está vacío o tiene fichas del mismo color,
        # simplemente se aumenta el conteo y se actualiza el símbolo si es necesario
        else:
            dest_triangle[0] += 1
            dest_triangle[2] = "●" if uses_white_checkers else "○"

        self.replace_multiple_triangles([(normal_origin, origin_triangle), (normal_dest, dest_triangle)],
                                        uses_white_checkers)
        return eaten_checker

    @staticmethod
    def generate_all_dice_combinations(dice_numbers: tuple[int, ...]) -> tuple:
        dice_combinations = []
        for i in range(1, len(dice_numbers) + 1):
            for combo in combinations(dice_numbers, i):
                if combo not in dice_combinations:
                    dice_combinations.append(combo)
                if 2 <= len(combo) == len(set(combo)):
                    dice_combinations.append(combo[::-1])

        return tuple(dice_combinations)

    def get_possible_dice_combinations(self, selected_checker_normal: int,
                                       uses_white_checkers: bool, dice_numbers: tuple[int, ...]) -> tuple:
        possible_dice_combs = []
        dice_combs_to_check = self.generate_all_dice_combinations(dice_numbers)

        for dice_comb in dice_combs_to_check:
            possible_dice_nums = []
            dest_normal_index = selected_checker_normal
            for dice_num in dice_comb:
                target_normal_index = dest_normal_index + dice_num
                if target_normal_index <= 24 and self.verify_checker_placement(target_normal_index,
                                                                               uses_white_checkers):
                    dest_normal_index += dice_num
                    possible_dice_nums.append(dice_num)
                elif target_normal_index > 24 and self.verify_player_can_take_out(uses_white_checkers):
                    if target_normal_index == 25:
                        dest_normal_index += dice_num
                        possible_dice_nums.append(dice_num)
                    elif target_normal_index > 25 and selected_checker_normal == self.get_most_advanced_checker(
                            uses_white_checkers):
                        dest_normal_index += dice_num
                        possible_dice_nums.append(dice_num)
                else:
                    possible_dice_nums = []
                    break
            if tuple(possible_dice_nums) == dice_comb:
                possible_dice_combs.append(dice_comb)
        return tuple(possible_dice_combs)

    @staticmethod
    def map_dice_combinations_to_normal_indexes(selected_checker_normal: int, dice_combs: tuple) -> dict:
        possible_moves_normal = {}
        for dice_comb in dice_combs:
            dest_normal_index = selected_checker_normal
            for dice_num in dice_comb:
                dest_normal_index += dice_num
            possible_moves_normal[dest_normal_index] = dice_comb
        return possible_moves_normal

    def select_checker(self, normal_index: int, uses_white_checkers: bool, dice_numbers: tuple[int, ...]) -> dict:
        """Selecciona una ficha en un triángulo específico si es movible
        y marca los movimientos posibles en el tablero.

        Args:
            normal_index: El índice normal (1-24) del triángulo.
            uses_white_checkers: Indica si el jugador usa fichas blancas.
            dice_numbers: Una tupla de números representando los dados lanzados.
        Returns:
            bool: True si la ficha fue seleccionada, False en caso contrario.
        """
        # Deselecciona cualquier ficha previamente seleccionada
        self.deselect_checker(uses_white_checkers)

        # Obtiene el triángulo seleccionado
        selected_triangle = self.get_triangle_from_normal(normal_index, uses_white_checkers)

        # Verifica si la ficha puede ser movida
        if self.verify_movable_checker(normal_index, uses_white_checkers):
            poss_dice_combs = self.get_possible_dice_combinations(normal_index, uses_white_checkers, dice_numbers)
            if poss_dice_combs:
                # Actualiza el estado de la variable de ficha seleccionada
                self.__selected_checker__ = normal_index
                # Marca la ficha en el tablero como seleccionada
                # (1 = Resaltador de ficha seleccionada)
                selected_triangle[1] = 1
                self.replace_triangle(normal_index, uses_white_checkers, selected_triangle)

                poss_moves = self.map_dice_combinations_to_normal_indexes(normal_index, poss_dice_combs)
                possible_moves_normals = list(poss_moves.keys())
                for move_normal in possible_moves_normals:
                    if move_normal == 25:
                        self.__off_tray_posible_move__[0 if uses_white_checkers else 1] = True
                        continue
                    move_triangle = self.get_triangle_from_normal(move_normal, uses_white_checkers)
                    # Marca el triángulo como un posible movimiento
                    # (2 = Posible movimiento)
                    move_triangle[1] = 2
                    self.replace_triangle(move_normal, uses_white_checkers, move_triangle)
                return poss_moves
        return {}

    def deselect_checker(self, uses_white_checkers: bool):
        """Verifica si hay un triángulo seleccionado. Si es así, lo deselecciona.
        Además, limpia todas las marcas de posibles movimientos en el tablero.

        Args:
            uses_white_checkers: Indica si el jugador usa fichas blancas.
        """
        # Si hay una ficha seleccionada la deselecciona
        if self.__selected_checker__ is not None:
            # Obtiene el triángulo seleccionado
            selected_triangle = self.get_triangle_from_normal(self.__selected_checker__, uses_white_checkers)
            # Si el triángulo está marcado como seleccionado para el jugador, lo deselecciona
            if selected_triangle[1] == 1:
                selected_triangle[1] = 0
                self.replace_triangle(self.__selected_checker__, uses_white_checkers, selected_triangle)
                self.__selected_checker__ = None

        # Quita como posible movimiento el retiro de ficha
        self.__off_tray_posible_move__ = [False, False]

        # Limpia todas las marcas de posibles movimientos en el tablero
        for normal_index in range(1, 25):
            triangle_to_check = self.get_triangle_from_normal(normal_index, uses_white_checkers)
            if triangle_to_check[1] == 2:
                triangle_to_check[1] = 0
                self.replace_triangle(normal_index, uses_white_checkers, triangle_to_check)

    def add_checker_to_bar(self, uses_white_checkers: bool):
        """Agrega una ficha a la barra del tablero.

        Args:
            uses_white_checkers: Indica si el jugador usa fichas blancas.
        """
        player_num = 1 if uses_white_checkers else 0
        self.__board_bar__[player_num] += 1
        self.__num_checkers_board_player__[player_num] -= 1
        self.__is_bar_empty__[player_num] = False

    def remove_checker_from_bar(self, uses_white_checkers: bool):
        """Remueve una ficha de la barra del tablero.
        Actualiza el estado de la barra si queda vacía.

        Args:
            uses_white_checkers: Indica si el jugador usa fichas blancas.
        """
        player_num = 0 if uses_white_checkers else 1
        if self.__board_bar__[player_num] > 0:
            self.__board_bar__[player_num] -= 1
            if self.__board_bar__[player_num] == 0:
                self.__is_bar_empty__[player_num] = True

    def verify_player_can_take_out(self, uses_white_checkers: bool) -> bool:
        """Verifica si un jugador puede comenzar a retirar sus fichas del tablero.

        Args:
            uses_white_checkers: Indica si el jugador usa fichas blancas.
        Returns:
            bool: True si el jugador puede comenzar a retirar fichas, False en caso contrario.
        """
        player_num = 0 if uses_white_checkers else 1
        # Si hay fichas en la barra, no puede retirar
        if self.__board_bar__[player_num] > 0:
            return False

        # Verifica si todas las fichas están en el área de retiro
        total_num_checkers = self.__num_checkers_board_player__[player_num]
        checkers_count = 0
        home_start = 19
        home_end = 25
        for normal_index in range(home_start, home_end):
            triangle_to_check = self.get_triangle_from_normal(normal_index, uses_white_checkers)
            count_checkers_in_triangle = triangle_to_check[0]
            if count_checkers_in_triangle > 0 and ((uses_white_checkers and triangle_to_check[2] == "●") or
                                                   (not uses_white_checkers and triangle_to_check[2] == "○")):
                checkers_count += count_checkers_in_triangle
        # Si todas las fichas están en el área de retiro, puede comenzar a retirar
        if checkers_count == total_num_checkers:
            return True
        return False

    def take_out_checker(self, normal_index: int, uses_white_checkers: bool):
        """Retira una ficha del tablero de juego.

        Args:
            uses_white_checkers: Indica si el jugador usa fichas blancas.
        """
        origin_triangle = self.get_triangle_from_normal(normal_index, uses_white_checkers)
        # Disminuye el conteo en el triángulo de origen
        # y actualiza el símbolo si es necesario
        origin_triangle[0] -= 1
        if origin_triangle[0] == 0:
            origin_triangle[2] = " "
        self.replace_triangle(normal_index, uses_white_checkers, origin_triangle)

        # Actualiza el conteo de fichas retiradas
        player_num = 0 if uses_white_checkers else 1
        self.__checkers_off__[player_num] += 1
        self.__num_checkers_board_player__[player_num] -= 1

    def is_match_won(self) -> tuple[bool, bool]:
        """Verifica si algún jugador ha ganado la partida.

        Returns:
            tuple: Un par de booleanos que indican si alguien ganó (primer booleano)
            y si el jugador de fichas blancas ganó (segundo booleano).
        """
        # Verifica si algún jugador ha retirado todas sus fichas
        if self.__checkers_off__[0] >= self.__num_checkers_total__:
            return True, True
        if self.__checkers_off__[1] >= self.__num_checkers_total__:
            return True, False
        return False, False

    def get_most_advanced_checker(self, uses_white_checkers: bool) -> int:
        """Obtiene el índice normal de la ficha más avanzada en el tablero para un jugador.

        Args:
            uses_white_checkers: Indica si el jugador usa fichas blancas.
        Returns:
            int: El índice normal (1-24) de la ficha más avanzada.
            Retorna -1 si no hay fichas en el tablero.
        """
        home_start = 19
        home_end = 25
        for normal_index in range(home_start, home_end):
            triangle_to_check = self.get_triangle_from_normal(normal_index, uses_white_checkers)
            if triangle_to_check[0] > 0 and ((uses_white_checkers and triangle_to_check[2] == "●") or
                                             (not uses_white_checkers and triangle_to_check[2] == "○")):
                return normal_index
        return -1
