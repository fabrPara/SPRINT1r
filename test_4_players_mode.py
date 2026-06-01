"""Test per verificare la modalità 4 giocatori."""

import pytest

from src.MODEL.Cell import Cell
from src.MODEL.QuoridorGame import QuoridorGame


def test_game_mode_initialization():
    """Test che la partita inizi in modalità 2 giocatori."""
    game = QuoridorGame()
    assert game._game_mode == 2
    assert len(game._players) == 2
    assert game._active_players == [1, 2]


def test_set_game_mode_4_players():
    """Test che la modalità 4 giocatori crei i giocatori necessari."""
    game = QuoridorGame()
    game.set_game_mode(4)

    assert game._game_mode == 4
    assert len(game._players) == 4
    assert game._active_players == [1, 2, 3, 4]

    # Verifica le posizioni di partenza
    assert game._players[0].get_position().get_coords() == (5, 1)  # P1: Nord
    assert game._players[1].get_position().get_coords() == (5, 9)  # P2: Sud
    assert game._players[2].get_position().get_coords() == (1, 5)  # P3: Ovest
    assert game._players[3].get_position().get_coords() == (9, 5)  # P4: Est


def test_walls_count_4_players():
    """Test che i muri siano ridotti a 5 per giocatore in modalità 4."""
    game = QuoridorGame()

    # In modalità 2: 10 muri
    assert game._players[0].get_walls_count() == 10
    assert game._players[1].get_walls_count() == 10

    # Cambia a modalità 4
    game.set_game_mode(4)

    # Tutti i giocatori devono avere 5 muri
    assert game._players[0].get_walls_count() == 5
    assert game._players[1].get_walls_count() == 5
    assert game._players[2].get_walls_count() == 5
    assert game._players[3].get_walls_count() == 5


def test_switch_turn_4_players():
    """Test che i turni si alternino correttamente tra 4 giocatori."""
    game = QuoridorGame()
    game.set_game_mode(4)

    # Sequenza di turni attesi
    expected_sequence = [1, 2, 3, 4, 1, 2, 3, 4]

    for expected_player in expected_sequence:
        assert game._current_turn == expected_player
        game.switch_turn()


def test_resign_2_players():
    """Test che in modalità 2 giocatori, l'abbandono determini un vincitore."""
    game = QuoridorGame()
    assert game._game_mode == 2

    # Il giocatore 1 abbandona
    winner = game.resign_current_player()

    # Il giocatore 2 deve vincere
    assert winner == 2
    assert game._winner == 2


def test_resign_4_players_removes_player():
    """Test che in modalità 4 giocatori, l'abbandono rimuova il giocatore dal ciclo."""
    game = QuoridorGame()
    game.set_game_mode(4)

    # Il giocatore 1 abbandona
    winner = game.resign_current_player()

    # Nessun vincitore ancora (ritorna -1)
    assert winner == -1
    assert game._winner is None

    # Il giocatore 1 non deve essere più attivo
    assert 1 not in game._active_players
    assert game._active_players == [2, 3, 4]

    # Il turno deve passare al prossimo giocatore attivo (2)
    assert game._current_turn == 2


def test_resign_4_players_last_player_wins():
    """Test che l'ultimo giocatore rimasto vinca in modalità 4."""
    game = QuoridorGame()
    game.set_game_mode(4)

    # Tutti i giocatori tranne uno si ritirano
    game.resign_current_player()  # P1 abbandona
    assert game._active_players == [2, 3, 4]

    game.resign_current_player()  # P2 abbandona
    assert game._active_players == [3, 4]

    game.resign_current_player()  # P3 abbandona
    assert game._active_players == [4]
    assert game._winner == 4


def test_victory_conditions_4_players():
    """Test che i target di vittoria siano corretti in modalità 4."""
    game = QuoridorGame()
    game.set_game_mode(4)

    # P1 deve raggiungere y=9 (Nord -> Sud)
    assert game._players[0]._target_row == 9

    # P2 deve raggiungere y=1 (Sud -> Nord)
    assert game._players[1]._target_row == 1

    # P3 deve raggiungere x=9 (Ovest -> Est)
    assert game._players[2]._target_row == -9

    # P4 deve raggiungere x=1 (Est -> Ovest)
    assert game._players[3]._target_row == -1


def test_check_victory_p1_4players():
    """Test che P1 vinca quando raggiunge la riga 9 in modalità 4."""
    game = QuoridorGame()
    game.set_game_mode(4)

    # Muovi P1 alla riga 9
    game._players[0].set_position(Cell(5, 9))

    assert game.check_victory() is True
    assert game._winner == 1


def test_check_victory_p3_4players():
    """Test che P3 vinca quando raggiunge la colonna 9 in modalità 4."""
    game = QuoridorGame()
    game.set_game_mode(4)

    # Muovi P3 alla colonna 9
    game._players[2].set_position(Cell(9, 5))

    assert game.check_victory() is True
    assert game._winner == 3


def test_set_game_mode_4_no_duplicate_players():
    """Test che chiamare set_game_mode(4) due volte non duplichi i giocatori."""
    game = QuoridorGame()

    game.set_game_mode(4)
    assert len(game._players) == 4

    game.set_game_mode(4)
    assert len(game._players) == 4  # Non deve aumentare


def test_invalid_game_mode():
    """Test che modi di gioco non validi lancino un errore."""
    game = QuoridorGame()

    with pytest.raises(ValueError, match="La modalità di gioco deve essere 2 o 4"):
        game.set_game_mode(3)

    with pytest.raises(ValueError, match="La modalità di gioco deve essere 2 o 4"):
        game.set_game_mode(5)


def test_reset_game():
    """Test che il reset ripristini la modalità a 2 giocatori."""
    game = QuoridorGame()
    game.set_game_mode(4)

    assert game._game_mode == 4
    assert len(game._players) == 4

    game.reset()

    assert game._game_mode == 2
    assert len(game._players) == 2
    assert game._active_players == [1, 2]
    assert game._current_turn == 1
    assert game._winner is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
