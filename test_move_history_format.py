#!/usr/bin/env python3
"""Test del sistema di cronologia mosse con formato di output."""

from src.MODEL.QuoridorGame import QuoridorGame


def format_move_history(move_history, num_players):
    """Formatta la cronologia mosse come mostrata nel show_move_history."""
    if not move_history:
        return "Non è stata ancora effettuata una mossa!"
    
    mosse_per_turno = {}
    
    for mossa_index, mossa in enumerate(move_history):
        player_id = mossa["player_id"]
        notation = mossa["notation"]
        
        turno_numero = (mossa_index // num_players) + 1
        
        if turno_numero not in mosse_per_turno:
            mosse_per_turno[turno_numero] = []
        
        mosse_per_turno[turno_numero].append(f"P{player_id} → {notation}")
    
    history_lines = []
    for turno in sorted(mosse_per_turno.keys()):
        mosse_turno = mosse_per_turno[turno]
        turno_str = f"TURNO {turno} " + " ".join(mosse_turno)
        history_lines.append(turno_str)
    
    return "\n".join(history_lines)

# Test 1: Cronologia vuota
print("=== TEST 1: CRONOLOGIA VUOTA ===")
game = QuoridorGame(num_players=2)
print(format_move_history(game.get_move_history(), 2))
print()

# Test 2: Alcuni movimenti
print("=== TEST 2: ALCUNI MOVIMENTI (2P) ===")
game = QuoridorGame(num_players=2)
game.move_player((5, 2))  # P1: e2
game.move_player((5, 8))  # P2: e8
game.move_player((5, 3))  # P1: e3
game.move_player((5, 7))  # P2: e7
print(format_move_history(game.get_move_history(), 2))
print()

# Test 3: Con muri (2P)
print("=== TEST 3: CON MOVIMENTI E MURI (2P) ===")
game = QuoridorGame(num_players=2)
game.move_player((5, 2))  # P1: e2
game.move_player((5, 8))  # P2: e8
game.move_player((6, 2))  # P1: f2
game.place_wall((3, 4, 'h'))  # P2: c4h
game.move_player((6, 3))  # P1: f3
game.place_wall((6, 8, 'v'))  # P2: f8v
print(format_move_history(game.get_move_history(), 2))
print()

# Test 4: 4 Giocatori
print("=== TEST 4: MODALITÀ 4 GIOCATORI ===")
game = QuoridorGame(num_players=4)
game.move_player((1, 6))  # P1: a6
game.move_player((9, 6))  # P2: i6
game.move_player((5, 2))  # P3: e2
game.move_player((5, 8))  # P4: e8
game.move_player((2, 6))  # P1: b6
game.move_player((8, 6))  # P2: h6
game.move_player((5, 3))  # P3: e3
game.place_wall((5, 3, 'h'))  # P4: e3h
print(format_move_history(game.get_move_history(), 4))
print()

print("=== TEST COMPLETATI ===")
