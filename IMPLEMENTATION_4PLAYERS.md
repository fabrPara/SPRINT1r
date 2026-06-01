# Implementazione Modalità 4 Giocatori - Quoridor

## Sommario delle Modifiche

### 1. **Modello di Gioco (QuoridorGame.py)**

#### Inizializzazione
- Aggiunto attributo `_game_mode` (default: 2)
- Aggiunto attributo `_active_players` per tracciare i giocatori ancora in partita

#### Metodo `set_game_mode(mode: int)`
- Attiva la modalità 4 giocatori
- Crea i giocatori 3 e 4 con posizioni corrette:
  - **P1 (Nord)**: Posizione (5, 1), Target: riga 9
  - **P2 (Sud)**: Posizione (5, 9), Target: riga 1
  - **P3 (Ovest)**: Posizione (1, 5), Target: colonna 9 (rappresentato da -9)
  - **P4 (Est)**: Posizione (9, 5), Target: colonna 1 (rappresentato da -1)
- Riduce i muri da 10 a 5 per giocatore in modalità 4
- Evita duplicazioni se chiamato più volte (controlla `len(self._players) < 4`)

#### Metodo `switch_turn()`
- Alterna i turni tra i giocatori attivi utilizzando una lista ciclica
- Supporta sia 2 che 4 giocatori

#### Metodo `resign_current_player()`
**Modalità 2 giocatori:**
- L'avversario vince immediatamente

**Modalità 4 giocatori:**
- Il giocatore viene rimosso da `_active_players`
- Se rimane solo 1 giocatore, lui vince
- Altrimenti, il turno passa al prossimo giocatore attivo

#### Metodo `check_victory()`
- Supporta sia target di riga (P1, P2) che target di colonna (P3, P4)
- Target di colonna rappresentati come numeri negativi

#### Metodo `reset()`
- Ripristina la modalità a 2 giocatori
- Crea solo 2 giocatori

---

### 2. **Visualizzazione (CLIView.py)**

#### Metodo `_draw_stats()`
- Legge l'attributo `active_players` dallo stato del gioco
- Visualizza solo i giocatori ancora attivi
- Supporta la visualizzazione dei tempi per tutti i giocatori

#### Metodo `_draw_board()`
- Supporta la visualizzazione di 4 giocatori con colori distinti:
  - **P1**: Magenta
  - **P2**: Cyan
  - **P3**: Verde
  - **P4**: Giallo

#### Metodo `show_exit()`
- Gestisce correttamente il messaggio di abbandono:
  - In 2 giocatori: mostra il vincitore
  - In 4 giocatori: comunica che gli altri giocatori continuano

---

### 3. **Controller del Gioco (GameController.py)**

#### Metodo `_render_game()`
- Passa i `clocks` per tutti i giocatori (non solo 1 e 2)
- Supporta sia modalità con timer che senza

#### Metodo `_reset_game()`
- Legge la modalità di gioco dal prompt
- Inizializza i `clocks` per il numero corretto di giocatori
- Chiama `set_game_mode(4)` se richiesto

#### Metodo `start_game()`
- Legge la preferenza sulla modalità (2 o 4 giocatori) all'inizio
- Inizializza correttamente i clocks
- Gestisce il ciclo dei turni per più giocatori

#### Comando "4giocatori"
- Permette di attivare la modalità 4 giocatori durante una partita in corso
- Aggiorna i clocks di conseguenza

---

### 4. **View Base (BaseView.py)**
- `prompt_game_mode()`: Richiede all'utente quanti giocatori parteciperanno

---

## Regole Implementate

✅ **1. Posizioni di Partenza e Obiettivi**
- P1: (5, 1) → (5, 9) - Dal Nord al Sud
- P2: (5, 9) → (5, 1) - Dal Sud al Nord  
- P3: (1, 5) → (9, 5) - Da Ovest a Est
- P4: (9, 5) → (1, 5) - Da Est a Ovest

✅ **2. Attivazione Modalità 4 Giocatori**
- Tramite prompt all'inizio della partita: "Quanti giocatori parteciperanno?"
- Tramite comando durante la partita: "4giocatori"

✅ **3. Turni Ciclici**
- Sequenza: P1 → P2 → P3 → P4 → P1 ...
- Gestione automatica tramite `switch_turn()`

✅ **4. Bilanciamento Muri**
- 2 giocatori: 10 muri per giocatore
- 4 giocatori: 5 muri per giocatore

✅ **5. Gestione Abbandono**
- 2 giocatori: L'altro vince immediatamente
- 4 giocatori: Il giocatore viene rimosso dal ciclo, gli altri 3 continuano
- Se rimane 1 giocatore, lui vince

---

## Test

Tutti i test in `test_4_players_mode.py` passano con successo:

- ✅ Inizializzazione della partita (modalità 2)
- ✅ Attivazione modalità 4 giocatori
- ✅ Riduzione dei muri a 5 in modalità 4
- ✅ Alternarsi dei turni tra 4 giocatori
- ✅ Gestione dell'abbandono in modalità 2
- ✅ Rimozione del giocatore dal ciclo in modalità 4
- ✅ Vittoria dell'ultimo giocatore rimasto
- ✅ Condizioni di vittoria corrette (righe e colonne)
- ✅ Vittoria di P1 al raggiungimento della riga 9
- ✅ Vittoria di P3 al raggiungimento della colonna 9
- ✅ Prevenzione di duplicazioni di giocatori
- ✅ Gestione di modalità non valide
- ✅ Reset della partita a modalità 2

---

## Comandi Disponibili

### Durante una Partita

| Comando | Descrizione |
|---------|-------------|
| `<colonna><riga>` | Muove il giocatore (es: e5) |
| `<colonna><riga>h` | Piazza un muro orizzontale (es: e5h) |
| `<colonna><riga>v` | Piazza un muro verticale (es: e5v) |
| `abbandona` | Abbandona la partita |
| `4giocatori` | Attiva modalità 4 giocatori (se non già attiva) |
| `help` | Mostra le regole |
| `exit` | Esce dal gioco |

---

## Note di Implementazione

1. **Target Negativi**: In modalità 4 giocatori, i target di colonna (P3 e P4) sono rappresentati come numeri negativi per distinguerli dai target di riga.

2. **Active Players List**: La lista `_active_players` traccia i giocatori ancora in partita, permettendo l'abbandono dinamico senza interrompere il gioco.

3. **Clocks Dinamici**: I clocks vengono inizializzati dinamicamente in base al numero di giocatori.

4. **Backward Compatibility**: La modalità 2 giocatori è completamente preservata e funziona esattamente come prima.

---

## File Modificati

1. `src/MODEL/QuoridorGame.py` - Logica principale del gioco
2. `src/CONTROLLER/GameController.py` - Gestione input e flow del gioco
3. `src/VIEW/CLIView.py` - Rendering della visualizzazione
4. `test_4_players_mode.py` - Suite di test completa (nuovo file)

---

## Prossimi Passi (Opzionali)

- [ ] Aggiungere persistenza del game state (save/load)
- [ ] Implementare AI per giocatori bot
- [ ] Aggiungere statistiche di partita
- [ ] Migliorare la GUI (se si usa una libreria grafica)
- [ ] Aggiungere replay della partita
