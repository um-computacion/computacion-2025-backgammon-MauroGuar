import unittest
from core.Board import Board


class TestBoard(unittest.TestCase):
    """Conjunto de pruebas para la clase Board."""

    def setUp(self):
        """Prepara los recursos necesarios para cada prueba.

        Define el estado esperado del tablero por defecto para evitar
        repetirlo en cada prueba y mejorar la legibilidad.
        """
        self.default_top_board = [[5, 0, "●"], [0, 0, " "], [0, 0, " "], [0, 0, " "], [3, 0, "○"], [0, 0, " "],
                                  [5, 0, "○"], [0, 0, " "], [0, 0, " "], [0, 0, " "], [0, 0, " "], [2, 0, "●"]]

        self.default_bot_board = [[5, 0, "○"], [0, 0, " "], [0, 0, " "], [0, 0, " "], [3, 0, "●"], [0, 0, " "],
                                  [5, 0, "●"], [0, 0, " "], [0, 0, " "], [0, 0, " "], [0, 0, " "], [2, 0, "○"]]

    def test_init_creates_new_board_by_default(self):
        """Verifica que se crea un tablero nuevo por defecto al no pasar argumentos."""
        board = Board()
        self.assertListEqual(board.__top_board_triangles__,
                             self.default_top_board)
        self.assertListEqual(board.__bot_board_triangles__,
                             self.default_bot_board)

    def test_init_with_one_argument_creates_new_board(self):
        """Verifica que se crea un tablero nuevo si solo se pasa un argumento."""
        # Caso 1: Solo se proporciona el tablero superior.
        board_top_only = Board(top_board_triangles=[[1, 1, "X"]])
        self.assertListEqual(board_top_only.__top_board_triangles__,
                             self.default_top_board)
        self.assertListEqual(board_top_only.__bot_board_triangles__,
                             self.default_bot_board)

        # Caso 2: Solo se proporciona el tablero inferior.
        board_bot_only = Board(bot_board_triangles=[[1, 1, "Y"]])
        self.assertListEqual(board_bot_only.__top_board_triangles__,
                             self.default_top_board)
        self.assertListEqual(board_bot_only.__bot_board_triangles__,
                             self.default_bot_board)

    def test_init_with_custom_board(self):
        """Verifica que la inicialización funciona con un tablero personalizado."""
        custom_top = [[1, 0, "A"]]
        custom_bot = [[2, 0, "B"]]
        board = Board(top_board_triangles=custom_top,
                      bot_board_triangles=custom_bot)

        self.assertListEqual(board.__top_board_triangles__, custom_top)
        self.assertListEqual(board.__bot_board_triangles__, custom_bot)

    def test_new_game_board_resets_state(self):
        """Verifica que new_game_board() resetea el tablero a su estado inicial."""
        # Se crea un tablero personalizado.
        custom_top = [[1, 0, "A"]]
        custom_bot = [[2, 0, "B"]]
        board = Board(top_board_triangles=custom_top,
                      bot_board_triangles=custom_bot)

        # Se llama al método para resetear el tablero.
        board.new_game_board()

        # Se comprueba que el tablero ha vuelto al estado por defecto.
        self.assertListEqual(board.__top_board_triangles__,
                             self.default_top_board)
        self.assertListEqual(board.__bot_board_triangles__,
                             self.default_bot_board)



if __name__ == '__main__':
    unittest.main()
