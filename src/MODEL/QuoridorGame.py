from .Board import Board
from .Cell import Cell
from .Player import Player

##importare la classe Exeption per gli tutti gli errori del gioco


class QuoridorGame:
    """Classe principale per il gioco Quoridor.

    Gestisce la logica del tabellone, i giocatori e il loro turno.
    Fornisce metodi per muovere i giocatori, posizionare muri, verificare il vincitore.
    """

    def __init__(self):
        """Inizializza una nuova partita di Quoridor.

        Args:
            Board: classe che rappresenta il tabellone di gioco
            Player: classe che rappresenta un giocatore
            Cell: classe che rappresenta una cella del tabellone

        """
        self._board = Board()  # crea il tabellone

        # crea i giocatori
        p1_start = Cell(5, 1)  # posizione iniziale del giocatore 1
        p2_start = Cell(5, 9)  # posizione iniziale del giocatore 2
        p1 = Player(player_id=1, start_pos=p1_start, target_row=8)
        p2 = Player(player_id=2, start_pos=p2_start, target_row=0)
        self._players = [p1, p2]

        self._current_turn = 1  ##indice del giocatore che deve muovere (1 o 2)
        self._winner = None

    def get_game_state(self) -> dict:
        """Ritorna lo stato attuale del gioco per permetterne il rendering.

        Returns:
            dict: Contiene i riferimenti alla board, alla lista giocatori,
                  all'indice del giocatore corrente e all'eventuale vincitore.

        """
        return {
            "board": self._board,
            "players": self._players,
            "current_player_id": self._current_turn,
            "winner": self._winner,
        }

    def check_victory(self):
        pass
