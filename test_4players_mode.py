"""Test per verificare la modalità 4 giocatori di Quoridor."""

import pytest

from src.MODEL.Cell import Cell
from src.MODEL.QuoridorGame import QuoridorGame


class Test4PlayersMode:
    """Test per la modalità 4 giocatori."""

    def test_init_default_2_players(self):
        """Test che l'inizializzazione di default crea 2 giocatori."""
        game = QuoridorGame()
        assert game._game_mode == 2
        assert len(game._players) == 2
        assert game._active_players == [1, 2]
        assert game._current_turn == 1

    def test_set_game_mode_4_players(self):
        """Test che set_game_mode(4) crea 4 giocatori."""
        game = QuoridorGame()
        game.set_game_mode(4)

        assert game._game_mode == 4
        assert len(game._players) == 4
        assert game._active_players == [1, 2, 3, 4]

        # Verifica posizioni iniziali
        assert game._players[0].get_position().get_coords() == (5, 1)  # P1
        assert game._players[1].get_position().get_coords() == (5, 9)  # P2
        assert game._players[2].get_position().get_coords() == (1, 5)  # P3
        assert game._players[3].get_position().get_coords() == (9, 5)  # P4

    def test_walls_distribution_2_players(self):
        """Test che in 2 giocatori gli muri iniziali sono 10."""
        game = QuoridorGame()
        assert game._players[0].get_walls_count() == 10
        assert game._players[1].get_walls_count() == 10

    def test_walls_distribution_4_players(self):
        """Test che in 4 giocatori gli muri iniziali sono 5 a testa."""
        game = QuoridorGame()
        game.set_game_mode(4)

        for player in game._players:
            assert player.get_walls_count() == 5

    def test_target_rows_4_players(self):
        """Test che i target rows sono corretti per 4 giocatori."""
        game = QuoridorGame()
        game.set_game_mode(4)

        # P1 e P2 hanno target row positivo (verticale)
        assert game._players[0]._target_row == 9
        assert game._players[1]._target_row == 1

        # P3 e P4 hanno target row negativo (significa colonna)
        assert game._players[2]._target_row == -9  # colonna 9
        assert game._players[3]._target_row == -1  # colonna 1

    def test_switch_turn_4_players(self):
        """Test che i turni ciclano correttamente tra 4 giocatori."""
        game = QuoridorGame()
        game.set_game_mode(4)

        assert game._current_turn == 1
        game.switch_turn()
        assert game._current_turn == 2
        game.switch_turn()
        assert game._current_turn == 3
        game.switch_turn()
        assert game._current_turn == 4
        game.switch_turn()
        assert game._current_turn == 1  # Torna a 1

    def test_check_victory_p1_p2_row_target(self):
        """Test che P1 e P2 vincono raggiungendo le righe target."""
        game = QuoridorGame()
        game.set_game_mode(4)

        # P1 raggiunge riga 9
        game._players[0].set_position(Cell(5, 9))
        assert game.check_victory() is True
        assert game._winner == 1

    def test_check_victory_p3_p4_col_target(self):
        """Test che P3 e P4 vincono raggiungendo le colonne target."""
        game = QuoridorGame()
        game.set_game_mode(4)

        # Resetta e testa P3 (target colonna 9)
        game._winner = None
        game._players[2].set_position(Cell(9, 5))
        assert game.check_victory() is True
        assert game._winner == 3

    def test_resign_2_players_immediate_winner(self):
        """Test che in 2 giocatori l'abbandono assegna vittoria immediata."""
        game = QuoridorGame()
        winner = game.resign_current_player()

        assert game._winner == 2  # P1 abbandona, P2 vince
        assert winner == 2

    def test_resign_4_players_removes_from_cycle(self):
        """Test che in 4 giocatori l'abbandono rimuove dal ciclo."""
        game = QuoridorGame()
        game.set_game_mode(4)

        # P1 abbandona
        winner = game.resign_current_player()

        assert winner == -1  # Nessun vincitore, partita continua
        assert game._current_turn == 2
        assert game._active_players == [2, 3, 4]

    def test_resign_4_players_last_one_wins(self):
        """Test che quando rimane 1 giocatore, lui vince."""
        game = QuoridorGame()
        game.set_game_mode(4)

        # Rimuovi 3 giocatori
        game._active_players = [1, 2, 3, 4]
        game._current_turn = 1

        # P1 abbandona
        game.resign_current_player()
        assert game._active_players == [2, 3, 4]

        game._current_turn = 2
        # P2 abbandona
        game.resign_current_player()
        assert game._active_players == [3, 4]

        game._current_turn = 3
        # P3 abbandona
        game.resign_current_player()
        assert game._winner == 4  # P4 vince!

    def test_move_with_multiple_adjacent_opponents(self):
        """Test movimento quando ci sono molteplici avversari adiacenti."""
        game = QuoridorGame()
        game.set_game_mode(4)

        # Posiziona P2, P3, P4 adiacenti a P1
        game._players[0].set_position(Cell(5, 5))
        game._players[1].set_position(Cell(5, 6))  # Sud di P1
        game._players[2].set_position(Cell(4, 5))  # Ovest di P1
        game._players[3].set_position(Cell(6, 5))  # Est di P1

        game._current_turn = 1

        # P1 deve riuscire a muoversi solo saltando su uno di loro
        # Se prova a muoversi verso P2, dovrebbe saltare
        game.move_player((5, 7))  # Salta su P2

        assert game._players[0].get_position().get_coords() == (5, 7)
        assert game._current_turn == 2

    def test_get_game_state_includes_4_player_info(self):
        """Test che get_game_state include le informazioni per 4 giocatori."""
        game = QuoridorGame()
        game.set_game_mode(4)

        state = game.get_game_state()

        assert state["game_mode"] == 4
        assert state["active_players"] == [1, 2, 3, 4]
        assert len(state["players"]) == 4

    def test_reset_returns_to_2_players(self):
        """Test che reset() ritorna a 2 giocatori di default."""
        game = QuoridorGame()
        game.set_game_mode(4)
        assert len(game._players) == 4

        game.reset()

        assert game._game_mode == 2
        assert len(game._players) == 2
        assert game._active_players == [1, 2]

    def test_invalid_game_mode(self):
        """Test che impostare una modalità invalida genera errore."""
        game = QuoridorGame()

        with pytest.raises(ValueError, match="La modalità di gioco deve essere"):
            game.set_game_mode(3)

        with pytest.raises(ValueError, match="La modalità di gioco deve essere"):
            game.set_game_mode(5)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
