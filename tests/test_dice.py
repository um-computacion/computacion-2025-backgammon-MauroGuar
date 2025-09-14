import unittest
from unittest import mock

from core.Dice import Dice


class TestDice(unittest.TestCase):
    """Conjunto de pruebas para la clase Dice."""
    def setUp(self):
        """Prepara los recursos necesarios para cada prueba."""
        # Crea una referencia a la clase Dice para ser usada en las pruebas
        self.dice = Dice()

    def test_init_default_value(self):
        """Verifica que el dado se inicializa en 0 por defecto."""
        self.assertEqual(self.dice.dice_number, 0)
        self.assertEqual(self.dice.dice_str, Dice.DICES_STR[0])

    def test_init_with_specific_value(self):
        """Verifica la inicialización con un valor específico."""
        dice = Dice(dice_number=5)
        self.assertEqual(dice.dice_number, 5)
        self.assertEqual(dice.dice_str, Dice.DICES_STR[5])

    def test_roll_dice_value_is_in_valid_range(self):
        """Verifica que el resultado de un lanzamiento está en el rango [1, 6]."""
        for _ in range(20):  # Realiza varios lanzamientos para mayor seguridad
            self.dice.roll_dice()
            self.assertIn(self.dice.dice_number, range(1, 7))
            self.assertNotEqual(self.dice.dice_number, 0)

    @mock.patch('random.randint')
    def test_roll_dice_updates_state_correctly(self, mock_randint):
        """Verifica que el estado del dado se actualiza tras un lanzamiento."""
        # Forzamos a random.randint a devolver un valor predecible
        mock_randint.return_value = 4

        self.dice.roll_dice()

        # Verificamos que el método fue llamado correctamente
        mock_randint.assert_called_once_with(1, 6)
        # Verificamos que el estado del dado es el esperado
        self.assertEqual(self.dice.dice_number, 4)
        self.assertEqual(self.dice.dice_str, Dice.DICES_STR[4])

    def test_reset_dice_sets_value_to_zero(self):
        """Verifica que el dado se reinicia al valor 0."""
        # Primero lanzamos el dado para cambiar su estado
        self.dice.roll_dice()

        # Luego lo reiniciamos
        self.dice.reset_dice()

        # Verificamos que el estado del dado es el esperado (0)
        self.assertEqual(self.dice.dice_number, 0)
        self.assertEqual(self.dice.dice_str, Dice.DICES_STR[0])

    def test_properties_are_read_only(self):
        """Verifica que las propiedades son de solo lectura."""
        with self.assertRaises(AttributeError):
            self.dice.dice_number = 5
        with self.assertRaises(AttributeError):
            self.dice.dice_str = Dice.DICES_STR[1]


if __name__ == '__main__':
    unittest.main()
