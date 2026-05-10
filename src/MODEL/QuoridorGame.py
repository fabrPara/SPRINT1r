from .Board import Board
from .Cell import Cell
<<<<<<< HEAD
from .Exception import MovementError  # Import richiesto
from .Player import Player
=======
from .Exception import InvalidCommandError, TurnError
from .Player import Player
from .Wall import Wall
>>>>>>> 60a00b434b4997f87b55139c930a0adef6d26798


class QuoridorGame:
    """Classe principale per il gioco Quoridor.

    Gestisce la logica del tabellone, i giocatori e il loro turno.
    Fornisce metodi per muovere i giocatori, posizionare muri, verificare il vincitore.
    """

    def __init__(self):
        """Inizializza una nuova partita di Quoridor."""
        self._board = Board()

        # Posizioni iniziali
        p1_start = Cell(4, 0)
        p2_start = Cell(4, 8)

        # Creazione istanze Player (corretto: rimosse le parentesi quadre esterne)
        p1 = Player(player_id=1, start_pos=p1_start, target_row=8)
        p2 = Player(player_id=2, start_pos=p2_start, target_row=0)

        self._players = [p1, p2]
        self._current_turn = 0  # Indice del giocatore corrente (0 o 1)
        self._winner = None

    def switch_turn(self):
        """Cambia il turno passando al giocatore successivo."""
        self._current_turn = (self._current_turn + 1) % len(self._players)

    def move_player(self, coords: str):
        """Muove il giocatore corrente nella cella specificata dalle coordinate.

        Args:
            coords (str): Le coordinate della destinazione nel formato "x,y".

        Raises:
            MovementError: Se il movimento non è consentito.

        """
        # 1. Recupera il giocatore di turno
        current_player = self._players[self._current_turn]

<<<<<<< HEAD
        # 2. Parsing della stringa coords
        try:
            x_str, y_str = coords.split(",")
            target_x = int(x_str.strip())
            target_y = int(y_str.strip())
        except (ValueError, IndexError):
            raise MovementError("Formato coordinate non valido. Usa 'x,y'.") from None

        # 3. Validazione movimento (Logica base: 1 passo adiacente)
        current_pos = current_player.get_position()
        curr_x, curr_y = current_pos.get_coords()

        dx = abs(target_x - curr_x)
        dy = abs(target_y - curr_y)

        # Controllo adiacenza (no diagonali, max 1 casella)
        if not ((dx == 1 and dy == 0) or (dx == 0 and dy == 1)):
            raise MovementError(
                "Movimento non valido: puoi muoverti solo di una cella in "
                "orizzontale o verticale."
            )

        # 4. Aggiornamento posizione
        # Nota: qui andrebbero aggiunti i controlli sui muri (tramite self._board)
        new_cell = Cell(target_x, target_y)
        current_player.set_position(new_cell)

        # 5. Cambio turno automatico dopo un movimento valido
        self.switch_turn()
=======
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

        if coords[2] not in ["h"]:
            raise InvalidCommandError("Orientamento non valido. Usa 'h' .")

        current_player = self._players[self._current_turn - 1]

        # 1. Controlla e scala il muro dal giocatore (lancia errore se a 0)
        current_player.use_wall()

        # 2. Traduce le stringhe in oggetti
        start_cell = Cell(coords[0], coords[1])
        new_wall = Wall(start_cell=start_cell, orientation=coords[2])

        # 3. Prova ad aggiungere il muro alla board
        try:
            self._board.add_wall(new_wall)
        except Exception as e:
            # Se la board rifiuta il muro, dobbiamo restituirlo al giocatore!
            current_player._walls_count += 1
            raise e  # Rilanciamo l'errore per farlo gestire al Controller

        # Se arriviamo qui, il muro è piazzato. Passiamo il turno.
>>>>>>> 60a00b434b4997f87b55139c930a0adef6d26798
