import unittest
from cli.CLI import CLI
from core.Board import Board


class TestCLI(unittest.TestCase):
    """Conjunto de proebas para la clase CLI."""

    def setUp(self):
        """Configura el entorno de prueba antes de cada test."""
        self.board = Board()
        self.cli = CLI(self.board)

    def test_translate_user_input_select_allowed_inpt(self):
        """Prueba la función translate_user_input_select con entradas válidas."""
        inpt_to_test = tuple("123456789abcdefghijklmnop")
        for i, char in enumerate(inpt_to_test):
            self.assertEqual(self.cli.translate_user_input_select(char), i + 1)

    def test_translate_user_input_select_not_allowed_inpt(self):
        """Prueba la función translate_user_input_select con entradas no válidas."""
        inpt_to_test = ("0", "!", "z", "", " ", "\n", "12", "aB", "a1")
        for char in inpt_to_test:
            self.assertEqual(self.cli.translate_user_input_select(char), -1)

    def test_generate_middle_board_both_zero(self):
        """Prueba que generate_middle_board devuelva la cadena correcta cuando ambas barras están vacías."""
        # La barra ya está en [0, 0] por defecto
        expected = ("│                    │                    │\n"
                    "│                    │                    │\n"
                    "│                    │                    │\n")
        self.assertEqual(self.cli.generate_middle_board().strip(), expected.strip())

    def test_generate_middle_board_white_only(self):
        """Prueba que generate_middle_board devuelva la cadena correcta cuando solo hay fichas blancas en la barra."""
        for _ in range(5):
            self.board.add_checker_to_bar(False)  # Agrega fichas blancas
        expected = ("│                    │                    │\n"
                    "│              0 ↠ ○ │ ● ↞ 5              │\n"
                    "│                    │                    │\n")
        self.assertEqual(self.cli.generate_middle_board().strip(), expected.strip())

    def test_generate_middle_board_black_only(self):
        """Prueba que generate_middle_board devuelva la cadena correcta cuando solo hay fichas negras en la barra."""
        for _ in range(7):
            self.board.add_checker_to_bar(True)  # Agrega fichas negras
        expected = ("│                    │                    │\n"
                    "│              7 ↠ ○ │ ● ↞ 0              │\n"
                    "│                    │                    │\n")
        self.assertEqual(self.cli.generate_middle_board().strip(), expected.strip())

    def test_generate_middle_board_both_non_zero(self):
        """Prueba que generate_middle_board devuelva la cadena correcta cuando ambas barras tienen fichas."""
        for _ in range(3):
            self.board.add_checker_to_bar(False)  # Blancas
        for _ in range(2):
            self.board.add_checker_to_bar(True)  # Negras
        expected = ("│                    │                    │\n"
                    "│              2 ↠ ○ │ ● ↞ 3              │\n"
                    "│                    │                    │\n")
        self.assertEqual(self.cli.generate_middle_board().strip(), expected.strip())

    def test_generate_middle_board_large_numbers(self):
        """Prueba que generate_middle_board maneje correctamente números grandes con alineación."""
        for _ in range(100):
            self.board.add_checker_to_bar(False)  # Blancas
        for _ in range(50):
            self.board.add_checker_to_bar(True)  # Negras
        expected = ("│                    │                    │\n"
                    "│             50 ↠ ○ │ ● ↞ 100            │\n"
                    "│                    │                    │\n")
        self.assertEqual(self.cli.generate_middle_board().strip(), expected.strip())

    def test_character_to_put_top_sum_less_than_line_number(self):
        """Prueba que character_to_put_top devuelva espacio cuando la suma es menor al número de línea."""
        triangle = [0, 0, " "]
        self.assertEqual(self.cli.character_to_put_top(1, triangle), " ")

    def test_character_to_put_top_normal_checker(self):
        """Prueba que character_to_put_top devuelva el carácter de ficha normal cuando corresponde."""
        triangle = [5, 0, "●"]
        self.assertEqual(self.cli.character_to_put_top(1, triangle), "●")
        self.assertEqual(self.cli.character_to_put_top(3, triangle), "●")

    def test_character_to_put_top_selected_checker(self):
        """Prueba que character_to_put_top devuelva el símbolo de ficha seleccionada cuando corresponde."""
        triangle = [1, 1, "●"]
        self.assertEqual(self.cli.character_to_put_top(2, triangle), "▲")

    def test_character_to_put_top_possible_move_diff_one(self):
        """Prueba que character_to_put_top devuelva el símbolo de posible movimiento para diferencia 1."""
        triangle = [0, 2, " "]
        self.assertEqual(self.cli.character_to_put_top(1, triangle), "⊕")

    def test_character_to_put_top_possible_move_diff_two(self):
        """Prueba que character_to_put_top devuelva el símbolo de posible movimiento para diferencia 2."""
        triangle = [0, 2, " "]
        self.assertEqual(self.cli.character_to_put_top(2, triangle), "△")

    def test_character_to_put_top_no_symbol_conditions_met(self):
        """Prueba que character_to_put_top devuelva espacio cuando no se cumplen condiciones de símbolo."""
        triangle = [1, 1, "●"]
        self.assertEqual(self.cli.character_to_put_top(3, triangle), " ")
        triangle = [0, 2, " "]
        self.assertEqual(self.cli.character_to_put_top(3, triangle), " ")

    def test_character_to_put_top_edge_cases(self):
        """Prueba casos límite para character_to_put_top."""
        # Línea 1 con triángulo vacío
        triangle = [0, 0, " "]
        self.assertEqual(self.cli.character_to_put_top(1, triangle), " ")
        # Línea 1 con ficha normal
        triangle = [1, 0, "○"]
        self.assertEqual(self.cli.character_to_put_top(1, triangle), "○")
        # Selección en línea 1
        triangle = [0, 1, " "]
        self.assertEqual(self.cli.character_to_put_top(1, triangle), "▲")

    def test_character_to_put_bottom_sum_less_than_line_number(self):
        """Prueba que character_to_put_bottom devuelva espacio cuando la suma es menor al número de línea."""
        triangle = [0, 0, " "]
        self.assertEqual(self.cli.character_to_put_bottom(1, triangle), " ")

    def test_character_to_put_bottom_no_selection_type(self):
        """Prueba que character_to_put_bottom devuelva el carácter cuando no hay tipo de selección."""
        triangle = [5, 0, "●"]
        self.assertEqual(self.cli.character_to_put_bottom(1, triangle), "●")
        self.assertEqual(self.cli.character_to_put_bottom(3, triangle), "●")

    def test_character_to_put_bottom_normal_checker_with_selection(self):
        """Prueba que character_to_put_bottom devuelva el carácter de ficha normal incluso con selección."""
        triangle = [5, 1, "●"]
        self.assertEqual(self.cli.character_to_put_bottom(1, triangle), "●")

    def test_character_to_put_bottom_selected_checker(self):
        """Prueba que character_to_put_bottom devuelva el símbolo de ficha seleccionada cuando corresponde."""
        triangle = [1, 1, "●"]
        self.assertEqual(self.cli.character_to_put_bottom(2, triangle), "▼")

    def test_character_to_put_bottom_possible_move_diff_one(self):
        """Prueba que character_to_put_bottom devuelva el símbolo de posible movimiento para diferencia 1."""
        triangle = [0, 2, " "]
        self.assertEqual(self.cli.character_to_put_bottom(1, triangle), "⊕")

    def test_character_to_put_bottom_possible_move_diff_two(self):
        """Prueba que character_to_put_bottom devuelva el símbolo de posible movimiento para diferencia 2."""
        triangle = [0, 2, " "]
        self.assertEqual(self.cli.character_to_put_bottom(2, triangle), "▽")

    def test_character_to_put_bottom_no_symbol_conditions_met(self):
        """Prueba que character_to_put_bottom devuelva espacio cuando no se cumplen condiciones de símbolo."""
        triangle = [1, 1, "●"]
        self.assertEqual(self.cli.character_to_put_bottom(3, triangle), " ")
        triangle = [0, 2, " "]
        self.assertEqual(self.cli.character_to_put_bottom(3, triangle), " ")

    def test_character_to_put_bottom_edge_cases(self):
        """Prueba casos límite para character_to_put_bottom."""
        # Línea 1 con triángulo vacío
        triangle = [0, 0, " "]
        self.assertEqual(self.cli.character_to_put_bottom(1, triangle), " ")
        # Línea 1 con ficha normal
        triangle = [1, 0, "○"]
        self.assertEqual(self.cli.character_to_put_bottom(1, triangle), "○")
        # Selección en línea 1
        triangle = [0, 1, " "]
        self.assertEqual(self.cli.character_to_put_bottom(1, triangle), "▼")

    def test_generate_top_board_str_empty_white(self):
        """Prueba que generate_top_board_str devuelva la cadena correcta para un tablero vacío con fichas blancas."""
        triangles = [[0, 0, " "]] * 12
        result = self.cli.generate_top_board_str(triangles, True)
        expected = (
            "                                   ┌──────┐\n"
            "                                   │ 00 ○ │\n"
            "  ─────────────────────────────────└──────┘\n"
            "   C  B  A  9  8  7     6  5  4  3  2  1\n"
            "┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐\n"
            "│  ▼  ▼  ▼  ▼  ▼  ▼  │  ▼  ▼  ▼  ▼  ▼  ▼  │\n"
        )
        self.assertEqual(result.strip(), expected.strip())

    def test_generate_top_board_str_empty_black(self):
        """Prueba que generate_top_board_str devuelva la cadena correcta para un tablero vacío con fichas negras."""
        triangles = [[0, 0, " "]] * 12
        result = self.cli.generate_top_board_str(triangles, False)
        expected = (
            "                                   ┌──────┐\n"
            "                                   │ 00 ● │\n"
            "  ─────────────────────────────────└──────┘\n"
            "   1  2  3  4  5  6     7  8  9  A  B  C\n"
            "┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐\n"
            "│  ▼  ▼  ▼  ▼  ▼  ▼  │  ▼  ▼  ▼  ▼  ▼  ▼  │\n"
        )
        self.assertEqual(result.strip(), expected.strip())

    def test_generate_bottom_board_str_empty_white(self):
        """Prueba que generate_bottom_board_str devuelva la cadena correcta para un tablero vacío con fichas blancas."""
        triangles = [[0, 0, " "]] * 12
        result = self.cli.generate_bottom_board_str(triangles, True)
        expected = (
            "│  ▲  ▲  ▲  ▲  ▲  ▲  │  ▲  ▲  ▲  ▲  ▲  ▲  │\n"
            "└──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘\n"
            "   D  E  F  G  H  I     J  K  L  M  N  O   \n"
            "  ─────────────────────────────────┌──────┐\n"
            "                               <P> │ 00 ● │\n"
            "                                   └──────┘\n"
        )
        self.assertEqual(result.strip(), expected.strip())

    def test_generate_bottom_board_str_empty_black(self):
        """Prueba que generate_bottom_board_str devuelva la cadena correcta para un tablero vacío con fichas negras."""
        triangles = [[0, 0, " "]] * 12
        result = self.cli.generate_bottom_board_str(triangles, False)
        expected = (
            "│  ▲  ▲  ▲  ▲  ▲  ▲  │  ▲  ▲  ▲  ▲  ▲  ▲  │\n"
            "└──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘\n"
            "   O  N  M  L  K  J     I  H  G  F  E  D   \n"
            "  ─────────────────────────────────┌──────┐\n"
            "                               <P> │ 00 ○ │\n"
            "                                   └──────┘\n"
        )
        self.assertEqual(result.strip(), expected.strip())

    def test_generate_top_board_str_single_checker_white(self):
        """Prueba que generate_top_board_str maneje correctamente un triángulo con una sola ficha blanca."""
        triangles = [[1, 0, "●"]] + [[0, 0, " "]] * 11
        result = self.cli.generate_top_board_str(triangles, True)
        expected = (
            "                                   ┌──────┐\n"
            "                                   │ 00 ○ │\n"
            "  ─────────────────────────────────└──────┘\n"
            "   C  B  A  9  8  7     6  5  4  3  2  1\n"
            "┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐\n"
            "│  ▼  ▼  ▼  ▼  ▼  ▼  │  ▼  ▼  ▼  ▼  ▼  ▼  │\n"
            "│  ●                 │                    │\n"
        )
        self.assertEqual(result.strip(), expected.strip())

    def test_generate_bottom_board_str_single_checker_white(self):
        """Prueba que generate_bottom_board_str maneje correctamente un triángulo con una sola ficha blanca."""
        triangles = [[1, 0, "●"]] + [[0, 0, " "]] * 11
        result = self.cli.generate_bottom_board_str(triangles, True)
        expected = (
            "│  ●                 │                    │\n"
            "│  ▲  ▲  ▲  ▲  ▲  ▲  │  ▲  ▲  ▲  ▲  ▲  ▲  │\n"
            "└──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘\n"
            "   D  E  F  G  H  I     J  K  L  M  N  O   \n"
            "  ─────────────────────────────────┌──────┐\n"
            "                               <P> │ 00 ● │\n"
            "                                   └──────┘\n"
        )
        self.assertEqual(result.strip(), expected.strip())

    def test_generate_top_board_str_with_selected_checker_white(self):
        """Prueba que generate_top_board_str maneje correctamente un triángulo con ficha seleccionada para jugador blanco."""
        triangles = [[1, 1, "●"]] + [[0, 0, " "]] * 11
        result = self.cli.generate_top_board_str(triangles, True)
        expected = (
            "                                   ┌──────┐\n"
            "                                   │ 00 ○ │\n"
            "  ─────────────────────────────────└──────┘\n"
            "   C  B  A  9  8  7     6  5  4  3  2  1\n"
            "┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐\n"
            "│  ▼  ▼  ▼  ▼  ▼  ▼  │  ▼  ▼  ▼  ▼  ▼  ▼  │\n"
            "│  ●                 │                    │\n"
            "│  ▲                 │                    │\n"
        )
        self.assertEqual(result.strip(), expected.strip())

    def test_generate_top_board_str_with_selected_checker_black(self):
        """Prueba que generate_top_board_str maneje correctamente un triángulo con ficha seleccionada para jugador negro."""
        triangles = [[1, 1, "○"]] + [[0, 0, " "]] * 11
        result = self.cli.generate_top_board_str(triangles, False)
        expected = (
            "                                   ┌──────┐\n"
            "                                   │ 00 ● │\n"
            "  ─────────────────────────────────└──────┘\n"
            "   1  2  3  4  5  6     7  8  9  A  B  C\n"
            "┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐\n"
            "│  ▼  ▼  ▼  ▼  ▼  ▼  │  ▼  ▼  ▼  ▼  ▼  ▼  │\n"
            "│  ○                 │                    │\n"
            "│  ▲                 │                    │\n"
        )
        self.assertEqual(result.strip(), expected.strip())

    def test_generate_top_board_str_with_possible_moves_white(self):
        """Prueba que generate_top_board_str maneje correctamente posibles movimientos."""
        triangles = [[0, 2, " "]] + [[0, 0, " "]] * 11
        result = self.cli.generate_top_board_str(triangles, True)
        expected = (
            "                                   ┌──────┐\n"
            "                                   │ 00 ○ │\n"
            "  ─────────────────────────────────└──────┘\n"
            "   C  B  A  9  8  7     6  5  4  3  2  1\n"
            "┌──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┬──┐\n"
            "│  ▼  ▼  ▼  ▼  ▼  ▼  │  ▼  ▼  ▼  ▼  ▼  ▼  │\n"
            "│  ⊕                 │                    │\n"
            "│  △                 │                    │\n"
        )
        self.assertEqual(result.strip(), expected.strip())

    def test_generate_bottom_board_str_with_possible_moves_white(self):
        """Prueba que generate_bottom_board_str maneje correctamente posibles movimientos."""
        triangles = [[0, 2, " "]] + [[0, 0, " "]] * 11
        result = self.cli.generate_bottom_board_str(triangles, True)
        expected = (
            "│  ▽                 │                    │\n"
            "│  ⊕                 │                    │\n"
            "│  ▲  ▲  ▲  ▲  ▲  ▲  │  ▲  ▲  ▲  ▲  ▲  ▲  │\n"
            "└──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘\n"
            "   D  E  F  G  H  I     J  K  L  M  N  O   \n"
            "  ─────────────────────────────────┌──────┐\n"
            "                               <P> │ 00 ● │\n"
            "                                   └──────┘\n"
        )
        self.assertEqual(result.strip(), expected.strip())

    def test_generate_top_board_str_large_count_white(self):
        """Prueba que generate_top_board_str maneje correctamente conteos grandes de fichas."""
        triangles = [[100, 0, "●"]] + [[0, 0, " "]] * 11
        result = self.cli.generate_top_board_str(triangles, True)
        lines = result.split('\n')
        self.assertEqual(len(lines), 107)
        # Verificar que la primera línea de triángulos contenga "●"
        self.assertIn("●", lines[6])

    def test_generate_bottom_board_str_large_count_white(self):
        """Prueba que generate_bottom_board_str maneje correctamente conteos grandes de fichas."""
        triangles = [[100, 0, "●"]] + [[0, 0, " "]] * 11
        result = self.cli.generate_bottom_board_str(triangles, True)
        lines = result.split('\n')
        self.assertEqual(len(lines), 107)
        # Verificar que la primera línea de triángulos contenga "●"
        self.assertIn("●", lines[0])

    def test_generate_top_board_str_default_white(self):
        """Prueba que generate_top_board_str funcione con el tablero por defecto para fichas blancas."""
        result = self.cli.generate_top_board_str(self.board.top_board_triangles, True)
        lines = result.split('\n')
        self.assertEqual(len(lines), 12)
        self.assertIn("●", result)
        self.assertIn("○", result)

    def test_generate_bottom_board_str_default_white(self):
        """Prueba que generate_bottom_board_str funcione con el tablero por defecto para fichas blancas."""
        result = self.cli.generate_bottom_board_str(self.board.bot_board_triangles, True)
        lines = result.split('\n')
        self.assertEqual(len(lines), 12)
        self.assertIn("●", result)
        self.assertIn("○", result)

    def test_generate_top_board_str_default_black(self):
        """Prueba que generate_top_board_str funcione con el tablero por defecto para fichas negras."""
        result = self.cli.generate_top_board_str(self.board.top_board_triangles, False)
        lines = result.split('\n')
        self.assertEqual(len(lines), 12)
        self.assertIn("1  2  3", result)

    def test_generate_bottom_board_str_default_black(self):
        """Prueba que generate_bottom_board_str funcione con el tablero por defecto para fichas negras."""
        result = self.cli.generate_bottom_board_str(self.board.bot_board_triangles, False)
        lines = result.split('\n')
        self.assertEqual(len(lines), 12)

    def test_generate_checkers_off_str_white_player_black_off_gt_zero(self):
        """Prueba que generate_checkers_off_str devuelva la cadena correcta para jugador blanco con fichas fuera > 0."""
        # Manually set checkers_off since it's a property without setter
        self.board.__checkers_off__ = [5, 0]  # White off: 5, Black off: 0
        result = self.cli.generate_checkers_off_str(True)
        self.assertEqual(result, "05 ●")

    def test_generate_checkers_off_str_white_player_black_off_gt_nine(self):
        """Prueba que generate_checkers_off_str devuelva la cadena correcta para jugador blanco con fichas fuera > 9."""
        # Manually set checkers_off since it's a property without setter
        self.board.__checkers_off__ = [15, 0]  # White off: 15, Black off: 0
        result = self.cli.generate_checkers_off_str(True)
        self.assertEqual(result, "15 ●")

    def test_generate_checkers_off_str_black_player_black_off_gt_zero(self):
        """Prueba que generate_checkers_off_str devuelva la cadena correcta para jugador negro con fichas fuera > 0."""
        # Manually set checkers_off since it's a property without setter
        self.board.__checkers_off__ = [0, 5]  # White off: 0, Black off: 5
        result = self.cli.generate_checkers_off_str(False)
        self.assertEqual(result, "05 ○")

    def test_generate_checkers_off_str_black_player_black_off_gt_nine(self):
        """Prueba que generate_checkers_off_str devuelva la cadena correcta para jugador negro con fichas fuera > 9."""
        # Manually set checkers_off since it's a property without setter
        self.board.__checkers_off__ = [0, 15]  # White off: 0, Black off: 15
        result = self.cli.generate_checkers_off_str(False)
        self.assertEqual(result, "15 ○")


if __name__ == '__main__':
    unittest.main()
