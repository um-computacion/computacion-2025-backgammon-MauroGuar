class Board:
    """Representa un tablero de juego.

    Permite la creación y gestión del tablero de juego.

    Por default, se divide en seis triángulos (o casillas)
    en la parte superior (top) y seis en la inferior (bot/bottom).

    Los triángulos son representados por una lista, por ejemplo "[5, 2, "●"]".
    En donde 5 es la cantidad de fichas normales ("●" o "○"),
    es el tipo de ficha en sí (que también puede ser un espacio en blanco " ")
    y 2 es el tipo de símbolo de selección:
    (0 = Ninguno; 1 = Resaltador de ficha seleccionada; 2 = Posible movimiento).
    Entonces, en este ejemplo, se representan 5 fichas blancas
    con un posible movimiento sobre ellas.

    La clase se encarga de mediar toda clase de cambios
    en el tablero (ej.: movimiento de fichas).

    Attributes:
        __top_board_triangles__: Una lista que contiene los triángulos superiores.
        __bot_board_triangles__: Una lista que contiene los triángulos inferiores.
    """

    def __init__(self, top_board_triangles: list = None, bot_board_triangles: list = None):
        """Inicializa una instancia de tablero de juego.

        Si no se proporcionan los triángulos superiores o inferiores,
        se crea una nueva.

        Args:
            top_board_triangles: Una lista con los triángulos superiores. Valor default: None.
            bot_board_triangles: Una lista con los triángulos inferiores. Valor default: None.
        """
        self.__top_board_triangles__ = top_board_triangles
        self.__bot_board_triangles__ = bot_board_triangles
        if not self.__top_board_triangles__ or not self.__bot_board_triangles__:
            self.new_game_board()

    @property
    def top_board_triangles(self) -> list:
        """La lista con los triángulos de la parte superior."""
        return self.__top_board_triangles__

    @property
    def bot_board_triangles(self) -> list:
        """La lista con los triángulos de la parte inferior."""
        return self.__bot_board_triangles__

    def new_game_board(self):
        """Resetea el tablero de juego a un estado inicial."""
        self.__top_board_triangles__ = [[5, 0, "●"], [0, 0, " "], [0, 0, " "], [0, 0, " "], [3, 0, "○"], [0, 0, " "],
                                        [5, 0, "○"], [0, 0, " "], [0, 0, " "], [0, 0, " "], [0, 0, " "], [2, 0, "●"]]

        self.__bot_board_triangles__ = [[5, 0, "○"], [0, 0, " "], [0, 0, " "], [0, 0, " "], [3, 0, "●"], [0, 0, " "],
                                        [5, 0, "●"], [0, 0, " "], [0, 0, " "], [0, 0, " "], [0, 0, " "], [2, 0, "○"]]
    
    def map_normal_index(self, normal_index: int, uses_white_checkers: bool) -> tuple[bool, int]:
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
            elif 13 <= normal_index <= 24:
                return False, 24 - normal_index

        # Si el jugador usa fichas negras, los triángulos 1-12
        # están en la parte inferior y los triángulos 13-24
        # están en la parte superior.
        else:
            if 1 <= normal_index <= 12:
                return False, normal_index - 1
            elif 13 <= normal_index <= 24:
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