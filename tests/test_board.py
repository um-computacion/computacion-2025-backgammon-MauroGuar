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

        # Crea una instancia de Board para ser usada en las pruebas
        self.board = Board()

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

    def test_map_normal_index_for_white_checkers(self):
        """Verifica el mapeo de índices para el jugador con fichas blancas."""
        # Triángulos superiores para blancas (1-12)
        self.assertEqual(self.board.map_normal_index(1, True), (True, 11))
        self.assertEqual(self.board.map_normal_index(6, True), (True, 6))
        self.assertEqual(self.board.map_normal_index(12, True), (True, 0))

        # Triángulos inferiores para blancas (13-24)
        self.assertEqual(self.board.map_normal_index(13, True), (False, 11))
        self.assertEqual(self.board.map_normal_index(18, True), (False, 6))
        self.assertEqual(self.board.map_normal_index(24, True), (False, 0))

    def test_map_normal_index_for_black_checkers(self):
        """Verifica el mapeo de índices para el jugador con fichas negras."""
        # Triángulos inferiores para negras (1-12)
        self.assertEqual(self.board.map_normal_index(1, False), (False, 0))
        self.assertEqual(self.board.map_normal_index(6, False), (False, 5))
        self.assertEqual(self.board.map_normal_index(12, False), (False, 11))

        # Triángulos superiores para negras (13-24)
        self.assertEqual(self.board.map_normal_index(13, False), (True, 0))
        self.assertEqual(self.board.map_normal_index(18, False), (True, 5))
        self.assertEqual(self.board.map_normal_index(24, False), (True, 11))

    def test_replace_triangle(self):
        """Verifica que un solo triángulo se reemplaza correctamente."""
        new_triangle_top = [1, 2, "●"]
        new_triangle_bot = [2, 2, "○"]

        # Reemplaza un triángulo en el tablero superior (perspectiva de blancas)
        self.board.replace_triangle(1, True, new_triangle_top)
        # Índice normal 1 para blancas es el índice 11 en la lista top
        self.assertEqual(self.board.top_board_triangles[11], new_triangle_top)

        # Reemplaza un triángulo en el tablero inferior (perspectiva de negras)
        self.board.replace_triangle(1, False, new_triangle_bot)
        # Índice normal 1 para negras es el índice 0 en la lista bot
        self.assertEqual(self.board.bot_board_triangles[0], new_triangle_bot)

    def test_replace_multiple_triangles(self):
        """Verifica que múltiples triángulos se reemplazan correctamente en una llamada."""
        new_triangle1 = [1, 1, "○"]
        new_triangle2 = [2, 2, "●"]
        new_triangle3 = [3, 0, "●"]

        replacements = [
            (1, new_triangle1),  # Top board para blancas (índice 11)
            (24, new_triangle2),  # Bot board para blancas (índice 0)
            (12, new_triangle3),  # Top board para blancas (índice 0)
        ]

        self.board.replace_multiple_triangles(replacements, uses_white_checkers=True)

        self.assertEqual(self.board.top_board_triangles[11], new_triangle1)
        self.assertEqual(self.board.bot_board_triangles[0], new_triangle2)
        self.assertEqual(self.board.top_board_triangles[0], new_triangle3)


if __name__ == '__main__':
    unittest.main()
