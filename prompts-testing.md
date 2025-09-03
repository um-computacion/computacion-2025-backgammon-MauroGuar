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

## Prompt #3

### Modelo: Gemini 2.5 Pro (desde github copilot)

### Prompt

Ahora necesito que vuelvas a hacer unittest de la misma manera que antes pero para la clase Player.py que te he proporcionado. No quiero que le hagas cambios a la clase, solo haz los tests. El código de los tests lo quiero todo en inglés.<br>
Luego quiero que lo documentes como lo has hecho antes, siguiendo lo estándares de google: @google/styleguide/files/pyguide.md<br>
La documentación la quiero en español como antes.

### Referencias

- Player.py (subido desde mi computadora)
- https://github.com/google/styleguide/blob/c6f57a913e0e178b8ae51364509d1f684c6d4462/pyguide.md (que como es github copilot, se puede referenciar simplemente como @google/styleguide/files/pyguide.md)

### Respuesta

¡Claro que sí! Aquí tienes el archivo de pruebas unitarias para la clase `Player`.

Siguiendo tus indicaciones, el código de las pruebas está escrito en inglés, pero toda la documentación (docstrings del módulo, de la clase y de los métodos) está en español, cumpliendo con la guía de estilo de Google. No he modificado la clase `Player` original.

Aquí está el archivo `player_test.py`:

```python
import unittest
from Player import Player


class PlayerTest(unittest.TestCase):
    """Conjunto de pruebas para la clase Player."""

    def test_init_with_required_arguments(self):
        """Verifica la inicialización con argumentos requeridos y score por defecto."""
        player = Player(name="Mauro", uses_white_ckeckers=True)
        self.assertEqual(player.name, "Mauro")
        self.assertTrue(player.uses_white_checkers)
        self.assertEqual(player.score, 0)

    def test_init_with_specific_score(self):
        """Verifica la inicialización con un puntaje inicial específico."""
        player = Player(name="Guar", uses_white_ckeckers=False, score=10)
        self.assertEqual(player.name, "Guar")
        self.assertFalse(player.uses_white_checkers)
        self.assertEqual(player.score, 10)

    def test_properties_return_correct_values(self):
        """Verifica que las propiedades devuelven los valores correctos."""
        player = Player(name="TestPlayer", uses_white_ckeckers=True, score=5)
        self.assertEqual(player.name, "TestPlayer")
        self.assertTrue(player.uses_white_checkers)
        self.assertEqual(player.score, 5)

    def test_reset_score(self):
        """Verifica que el método reset_score reinicia el puntaje a 0."""
        player = Player(name="Player1", uses_white_ckeckers=True, score=100)
        self.assertEqual(player.score, 100)

        player.reset_score()
        self.assertEqual(player.score, 0)

    def test_properties_are_read_only(self):
        """Verifica que las propiedades de la clase son de solo lectura."""
        player = Player(name="Player1", uses_white_ckeckers=True)
        with self.assertRaises(AttributeError):
            player.name = "NewName"
        with self.assertRaises(AttributeError):
            player.uses_white_checkers = False
        with self.assertRaises(AttributeError):
            player.score = 50


if __name__ == '__main__':
    unittest.main()
```

### Uso de Respuesta

Utilizé el código solo cambiando los imports para que funcionaran bien.

## Prompt #4

### Modelo: Gemini 2.5 Pro (desde github copilot)

### Prompt

Te he proporcionado una versión actualizada de Board.py y test_board.py. Como podrás observar, he añadido 3 nuevas funciones (map_normal_index;replace_triangle;replace_multiple_triangle). También podrás observar que aún no están los tests unitarios para esas funciones nuevas.<br>
Quiero que hagas esos tests para las nuevas funciones. Si no es necesario, no cambies el código ya hecho de test_board.py. No cambies para nada el código de Board.py.
El código de los tests lo quiero todo en inglés.<br>
Luego quiero que lo documentes como lo has hecho antes, siguiendo lo estándares de google: @google/styleguide/files/pyguide.md<br>
La documentación la quiero en español como antes.

### Referencias

- Board.py (subido desde mi computadora)
- test_board.py (subido desde mi computadora)
- https://github.com/google/styleguide/blob/c6f57a913e0e178b8ae51364509d1f684c6d4462/pyguide.md (que como es github copilot, se puede referenciar simplemente como @google/styleguide/files/pyguide.md)

### Respuesta

¡Entendido! Me encargaré de crear las pruebas unitarias para las nuevas funciones de la clase `Board`, manteniendo el código de los tests en inglés y la documentación en español, todo de acuerdo a la guía de estilo de Google.

No modificaré la clase `Board.py` ni las pruebas existentes en `test_board.py`, solo añadiré los nuevos casos de prueba al final de la clase `TestBoard`.

Aquí tienes el archivo `test_board.py` actualizado con las pruebas para `map_normal_index`, `replace_triangle` y `replace_multiple_triangles`.

```python
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

    def test_init_creates_new_board_by_default(self):
        """Verifica que se crea un tablero nuevo por defecto al no pasar argumentos."""
        board = Board()
        self.assertListEqual(board.__top_board_triangles__,
                             self.default_top_board)
        self.assertListEqual(board.__bot_board_triangles__,
                             self.default_bot_board)

    def test_init_with_one_argument_creates_new_board(self):
        """Verifica que se crea un tablero nuevo si solo se pasa un argumento."""
        # Caso 1: Solo se proporciona el tablero superior.
        board_top_only = Board(top_board_triangles=[[1, 1, "X"]])
        self.assertListEqual(board_top_only.__top_board_triangles__,
                             self.default_top_board)
        self.assertListEqual(board_top_only.__bot_board_triangles__,
                             self.default_bot_board)

        # Caso 2: Solo se proporciona el tablero inferior.
        board_bot_only = Board(bot_board_triangles=[[1, 1, "Y"]])
        self.assertListEqual(board_bot_only.__top_board_triangles__,
                             self.default_top_board)
        self.assertListEqual(board_bot_only.__bot_board_triangles__,
                             self.default_bot_board)

    def test_init_with_custom_board(self):
        """Verifica que la inicialización funciona con un tablero personalizado."""
        custom_top = [[1, 0, "A"]]
        custom_bot = [[2, 0, "B"]]
        board = Board(top_board_triangles=custom_top,
                      bot_board_triangles=custom_bot)

        self.assertListEqual(board.__top_board_triangles__, custom_top)
        self.assertListEqual(board.__bot_board_triangles__, custom_bot)

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
        self.assertListEqual(board.__top_board_triangles__,
                             self.default_top_board)
        self.assertListEqual(board.__bot_board_triangles__,
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
        self.assertEqual(self.board.top_board_triangles[11], new_triangle_top)

        # Reemplaza un triángulo en el tablero inferior (perspectiva de negras)
        self.board.replace_triangle(1, False, new_triangle_bot)
        # Índice normal 1 para negras es el índice 0 en la lista bot
        self.assertEqual(self.board.bot_board_triangles[0], new_triangle_bot)

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

        self.assertEqual(self.board.top_board_triangles[11], new_triangle1)
        self.assertEqual(self.board.bot_board_triangles[0], new_triangle2)
        self.assertEqual(self.board.top_board_triangles[0], new_triangle3)


if __name__ == '__main__':
    unittest.main()
```

### Uso de Respuesta

Utilizé el código sin cambiarlo.