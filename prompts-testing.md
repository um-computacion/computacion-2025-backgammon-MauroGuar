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

## Prompt #2

### Modelo: Gemini 2.5 Pro (desde github copilot)

### Prompt

Ahora necesito que hagas lo mismo pero para otra clase llamada Board que te he proporcionado. Solo quiero que hagas los tests, no alteres el código de la clase original.<br>
@google/styleguide/files/pyguide.md

### Referencias

- Board.py (subido desde mi computadora)
- https://github.com/google/styleguide/blob/c6f57a913e0e178b8ae51364509d1f684c6d4462/pyguide.md (que como es github copilot, se puede referenciar simplemente como @google/styleguide/files/pyguide.md)

### Respuesta
¡Por supuesto! Siguiendo la misma línea, he creado un conjunto de pruebas unitarias para la clase `Board`.

Como me pediste, **no he modificado la clase `Board` original**. Para poder realizar las pruebas, he accedido a los atributos "privados" (`__top_board_triangles__` y `__bot_board_triangles__`) utilizando la técnica de *name mangling* de Python, que es una práctica aceptable y a veces necesaria en el contexto de las pruebas unitarias.

Aquí tienes el archivo `board_test.py` con las pruebas unitarias profesionales y su respectiva documentación en español, siguiendo las directrices de estilo de Google.

```python
import unittest
from Board import Board


class BoardTest(unittest.TestCase):
    """Conjunto de pruebas para la clase Board."""

    def setUp(self):
        """Prepara los recursos necesarios para cada prueba.

        Define el estado esperado del tablero por defecto para evitar
        repetirlo en cada prueba y mejorar la legibilidad.
        """
        self.default_top_board = [
            [5, 0, "●"], [0, 0, " "], [0, 0, " "], [0, 0, " "], [3, 0, "○"],
            [0, 0, " "], [5, 0, "○"], [0, 0, " "], [0, 0, " "], [0, 0, " "],
            [0, 0, " "], [2, 0, "●"]
        ]
        self.default_bot_board = [
            [5, 0, "○"], [0, 0, " "], [0, 0, " "], [0, 0, " "], [3, 0, "●"],
            [0, 0, " "], [5, 0, "●"], [0, 0, " "], [0, 0, " "], [0, 0, " "],
            [0, 0, " "], [2, 0, "○"]
        ]

    def test_init_creates_new_board_by_default(self):
        """Verifica que se crea un tablero nuevo por defecto al no pasar argumentos."""
        board = Board()
        # Se accede a los atributos con "name mangling" para la prueba.
        self.assertListEqual(board._Board__top_board_triangles__,
                             self.default_top_board)
        self.assertListEqual(board._Board__bot_board_triangles__,
                             self.default_bot_board)

    def test_init_with_one_argument_creates_new_board(self):
        """Verifica que se crea un tablero nuevo si solo se pasa un argumento."""
        # Caso 1: Solo se proporciona el tablero superior.
        board_top_only = Board(top_board_triangles=[[1, 1, "X"]])
        self.assertListEqual(board_top_only._Board__top_board_triangles__,
                             self.default_top_board)
        self.assertListEqual(board_top_only._Board__bot_board_triangles__,
                             self.default_bot_board)

        # Caso 2: Solo se proporciona el tablero inferior.
        board_bot_only = Board(bot_board_triangles=[[1, 1, "Y"]])
        self.assertListEqual(board_bot_only._Board__top_board_triangles__,
                             self.default_top_board)
        self.assertListEqual(board_bot_only._Board__bot_board_triangles__,
                             self.default_bot_board)

    def test_init_with_custom_board(self):
        """Verifica que la inicialización funciona con un tablero personalizado."""
        custom_top = [[1, 0, "A"]]
        custom_bot = [[2, 0, "B"]]
        board = Board(top_board_triangles=custom_top,
                      bot_board_triangles=custom_bot)

        self.assertListEqual(board._Board__top_board_triangles__, custom_top)
        self.assertListEqual(board._Board__bot_board_triangles__, custom_bot)

    def test_new_game_board_resets_state(self):
        """Verifica que new_game_board() resetea el tablero a su estado inicial."""
        # Se crea un tablero personalizado.
        custom_top = [[1, 0, "A"]]
        custom_bot = [[2, 0, "B"]]
        board = Board(top_board_triangles=custom_top,
                      bot_board_triangles=custom_bot)

        # Se llama al método para resetear el tablero.
        board.new_game_board()

        # Se comprueba que el tablero ha vuelto al estado por defecto.
        self.assertListEqual(board._Board__top_board_triangles__,
                             self.default_top_board)
        self.assertListEqual(board._Board__bot_board_triangles__,
                             self.default_bot_board)


if __name__ == '__main__':
    unittest.main()
```

### Uso de Respuesta

Utilizé el código solo cambiando los imports para que funcionaran bien y cambiando lo del "name mangling" que daba errores.
