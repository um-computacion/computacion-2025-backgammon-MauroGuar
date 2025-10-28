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

        self.default_board_bar = [0, 0]  # [white_checkers_on_bar, black_checkers_on_bar]

        self.default_is_bar_empty = [True, True]  # [is_white_bar_empty, is_black_bar_empty]

        # Crea una instancia de Board para ser usada en las pruebas
        self.board = Board()

    def test_new_game_board_resets_state(self):
        """Verifica que new_game_board() resetea el tablero a su estado inicial."""
        # Se crea un tablero personalizado.
        custom_triangle = [9, 0, "○"]
        self.board.replace_triangle(1, True, custom_triangle)
        self.board.select_checker(1, True)
        self.board.__board_bar__ = [2, 3]
        self.board.__is_bar_empty__ = [False, False]

        # Se llama al método para resetear el tablero.
        self.board.new_game_board()

        # Se comprueba que el tablero ha vuelto al estado por defecto.
        self.assertListEqual(self.board.__top_board_triangles__,
                             self.default_top_board)
        self.assertListEqual(self.board.__bot_board_triangles__,
                             self.default_bot_board)
        self.assertIsNone(self.board.selected_checker)
        self.assertListEqual(self.board.__board_bar__,
                             self.default_board_bar)
        self.assertListEqual(self.board.__is_bar_empty__,
                             self.default_is_bar_empty)

    def test_map_normal_index_for_white_checkers(self):
        """Verifica el mapeo de índices para el jugador con fichas blancas."""
        # Triángulos superiores para blancas (1-12)
        self.assertEqual(self.board.map_normal_index(1, True), (True, 11))
        self.assertEqual(self.board.map_normal_index(6, True), (True, 6))
        self.assertEqual(self.board.map_normal_index(12, True), (True, 0))

        # Triángulos inferiores para blancas (13-24)
        self.assertEqual(self.board.map_normal_index(13, True), (False, 0))
        self.assertEqual(self.board.map_normal_index(18, True), (False, 5))
        self.assertEqual(self.board.map_normal_index(24, True), (False, 11))

    def test_map_normal_index_for_black_checkers(self):
        """Verifica el mapeo de índices para el jugador con fichas negras."""
        # Triángulos inferiores para negras (1-12)
        self.assertEqual(self.board.map_normal_index(1, False), (False, 11))
        self.assertEqual(self.board.map_normal_index(6, False), (False, 6))
        self.assertEqual(self.board.map_normal_index(12, False), (False, 0))

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
        # Índice normal 1 para negras es el índice 11 en la lista bot
        self.assertEqual(self.board.__bot_board_triangles__[11], new_triangle_bot)

    def test_replace_multiple_triangles(self):
        """Verifica que múltiples triángulos se reemplazan correctamente en una llamada."""
        new_triangle1 = [1, 1, "○"]
        new_triangle2 = [2, 2, "●"]
        new_triangle3 = [3, 0, "●"]

        replacements = [
            (1, new_triangle1),  # Top board para blancas (índice 11)
            (24, new_triangle2),  # Bot board para blancas (índice 11)
            (12, new_triangle3),  # Top board para blancas (índice 0)
        ]

        self.board.replace_multiple_triangles(replacements, uses_white_checkers=True)

        self.assertEqual(self.board.__top_board_triangles__[11], new_triangle1)
        self.assertEqual(self.board.__bot_board_triangles__[11], new_triangle2)
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

        # Mueve una ficha negra del triángulo 1 (2 negras) al triángulo 2 (1 negras)
        self.board.move_checker(1, 2, False)
        self.assertEqual(self.board.__bot_board_triangles__[11], [1, 0, "○"])
        self.assertEqual(self.board.__bot_board_triangles__[10], [2, 0, "○"])

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
        # Mueve una ficha negra del triángulo 1 (2 negras) al triángulo 2 (vacío)
        self.board.move_checker(1, 2, False)
        self.assertEqual(self.board.__bot_board_triangles__[11], [1, 0, "○"])
        self.assertEqual(self.board.__bot_board_triangles__[10], [1, 0, "○"])

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
        self.assertEqual(self.board.__board_bar__[1], 1)
        self.assertFalse(self.board.__is_bar_empty__[1])

        # --- Pruebas para el jugador con fichas negras ---
        # Mueve una ficha negra del triángulo 1 (2 negras) al triángulo 2 (1 blanca)
        move_result = self.board.move_checker(1, 2, False)
        self.assertEqual(self.board.__bot_board_triangles__[11], [1, 0, "○"])
        self.assertEqual(self.board.__bot_board_triangles__[10], [1, 0, "○"])
        # Verifica que se devolvió True al comer la ficha enemiga
        self.assertTrue(move_result)
        # Verifica que la ficha blanca ha sido capturada y movida a la barra
        self.assertEqual(self.board.__board_bar__[0], 1)
        self.assertFalse(self.board.__is_bar_empty__[0])

    def test_get_possible_sums_tuple(self):
        """Verifica get_possible_sums_tuple() con varios conjuntos de dados."""
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
        # Objetivo vacío (Se permite mover)
        self.assertTupleEqual(self.board.get_possible_moves(1, True, (2,)), (3,))
        # Objetivo con una ficha enemiga (Se permite mover)
        self.assertTupleEqual(self.board.get_possible_moves(1, True, (1,)), (2,))
        # Dos dados, un objetivo válido y otro bloqueado por el enemigo
        self.assertTupleEqual(self.board.get_possible_moves(1, True, (1, 6)), (2, 7))
        # Movimiento para retirar una ficha (devuelve 25)
        self.assertTupleEqual(self.board.get_possible_moves(24, True, (1,)), (25,))
        # Movimiento con dados dobles
        self.assertTupleEqual(self.board.get_possible_moves(19, True, (2, 2, 2, 2)), (21, 23, 25))

        # --- Pruebas para el jugador con fichas negras ---
        # Objetivo vacío (Se permite mover)
        self.assertTupleEqual(self.board.get_possible_moves(1, False, (2,)), (3,))
        # Objetivo con una ficha enemiga (Se permite mover)
        self.assertTupleEqual(self.board.get_possible_moves(1, False, (1,)), (2,))
        # Dos dados, ambos objetivos son válidos (uno es captura, el otro vacío)
        self.assertTupleEqual(self.board.get_possible_moves(1, False, (1, 4)), (2, 5))
        # Movimiento para retirar una ficha (devuelve 25)
        self.assertTupleEqual(self.board.get_possible_moves(24, False, (1,)), (25,))
        # Movimiento con dados dobles a casillas vacías
        self.assertTupleEqual(self.board.get_possible_moves(1, False, (2, 2, 2, 2)), (3, 5, 7, 9))

    def test_add_checker_to_bar_white(self):
        """Verifica add_checker_to_bar() para el jugador con fichas blancas."""
        self.assertEqual(self.board.__board_bar__[0], 0)
        self.assertTrue(self.board.__is_bar_empty__[0])
        self.board.add_checker_to_bar(True)  # White
        self.assertEqual(self.board.__board_bar__[1], 1)
        self.assertFalse(self.board.__is_bar_empty__[1])

    def test_add_checker_to_bar_black(self):
        """Verifica add_checker_to_bar() para el jugador con fichas negras."""
        self.assertEqual(self.board.__board_bar__[1], 0)
        self.assertTrue(self.board.__is_bar_empty__[1])
        self.board.add_checker_to_bar(False)  # Black
        self.assertEqual(self.board.__board_bar__[0], 1)
        self.assertFalse(self.board.__is_bar_empty__[0])

    def test_add_multiple_checkers_to_bar(self):
        """Verifica add_checker_to_bar() al agregar múltiples fichas a la barra."""
        self.board.add_checker_to_bar(True)
        self.board.add_checker_to_bar(True)
        self.assertEqual(self.board.__board_bar__[1], 2)
        self.board.add_checker_to_bar(False)
        self.board.add_checker_to_bar(False)
        self.board.add_checker_to_bar(False)
        self.assertEqual(self.board.__board_bar__[0], 3)

    def test_remove_checker_from_bar_white(self):
        """Verifica remove_checker_from_bar() para el jugador con fichas blancas."""
        self.board.add_checker_to_bar(False)
        self.board.add_checker_to_bar(False)
        self.board.remove_checker_from_bar(True)
        self.assertEqual(self.board.__board_bar__[0], 1)
        self.assertFalse(self.board.__is_bar_empty__[0])
        self.board.remove_checker_from_bar(True)
        self.assertEqual(self.board.__board_bar__[0], 0)
        self.assertTrue(self.board.__is_bar_empty__[0])

    def test_remove_checker_from_bar_black(self):
        """Verifica remove_checker_from_bar() para el jugador con fichas negras."""
        self.board.add_checker_to_bar(True)
        self.board.add_checker_to_bar(True)
        self.board.remove_checker_from_bar(False)
        self.assertEqual(self.board.__board_bar__[1], 1)
        self.assertFalse(self.board.__is_bar_empty__[1])
        self.board.remove_checker_from_bar(False)
        self.assertEqual(self.board.__board_bar__[1], 0)
        self.assertTrue(self.board.__is_bar_empty__[1])

    def test_remove_from_empty_bar_white(self):
        """Verifica remove_checker_from_bar() al intentar remover de una barra vacía."""
        self.assertEqual(self.board.__board_bar__[0], 0)
        self.assertTrue(self.board.__is_bar_empty__[0])
        self.board.remove_checker_from_bar(True)
        self.assertEqual(self.board.__board_bar__[0], 0)
        self.assertTrue(self.board.__is_bar_empty__[0])

    def test_remove_from_empty_bar_black(self):
        """Verifica remove_checker_from_bar() al intentar remover de una barra vacía."""
        self.assertEqual(self.board.__board_bar__[1], 0)
        self.assertTrue(self.board.__is_bar_empty__[1])
        self.board.remove_checker_from_bar(False)
        self.assertEqual(self.board.__board_bar__[1], 0)
        self.assertTrue(self.board.__is_bar_empty__[1])

    def test_select_checker_valid_white_top(self):
        """Verifica select_checker() para seleccionar una ficha blanca válida en la parte superior."""
        # El índice 1 para blancas corresponde al triángulo superior índice 11
        result = self.board.select_checker(1, True)
        self.assertTrue(result)
        self.assertEqual(self.board.selected_checker, 1)
        self.assertEqual(self.board.__top_board_triangles__[11][1], 1)

    def test_select_checker_valid_white_bot(self):
        """Verifica select_checker() para seleccionar una ficha blanca válida en la parte inferior."""
        # El índice 19 para blancas corresponde al triángulo inferior índice 6
        result = self.board.select_checker(19, True)
        self.assertTrue(result)
        self.assertEqual(self.board.selected_checker, 19)
        self.assertEqual(self.board.__bot_board_triangles__[6][1], 1)

    def test_select_checker_valid_black_top(self):
        """Verifica select_checker() para seleccionar una ficha negra válida en la parte superior."""
        # El índice 19 para negras corresponde al triángulo superior índice 6
        result = self.board.select_checker(19, False)
        self.assertTrue(result)
        self.assertEqual(self.board.selected_checker, 19)
        self.assertEqual(self.board.__top_board_triangles__[6][1], 1)

    def test_select_checker_valid_black_bot(self):
        """Verifica select_checker() para seleccionar una ficha negra válida en la parte inferior."""
        # El índice 1 para negras corresponde al triángulo inferior índice 11
        result = self.board.select_checker(1, False)
        self.assertTrue(result)
        self.assertEqual(self.board.selected_checker, 1)
        self.assertEqual(self.board.__bot_board_triangles__[11][1], 1)

    def test_select_checker_empty_triangle(self):
        """Verifica select_checker() al intentar seleccionar en un triángulo vacío."""
        # El triángulo 2 está vacío por defecto
        result = self.board.select_checker(2, True)
        self.assertFalse(result)
        # Verifica que no se haya establecido selección
        self.assertNotEqual(self.board.selected_checker, 2)

    def test_select_checker_opponent_checker(self):
        """Verifica select_checker() al intentar seleccionar una ficha del oponente."""
        # El triángulo 5 tiene fichas negras (○) por defecto
        result = self.board.select_checker(5, True)  # Blancas intentando seleccionar negras
        self.assertFalse(result)
        # Verifica que no se haya establecido selección
        self.assertNotEqual(self.board.selected_checker, 5)

    def test_verify_player_can_take_out_white_default_board(self):
        """Verifica que el jugador blanco no puede retirar fichas en el tablero por defecto."""
        self.board.verify_player_can_take_out(True)
        self.assertFalse(self.board.__can_take_out__[0], "El blanco no debería poder retirar en el estado inicial.")

    def test_verify_player_can_take_out_black_default_board(self):
        """Verifica que el jugador negro no puede retirar fichas en el tablero por defecto."""
        self.board.verify_player_can_take_out(False)
        self.assertFalse(self.board.__can_take_out__[1], "El negro no debería poder retirar en el estado inicial.")

    def test_verify_player_can_take_out_white_all_in_home(self):
        """Verifica que el jugador blanco puede retirar cuando todas sus fichas están en el hogar."""
        # Remover todas las fichas blancas de 1-18
        for i in range(1, 19):
            triangle = self.board.get_triangle_from_normal(i, True)
            if triangle[2] == "●":
                self.board.replace_triangle(i, True, [0, 0, " "])
                self.board.__num_checkers_board_player__[0] -= triangle[0]
        self.board.verify_player_can_take_out(True)
        self.assertTrue(self.board.__can_take_out__[0], "El blanco debería poder retirar cuando todas las fichas están en el hogar.")

    def test_verify_player_can_take_out_black_all_in_home(self):
        """Verifica que el jugador negro puede retirar cuando todas sus fichas están en el hogar."""
        # Remover todas las fichas negras de 1-18
        for i in range(1, 19):
            triangle = self.board.get_triangle_from_normal(i, False)
            if triangle[2] == "○":
                self.board.replace_triangle(i, False, [0, 0, " "])
                self.board.__num_checkers_board_player__[1] -= triangle[0]
        self.board.verify_player_can_take_out(False)
        self.assertTrue(self.board.__can_take_out__[1], "El negro debería poder retirar cuando todas las fichas están en el hogar.")

    def test_verify_player_can_take_out_white_with_checker_in_18(self):
        """Verifica que el blanco no puede retirar si tiene una ficha fuera del hogar."""
        self.board.replace_triangle(18, True, [1, 0, "●"])
        self.board.replace_triangle(1, True, [0, 0, " "])
        self.board.replace_triangle(12, True, [0, 0, " "])
        self.board.replace_triangle(17, True, [0, 0, " "])
        self.board.verify_player_can_take_out(True)
        self.assertFalse(self.board.__can_take_out__[0], "No debería poder retirar con ficha en 18.")

    def test_verify_player_can_take_out_black_with_checker_in_18(self):
        """Verifica que el negro no puede retirar si tiene una ficha fuera del hogar."""
        self.board.replace_triangle(18, False, [1, 0, "○"])
        self.board.replace_triangle(1, False, [0, 0, " "])
        self.board.replace_triangle(12, False, [0, 0, " "])
        self.board.replace_triangle(17, False, [0, 0, " "])
        self.board.verify_player_can_take_out(False)
        self.assertFalse(self.board.__can_take_out__[1], "No debería poder retirar con ficha en 18.")

    def test_verify_player_can_take_out_white_with_opponent_in_home(self):
        """Verifica que fichas del oponente en el hogar no impiden retirar."""
        # Remover propias de 1-18, dejar oponente
        for i in range(1, 19):
            triangle = self.board.get_triangle_from_normal(i, True)
            if triangle[2] == "●":
                self.board.replace_triangle(i, True, [0, 0, " "])
                self.board.__num_checkers_board_player__[0] -= triangle[0]
        self.board.verify_player_can_take_out(True)
        self.assertTrue(self.board.__can_take_out__[0], "Debería poder retirar aunque oponente tenga fichas en hogar.")

    def test_verify_player_can_take_out_black_with_opponent_in_home(self):
        """Verifica que fichas del oponente en el hogar no impiden retirar."""
        for i in range(1, 19):
            triangle = self.board.get_triangle_from_normal(i, False)
            if triangle[2] == "○":
                self.board.replace_triangle(i, False, [0, 0, " "])
                self.board.__num_checkers_board_player__[1] -= triangle[0]
        self.board.verify_player_can_take_out(False)
        self.assertTrue(self.board.__can_take_out__[1], "Debería poder retirar aunque oponente tenga fichas en hogar.")

    def test_verify_player_can_take_out_white_with_checker_in_bar(self):
        """Verifica que no puede retirar si tiene fichas en la barra para blancas."""
        for i in range(1, 19):
            triangle = self.board.get_triangle_from_normal(i, True)
            if triangle[2] == "●":
                self.board.replace_triangle(i, True, [0, 0, " "])
                self.board.__num_checkers_board_player__[0] -= triangle[0]
        self.board.add_checker_to_bar(False)
        self.board.verify_player_can_take_out(True)
        self.assertFalse(self.board.__can_take_out__[0], "No debería poder retirar con fichas en barra.")

    def test_verify_player_can_take_out_black_with_checker_in_bar(self):
        """Verifica que no puede retirar si tiene fichas en la barra para negras."""
        for i in range(1, 19):
            triangle = self.board.get_triangle_from_normal(i, False)
            if triangle[2] == "○":
                self.board.replace_triangle(i, False, [0, 0, " "])
                self.board.__num_checkers_board_player__[1] -= triangle[0]
        self.board.add_checker_to_bar(True)
        self.board.verify_player_can_take_out(False)
        self.assertFalse(self.board.__can_take_out__[1], "No debería poder retirar con fichas en barra.")

    def test_verify_player_can_take_out_white_mixed_positions(self):
        """Verifica que no puede retirar si tiene fichas en posiciones mixtas."""
        # Dejar algunas en 1-18
        self.board.verify_player_can_take_out(True)
        self.assertFalse(self.board.__can_take_out__[0], "No debería poder retirar con fichas fuera del hogar.")

    def test_verify_player_can_take_out_black_mixed_positions(self):
        """Verifica que no puede retirar si tiene fichas en posiciones mixtas."""
        self.board.verify_player_can_take_out(False)
        self.assertFalse(self.board.__can_take_out__[1], "No debería poder retirar con fichas fuera del hogar.")

    def test_get_triangle_from_normal_white_checkers_top(self):
        """Verifica get_triangle_from_normal() para fichas blancas en triángulos superiores."""
        # Triángulos 1-12 para blancas están en top
        self.assertEqual(self.board.get_triangle_from_normal(1, True), [2, 0, "●"])
        self.assertEqual(self.board.get_triangle_from_normal(6, True), [5, 0, "○"])
        self.assertEqual(self.board.get_triangle_from_normal(12, True), [5, 0, "●"])

    def test_get_triangle_from_normal_white_checkers_bot(self):
        """Verifica get_triangle_from_normal() para fichas blancas en triángulos inferiores."""
        # Triángulos 13-24 para blancas están en bot
        self.assertEqual(self.board.get_triangle_from_normal(13, True), [5, 0, "○"])
        self.assertEqual(self.board.get_triangle_from_normal(18, True), [0, 0, " "])
        self.assertEqual(self.board.get_triangle_from_normal(24, True), [2, 0, "○"])

    def test_get_triangle_from_normal_black_checkers_top(self):
        """Verifica get_triangle_from_normal() para fichas negras en triángulos superiores."""
        # Triángulos 13-24 para negras están en top
        self.assertEqual(self.board.get_triangle_from_normal(13, False), [5, 0, "●"])
        self.assertEqual(self.board.get_triangle_from_normal(18, False), [0, 0, " "])
        self.assertEqual(self.board.get_triangle_from_normal(24, False), [2, 0, "●"])

    def test_get_triangle_from_normal_black_checkers_bot(self):
        """Verifica get_triangle_from_normal() para fichas negras en triángulos inferiores."""
        # Triángulos 1-12 para negras están en bot
        self.assertEqual(self.board.get_triangle_from_normal(1, False), [2, 0, "○"])
        self.assertEqual(self.board.get_triangle_from_normal(6, False), [5, 0, "●"])
        self.assertEqual(self.board.get_triangle_from_normal(12, False), [5, 0, "○"])

    def test_get_triangle_from_normal_modified_triangle(self):
        """Verifica get_triangle_from_normal() después de modificar un triángulo."""
        # Modifica un triángulo y verifica que se obtenga correctamente
        new_triangle = [3, 1, "●"]
        self.board.replace_triangle(1, True, new_triangle)
        self.assertEqual(self.board.get_triangle_from_normal(1, True), new_triangle)

    def test_deselect_checker_no_selection(self):
        """Verifica deselect_checker() cuando no hay ficha seleccionada."""
        # Sin selección previa
        self.assertIsNone(self.board.selected_checker)
        # El método debería devolver False si no hay selección
        result = self.board.deselect_checker(True)
        self.assertFalse(result)

    def test_deselect_checker_with_selection_white(self):
        """Verifica deselect_checker() para fichas blancas con selección previa."""
        # Selecciona una ficha blanca
        self.board.select_checker(1, True)
        self.assertEqual(self.board.selected_checker, 1)
        # Verifica que esté marcada como seleccionada
        triangle = self.board.get_triangle_from_normal(1, True)
        self.assertEqual(triangle[1], 1)
        # Deselecciona
        result = self.board.deselect_checker(True)
        self.assertTrue(result)
        # Verifica que ya no esté seleccionada
        triangle = self.board.get_triangle_from_normal(1, True)
        self.assertEqual(triangle[1], 0)
        self.assertIsNone(self.board.selected_checker)

    def test_deselect_checker_with_selection_black(self):
        """Verifica deselect_checker() para fichas negras con selección previa."""
        # Selecciona una ficha negra
        self.board.select_checker(1, False)
        self.assertEqual(self.board.selected_checker, 1)
        # Verifica que esté marcada como seleccionada
        triangle = self.board.get_triangle_from_normal(1, False)
        self.assertEqual(triangle[1], 1)
        # Deselecciona
        result = self.board.deselect_checker(False)
        self.assertTrue(result)
        # Verifica que ya no esté seleccionada
        triangle = self.board.get_triangle_from_normal(1, False)
        self.assertEqual(triangle[1], 0)
        self.assertIsNone(self.board.selected_checker)

    def test_deselect_checker_wrong_player(self):
        """Verifica deselect_checker() cuando el jugador no coincide con la selección."""
        # Selecciona con blancas
        self.board.select_checker(1, True)
        # Intenta deseleccionar con negras
        result = self.board.deselect_checker(False)
        self.assertFalse(result)
        # Verifica que siga seleccionada
        self.assertEqual(self.board.selected_checker, 1)
        triangle = self.board.get_triangle_from_normal(1, True)
        self.assertEqual(triangle[1], 1)

    def test_clean_selection_single_triangle_white(self):
        """Verifica clean_selection() para deseleccionar un solo triángulo con fichas blancas."""
        # Selecciona un triángulo blanco
        self.board.select_checker(1, True)
        triangle = self.board.get_triangle_from_normal(1, True)
        self.assertEqual(triangle[1], 1)

        # Deselecciona el triángulo
        self.board.clean_selection((1,), True)
        triangle = self.board.get_triangle_from_normal(1, True)
        self.assertEqual(triangle[1], 0)

    def test_clean_selection_single_triangle_black(self):
        """Verifica clean_selection() para deseleccionar un solo triángulo con fichas negras."""
        # Selecciona un triángulo negro
        self.board.select_checker(1, False)
        triangle = self.board.get_triangle_from_normal(1, False)
        self.assertEqual(triangle[1], 1)

        # Deselecciona el triángulo
        self.board.clean_selection((1,), False)
        triangle = self.board.get_triangle_from_normal(1, False)
        self.assertEqual(triangle[1], 0)

    def test_clean_selection_multiple_triangles_white(self):
        """Verifica clean_selection() para deseleccionar múltiples triángulos con fichas blancas."""
        # Selecciona varios triángulos blancos
        self.board.select_checker(1, True)
        self.board.select_checker(19, True)
        self.assertEqual(self.board.get_triangle_from_normal(1, True)[1], 1)
        self.assertEqual(self.board.get_triangle_from_normal(19, True)[1], 1)

        # Deselecciona los triángulos
        self.board.clean_selection((1, 19), True)
        self.assertEqual(self.board.get_triangle_from_normal(1, True)[1], 0)
        self.assertEqual(self.board.get_triangle_from_normal(19, True)[1], 0)

    def test_clean_selection_multiple_triangles_black(self):
        """Verifica clean_selection() para deseleccionar múltiples triángulos con fichas negras."""
        # Selecciona varios triángulos negros
        self.board.select_checker(1, False)
        self.board.select_checker(19, False)
        self.assertEqual(self.board.get_triangle_from_normal(1, False)[1], 1)
        self.assertEqual(self.board.get_triangle_from_normal(19, False)[1], 1)

        # Deselecciona los triángulos
        self.board.clean_selection((1, 19), False)
        self.assertEqual(self.board.get_triangle_from_normal(1, False)[1], 0)
        self.assertEqual(self.board.get_triangle_from_normal(19, False)[1], 0)

    def test_clean_selection_empty_tuple_white(self):
        """Verifica clean_selection() con una tupla vacía para fichas blancas."""
        # No hay cambios esperados
        original_top = [triangle[:] for triangle in self.board.__top_board_triangles__]
        self.board.clean_selection((), True)
        self.assertEqual(self.board.__top_board_triangles__, original_top)

    def test_clean_selection_empty_tuple_black(self):
        """Verifica clean_selection() con una tupla vacía para fichas negras."""
        # No hay cambios esperados
        original_bot = [triangle[:] for triangle in self.board.__bot_board_triangles__]
        self.board.clean_selection((), False)
        self.assertEqual(self.board.__bot_board_triangles__, original_bot)

    def test_clean_selection_already_deselected_white(self):
        """Verifica clean_selection() en triángulos ya deseleccionados con fichas blancas."""
        # Los triángulos por defecto no están seleccionados
        triangle = self.board.get_triangle_from_normal(2, True)
        self.assertEqual(triangle[1], 0)

        # Deseleccionar no debería cambiar nada
        self.board.clean_selection((2,), True)
        triangle = self.board.get_triangle_from_normal(2, True)
        self.assertEqual(triangle[1], 0)

    def test_clean_selection_already_deselected_black(self):
        """Verifica clean_selection() en triángulos ya deseleccionados con fichas negras."""
        # Los triángulos por defecto no están seleccionados
        triangle = self.board.get_triangle_from_normal(2, False)
        self.assertEqual(triangle[1], 0)

        # Deseleccionar no debería cambiar nada
        self.board.clean_selection((2,), False)
        triangle = self.board.get_triangle_from_normal(2, False)
        self.assertEqual(triangle[1], 0)

    def test_clean_selection_mixed_selected_deselected_white(self):
        """Verifica clean_selection() con mezcla de triángulos seleccionados y deseleccionados para blancas."""
        # Selecciona uno, deja otro deseleccionado
        self.board.select_checker(1, True)
        self.assertEqual(self.board.get_triangle_from_normal(1, True)[1], 1)
        self.assertEqual(self.board.get_triangle_from_normal(2, True)[1], 0)

        # Deselecciona ambos
        self.board.clean_selection((1, 2), True)
        self.assertEqual(self.board.get_triangle_from_normal(1, True)[1], 0)
        self.assertEqual(self.board.get_triangle_from_normal(2, True)[1], 0)

    def test_clean_selection_mixed_selected_deselected_black(self):
        """Verifica clean_selection() con mezcla de triángulos seleccionados y deseleccionados para negras."""
        # Selecciona uno, deja otro deseleccionado
        self.board.select_checker(1, False)
        self.assertEqual(self.board.get_triangle_from_normal(1, False)[1], 1)
        self.assertEqual(self.board.get_triangle_from_normal(2, False)[1], 0)

        # Deselecciona ambos
        self.board.clean_selection((1, 2), False)
        self.assertEqual(self.board.get_triangle_from_normal(1, False)[1], 0)
        self.assertEqual(self.board.get_triangle_from_normal(2, False)[1], 0)

    def test_clean_selection_does_not_affect_other_triangles_white(self):
        """Verifica que clean_selection() no afecte otros triángulos para fichas blancas."""
        # Selecciona dos triángulos
        self.board.select_checker(1, True)
        self.board.select_checker(19, True)
        self.assertEqual(self.board.get_triangle_from_normal(1, True)[1], 1)
        self.assertEqual(self.board.get_triangle_from_normal(19, True)[1], 1)
        self.assertEqual(self.board.get_triangle_from_normal(2, True)[1], 0)

        # Deselecciona solo uno
        self.board.clean_selection((1,), True)
        self.assertEqual(self.board.get_triangle_from_normal(1, True)[1], 0)
        self.assertEqual(self.board.get_triangle_from_normal(19, True)[1], 1)  # Aún seleccionado
        self.assertEqual(self.board.get_triangle_from_normal(2, True)[1], 0)

    def test_clean_selection_does_not_affect_other_triangles_black(self):
        """Verifica que clean_selection() no afecte otros triángulos para fichas negras."""
        # Selecciona dos triángulos
        self.board.select_checker(1, False)
        self.board.select_checker(19, False)
        self.assertEqual(self.board.get_triangle_from_normal(1, False)[1], 1)
        self.assertEqual(self.board.get_triangle_from_normal(19, False)[1], 1)
        self.assertEqual(self.board.get_triangle_from_normal(2, False)[1], 0)

        # Deselecciona solo uno
        self.board.clean_selection((1,), False)
        self.assertEqual(self.board.get_triangle_from_normal(1, False)[1], 0)
        self.assertEqual(self.board.get_triangle_from_normal(19, False)[1], 1)  # Aún seleccionado
        self.assertEqual(self.board.get_triangle_from_normal(2, False)[1], 0)

    def test_take_out_checker_white(self):
        """Verifica take_out_checker() para retirar una ficha blanca."""
        initial_off = self.board.__checkers_off__[0]
        self.board.take_out_checker(True)
        self.assertEqual(self.board.__checkers_off__[0], initial_off + 1,
                         "La cantidad de fichas blancas retiradas debe incrementarse en 1.")

    def test_take_out_checker_black(self):
        """Verifica take_out_checker() para retirar una ficha negra."""
        initial_off = self.board.__checkers_off__[1]
        self.board.take_out_checker(False)
        self.assertEqual(self.board.__checkers_off__[1], initial_off + 1,
                         "La cantidad de fichas negras retiradas debe incrementarse en 1.")

    def test_take_out_checker_multiple_white(self):
        """Verifica take_out_checker() al retirar múltiples fichas blancas."""
        initial_off = self.board.__checkers_off__[0]
        self.board.take_out_checker(True)
        self.board.take_out_checker(True)
        self.board.take_out_checker(True)
        self.assertEqual(self.board.__checkers_off__[0], initial_off + 3,
                         "La cantidad de fichas blancas retiradas debe incrementarse correctamente.")

    def test_take_out_checker_multiple_black(self):
        """Verifica take_out_checker() al retirar múltiples fichas negras."""
        initial_off = self.board.__checkers_off__[1]
        self.board.take_out_checker(False)
        self.board.take_out_checker(False)
        self.board.take_out_checker(False)
        self.assertEqual(self.board.__checkers_off__[1], initial_off + 3,
                         "La cantidad de fichas negras retiradas debe incrementarse correctamente.")

    def test_is_match_won_no_winner(self):
        """Verifica is_match_won() cuando ningún jugador ha ganado."""
        # Estado inicial: ningún jugador tiene fichas retiradas suficientes
        won, white_won = self.board.is_match_won()
        self.assertFalse(won, "No debería haber ganador en el estado inicial.")
        self.assertFalse(white_won, "El segundo valor debería ser False cuando no hay ganador.")

    def test_is_match_won_white_wins(self):
        """Verifica is_match_won() cuando el jugador blanco gana."""
        # Simula que el blanco tiene todas las fichas retiradas
        self.board.__checkers_off__[0] = 15
        won, white_won = self.board.is_match_won()
        self.assertTrue(won, "Debería indicar que hay un ganador.")
        self.assertTrue(white_won, "Debería indicar que el blanco ganó.")

    def test_is_match_won_black_wins(self):
        """Verifica is_match_won() cuando el jugador negro gana."""
        # Simula que el negro tiene todas las fichas retiradas
        self.board.__checkers_off__[1] = 15
        won, white_won = self.board.is_match_won()
        self.assertTrue(won, "Debería indicar que hay un ganador.")
        self.assertFalse(white_won, "Debería indicar que el negro ganó.")

    def test_is_match_won_white_over_limit(self):
        """Verifica is_match_won() cuando el blanco tiene más de 15 fichas retiradas."""
        # Simula que el blanco tiene más de 15 fichas retiradas (caso límite)
        self.board.__checkers_off__[0] = 16
        won, white_won = self.board.is_match_won()
        self.assertTrue(won, "Debería indicar que hay un ganador incluso si excede.")
        self.assertTrue(white_won, "Debería indicar que el blanco ganó.")

    def test_is_match_won_black_over_limit(self):
        """Verifica is_match_won() cuando el negro tiene más de 15 fichas retiradas."""
        # Simula que el negro tiene más de 15 fichas retiradas (caso límite)
        self.board.__checkers_off__[1] = 16
        won, white_won = self.board.is_match_won()
        self.assertTrue(won, "Debería indicar que hay un ganador incluso si excede.")
        self.assertFalse(white_won, "Debería indicar que el negro ganó.")

    def test_is_match_won_both_near_win(self):
        """Verifica is_match_won() cuando ambos jugadores están cerca de ganar pero ninguno lo ha hecho."""
        # Ambos tienen 14 fichas retiradas
        self.board.__checkers_off__[0] = 14
        self.board.__checkers_off__[1] = 14
        won, white_won = self.board.is_match_won()
        self.assertFalse(won, "No debería haber ganador si ninguno alcanza 15.")
        self.assertFalse(white_won, "El segundo valor debería ser False.")

    def test_is_match_won_white_at_limit_black_over(self):
        """Verifica is_match_won() cuando blanco gana exactamente en el límite y negro tiene más."""
        # Blanco en 15, negro en 16
        self.board.__checkers_off__[0] = 15
        self.board.__checkers_off__[1] = 16
        won, white_won = self.board.is_match_won()
        self.assertTrue(won, "Debería haber un ganador.")
        self.assertTrue(white_won, "Debería ganar el blanco primero en orden de verificación.")

    def test_is_match_won_white_at_limit_black_over(self):
        """Verifica is_match_won() cuando blanco gana exactamente en el límite y negro tiene más."""
        # Blanco en 15, negro en 16
        self.board.__checkers_off__[0] = 15
        self.board.__checkers_off__[1] = 16
        won, white_won = self.board.is_match_won()
        self.assertTrue(won, "Debería haber un ganador.")
        self.assertTrue(white_won, "Debería ganar el blanco primero en orden de verificación.")

    def test_get_total_num_checkers_player_white_default(self):
        """Verifica get_total_num_checkers_player para blancas en estado inicial."""
        total = self.board.get_total_num_checkers_player(True)
        self.assertEqual(total, 15, "El total de fichas blancas debería ser 15 en el estado inicial.")

    def test_get_total_num_checkers_player_black_default(self):
        """Verifica get_total_num_checkers_player para negras en estado inicial."""
        total = self.board.get_total_num_checkers_player(False)
        self.assertEqual(total, 15, "El total de fichas negras debería ser 15 en el estado inicial.")

    def test_get_total_num_checkers_player_white_after_add_to_bar(self):
        """Verifica que el total permanece igual después de agregar a la barra para blancas."""
        initial_total = self.board.get_total_num_checkers_player(True)
        self.board.add_checker_to_bar(False)
        new_total = self.board.get_total_num_checkers_player(True)
        self.assertEqual(new_total, initial_total, "El total debería permanecer igual al agregar a la barra.")

    def test_get_total_num_checkers_player_black_after_add_to_bar(self):
        """Verifica que el total permanece igual después de agregar a la barra para negras."""
        initial_total = self.board.get_total_num_checkers_player(False)
        self.board.add_checker_to_bar(False)
        new_total = self.board.get_total_num_checkers_player(False)
        self.assertEqual(new_total, initial_total, "El total debería permanecer igual al agregar a la barra.")

    def test_get_total_num_checkers_player_white_after_take_out(self):
        """Verifica que el total permanece igual después de retirar una ficha para blancas."""
        initial_total = self.board.get_total_num_checkers_player(True)
        self.board.take_out_checker(True)
        new_total = self.board.get_total_num_checkers_player(True)
        self.assertEqual(new_total, initial_total, "El total debería permanecer igual al retirar una ficha.")

    def test_get_total_num_checkers_player_black_after_take_out(self):
        """Verifica que el total permanece igual después de retirar una ficha para negras."""
        initial_total = self.board.get_total_num_checkers_player(False)
        self.board.take_out_checker(False)
        new_total = self.board.get_total_num_checkers_player(False)
        self.assertEqual(new_total, initial_total, "El total debería permanecer igual al retirar una ficha.")

    def test_get_total_num_checkers_player_white_multiple_operations(self):
        """Verifica el total después de múltiples operaciones para blancas."""
        initial_total = self.board.get_total_num_checkers_player(True)
        self.board.add_checker_to_bar(True)
        self.board.add_checker_to_bar(True)
        self.board.take_out_checker(True)
        new_total = self.board.get_total_num_checkers_player(True)
        self.assertEqual(new_total, initial_total, "El total debería permanecer constante tras múltiples operaciones.")

    def test_get_total_num_checkers_player_black_multiple_operations(self):
        """Verifica el total después de múltiples operaciones para negras."""
        initial_total = self.board.get_total_num_checkers_player(False)
        self.board.add_checker_to_bar(False)
        self.board.take_out_checker(False)
        self.board.take_out_checker(False)
        new_total = self.board.get_total_num_checkers_player(False)
        self.assertEqual(new_total, initial_total, "El total debería permanecer constante tras múltiples operaciones.")

    def test_get_total_num_checkers_player_white_edge_case_all_off(self):
        """Verifica el total cuando todas las fichas blancas están retiradas."""
        # Simular todas retiradas
        self.board.__checkers_off__[0] = 15
        self.board.__num_checkers_board_player__[0] = 0
        self.board.__board_bar__[0] = 0
        total = self.board.get_total_num_checkers_player(True)
        self.assertEqual(total, 15, "El total debería ser 15 incluso si todas están retiradas.")

    def test_get_total_num_checkers_player_black_edge_case_all_off(self):
        """Verifica el total cuando todas las fichas negras están retiradas."""
        self.board.__checkers_off__[1] = 15
        self.board.__num_checkers_board_player__[1] = 0
        self.board.__board_bar__[1] = 0
        total = self.board.get_total_num_checkers_player(False)
        self.assertEqual(total, 15, "El total debería ser 15 incluso si todas están retiradas.")

    def test_get_total_num_checkers_player_white_edge_case_all_in_bar(self):
        """Verifica el total cuando todas las fichas blancas están en la barra."""
        self.board.__board_bar__[0] = 15
        self.board.__num_checkers_board_player__[0] = 0
        self.board.__checkers_off__[0] = 0
        total = self.board.get_total_num_checkers_player(True)
        self.assertEqual(total, 15, "El total debería ser 15 si todas están en la barra.")

    def test_get_total_num_checkers_player_black_edge_case_all_in_bar(self):
        """Verifica el total cuando todas las fichas negras están en la barra."""
        self.board.__board_bar__[1] = 15
        self.board.__num_checkers_board_player__[1] = 0
        self.board.__checkers_off__[1] = 0
        total = self.board.get_total_num_checkers_player(False)
        self.assertEqual(total, 15, "El total debería ser 15 si todas están en la barra.")

if __name__ == '__main__':
    unittest.main()
