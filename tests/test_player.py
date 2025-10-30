import unittest
from core.Player import Player


class TestPlayer(unittest.TestCase):
    """Conjunto de pruebas para la clase Player."""

    def test_init_with_required_arguments(self):
        """Verifica la inicialización con argumentos requeridos y score por defecto."""
        player = Player(player_name="Pablo", uses_white_ckeckers=True)
        self.assertEqual(player.name, "Pablo")
        self.assertTrue(player.uses_white_checkers)
        self.assertEqual(player.score, 0)

    def test_init_with_specific_score(self):
        """Verifica la inicialización con un puntaje inicial específico."""
        player = Player(player_name="Juan", uses_white_ckeckers=False, score=10)
        self.assertEqual(player.name, "Juan")
        self.assertFalse(player.uses_white_checkers)
        self.assertEqual(player.score, 10)

    def test_properties_return_correct_values(self):
        """Verifica que las propiedades devuelven los valores correctos."""
        player = Player(player_name="TestPlayer", uses_white_ckeckers=True, score=5)
        self.assertEqual(player.name, "TestPlayer")
        self.assertTrue(player.uses_white_checkers)
        self.assertEqual(player.score, 5)

    def test_reset_score(self):
        """Verifica que el método reset_score reinicia el puntaje a 0."""
        player = Player(player_name="Player1", uses_white_ckeckers=True, score=100)
        self.assertEqual(player.score, 100)

        player.reset_score()
        self.assertEqual(player.score, 0)


if __name__ == '__main__':
    unittest.main()
