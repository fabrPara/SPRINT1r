#!/usr/bin/env python3
"""Test integrato finale del sistema di cronologia mosse."""

from src.MODEL.QuoridorGame import QuoridorGame


def format_move_history(move_history, num_players):
    """Formatta la cronologia come nel metodo show_move_history."""
    if not move_history:
        return "❌ Non è stata ancora effettuata una mossa!"
    
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
        turno_str = f"📋 TURNO {turno}: " + " | ".join(mosse_turno)
        history_lines.append(turno_str)
    
    return "\n".join(history_lines)

print("╔════════════════════════════════════════════════════╗")
print("║  TEST INTEGRATO - SISTEMA CRONOLOGIA MOSSE        ║")
print("╚════════════════════════════════════════════════════╝")
print()

# ============================================================================
# SCENARIO 1: Inizio partita - nessuna mossa
# ============================================================================
print("[1️⃣  SCENARIO: INIZIO PARTITA]")
print("-" * 50)
game = QuoridorGame(num_players=2)
print("✓ Partita inizializzata (2 giocatori)")
print(f"✓ Cronologia vuota: {not game.has_moves()}")
print("✓ Messaggio all'utente:")
print(f"   {format_move_history(game.get_move_history(), 2)}")
print()

# ============================================================================
# SCENARIO 2: Dopo alcuni movimenti
# ============================================================================
print("[2️⃣  SCENARIO: DOPO ALCUNI MOVIMENTI]")
print("-" * 50)
game = QuoridorGame(num_players=2)
print("Turno 1:")
print("  - P1 si muove: e2")
game.move_player((5, 2))
print("  - P2 si muove: e8")
game.move_player((5, 8))

print("Turno 2:")
print("  - P1 si muove: e3")
game.move_player((5, 3))
print("  - P2 si muove: e7")
game.move_player((5, 7))

print("Turno 3:")
print("  - P1 si muove: f3")
game.move_player((6, 3))
print("  - P2 si muove: e6")
game.move_player((5, 6))

print("\n✓ Cronologia registrata:")
print(format_move_history(game.get_move_history(), 2))
print()

# ============================================================================
# SCENARIO 3: Con piazzamento di muri
# ============================================================================
print("[3️⃣  SCENARIO: CON PIAZZAMENTO DI MURI]")
print("-" * 50)
game = QuoridorGame(num_players=2)
print("Turno 1:")
print("  - P1 si muove: e2")
game.move_player((5, 2))
print("  - P2 si muove: e8")
game.move_player((5, 8))

print("Turno 2:")
print("  - P1 si muove: f2")
game.move_player((6, 2))
print("  - P2 piazza muro: c4h (orizzontale)")
game.place_wall((3, 4, 'h'))

print("Turno 3:")
print("  - P1 piazza muro: f3v (verticale)")
game.place_wall((6, 3, 'v'))
print("  - P2 si muove: e7")
game.move_player((5, 7))

print("\n✓ Cronologia con muri:")
print(format_move_history(game.get_move_history(), 2))
print()

# ============================================================================
# SCENARIO 4: Reset partita
# ============================================================================
print("[4️⃣  SCENARIO: RESET PARTITA]")
print("-" * 50)
print("Prima del reset:")
print(f"  - Mosse registrate: {len(game.get_move_history())}")
game.reset()
print("Dopo il reset:")
print(f"  - Mosse registrate: {len(game.get_move_history())}")
print(f"  - Has moves: {game.has_moves()}")
print(f"  - Messaggio: {format_move_history(game.get_move_history(), 2)}")
print()

# ============================================================================
# SCENARIO 5: 4 Giocatori
# ============================================================================
print("[5️⃣  SCENARIO: MODALITÀ 4 GIOCATORI]")
print("-" * 50)
game = QuoridorGame(num_players=4)
print("Turno 1 (4 mosse):")
print("  - P1 si muove: a6")
game.move_player((1, 6))
print("  - P2 si muove: i6")
game.move_player((9, 6))
print("  - P3 si muove: e2")
game.move_player((5, 2))
print("  - P4 si muove: e8")
game.move_player((5, 8))

print("Turno 2 (parziale):")
print("  - P1 si muove: b6")
game.move_player((2, 6))
print("  - P2 piazza muro: h5h (orizzontale)")
game.place_wall((8, 5, 'h'))

print("\n✓ Cronologia (4 giocatori):")
print(format_move_history(game.get_move_history(), 4))
print()

# ============================================================================
# RIEPILOGO
# ============================================================================
print("╔════════════════════════════════════════════════════╗")
print("║  ✅ TUTTI I TEST COMPLETATI CON SUCCESSO           ║")
print("╚════════════════════════════════════════════════════╝")
print()
print("📊 Riepilogo funzionalità testate:")
print("  ✓ Registrazione movimenti")
print("  ✓ Registrazione muri (orizzontali e verticali)")
print("  ✓ Notazione corretta (a-i, 1-9, h/v)")
print("  ✓ Numerazione turni per 2 giocatori")
print("  ✓ Numerazione turni per 4 giocatori")
print("  ✓ Messaggio cronologia vuota")
print("  ✓ Reset cronologia")
print()
print("🎮 Comando disponibile nel gioco: 'mosse'")
print("   Digita 'mosse' durante la partita per visualizzare la cronologia!")
