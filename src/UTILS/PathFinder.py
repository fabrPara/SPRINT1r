"""Modulo per il calcolo dei percorsi e la validazione dei blocchi di gioco."""

from collections import deque  # noqa: F401


class PathFinder:
    """Classe di utility per verificare la raggiungibilità degli obiettivi."""

    @staticmethod
    def _is_move_blocked(c1: tuple[int, int], c2: tuple[int, int], walls: list) -> bool:
        """Verifica se il passaggio diretto tra due celle è bloccato da un muro."""
        x1, y1 = c1
        x2, y2 = c2

        for w in walls:
            wx = w.get_start_cell().x
            wy = w.get_start_cell().y
            wo = w.get_orientation().lower()

            # Movimento Verticale (Nord/Sud)
            if x1 == x2:
                ry = max(y1, y2)
                if wo == "h" and wy == ry and (wx == x1 or wx == x1 - 1):
                    return True

            # Movimento Orizzontale (Est/Ovest)
            elif y1 == y2:
                rx = max(x1, x2)
                if wo == "v" and wx == rx and (wy == y1 or wy == y1 + 1):
                    return True

        return False

    @staticmethod
    def _get_valid_neighbors(
        curr: tuple[int, int], opp: tuple[int, int], walls: list
    ) -> list[tuple[int, int]]:
        """Calcola i vicini legali considerando i muri e i salti del pedone."""
        cx, cy = curr
        ox, oy = opp
        valid_moves = []

        # Direzioni base: Nord, Sud, Est, Ovest
        directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]

        for dx, dy in directions:
            nxt = (cx + dx, cy + dy)

            # Controlla confini plancia e se il passaggio diretto è bloccato
            if not (1 <= nxt[0] <= 9 and 1 <= nxt[1] <= 9):
                continue
            if PathFinder._is_move_blocked(curr, nxt, walls):
                continue

            # Se la cella adiacente è occupata dall'avversario corrente, gestisci il salto  # noqa: E501
            if nxt == opp:
                jump = (ox + dx, oy + dy)

                # Verifica se il salto dritto è dentro la plancia e non bloccato dal muro dietro l'avversario  # noqa: E501
                if (
                    1 <= jump[0] <= 9
                    and 1 <= jump[1] <= 9
                    and not PathFinder._is_move_blocked(opp, jump, walls)
                ):
                    valid_moves.append(jump)
                else:
                    # Salto dritto bloccato da muro o fuori board: calcola i movimenti diagonali legali.  # noqa: E501
                    # Se ci muovevamo in verticale (dx==0), le deviazioni sono a destra/sinistra [(-1, 0), (1, 0)]  # noqa: E501
                    # Se in orizzontale, le deviazioni sono sopra/sotto [(0, -1), (0, 1)]  # noqa: E501
                    diag_sides = [(-1, 0), (1, 0)] if dx == 0 else [(0, -1), (0, 1)]

                    for sx, sy in diag_sides:
                        # La cella laterale rispetto all'avversario
                        diag = (ox + sx, oy + sy)

                        if 1 <= diag[0] <= 9 and 1 <= diag[1] <= 9:  # noqa: SIM102
                            # IMPORTANTE: Il muro taglia il percorso se si trova tra la cella dell'avversario (ox, oy)  # noqa: E501
                            # e la destinazione diagonale finale (diag). Essendo adiacenti di 1 passo, _is_move_blocked ora funziona.  # noqa: E501
                            if not PathFinder._is_move_blocked(opp, diag, walls):
                                valid_moves.append(diag)
            else:
                # Cella libera, movimento standard superato
                valid_moves.append(nxt)

        return valid_moves

    @staticmethod
    def has_path(
        start: tuple[int, int],
        other_players_positions: list[tuple[int, int]],
        target_row: int,
        walls: list,
    ) -> bool:
        """Verifica tramite BFS se esiste un percorso fino all'obiettivo."""
        queue = deque([start])
        visited = {start}

        while queue:
            curr = queue.popleft()
            cx, cy = curr

            # Controllo obiettivo (Asse X se target < 0, Asse Y se target >= 1)
            if target_row < 0:
                if cx == -target_row:
                    return True
            else:
                if cy == target_row:
                    return True

            # --- GESTIONE OTTIMIZZATA DEI VICINI ---
            neighbors = []

            # Direzioni base per trovare eventuali avversari adiacenti a 'curr'
            adjacent_directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
            found_adjacent_opponent = False

            for dx, dy in adjacent_directions:
                adj_cell = (cx + dx, cy + dy)

                # Se c'è un avversario adiacente, usiamo lui per calcolare il salto (dritto o diagonale)  # noqa: E501
                if adj_cell in other_players_positions:
                    found_adjacent_opponent = True
                    moves = PathFinder._get_valid_neighbors(curr, adj_cell, walls)
                    for m in moves:
                        # Evita che il salto termini sopra un altro giocatore presente nella scacchiera  # noqa: E501
                        if m not in other_players_positions:
                            neighbors.append(m)

            # Se non ci sono avversari attorno a questa cella, calcola i movimenti standard liberi.  # noqa: E501
            # Passiamo (0, 0) come avversario fittizio in modo che _get_valid_neighbors generi solo mosse standard pulite.  # noqa: E501
            if not found_adjacent_opponent:
                neighbors = PathFinder._get_valid_neighbors(curr, (0, 0), walls)
            # ---------------------------------------

            for nxt in neighbors:
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)

        return False
