from .Board import Board
from .Cell import Cell
from .Exception import InvalidCommandError, TurnError
from .Player import Player
from .Wall import Wall


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

   
    def place_wall(self, coords: tuple[int, int, str]) -> None:
        """Piazza un muro per il giocatore corrente."""
        if self._winner is not None:
            raise TurnError("La partita è già finita.")

        if coords[2] not in ['h']:
            raise InvalidCommandError("Orientamento non valido. Usa 'h' .")

        current_player = self._players[self._current_turn]

        # 1. Controlla e scala il muro dal giocatore (lancia errore se a 0)
        current_player.use_wall()

        # 2. Traduce le stringhe in oggetti
        start_cell = Cell(coords[0],coords[1])
        new_wall = Wall(start_cell=start_cell, orientation=coords[2])

        # 3. Prova ad aggiungere il muro alla board
        try:
            self._board.add_wall(new_wall)
        except Exception as e:
            # Se la board rifiuta il muro, dobbiamo restituirlo al giocatore!
            current_player._walls_count += 1 
            raise e # Rilanciamo l'errore per farlo gestire al Controller

        # Se arriviamo qui, il muro è piazzato. Passiamo il turno.
       

    

