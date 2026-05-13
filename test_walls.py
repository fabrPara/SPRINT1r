"""Test script per verificare la logica dei muri."""

from src.MODEL.Cell import Cell
from src.MODEL.Exception import MovementError
from src.MODEL.QuoridorGame import QuoridorGame


def test_horizontal_wall_block():
    """Test: muro orizzontale deve bloccare movimento verticale."""
    print("\n" + "="*60)
    print("TEST: MURO ORIZZONTALE BLOCCA MOVIMENTO VERTICALE")
    print("="*60)
    
    game = QuoridorGame()
    
    # Posiziona P1 in e3 e P2 in e5 (fuori dal cammino)
    game._players[0].set_position(Cell(5, 3))  # P1 at e3
    game._players[1].set_position(Cell(5, 5))  # P2 at e5
    
    # Piazza un muro orizzontale in e4-f4 (cioè start cell at e4)
    # Questo muro dovrebbe bloccare il passaggio dalla riga 3 alla riga 4
    game.place_wall((5, 4, 'h'))
    
    print(f"P1 posizione: {game._players[0].get_position().get_coords()}")
    print("Muro H in (5, 4) - (6, 4)")
    print("P1 tenta di muoversi da (5, 3) a (5, 4)...")
    
    try:
        game._players[0].set_position(Cell(5, 3))  # Reset
        game._current_turn = 1
        game.move_player((5, 4))
        print("❌ ERRORE: P1 ha saltato il muro!")
    except MovementError as e:
        print(f"✓ Bloccato: {e}")


def test_vertical_wall_block():
    """Test: muro verticale deve bloccare movimento orizzontale."""
    print("\n" + "="*60)
    print("TEST: MURO VERTICALE BLOCCA MOVIMENTO ORIZZONTALE")
    print("="*60)
    
    game = QuoridorGame()
    
    # Posiziona P1 in d4 e P2 fuori dal cammino
    game._players[0].set_position(Cell(4, 4))  # P1 at d4
    game._players[1].set_position(Cell(8, 8))  # P2 at h8
    
    # Piazza un muro verticale in e4-e5 (cioè start cell at e4)
    # Questo muro dovrebbe bloccare il passaggio dalla colonna d alla colonna e
    game.place_wall((5, 4, 'v'))
    
    print(f"P1 posizione: {game._players[0].get_position().get_coords()}")
    print("Muro V in (5, 4) - (5, 5)")
    print("P1 tenta di muoversi da (4, 4) a (5, 4)...")
    
    try:
        game._players[0].set_position(Cell(4, 4))  # Reset
        game._current_turn = 1
        game.move_player((5, 4))
        print("❌ ERRORE: P1 ha saltato il muro!")
    except MovementError as e:
        print(f"✓ Bloccato: {e}")


def test_wall_coordinates():
    """Analizza le coordinate del muro."""
    print("\n" + "="*60)
    print("TEST: ANALISI COORDINATE MURO")
    print("="*60)
    
    game = QuoridorGame()
    
    # Piazza un muro
    game._players[0].set_position(Cell(5, 1))
    game._players[1].set_position(Cell(8, 9))
    
    game.place_wall((5, 4, 'h'))
    
    for wall in game._board.get_walls():
        start = wall.get_start_cell()
        orient = wall.get_orientation()
        print(f"Muro {orient.upper()} start_cell: {start.get_coords()}")


if __name__ == "__main__":
    test_wall_coordinates()
    test_horizontal_wall_block()
    test_vertical_wall_block()
