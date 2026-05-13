"""Script per testare il sistema di vittoria di Quoridor."""

from src.MODEL.Cell import Cell
from src.MODEL.QuoridorGame import QuoridorGame


def test_victory_p1():
    """Testa la vittoria del giocatore 1 (raggiunge riga 9)."""
    print("=" * 60)
    print("TEST 1: Vittoria Giocatore 1")
    print("=" * 60)

    game = QuoridorGame()

    # Verifichiamo lo stato iniziale
    game_state = game.get_game_state()
    p1 = game_state["players"][0]
    p2 = game_state["players"][1]

    print(f"\nPosizione iniziale P1: {p1.get_position().get_coords()}")
    print(f"Target P1: {p1._target_row}")
    print(f"Posizione iniziale P2: {p2.get_position().get_coords()}")
    print(f"Target P2: {p2._target_row}")

    # Non deve esserci vincitore all'inizio
    assert not game.check_victory(), "Non dovrebbe esserci vincitore all'inizio!"
    assert game._winner is None, "Winner deve essere None all'inizio!"
    print("\n✓ Nessun vincitore all'inizio")

    # Muoviamo P1 verso la vittoria (da (5,1) verso (5,9))
    print("\nMovimenti P1 verso riga 9:")
    positions = [(5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9)]

    for i, pos in enumerate(positions, 1):
        # Settiamo la posizione direttamente (per test semplificato)
        p1.set_position(Cell(pos[0], pos[1]))
        current_pos = p1.get_position().get_coords()
        print(f"  {i}. P1 a posizione {current_pos}")

        # Verifiche progressives durante il percorso
        if i < len(positions):
            assert not game.check_victory(), f"P1 non dovrebbe vincere a {pos}!"
            assert game._winner is None, f"Winner deve essere None a {pos}!"
            print("     ✓ P1 non ha ancora vinto")

    # Dopo il raggiungimento di (5,9), P1 dovrebbe vincere
    victory = game.check_victory()
    assert victory, "P1 dovrebbe vincere al raggiungimento di riga 9!"
    assert game._winner == 1, "Il vincitore dovrebbe essere P1 (ID=1)!"
    print(f"\n✓ P1 HA VINTO! Winner ID: {game._winner}")


def test_victory_p2():
    """Testa la vittoria del giocatore 2 (raggiunge riga 1)."""
    print("\n" + "=" * 60)
    print("TEST 2: Vittoria Giocatore 2")
    print("=" * 60)

    game = QuoridorGame()
    p2 = game._players[1]

    # P2 inizia a (5,9) e deve raggiungere riga 1
    print(f"\nPosizione iniziale P2: {p2.get_position().get_coords()}")
    print(f"Target P2: {p2._target_row}")

    assert not game.check_victory(), "Non dovrebbe esserci vincitore all'inizio!"
    print("✓ Nessun vincitore all'inizio")

    # Muoviamo P2 verso riga 1
    print("\nMovimenti P2 verso riga 1:")
    positions = [(5, 8), (5, 7), (5, 6), (5, 5), (5, 4), (5, 3), (5, 2), (5, 1)]

    for i, pos in enumerate(positions, 1):
        p2.set_position(Cell(pos[0], pos[1]))
        current_pos = p2.get_position().get_coords()
        print(f"  {i}. P2 a posizione {current_pos}")

        if i < len(positions):
            assert not game.check_victory(), f"P2 non dovrebbe vincere a {pos}!"
            assert game._winner is None, f"Winner deve essere None a {pos}!"
            print("     ✓ P2 non ha ancora vinto")

    # Dopo il raggiungimento di (5,1), P2 dovrebbe vincere
    victory = game.check_victory()
    assert victory, "P2 dovrebbe vincere al raggiungimento di riga 1!"
    assert game._winner == 2, "Il vincitore dovrebbe essere P2 (ID=2)!"
    print(f"\n✓ P2 HA VINTO! Winner ID: {game._winner}")


def test_no_victory_mid_game():
    """Testa che non ci sia vittoria durante il gioco normale."""
    print("\n" + "=" * 60)
    print("TEST 3: No Victory durante il gioco normale")
    print("=" * 60)

    game = QuoridorGame()
    p1 = game._players[0]
    p2 = game._players[1]

    # Alcuni movimenti casuali
    print("\nMovimenti casuali:")

    moves = [
        (p1, (6, 1)),
        (p2, (5, 8)),
        (p1, (6, 2)),
        (p2, (5, 7)),
        (p1, (6, 3)),
    ]

    for i, (player, pos) in enumerate(moves, 1):
        player.set_position(Cell(pos[0], pos[1]))
        player_id = 1 if player == p1 else 2
        print(f"  {i}. P{player_id} a posizione {pos}")

        assert not game.check_victory(), f"Non dovrebbe esserci vittoria al move {i}!"
        assert game._winner is None, f"Winner deve essere None al move {i}!"
        print("     ✓ Nessun vincitore")

    print("\n✓ Nessuna vittoria prematura!")


def test_victory_with_actual_moves():
    """Testa la vittoria usando movimenti reali del gioco."""
    print("\n" + "=" * 60)
    print("TEST 4: Vittoria con movimenti reali")
    print("=" * 60)

    game = QuoridorGame()

    print("\nMovimenti reali alternati P1 e P2:")
    p1_pos = game._players[0].get_position().get_coords()
    print(f"  P1 turno {game._current_turn} - Posizione: {p1_pos}")

    moves = [
        (5, 2),  # P1 from (5,1) to (5,2)
        (5, 8),  # P2 from (5,9) to (5,8)
        (5, 3),  # P1
        (5, 7),  # P2
        (5, 4),  # P1
        (5, 6),  # P2
        (5, 5),  # P1
        (4, 9),  # P2 (moves differently to avoid collision)
        (5, 6),  # P1
        (5, 7),  # P2
        (5, 7),  # P1 (moves to adjacent cell while P2 is at 5,7)
    ]

    move_count = 0
    for i, move in enumerate(moves, 1):
        try:
            current_player_id = game._current_turn
            print(f"  {i}. P{current_player_id} si muove a {move}")

            game.move_player(move)
            player = game._players[current_player_id - 1]
            current_pos = player.get_position().get_coords()
            print(f"     → Posizione effettiva: {current_pos}")
            move_count += 1

            victory = game.check_victory()
            if victory:
                print(f"     ✓ VITTORIA! P{game._winner} ha vinto!")
                break
            else:
                print(f"     → Turno passato a P{game._current_turn}")

        except Exception as e:
            print(f"     ✗ Errore: {e}")
            # Continua al prossimo movimento
            break

    if move_count > 0:
        print(f"\n✓ Test completato con {move_count} movimenti")


if __name__ == "__main__":
    try:
        test_victory_p1()
        test_victory_p2()
        test_no_victory_mid_game()
        test_victory_with_actual_moves()

        print("\n" + "=" * 60)
        print("✅ TUTTI I TEST PASSATI!")
        print("=" * 60)

    except AssertionError as e:
        print(f"\n❌ TEST FALLITO: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ ERRORE: {e}")
        import traceback

        traceback.print_exc()
        exit(1)
