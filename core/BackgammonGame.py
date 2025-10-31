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
        self.__dices_values__ = []
        self.__twin_dice__ = False

    def refresh(self, no_dices: bool = False):
        if self.__pygame_mode__:
            pass
        else:
            self.__cli__.refresh_cli(self.__player_playing__.uses_white_checkers, no_dices, self.__dices__)

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
            unsorted_dices = self.roll_dices(True)
            if unsorted_dices[0].dice_number > unsorted_dices[1].dice_number:
                self.__player_playing__ = self.__white_player__
                break
            elif unsorted_dices[0].dice_number < unsorted_dices[1].dice_number:
                self.__player_playing__ = self.__black_player__
                break

    def roll_dices(self, unsorted: bool = False) -> tuple[Dice, ...]:
        unsorted_dices = []
        self.__dices__ = [Dice(), Dice()]
        self.__dices_values__ = []
        for dice in self.__dices__:
            dice.roll_dice()

        if self.__dices__[0].dice_number == self.__dices__[1].dice_number:
            self.__dices__.extend(self.__dices__.copy())
            unsorted_dices = self.__dices__
        else:
            unsorted_dices = self.__dices__.copy()
            self.__dices__ = sorted(self.__dices__, key=lambda dado: dado.dice_number)

        for dice in self.__dices__:
            self.__dices_values__.append(dice.dice_number)

        if unsorted:
            return tuple(unsorted_dices)
        return tuple(self.__dices__)

    def change_turn(self):
        """Cambia el jugador que está jugando por el otro."""
        if self.__player_playing__.uses_white_checkers:
            self.__player_playing__ = self.__black_player__
        else:
            self.__player_playing__ = self.__white_player__

    def checker_selection(self) -> dict:
        user_input_normal_index = self.get_user_input_check_type("Seleccione una ficha para mover",
                                                                 (InputType.NORMAL_INDEX,))
        possible_moves = self.__board__.select_checker(user_input_normal_index,
                                                       self.__player_playing__.uses_white_checkers,
                                                       tuple(self.__dices_values__))
        return possible_moves

    def selected_checker_move(self, possible_moves: dict):
        user_input_normal_index = self.get_user_input_check_type("Seleccione donde mover la ficha",
                                                                 (InputType.NORMAL_INDEX,))
        while user_input_normal_index not in possible_moves:
            user_input_normal_index = self.get_user_input_check_type("Seleccione un lugar válido donde"
                                                                     "mover la ficha", (InputType.NORMAL_INDEX,))
        self.__board__.move_checker(self.__board__.selected_checker, user_input_normal_index,
                                    self.__player_playing__.uses_white_checkers)
        self.consume_dice(user_input_normal_index, possible_moves)

    def consume_dice(self, dest_triangle_normal: int, possible_moves: dict):
        dices_number_to_consume = possible_moves[dest_triangle_normal]
        for dcn in dices_number_to_consume:
            for dice in self.__dices__:
                if dice.dice_number == dcn:
                    dice.reset_dice()

    def interactive_roll_dices(self):
        self.get_user_input_check_type("Presiona enter para lanzar los dados", (InputType.ENTER,))
        self.roll_dices()

    def try_return_checker(self) -> bool:
        possible_moves = self.__board__.return_to_board_possible_moves(self.__player_playing__.uses_white_checkers,
                                                                       self.__dices_values__)
        if possible_moves:
            self.refresh()
            user_input_normal_index = self.get_user_input_check_type("Seleccione donde colocar la ficha",
                                                                     (InputType.NORMAL_INDEX,))
            while user_input_normal_index not in possible_moves:
                user_input_normal_index = self.get_user_input_check_type("Seleccione un lugar válido donde "
                                                                         "colocar la ficha", (InputType.NORMAL_INDEX,))
            self.__board__.return_to_board(self.__player_playing__.uses_white_checkers, user_input_normal_index)
            return True
        return False
