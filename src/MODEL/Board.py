"""Modulo per la gestione del tabellone di gioco."""


class Board:
    """Rappresenta il tabellone di gioco.

    Questa classe gestisce gli elementi strutturali del tabellone,
    mantenendo traccia delle celle che lo compongono e dei muri
    posizionati al suo interno.
    """

    def __init__(self):
        """Inizializza una nuova istanza del tabellone (Board).

        Crea le strutture dati iniziali (liste vuote) necessarie per
        memorizzare le celle e i muri. Gli attributi sono definiti
        come protetti (prefisso '_') per indicare che il loro accesso
        e la loro modifica dovrebbero avvenire tramite futuri metodi
        della classe.

        Attributes:
            _cells (list[Cell]): Una lista destinata a contenere gli
                oggetti di tipo `Cell` (le caselle).
            _walls (list[Wall]): Una lista destinata a contenere gli
                oggetti di tipo `Wall` (i muri o ostacoli).

        """
        self._cells: list[Cell] = []  # noqa: F821
        self._walls: list[Wall] = []  # noqa: F821