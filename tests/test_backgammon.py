import unittest
from core.BackgammonGame import BackgammonGame


class TestBackgammonGame(unittest.TestCase):
    def setUp(self):
        """Inicializa una instancia de BackgammonGame para cada prueba."""
        self.game = BackgammonGame()

    def test_set_player_name_invalid_type(self):
        """Prueba que se lance ValueError cuando el nombre no es una cadena de texto."""
        with self.assertRaises(ValueError) as cm:
            self.game.set_player_name(True, 123)
        self.assertEqual(str(cm.exception), "El nombre debe ser una cadena de texto.")

    def test_set_player_name_length_too_short(self):
        """Prueba que se lance ValueError cuando el nombre tiene menos de 3 caracteres."""
        with self.assertRaises(ValueError) as cm:
            self.game.set_player_name(True, "AB")
        self.assertEqual(str(cm.exception), "El nombre debe tener entre 3 y 7 caracteres.")

    def test_set_player_name_length_too_long(self):
        """Prueba que se lance ValueError cuando el nombre tiene más de 7 caracteres."""
        with self.assertRaises(ValueError) as cm:
            self.game.set_player_name(True, "ABCDEFGH")
        self.assertEqual(str(cm.exception), "El nombre debe tener entre 3 y 7 caracteres.")

    def test_set_player_name_invalid_characters(self):
        """Prueba que se lance ValueError cuando el nombre contiene caracteres no alfanuméricos."""
        with self.assertRaises(ValueError) as cm:
            self.game.set_player_name(True, "ABC!")
        self.assertEqual(str(cm.exception), "El nombre solo puede contener letras y números, y debe incluir al menos 3 letras.")

    def test_set_player_name_insufficient_letters(self):
        """Prueba que se lance ValueError cuando el nombre tiene menos de 3 letras."""
        with self.assertRaises(ValueError) as cm:
            self.game.set_player_name(True, "123")
        self.assertEqual(str(cm.exception), "El nombre solo puede contener letras y números, y debe incluir al menos 3 letras.")

    def test_set_player_name_same_as_other_case_insensitive(self):
        """Prueba que se lance ValueError cuando el nombre es igual al del otro jugador, ignorando mayúsculas."""
        self.game.set_player_name(True, "ALICE")  # Establecer nombre para blanco
        with self.assertRaises(ValueError) as cm:
            self.game.set_player_name(False, "alice")  # Intentar establecer para negro
        self.assertEqual(str(cm.exception), "El nombre no puede ser igual al del otro jugador.")

    def test_set_player_name_valid_white(self):
        """Prueba la configuración válida del nombre para el jugador blanco."""
        result = self.game.set_player_name(True, "alice")
        self.assertEqual(result, "ALICE")
        self.assertEqual(self.game.__white_player__.name, "ALICE")

    def test_set_player_name_valid_black(self):
        """Prueba la configuración válida del nombre para el jugador negro."""
        result = self.game.set_player_name(False, "bob")
        self.assertEqual(result, "BOB")
        self.assertEqual(self.game.__black_player__.name, "BOB")

    def test_set_player_name_boundary_length_3(self):
        """Prueba la configuración válida con longitud mínima de 3 caracteres."""
        result = self.game.set_player_name(True, "ABC")
        self.assertEqual(result, "ABC")
        self.assertEqual(self.game.__white_player__.name, "ABC")

    def test_set_player_name_boundary_length_7(self):
        """Prueba la configuración válida con longitud máxima de 7 caracteres."""
        result = self.game.set_player_name(True, "ABCDEFG")
        self.assertEqual(result, "ABCDEFG")
        self.assertEqual(self.game.__white_player__.name, "ABCDEFG")

    def test_set_player_name_mixed_case(self):
        """Prueba que el nombre se convierta a mayúsculas."""
        result = self.game.set_player_name(True, "aLiCe")
        self.assertEqual(result, "ALICE")
        self.assertEqual(self.game.__white_player__.name, "ALICE")

    def test_set_player_name_numbers_and_letters(self):
        """Prueba la configuración válida con letras y números."""
        result = self.game.set_player_name(True, "ABC123")
        self.assertEqual(result, "ABC123")
        self.assertEqual(self.game.__white_player__.name, "ABC123")


if __name__ == '__main__':
    unittest.main()
