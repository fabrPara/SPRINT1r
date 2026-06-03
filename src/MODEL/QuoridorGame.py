"""Modulo principale per la logica del gioco Quoridor."""

from .Board import Board
from .Cell import Cell
from .Exception import InvalidCommandError, MovementError, TurnError
from .Player import WALLS_2P, WALLS_4P, Player
from .Wall import Wall


class QuoridorGame:
    """Classe principale per il gioco Quoridor.

    Gestisce la logica del tabellone, i giocatori e il loro turno.
    Fornisce metodi per muovere i giocatori, posizionare muri, verificare il vincitore.
    Supporta sia la modalità a 2 giocatori che quella a 4 giocatori.
    """

    def __init__(self, num_players: int = 2):
        """Inizializza una nuova partita di Quoridor.

        Args:
            num_players (int): Numero di giocatori (2 o 4). Default 2.

        """
        self._num_players = num_players
        self._board = Board()
        self._players: list[Player] = []
        self._active_player_ids: list[int] = []
        self._winner: int | None = None
        self._current_turn_index: int = 0
        self._move_history: list[dict] = []
        self._setup_players()

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def _setup_players(self) -> None:
        """Crea e posiziona i giocatori in base alla modalità selezionata."""
        if self._num_players == 4:
            walls = WALLS_4P
            # P1: lato sinistro (x=1), obiettivo x=9  — target_row usato come target_col
            # P2: lato destro  (x=9), obiettivo x=1
            # P3: lato alto    (y=1), obiettivo y=9
            # P4: lato basso   (y=9), obiettivo y=1
            # Convenzione: target_row < 0 indica un obiettivo su colonna (asse x).
            # target_row >= 1 indica un obiettivo su riga (asse y).
            configs = [
                (1, Cell(1, 5), -9),  # P1: parte da (1,5), deve raggiungere colonna 9
                (2, Cell(9, 5), -1),  # P2: parte da (9,5), deve raggiungere colonna 1
                (3, Cell(5, 1), 9),  # P3: parte da (5,1), deve raggiungere riga 9
                (4, Cell(5, 9), 1),  # P4: parte da (5,9), deve raggiungere riga 1
            ]
        else:
            walls = WALLS_2P
            configs = [
                (1, Cell(5, 1), 9),
                (2, Cell(5, 9), 1),
            ]

        self._players = [
            Player(player_id=pid, start_pos=pos, target_row=target, walls_count=walls)
            for pid, pos, target in configs
        ]
        self._active_player_ids = [p._id for p in self._players]
        self._current_turn_index = 0
        self._winner = None

    # ------------------------------------------------------------------
    # Turni
    # ------------------------------------------------------------------

    @property
    def _current_turn(self) -> int:
        """Restituisce l'ID del giocatore di turno corrente."""
        if not self._active_player_ids:
            return 0
        return self._active_player_ids[
            self._current_turn_index % len(self._active_player_ids)
        ]  # noqa: E501

    def switch_turn(self) -> None:
        """Avanza al turno del prossimo giocatore attivo."""
        if self._active_player_ids:
            self._current_turn_index = (self._current_turn_index + 1) % len(
                self._active_player_ids
            )

    def _get_player_by_id(self, player_id: int) -> Player:
        """Restituisce il Player corrispondente all'ID fornito."""
        for p in self._players:
            if p._id == player_id:
                return p
        msg = f"Giocatore con ID {player_id} non trovato."
        raise ValueError(msg)

    # ------------------------------------------------------------------
    # Cronologia Mosse
    # ------------------------------------------------------------------

    def _coord_to_notation(self, col: int, row: int, orient: str | None = None) -> str:
        """Converti coordinate numeriche a notazione alfanumerica.

        Args:
            col (int): Colonna (1-9)
            row (int): Riga (1-9)
            orient (str): Orientamento ('h' o 'v' per muri)

        Returns:
            str: Notazione (es. 'e1', 'e3h', 'e3v')

        """
        col_letter = chr(ord('a') + col - 1)
        if orient:
            return f"{col_letter}{row}{orient.lower()}"
        return f"{col_letter}{row}"

    def _record_move(self, player_id: int, move_type: str, notation: str) -> None:
        """Registra una mossa nella cronologia.

        Args:
            player_id (int): ID del giocatore che ha fatto la mossa
            move_type (str): Tipo di mossa ('movimento' o 'muro')
            notation (str): Notazione della mossa

        """
        move_entry = {
            "player_id": player_id,
            "move_type": move_type,
            "notation": notation,
        }
        self._move_history.append(move_entry)

    def record_event(
        self,
        player_id: int,
        event_type: str,
        notation: str | None = None,
    ) -> None:
        """Registra un evento speciale nella cronologia.

        Esempi: 'resign', 'timeout', 'vittoria'. Evita duplicati per vittoria.
        """
        # Evita duplicati di vittoria per lo stesso giocatore
        if event_type == "vittoria":
            for e in self._move_history:
                if e.get("move_type") == "vittoria" and e.get("player_id") == player_id:
                    return

        entry = {
            "player_id": player_id,
            "move_type": event_type,
            "notation": notation or "",
        }
        self._move_history.append(entry)

    def get_move_history(self) -> list[dict]:
        """Restituisce la cronologia completa delle mosse.

        Returns:
            list[dict]: Lista di mosse registrate

        """
        return self._move_history.copy()

    def has_moves(self) -> bool:
        """Verifica se sono state effettuate mosse nella partita.

        Returns:
            bool: True se ci sono mosse, False altrimenti

        """
        return len(self._move_history) > 0

    # ------------------------------------------------------------------
    # Movimento
    # ------------------------------------------------------------------

    def move_player(self, coords: tuple[int, int]) -> None:
        """Muove il giocatore corrente nella cella specificata dalle coordinate."""
        if len(coords) != 2:
            raise MovementError("Formato coordinate non valido. Usa una tupla (x, y).")

        target_x, target_y = coords

        if not isinstance(target_x, int) or not isinstance(target_y, int):
            raise MovementError("Coordinate non valide. Usa numeri interi.")

        if not (1 <= target_x <= 9 and 1 <= target_y <= 9):
            raise MovementError("Movimento fuori dai confini della scacchiera (1-9).")

        current_player = self._get_player_by_id(self._current_turn)
        current_pos = current_player.get_position()
        curr_x, curr_y = current_pos.get_coords()

        dx = target_x - curr_x
        dy = target_y - curr_y

        # Raccoglie tutti gli avversari attivi (non il giocatore corrente)
        opponents = [
            p
            for p in self._players
            if p._id != self._current_turn and p._id in self._active_player_ids
        ]

        # --- RICERCA AVVERSARIO ADIACENTE OTTIMIZZATA PER IL SALTO ---
        # Un avversario è d'intralcio se si trova nella casella adiacente in cui stiamo provando ad andare,  # noqa: E501
        # oppure a metà strada se stiamo tentando un salto dritto di 2 caselle.
        adjacent_opponent: Player | None = None
        for opp in opponents:
            ox, oy = opp.get_position().get_coords()
            # Se la mossa è un salto dritto di 2 caselle, l'avversario deve essere a metà strada  # noqa: E501
            if abs(dx) == 2 and dy == 0 and ox == curr_x + (dx // 2) and oy == curr_y:  # noqa: SIM114
                adjacent_opponent = opp
                break
            elif dx == 0 and abs(dy) == 2 and ox == curr_x and oy == curr_y + (dy // 2):
                adjacent_opponent = opp
                break
            # Se la mossa è diagonale (es. salto diagonale), cerchiamo l'avversario nella casella adiacente di partenza  # noqa: E501
            elif abs(dx) == 1 and abs(dy) == 1:
                # Se ci muoviamo in diagonale, l'avversario potrebbe essere o sulla stessa riga o sulla stessa colonna  # noqa: E501
                if (ox == curr_x and oy == target_y) or (
                    ox == target_x and oy == curr_y
                ):  # noqa: E501
                    adjacent_opponent = opp
                    break

        def is_within_bounds(x: int, y: int) -> bool:
            return 1 <= x <= 9 and 1 <= y <= 9

        def is_cell_occupied(x: int, y: int) -> bool:
            return any(
                p.get_position().get_coords() == (x, y)
                for p in self._players
                if p._id in self._active_player_ids
            )

        def segment_blocked(x1: int, y1: int, x2: int, y2: int) -> bool:
            move_dx = x2 - x1
            move_dy = y2 - y1
            for wall in self._board.get_walls():
                wx, wy = wall.get_start_cell().get_coords()
                w_orient = wall.get_orientation().lower()
                if (
                    move_dx == 0
                    and abs(move_dy) == 1
                    and w_orient == "h"
                    and wy == max(y1, y2)
                    and (wx == x1 or wx == x1 - 1)
                ):
                    return True
                if (
                    move_dy == 0
                    and abs(move_dx) == 1
                    and w_orient == "v"
                    and wx == max(x1, x2)
                    and (wy == y1 or wy == y1 + 1)
                ):
                    return True
            return False

        if adjacent_opponent is not None:
            opp_x, opp_y = adjacent_opponent.get_position().get_coords()
            opp_dx = opp_x - curr_x
            opp_dy = opp_y - curr_y

            direct_jump_x = curr_x + 2 * opp_dx
            direct_jump_y = curr_y + 2 * opp_dy
            direct_target = (direct_jump_x, direct_jump_y)
            pivot_blocked = segment_blocked(curr_x, curr_y, opp_x, opp_y)

            if (target_x, target_y) == (opp_x, opp_y):
                raise MovementError("Movimento non valido: cella occupata.")

            if (target_x, target_y) == direct_target:
                if (
                    pivot_blocked
                    or not is_within_bounds(direct_jump_x, direct_jump_y)
                    or is_cell_occupied(direct_jump_x, direct_jump_y)
                    or segment_blocked(opp_x, opp_y, direct_jump_x, direct_jump_y)
                ):
                    raise MovementError("Salto non permesso: muro blocca il passaggio.")
                current_player.set_position(Cell(direct_jump_x, direct_jump_y))
                notation = self._coord_to_notation(direct_jump_x, direct_jump_y)
                self._record_move(self._current_turn, "movimento", notation)
                self.switch_turn()
                return

            if opp_dx == 0:
                diagonal_targets = [(opp_x - 1, opp_y), (opp_x + 1, opp_y)]
            else:
                diagonal_targets = [(opp_x, opp_y - 1), (opp_x, opp_y + 1)]

            if pivot_blocked and (target_x, target_y) in diagonal_targets:
                raise MovementError("Salto non permesso: muro blocca il passaggio.")

            if (target_x, target_y) in diagonal_targets:
                direct_blocked = (
                    not is_within_bounds(direct_jump_x, direct_jump_y)
                    or is_cell_occupied(direct_jump_x, direct_jump_y)
                    or segment_blocked(opp_x, opp_y, direct_jump_x, direct_jump_y)
                )
                if not direct_blocked:
                    raise MovementError(
                        "Movimento non valido: puoi muoverti solo di una cella."
                    )
                if is_cell_occupied(target_x, target_y):
                    raise MovementError("Movimento non valido: cella occupata.")
                if segment_blocked(opp_x, opp_y, target_x, target_y):
                    raise MovementError("Salto non permesso: muro blocca il passaggio.")
                current_player.set_position(Cell(target_x, target_y))
                notation = self._coord_to_notation(target_x, target_y)
                self._record_move(self._current_turn, "movimento", notation)
                self.switch_turn()
                return

        # Controllo standard per mosse di un singolo passo
        if not ((abs(dx) == 1 and dy == 0) or (dx == 0 and abs(dy) == 1)):
            raise MovementError(
                "Movimento non valido: puoi muoverti solo di una cella."
            )

        for wall in self._board.get_walls():
            wx, wy = wall.get_start_cell().get_coords()
            w_orient = wall.get_orientation().lower()

            if (
                dy != 0
                and w_orient == "h"
                and wy == max(curr_y, target_y)
                and (wx == curr_x or wx == curr_x - 1)
            ):
                raise MovementError("Un muro orizzontale blocca il passaggio.")

            if (
                dx != 0
                and w_orient == "v"
                and wx == max(curr_x, target_x)
                and (wy == curr_y or wy == curr_y + 1)
            ):
                raise MovementError("Un muro verticale blocca il passaggio.")

        # Se la casella d'arrivo di 1 passo è comunque occupata da qualcuno, impedisci la mossa  # noqa: E501
        if is_cell_occupied(target_x, target_y):
            raise MovementError("Movimento non valido: cella occupata.")

        current_player.set_position(Cell(target_x, target_y))
        notation = self._coord_to_notation(target_x, target_y)
        self._record_move(self._current_turn, "movimento", notation)
        self.switch_turn()

    # ------------------------------------------------------------------
    # Vittoria
    # ------------------------------------------------------------------

    def check_victory(self) -> bool:
        """Controlla se uno dei giocatori ha raggiunto la vittoria."""
        for player in self._players:
            if player._id not in self._active_player_ids:
                continue

            cx, cy = player.get_position().get_coords()
            target = player._target_row

            # target < 0  → obiettivo su colonna (modalità 4P, P1 e P2)
            # target >= 1 → obiettivo su riga    (modalità 2P e P3/P4)
            reached = (cx == -target) if target < 0 else (cy == target)

            if reached:
                self._winner = player._id
                return True

        return False

    # ------------------------------------------------------------------
    # Stato partita
    # ------------------------------------------------------------------

    def get_game_state(self) -> dict:
        """Ritorna lo stato attuale del gioco per permetterne il rendering."""
        # Filtra i giocatori includendo nella stampa SOLO quelli ancora attivi
        active_players_for_render = [
            p for p in self._players if p._id in self._active_player_ids
        ]

        return {
            "board": self._board,
            "players": active_players_for_render,  # Mostra solo chi è in gioco
            "active_player_ids": list(self._active_player_ids),
            "current_player_id": self._current_turn,
            "winner": self._winner,
            "num_players": self._num_players,
        }

    # ------------------------------------------------------------------
    # Abbandono
    # ------------------------------------------------------------------

    def resign_current_player(self) -> int:
        """Gestisce la resa del giocatore corrente.

        In modalità 2P: l'avversario vince immediatamente.
        In modalità 4P: il giocatore viene rimosso dal ciclo, la partita continua.
        Restituisce l'ID del vincitore (2P) o 0 se la partita prosegue (4P).
        """
        if self._winner is not None:
            return self._winner

        resigning_id = self._current_turn

        if self._num_players == 2:
            self._winner = 2 if resigning_id == 1 else 1
            return self._winner

        # Modalità 4P: rimuovi il giocatore dal ciclo
        if resigning_id in self._active_player_ids:
            idx = self._active_player_ids.index(resigning_id)
            self._active_player_ids.remove(resigning_id)
            # Aggiusta l'indice per non saltare il prossimo giocatore
            if self._active_player_ids:
                self._current_turn_index = idx % len(self._active_player_ids)

        # Se rimane un solo giocatore, vince lui
        if len(self._active_player_ids) == 1:
            self._winner = self._active_player_ids[0]
            return self._winner

        return 0  # Partita ancora in corso

    # ------------------------------------------------------------------
    # Muri
    # ------------------------------------------------------------------

    def place_wall(self, coords: tuple[int, int, str]) -> None:
        """Piazza un muro per il giocatore corrente."""
        if self._winner is not None:
            raise TurnError("La partita è già finita.")

        if len(coords) != 3 or coords[2] not in ["h", "v"]:
            raise InvalidCommandError("Orientamento non valido. Usa 'h' o 'v'.")

        current_player = self._get_player_by_id(self._current_turn)
        current_player.use_wall()

        start_cell = Cell(coords[0], coords[1])
        new_wall = Wall(start_cell=start_cell, orientation=coords[2])

        try:
            active_players = [
                p for p in self._players if p._id in self._active_player_ids
            ]  # noqa: E501
            self._board.add_wall(new_wall, active_players)
        except Exception as e:
            current_player._walls_count += 1
            raise e

        notation = self._coord_to_notation(coords[0], coords[1], coords[2])
        self._record_move(self._current_turn, "muro", notation)
        self.switch_turn()

    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------

    def reset(self, num_players: int | None = None) -> None:
        """Resetta il gioco per una nuova partita.

        Args:
            num_players (int | None): Se fornito, cambia la modalità di gioco.

        """
        if num_players is not None:
            self._num_players = num_players
        self._board = Board()
        self._move_history = []
        self._setup_players()
