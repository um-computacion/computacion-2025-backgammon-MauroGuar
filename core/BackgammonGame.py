from cli.CLI import CLI
from core.Board import Board
from core.Dice import Dice
from core.Player import Player
from core.InputType import InputType


class BackgammonGame:
    def __init__(self):
        self.__pygame_mode__ = False
        self.__board__ = Board()
        self.__cli__ = CLI(self.__board__)
        self.__white_player__ = Player("Blanco", True)
        self.__black_player__ = Player("Negro", False)
        self.__player_playing__ = None
        self.__dices__ = [Dice(), Dice()]
        self.__twin_dice__ = False

    def refresh(self, dices: tuple[int, ...] = None, twin_dice: bool = False):
        if self.__pygame_mode__:
            pass
        else:
            self.__cli__.refresh_cli(self.__player_playing__.uses_white_checkers, dices, twin_dice)

    def print_usr_message(self, message: str):
        if self.__pygame_mode__:
            pass
        else:
            self.__cli__.print_usr_msg_cli(message)

    def get_user_input_check_type(self, input_message: str, allowed_types: tuple[InputType, ...]) -> int | str | None:
        input_result = self.get_user_input(input_message)
        while True:
            if InputType.ENTER in allowed_types and input_result[0] == InputType.ENTER:
                return None
            if InputType.NORMAL_INDEX in allowed_types and input_result[0] == InputType.NORMAL_INDEX:
                return input_result[1]
            if InputType.OTHER in allowed_types and input_result[0] == InputType.OTHER:
                return input_result[1]
            input_result = self.get_user_input("Valor inválido, inténtelo de nuevo")

    def get_user_input(self, input_message: str) -> tuple[InputType, int | str | None]:
        if self.__pygame_mode__:
            pass
        else:
            return self.__cli__.input_cli(input_message)
        raise Exception("Algo anduvo mal con el manejo interno del input de usuario.")

    def start_dice_roll(self):
        while True:
            for dice in self.__dices__:
                dice.roll_dice()

            if self.__dices__[0] > self.__dices__[1]:
                self.__player_playing__ = self.__white_player__
                break
            elif self.__dices__[0] < self.__dices__[1]:
                self.__player_playing__ = self.__black_player__
                break

    def change_turn(self):
        """Cambia el jugador que está jugando por el otro."""
        if self.__player_playing__.uses_white_checkers:
            self.__player_playing__ = self.__black_player__
        else:
            self.__player_playing__ = self.__white_player__
