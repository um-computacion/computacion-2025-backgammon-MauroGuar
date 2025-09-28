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
        inpt_to_test = tuple("123456789abcdefghijklmno")
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
            self.board.add_checker_to_bar(True)   # Negras
        expected = ("│                    │                    │\n"
                    "│              2 ↠ ○ │ ● ↞ 3              │\n"
                    "│                    │                    │\n")
        self.assertEqual(self.cli.generate_middle_board().strip(), expected.strip())

    def test_generate_middle_board_large_numbers(self):
        """Prueba que generate_middle_board maneje correctamente números grandes con alineación."""
        for _ in range(100):
            self.board.add_checker_to_bar(False)  # Blancas
        for _ in range(50):
            self.board.add_checker_to_bar(True)   # Negras
        expected = ("│                    │                    │\n"
                    "│             50 ↠ ○ │ ● ↞ 100            │\n"
                    "│                    │                    │\n")
        self.assertEqual(self.cli.generate_middle_board().strip(), expected.strip())


if __name__ == '__main__':
    unittest.main()
