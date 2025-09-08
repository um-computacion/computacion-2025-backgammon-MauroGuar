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

    def test_new_game_board_resets_state(self):
        """Verifica que new_game_board() resetea el tablero a su estado inicial."""
        # Se crea un tablero personalizado.
        custom_triangle = [9, 0, "○"]
        self.board.replace_triangle(1, True, custom_triangle)

        # Se llama al método para resetear el tablero.
        self.board.new_game_board()

        # Se comprueba que el tablero ha vuelto al estado por defecto.
        self.assertListEqual(self.board.__top_board_triangles__,
                             self.default_top_board)
        self.assertListEqual(self.board.__bot_board_triangles__,
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
        self.assertEqual(self.board.__top_board_triangles__[11], new_triangle_top)

        # Reemplaza un triángulo en el tablero inferior (perspectiva de negras)
        self.board.replace_triangle(1, False, new_triangle_bot)
        # Índice normal 1 para negras es el índice 0 en la lista bot
        self.assertEqual(self.board.__bot_board_triangles__[0], new_triangle_bot)

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

        self.assertEqual(self.board.__top_board_triangles__[11], new_triangle1)
        self.assertEqual(self.board.__bot_board_triangles__[0], new_triangle2)
        self.assertEqual(self.board.__top_board_triangles__[0], new_triangle3)

    def test_verify_checker_placement(self):
        """Verifica verify_checker_placement() en varios escenarios."""
        # Resetea el tablero a su estado inicial antes de cada verificación

        # Triángulo vacío (Se permite)
        self.assertTrue(self.board.verify_checker_placement(2, True))

        # Triángulo con fichas propias (Se permite)
        self.assertTrue(self.board.verify_checker_placement(1, True))

        # Triángulo con una sola ficha enemiga (Se permite)
        self.board.replace_triangle(3, True, [1, 0, "○"])
        self.assertTrue(self.board.verify_checker_placement(3, True))

        # Triángulo con múltiples fichas enemigas (No se permite)
        self.assertFalse(self.board.verify_checker_placement(8, True))

    def test_verify_movable_checker(self):
        """Verifica verify_movable_checker() en varios escenarios."""
        # Se colocan triángulos personalizados con una ficha para ambos jugadores
        custom_triangle_white = [1, 0, "●"]
        custom_triangle_black = [1, 0, "○"]
        self.board.replace_triangle(2, True, custom_triangle_white)
        self.board.replace_triangle(2, False, custom_triangle_black)

        # Jugador con fichas blancas
        # Triángulo con al menos una ficha propia (Se permite mover)
        self.assertTrue(self.board.verify_movable_checker(1, True))
        # Triángulo con exactamente una ficha propia (Se permite mover)
        self.assertTrue(self.board.verify_movable_checker(2, True))
        # Triángulo sin fichas propias (No se permite mover)
        self.assertFalse(self.board.verify_movable_checker(3, True))
        # Triángulo con fichas enemigas (No se permite mover)
        self.assertFalse(self.board.verify_movable_checker(13, True))

        # Mismo conjunto de pruebas para el jugador con fichas negras
        self.assertTrue(self.board.verify_movable_checker(1, False))
        self.assertTrue(self.board.verify_movable_checker(2, False))
        self.assertFalse(self.board.verify_movable_checker(3, False))
        self.assertFalse(self.board.verify_movable_checker(13, False))


if __name__ == '__main__':
    unittest.main()
