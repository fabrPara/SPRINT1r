#!/usr/bin/env python3
"""Test del sistema di cronologia mosse."""

from src.MODEL.QuoridorGame import QuoridorGame

# Crea un gioco
game = QuoridorGame(num_players=2)

print("=== TEST CRONOLOGIA MOSSE ===\n")

# Verifica iniziale - no mosse
print(f"1. Mosse registrate all'inizio: {len(game.get_move_history())}")
print(f"   Has moves: {game.has_moves()}")
print()

# Muovi P1
print("2. P1 si muove da e1 a e2...")
game.move_player((5, 2))  # e2
print(f"   Mosse registrate: {len(game.get_move_history())}")
print(f"   Cronologia: {game.get_move_history()}")
print()

# Muovi P2
print("3. P2 si muove da e9 a e8...")
game.move_player((5, 8))  # e8
print(f"   Mosse registrate: {len(game.get_move_history())}")
print(f"   Cronologia: {game.get_move_history()}")
print()

# Piazza un muro P1
print("4. P1 piazza un muro a e3 orizzontale...")
game.move_player((5, 3))  # e3
game.place_wall((5, 3, 'h'))  # e3h
print(f"   Mosse registrate: {len(game.get_move_history())}")
print(f"   Cronologia: {game.get_move_history()}")
print()

# Test reset
print("5. Reset del gioco...")
game.reset(num_players=2)
print(f"   Mosse dopo reset: {len(game.get_move_history())}")
print(f"   Has moves: {game.has_moves()}")
print()

print("=== TEST COMPLETATO ===")
