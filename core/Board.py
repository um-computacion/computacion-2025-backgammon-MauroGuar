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