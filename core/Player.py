class Player:
    """Representa a un jugador en el juego.

    Attributes:
        __name__: El nombre del jugador.
        __uses_white_checkers__: Indica si el jugador usa fichas blancas (True) o negras (False).
        __score__: El puntaje del jugador.
    """
    def __init__(self, name, uses_white_ckeckers: bool,score: int = 0):
        self.__name__ = name
        self.__uses_white_checkers__ = uses_white_ckeckers
        self.__score__ = score

    @property
    def name(self) -> str:
        """El nombre del jugador."""
        return self.__name__

    @property
    def uses_white_checkers(self) -> bool:
        """Indica si el jugador usa fichas blancas (True) o negras (False)."""
        return self.__uses_white_checkers__

    @property
    def score(self) -> int:
        """El puntaje del jugador."""
        return self.__score__

    def reset_score(self) -> None:
        """Resetea el puntaje del jugador a 0."""
        self.__score__ = 0
