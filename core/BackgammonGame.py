from core import Board, Player, Dice


class BackgammonGame:
    def __init__(self):
        self.__board__ = Board.Board()
        self.__white_player__ = Player.Player(None, True)
        self.__black_player__ = Player.Player(None, False)
        self.__dice1__ = Dice.Dice()
        self.__dice2__ = Dice.Dice()

    def set_player_name(self, is_white_player: bool, name: str) -> str:
        """Define el nombre de un jugador.

        Args:
            is_white_player: True si el jugador es el de fichas blancas, False si es el de fichas negras.
            name: El nombre a asignar al jugador.
        Returns:
            str: El nombre asignado al jugador en mayúsculas.
        Raises:
            ValueError: Si el nombre no cumple con las restricciones.
        """
        if not isinstance(name, str):
            raise ValueError("El nombre debe ser una cadena de texto.")
        if not (3 <= len(name) <= 7):
            raise ValueError("El nombre debe tener entre 3 y 7 caracteres.")
        letter_count = sum(1 for c in name if c.isalpha())
        if not all(c.isalnum() for c in name) or letter_count < 3:
            raise ValueError("El nombre solo puede contener letras y números, y debe incluir al menos 3 letras.")
        other_name = self.__black_player__.name if is_white_player else self.__white_player__.name
        if other_name and name.upper() == other_name.upper():
            raise ValueError("El nombre no puede ser igual al del otro jugador.")
        upper_name = name.upper()
        if is_white_player:
            self.__white_player__.name = upper_name
        else:
            self.__black_player__.name = upper_name
        return upper_name
