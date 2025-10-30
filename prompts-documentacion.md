# Prompts Utilizados para la Documentación

## Prompt #1

### Modelo: Gemini 2.5 Pro (desde github copilot)

### Prompt

Quiero que realices la documentación entera de este archivo de python.
Utiliza el estándar de google descripto en @google/styleguide/files/pyguide.md<br>
Lo unico que si quiero es que este en español

### Referencias

- Dice.py (subido desde mi computadora)
- https://github.com/google/styleguide/blob/c6f57a913e0e178b8ae51364509d1f684c6d4462/pyguide.md (que como es github copilot, se puede referenciar simplemente como @google/styleguide/files/pyguide.md)

### Respuesta

Claro, aquí tienes el archivo `Dice.py` documentado en español, siguiendo las directrices de la guía de estilo de Python de Google.

Aquí está el código actualizado:

```python
import random


class Dice:
    """Representa un dado de seis caras.

    Permite simular el lanzamiento de un dado, almacenar su valor numérico
    y obtener una representación ASCII del mismo.

    Attributes:
        __dice_number__: Un entero que representa el valor numérico actual del dado.
        __dice_str__: Una tupla de cadenas de texto que forma una representación
          ASCII del valor actual del dado.
    """
    DICES_STR = {
        0: ("┌─────────┐",
            "│         │",
            "│         │",
            "│         │",
            "└─────────┘"),
        1: ("┌─────────┐",
            "│         │",
            "│    ●    │",
            "│         │",
            "└─────────┘"),
        2: ("┌─────────┐",
            "│  ●      │",
            "│         │",
            "│      ●  │",
            "└─────────┘"),
        3: ("┌─────────┐",
            "│  ●      │",
            "│    ●    │",
            "│      ●  │",
            "└─────────┘"),
        4: ("┌─────────┐",
            "│  ●   ●  │",
            "│         │",
            "│  ●   ●  │",
            "└─────────┘"),
        5: ("┌─────────┐",
            "│  ●   ●  │",
            "│    ●    │",
            "│  ●   ●  │",
            "└─────────┘"),
        6: ("┌─────────┐",
            "│  ●   ●  │",
            "│  ●   ●  │",
            "│  ●   ●  │",
            "└─────────┘")
    }

    def __init__(self, dice_number=0):
        """Inicializa una instancia del dado.

        Args:
            dice_number: El valor inicial del dado.
        """
        self.__dice_number__ = dice_number
        self.__dice_str__ = self.DICES_STR[self.__dice_number__]

    @property
    def dice_number(self) -> int:
        """El valor numérico actual del dado (solo lectura)."""
        return self.__dice_number__

    @property
    def dice_str(self) -> tuple[str, ...]:
        """La representación ASCII del dado (solo lectura)."""
        return self.__dice_str__

    def roll_dice(self):
        """Simula el lanzamiento del dado.

        Asigna un nuevo valor aleatorio (entre 1 y 6) al dado y actualiza
        su representación ASCII.
        """
        self.__dice_number__ = random.randint(1, 6)
        self.__dice_str__ = self.DICES_STR[self.__dice_number__]

    def reset_dice(self):
        """Reinicia el valor del dado a 0 y actualiza su representación ASCII."""
        self.__dice_number__ = 0
        self.__dice_str__ = self.DICES_STR[self.__dice_number__]
```

### Uso de Respuesta

Utilicé la documentación generada.