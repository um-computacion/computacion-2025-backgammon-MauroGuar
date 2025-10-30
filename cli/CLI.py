from core.Board import Board


class CLI:
    """Maneja la interfaz gráfica por consola.

    Se encarga de administrar toda la interfaz gráfica del juego.

    Attributes:
        __board__: El tablero del juego.
        SELECTED_CHECKER_TOP_STR: Carácter para simbolizar la ficha seleccionada (en top).
        SELECTED_CHECKER_BOT_STR: Carácter para simbolizar la ficha seleccionada (en bot).
        POSIBLE_CHECKER_TOP_STR: Tupla de carácteres para simbolizar un posible movimiento (en top).
        POSIBLE_CHECKER_BOT_STR: Tupla de carácteres para simbolizar un posible movimiento (en bot).
    """
    SELECTED_CHECKER_TOP_STR = "▲"
    SELECTED_CHECKER_BOT_STR = "▼"
    POSIBLE_CHECKER_TOP_STR = ("⊕", "△")
    POSIBLE_CHECKER_BOT_STR = ("⊕", "▽")

    def __init__(self, board: Board):
        """Inicializa una instancia de la interfaz gráfica por consola.

        Args:
            board: El tablero del juego.
        """
        self.__board__ = board

    def print_board(self, uses_white_checkers: bool):
        """Imprime el tablero del juego en la consola.

        Args:
            uses_white_checkers: Indica si el jugador actual usa fichas blancas.
        """
        board_top_triangles = self.__board__.top_board_triangles
        board_bot_triangles = self.__board__.bot_board_triangles

        # Si el jugador actual no usa fichas blancas,
        # se invierten los triángulos para que la perspectiva sea correcta.
        if not uses_white_checkers:
            tmp_top_triangles = board_top_triangles.copy()
            board_top_triangles = list(reversed(board_bot_triangles))
            board_bot_triangles = list(reversed(tmp_top_triangles))

        # Imprime el tablero superior.
        print(self.generate_top_board_str(board_top_triangles, uses_white_checkers), end="")
        # Imprimir el tablero medio.
        print(self.generate_middle_board(), end="")
        # Imprime el tablero inferior.
        print(self.generate_bottom_board_str(board_bot_triangles, uses_white_checkers), end="")

    def character_to_put_top(self, line_number: int, triangle: list) -> str:
        """Determina el carácter a colocar
        (ficha normal / espacio en blanco / símbolo de selección)
        en una línea específica de un triángulo superior.

        Args:
            line_number: El número de línea actual (1-indexed).
            triangle: La lista que representa el triángulo actual.
        """

        # Si la suma de la cantidad de fichas normales y el tipo de símbolo de selección
        # es mayor o igual al número de línea actual, entonces se debe colocar un carácter.
        if triangle[0] + triangle[1] >= line_number:
            # Si la cantidad de fichas normales es mayor o igual al número de línea actual,
            # se coloca la ficha normal (o espacio en blanco).
            if triangle[0] >= line_number:
                return triangle[2]

            # Si no, se debe colocar un símbolo de selección.
            if triangle[1] == 1:
                return self.SELECTED_CHECKER_TOP_STR
            else:
                return self.POSIBLE_CHECKER_TOP_STR[line_number - triangle[0] - 1]

        # Si no se debe colocar ningún carácter, se devuelve un espacio en blanco.
        return " "

    def generate_top_board_str(self, top_board_triangles: list, uses_white_checkers: bool) -> str:
        """Genera la representación en cadena del tablero superior.

        Args:
            top_board_triangles: La lista con los triángulos de la parte superior.
            uses_white_checkers: Indica si el jugador actual usa fichas blancas.
        Returns:
            str: Una cadena que representa el tablero superior.
        """
        # Encabezado del tablero superior.
        if uses_white_checkers:
            top_board_str = (
                "  ───────────────────────────────────────\n"
                "   c  b  a  9  8  7     6  5  4  3  2  1\n"
                "┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐\n"
                "│  ▼  ▼  ▼  ▼  ▼  ▼  │  ▼  ▼  ▼  ▼  ▼  ▼  │\n"
            )
        else:
            top_board_str = (
                "  ───────────────────────────────────────\n"
                "   1  2  3  4  5  6     7  8  9  a  b  c\n"
                "┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐\n"
                "│  ▼  ▼  ▼  ▼  ▼  ▼  │  ▼  ▼  ▼  ▼  ▼  ▼  │\n"
            )

        # Determina la altura máxima de los triángulos para saber cuántas líneas dibujar.
        max_triangle_height = max(triangle[0] + triangle[1] for triangle in top_board_triangles)

        # Genera cada línea del tablero superior.
        for actual_line_number in range(1, max_triangle_height + 1):
            # Lista para almacenar las partes de la línea actual.
            line_parts = ["│"]

            # Recorre los primeros 6 triángulos (de izquierda a derecha).
            for i in range(6):
                # Obtiene el carácter a colocar en la línea actual para el triángulo i
                # y lo agrega a la lista de partes de la línea.
                char = self.character_to_put_top(actual_line_number, top_board_triangles[i])
                line_parts.append(f"  {char}")

            # Agrega el separador central de la línea.
            line_parts.append("  │")

            # Recorre los últimos 6 triángulos (de izquierda a derecha).
            for i in range(6, 12):
                char = self.character_to_put_top(actual_line_number, top_board_triangles[i])
                line_parts.append(f"  {char}")

            line_parts.append("  │\n")

            # Une las partes de la línea y las agrega a la cadena del tablero superior.
            top_board_str += "".join(line_parts)

        return top_board_str

    def character_to_put_bottom(self, line_number: int, triangle: list) -> str:
        """Determina el carácter a colocar
        (ficha normal / espacio en blanco / símbolo de selección)
        en una línea específica de un triángulo inferior.

        Args:
            line_number: El número de línea actual (1-indexed).
            triangle: La lista que representa el triángulo actual.
        """
        # Si la suma de la cantidad de fichas normales y el tipo de símbolo de selección
        # es mayor o igual al número de línea actual, entonces se debe colocar un carácter.
        if triangle[0] + triangle[1] >= line_number:
            # Si la cantidad de fichas normales es mayor o igual al número de línea actual,
            # se coloca la ficha normal (o espacio en blanco).
            if triangle[0] >= line_number:
                return triangle[2]

            # Si no, se debe colocar un símbolo de selección.
            if triangle[1] == 1:
                return self.SELECTED_CHECKER_BOT_STR
            else:
                return self.POSIBLE_CHECKER_BOT_STR[line_number - triangle[0] - 1]

        # Si no se debe colocar ningún carácter, se devuelve un espacio en blanco.
        return " "

    def generate_bottom_board_str(self, bottom_board_triangles: list, uses_white_checkers: bool) -> str:
        """Genera la representación en cadena del tablero inferior.

        Args:
            bottom_board_triangles: La lista con los triángulos de la parte inferior.
        Returns:
            str: Una cadena que representa el tablero inferior.
        """

        # Determina la altura máxima de los triángulos para saber cuántas líneas dibujar.
        max_triangle_height = max(triangle[0] + triangle[1] for triangle in bottom_board_triangles)

        # Utiliza una lista temporal para almacenar las líneas del tablero inferior
        # y poder insertarlas en orden inverso para que se dibujen de abajo hacia arriba.
        str_tmp_pile = []
        for actual_line_number in range(1, max_triangle_height + 1):
            line_parts = ["│"]

            for i in range(6):
                char = self.character_to_put_bottom(actual_line_number, bottom_board_triangles[i])
                line_parts.append(f"  {char}")

            line_parts.append("  │")

            for i in range(6, 12):
                char = self.character_to_put_bottom(actual_line_number, bottom_board_triangles[i])
                line_parts.append(f"  {char}")

            line_parts.append("  │\n")

            # Inserta la línea actual al inicio de la lista temporal
            # para que las líneas se dibujen de abajo hacia arriba.
            str_tmp_pile.insert(0, "".join(line_parts))

        # Une todas las líneas almacenadas en la lista temporal
        bottom_board_str = "".join(str_tmp_pile)

        # Agrega el pie del tablero inferior.
        if uses_white_checkers:
            bottom_board_str += (
                "│  ▲  ▲  ▲  ▲  ▲  ▲  │  ▲  ▲  ▲  ▲  ▲  ▲  │\n"
                "└──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘\n"
                "   d  e  f  g  h  i     j  k  l  m  n  o   \n"
                "  ───────────────────────────────────────\n"
            )
        else:
            bottom_board_str += (
                "│  ▲  ▲  ▲  ▲  ▲  ▲  │  ▲  ▲  ▲  ▲  ▲  ▲  │\n"
                "└──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘\n"
                "   o  n  m  l  k  j     i  h  g  f  e  d   \n"
                "  ───────────────────────────────────────\n"
            )

        return bottom_board_str

    def generate_middle_board(self) -> str:
        """Genera la representación en cadena del tablero medio.
        
        Returns:
            str: Una cadena que representa el tablero medio.
        """
        # Obtiene la cantidad de fichas en la barra para ambos jugadores.
        white_check_num, black_check_num = self.__board__.board_bar

        # Genera la cadena del tablero medio con espacios en blanco por defecto.
        middle_board_str = ("│                    │                    │\n"
                            "│                    │                    │\n"
                            "│                    │                    │\n"
                            )

        # Si hay fichas en la barra, actualiza la cadena del tablero medio
        # para mostrar la cantidad de fichas.
        if white_check_num != 0 or black_check_num != 0:
            # Calcula la cantidad de dígitos en los números de fichas
            white_check_digit_num = len(str(white_check_num))
            black_check_digit_num = len(str(black_check_num))

            # Calcula la cantidad de espacios necesarios para alinear los números.
            white_space_num = 15 - white_check_digit_num
            black_space_num = 15 - black_check_digit_num

            # Genera la cadena del tablero medio con los números de fichas alineados.
            middle_board_str = ("│                    │                    │\n"
                                f"│{' ' * black_space_num}{black_check_num} ↠ ○ │"
                                f" ● ↞ {white_check_num}{' ' * white_space_num}│\n"
                                "│                    │                    │\n"
                                )

        return middle_board_str

    @staticmethod
    def translate_user_input_select(user_input: str) -> int:
        """Traduce la entrada del usuario para seleccionar un triángulo.

        Args:
            user_input: La entrada del usuario como cadena.
        Returns:
            int: El índice del triángulo seleccionado (1-25) o -1 si la entrada es inválida.
        """
        # Carácteres permitidos para seleccionar triángulos.
        allowed_inputs = tuple("123456789abcdefghijklmnop")

        # Verifica si la entrada del usuario es válida.
        if user_input.lower() in allowed_inputs and len(user_input) == 1:
            return allowed_inputs.index(user_input.lower()) + 1
        return -1
