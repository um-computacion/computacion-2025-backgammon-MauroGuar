# Prompts Utilizados para el Testing

## Prompt #1

### Modelo: Gemini 2.5 Pro (desde github copilot)

### Prompt

Teniendo en cuenta el archivo Dice.py que te proporcioné, realiza unittests utilizando la librería estándar de python "unittest".<br>
Haz varios test unitarios profesionales. Luego documéntalo todo (siguiendo los estámdares de google: @google/styleguide/files/pyguide.md )

### Referencias

- Dice.py (subido desde mi computadora)
- https://github.com/google/styleguide/blob/c6f57a913e0e178b8ae51364509d1f684c6d4462/pyguide.md (que como es github copilot, se puede referenciar simplemente como @google/styleguide/files/pyguide.md)

### Respuesta

¡Excelente idea! Profesionalizar el código con pruebas unitarias es un paso fundamental.

Aquí está el código actualizado para las pruebas unitarias de tu archivo `Dice.py`:

```python
import unittest

from Dice import Dice


class TestDice(unittest.TestCase):
    """Conjunto de pruebas para la clase Dice."""

    def test_init_default_value(self):
        """Verifica que el dado se inicializa en 0 por defecto."""
        dice = Dice()
        self.assertEqual(dice.dice_number, 0)
        self.assertEqual(dice.dice_str, Dice.DICES_STR[0])

    def test_init_with_specific_value(self):
        """Verifica la inicialización con un valor específico."""
        dice = Dice(dice_number=5)
        self.assertEqual(dice.dice_number, 5)
        self.assertEqual(dice.dice_str, Dice.DICES_STR[5])

    def test_roll_dice_value_is_in_valid_range(self):
        """Verifica que el resultado de un lanzamiento está en el rango [1, 6]."""
        dice = Dice()
        for _ in range(20):  # Realiza varios lanzamientos para mayor seguridad
            dice.roll_dice()
            self.assertIn(dice.dice_number, range(1, 7))
            self.assertNotEqual(dice.dice_number, 0)

    @mock.patch('random.randint')
    def test_roll_dice_updates_state_correctly(self, mock_randint):
        """Verifica que el estado del dado se actualiza tras un lanzamiento."""
        # Forzamos a random.randint a devolver un valor predecible
        mock_randint.return_value = 4
        dice = Dice()

        dice.roll_dice()

        # Verificamos que el método fue llamado correctamente
        mock_randint.assert_called_once_with(1, 6)
        # Verificamos que el estado del dado es el esperado
        self.assertEqual(dice.dice_number, 4)
        self.assertEqual(dice.dice_str, Dice.DICES_STR[4])

    def test_reset_dice_sets_value_to_zero(self):
        """Verifica que el dado se reinicia al valor 0."""
        dice = Dice(dice_number=6)
        dice.reset_dice()
        self.assertEqual(dice.dice_number, 0)
        self.assertEqual(dice.dice_str, Dice.DICES_STR[0])

    def test_properties_are_read_only(self):
        """Verifica que las propiedades son de solo lectura."""
        dice = Dice()
        with self.assertRaises(AttributeError):
            dice.dice_number = 5
        with self.assertRaises(AttributeError):
            dice.dice_str = Dice.DICES_STR[1]


if __name__ == '__main__':
    unittest.main()
```

### Uso de Respuesta

Utilizé el código solo cambiando los imports para que funcionaran bien.
