"""Modulo per il calcolo dei percorsi e la validazione dei blocchi di gioco."""

from collections import deque


class PathFinder:
    """Classe di utility per verificare la raggiungibilità degli obiettivi."""

    @staticmethod
    def _is_move_blocked(
        c1: tuple[int, int], c2: tuple[int, int], walls: list
    ) -> bool:
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

        # Direzioni base: (dx, dy) -> Nord, Sud, Est, Ovest
        directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]

        for dx, dy in directions:
            nxt = (cx + dx, cy + dy)

            # Controlla confini plancia e se il passaggio diretto è bloccato
            if not (1 <= nxt[0] <= 9 and 1 <= nxt[1] <= 9):
                continue
            if PathFinder._is_move_blocked(curr, nxt, walls):
                continue

            # Se la cella adiacente è occupata dall'avversario, gestisci il salto
            if nxt == opp:
                jump = (ox + dx, oy + dy)

                # Verifica se il salto dritto è dentro la plancia e non bloccato
                if (
                    1 <= jump[0] <= 9
                    and 1 <= jump[1] <= 9
                    and not PathFinder._is_move_blocked(opp, jump, walls)
                ):
                    valid_moves.append(jump)
                else:
                    # Risolto SIM108: Usato l'operatore ternario in riga singola
                    diag_sides = (
                        [(-1, 0), (1, 0)]
                        if dx == 0
                        else [(0, -1), (0, 1)]
                    )

                    for sx, sy in diag_sides:
                        diag = (ox + sx, oy + sy)
                        # Risolto SIM102: Uniti i due if nidificati con 'and'
                        if (
                            1 <= diag[0] <= 9
                            and 1 <= diag[1] <= 9
                            and not PathFinder._is_move_blocked(
                                opp, diag, walls
                            )
                        ):
                            valid_moves.append(diag)
            else:
                # Cella libera, movimento standard superato
                valid_moves.append(nxt)

        return valid_moves

    @staticmethod
    def has_path(
        start: tuple[int, int],
        opponent: tuple[int, int],
        target_row: int,
        walls: list,
    ) -> bool:
        """Verifica tramite BFS se esiste un percorso fino alla riga obiettivo."""
        queue = deque([start])
        visited = {start}

        while queue:
            curr = queue.popleft()
            _, cy = curr

            if cy == target_row:
                return True

            # Ottiene i vicini calcolando dinamicamente salti e diagonali
            neighbors = PathFinder._get_valid_neighbors(curr, opponent, walls)

            for nxt in neighbors:
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)

        return False