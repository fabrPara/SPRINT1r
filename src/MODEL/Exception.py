class QuoridorError(Exception):
    """Classe base per tutte le eccezioni del gioco ."""

    pass


class MovementError(QuoridorError):
    """Lanciata per spostamenti non validi ."""

    pass


class WallPlacementError(QuoridorError):
    """Lanciata per posizionamento muri errato ."""

    pass


class WallDepletionError(QuoridorError):
    """Lanciata quando un giocatore ha esaurito i muri."""

    pass


class TurnError(QuoridorError):
    """lanciata quando un giocatore tenta di agire fuori dal proprio turno."""

    pass


class InvalidCommandError(QuoridorError):
    """Lanciata per errori di input o sintassi."""

    pass
