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

    def test_move_checker_same_color(self):
        """Verifica que move_checker() mueve una ficha correctamente.
        Mueve de un lugar con fichas a otro con fichas (ambos del mismo color)
        """
        # Se colocan triángulos personalizados con una ficha para ambos jugadores
        custom_triangle_white = [1, 0, "●"]
        custom_triangle_black = [1, 0, "○"]
        self.board.replace_triangle(2, True, custom_triangle_white)
        self.board.replace_triangle(2, False, custom_triangle_black)

        # Mueve una ficha blanca del triángulo 1 (2 blancas) al triángulo 2 (1 blancas)
        self.board.move_checker(1, 2, True)
        self.assertEqual(self.board.__top_board_triangles__[11], [1, 0, "●"])
        self.assertEqual(self.board.__top_board_triangles__[10], [2, 0, "●"])

        # Mueve una ficha negra del triángulo 1 (5 negras) al triángulo 2 (1 negras)
        self.board.move_checker(1, 2, False)
        self.assertEqual(self.board.__bot_board_triangles__[0], [4, 0, "○"])
        self.assertEqual(self.board.__bot_board_triangles__[1], [2, 0, "○"])

    def test_move_checker_empty_triangle(self):
        """Verifica que move_checker() mueve una ficha correctamente.
        Mueve de un lugar con fichas a otro vacío.
        """
        # --- Pruebas para el jugador con fichas blancas ---
        # Mueve una ficha blanca del triángulo 1 (2 blancas) al triángulo 2 (vacío)
        self.board.move_checker(1, 2, True)
        self.assertEqual(self.board.__top_board_triangles__[11], [1, 0, "●"])
        self.assertEqual(self.board.__top_board_triangles__[10], [1, 0, "●"])

        # --- Pruebas para el jugador con fichas negras ---
        # Mueve una ficha negra del triángulo 1 (5 negras) al triángulo 2 (vacío)
        self.board.move_checker(1, 2, False)
        self.assertEqual(self.board.__bot_board_triangles__[0], [4, 0, "○"])
        self.assertEqual(self.board.__bot_board_triangles__[1], [1, 0, "○"])

    def test_move_checker_capture(self):
        """Verifica que move_checker() mueve una ficha correctamente.
        Mueve de un lugar con fichas a otro con una ficha enemiga (captura).
        """
        # Se colocan triángulos personalizados con una ficha para ambos jugadores
        custom_triangle_white = [1, 0, "●"]
        custom_triangle_black = [1, 0, "○"]
        self.board.replace_triangle(2, True, custom_triangle_black)
        self.board.replace_triangle(2, False, custom_triangle_white)

        # --- Pruebas para el jugador con fichas blancas ---
        # Mueve una ficha blanca del triángulo 1 (2 blancas) al triángulo 2 (1 negra)
        move_result = self.board.move_checker(1, 2, True)
        self.assertEqual(self.board.__top_board_triangles__[11], [1, 0, "●"])
        self.assertEqual(self.board.__top_board_triangles__[10], [1, 0, "●"])
        # Verifica que se devolvió True al comer la ficha enemiga
        self.assertTrue(move_result)
        # Verifica que la ficha negra ha sido capturada y movida a la barra
        self.assertEqual(self.board.__bar__[1], 1)

        # --- Pruebas para el jugador con fichas negras ---
        # Mueve una ficha negra del triángulo 1 (5 negras) al triángulo 2 (1 blanca)
        move_result = self.board.move_checker(1, 2, False)
        self.assertEqual(self.board.__bot_board_triangles__[0], [4, 0, "○"])
        self.assertEqual(self.board.__bot_board_triangles__[1], [1, 0, "○"])
        # Verifica que se devolvió True al comer la ficha enemiga
        self.assertTrue(move_result)
        # Verifica que la ficha blanca ha sido capturada y movida a la barra
        self.assertEqual(self.board.__bar__[0], 1)

    def test_get_possible_sums_tuple(self):
        test_tuples = ((1, 2), (3, 4), (5, 6), (2, 2), (3, 3, 3), (6, 6, 6, 6))
        expected_tuples = ((1, 2, 3), (3, 4, 7), (5, 6, 11), (2, 4), (3, 6, 9), (6, 12, 18, 24))
        for i, test in enumerate(test_tuples):
            with self.subTest(i=i):
                self.assertEqual(self.board.get_possible_sums_tuple(test), expected_tuples[i])

    def test_get_possible_moves_white_and_black(self):
        """Verifica get_possible_moves() para ambos jugadores en varios escenarios."""
        # Se colocan triángulos personalizados con una ficha para ambos jugadores
        custom_triangle_white = [1, 0, "●"]
        custom_triangle_black = [1, 0, "○"]
        self.board.replace_triangle(2, True, custom_triangle_black)
        self.board.replace_triangle(2, False, custom_triangle_white)

        # --- Pruebas para el jugador con fichas blancas ---
        # Triángulo con al menos una ficha propia y
        # objetivo vacío (Se permite mover)
        self.assertTupleEqual(self.board.get_possible_moves(1, True, (2,)), (3,))
        # Triángulo con al menos una ficha propia y
        # objetivo con una ficha enemiga (Se permite mover)
        self.assertTupleEqual(self.board.get_possible_moves(1, True, (1,)), (2,))
        # Dos dados. Triángulo con al menos una ficha propia
        # y objetivo con múltiples fichas enemiga (No se permite mover)
        self.assertTupleEqual(self.board.get_possible_moves(1, True, (1, 4)), (2, 5))
        # Movimiento fuera de límites (devuelve 25) # TODO Idear mejor esto
        self.assertTupleEqual(self.board.get_possible_moves(24, True, (1,)), (25,))
        # Movimiento con dados dobles
        self.assertTupleEqual(self.board.get_possible_moves(1, True, (2, 2, 2, 2)), (3, 5, 7, 9))

        # --- Pruebas para el jugador con fichas negras ---
        # Triángulo con al menos una ficha propia y
        # objetivo vacío (Se permite mover)
        self.assertTupleEqual(self.board.get_possible_moves(1, False, (2,)), (3,))
        # Triángulo con al menos una ficha propia y
        # objetivo con una ficha enemiga (Se permite mover)
        self.assertTupleEqual(self.board.get_possible_moves(1, False, (1,)), (2,))
        # Dos dados. Triángulo con al menos una ficha propia y
        # objetivo con múltiples fichas enemigas (No se permite mover)
        self.assertTupleEqual(self.board.get_possible_moves(1, False, (1, 4)), (2, 6))
        # Movimiento fuera de límites (devuelve 25)
        self.assertTupleEqual(self.board.get_possible_moves(24, False, (1,)), (25, ))
        # Movimiento con dados dobles
        self.assertTupleEqual(self.board.get_possible_moves(1, False, (2, 2, 2, 2)), (3, 9))


if __name__ == '__main__':
    unittest.main()
