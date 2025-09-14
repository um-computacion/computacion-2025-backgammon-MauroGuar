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


if __name__ == '__main__':
    unittest.main()
