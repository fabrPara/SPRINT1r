# Quoridor - Documentazione Progetto SPRINT1r

## 📋 Indice
- [Introduzione](#introduzione)
- [Tutorial: Primi Passi](#tutorial-primi-passi)
- [Guide Pratiche](#guide-pratiche)
- [Riferimenti Tecnici](#riferimenti-tecnici)
- [Architettura e Design](#architettura-e-design)
- [Gestione del Progetto](#gestione-del-progetto)

---

## 🎯 Introduzione

### Cos'è Quoridor?
**Quoridor** è un gioco da tavolo strategico a turni per 2 giocatori implementato in Python.

**Obiettivo**: Raggiungere il lato opposto del tabellone prima dell'avversario, posizionando muri strategicamente per bloccare i percorsi.

**Tecnologie Stack**:
- Python ≥ 3.11.9
- Rich (formattazione CLI)
- Typer (parsing comandi)
- Pytest (testing)

### Struttura del Progetto (MVC)
```
src/
├── MODEL/          → Logica di gioco pura
├── VIEW/           → Interfaccia utente (CLI)
└── CONTROLLER/     → Coordinamento Model-View
```

---

## 🚀 Tutorial: Primi Passi

### 1. Preparazione Ambiente

#### Prerequisiti
- Python 3.11.9 o superiore
- pip o uv (gestire dipendenze)

#### Installazione Dipendenze
```bash
# Clona il repository
git clone <repository-url>
cd SPRINT1r

# Installa dipendenze
pip install -e .

# Installa dipendenze di sviluppo (opzionale)
pip install -e ".[dev]"
```

### 2. Eseguire il Gioco

#### Avvio Applicazione
```bash
python -m src.main
```

**Output atteso**: Tabellone 9×9 con:
- 🔴 Giocatore 1 (Rosso, fondo) all'inizio in posizione (5,1)
- 🔵 Giocatore 2 (Blu, alto) all'inizio in posizione (5,9)

#### Comandi di Gioco (da implementare)
| Comando | Sintassi | Descrizione |
|---------|----------|-------------|
| Movimento | `move A5` | Sposta giocatore nella cella (A=colonna, 5=riga) |
| Muro Orizzontale | `wall B3H` | Posiziona muro orizzontale in B3 |
| Muro Verticale | `wall C4V` | Posiziona muro verticale in C4 |
| Aiuto | `help` | Mostra comandi disponibili |
| Esci | `quit` o `exit` | Termina la partita |

### 3. Esempio di Giocata

```
------- TURNO 1 -------
Turno di: P1
Muri P1: 10 | Muri P2: 10

Giocatore 1 inserisce: move E5
Risultato: Giocatore 1 si sposta verso il basso

------- TURNO 2 -------
Turno di: P2
Giocatore 2 inserisce: wall E6H
Risultato: Posizionato muro orizzontale bloccando il percorso
```

---

## 📚 Guide Pratiche

### Guida 1: Comprendere il Movimento

**Problema**: Come funzionano i movimenti validi?

**Soluzione**:
1. Un giocatore può muoversi **solo di 1 cella** per turno
2. Il movimento è consentito in **4 direzioni** (Nord, Sud, Est, Ovest)
3. **Non è possibile** muoversi attraverso i muri
4. Se bloccati, non possono muoversi

**Codice rilevante**: [src/MODEL/QuoridorGame.py](../../src/MODEL/QuoridorGame.py#L35)

### Guida 2: Posizionare i Muri

**Problema**: Quando e come posizionare i muri in modo strategico?

**Soluzione**:
1. Ogni giocatore inizia con **10 muri**
2. I muri occupano **2 celle** (orizzontali o verticali)
3. I muri **non possono sovrapporsi**
4. I muri **non possono impedire definitivamente il percorso verso la vittoria**
5. Scegli muri che bloccano il percorso più breve dell'avversario

**Strategia consigliata**:
- Turni iniziali: difenditi posizionando muri di protezione
- Turni centrali: blocca l'avanzamento dell'avversario
- Turni finali: crea labirinti per guadagnare posizione

**Codice rilevante**: [src/MODEL/Board.py](../../src/MODEL/Board.py) e [src/MODEL/Wall.py](../../src/MODEL/Wall.py)

### Guida 3: Gestire le Eccezioni di Gioco

**Problema**: Cosa accade quando un comando non è valido?

**Soluzione**: Il sistema lancia eccezioni specifiche:

| Eccezione | Causa | Gestione |
|-----------|-------|----------|
| `MovementError` | Movimento non valido/percorso bloccato | Riprova con altra cella |
| `WallPlacementError` | Muro sovrapposto o fuori limite | Riprova con altra posizione |
| `WallDepletionError` | Muri esauriti | Puoi solo muoverti |
| `TurnError` | Azione fuori turno | Aspetta il tuo turno |
| `InvalidCommandError` | Comando sconosciuto | Digita `help` per sintassi |

**Codice rilevante**: [src/MODEL/Exception.py](../../src/MODEL/Exception.py)

### Guida 4: Estendere il Gioco (per Sviluppatori)

#### Aggiungere una Nuova Feature: Modalità 4 Giocatori

**Passi**:

1. **Modifica [src/MODEL/QuoridorGame.py](../../src/MODEL/QuoridorGame.py)**:
   ```python
   def __init__(self, num_players: int = 2):
       if num_players not in [2, 4]:
           raise ValueError("Solo 2 o 4 giocatori supportati")
       self._players = self._init_players(num_players)
   ```

2. **Aggiorna [src/VIEW/CLIView.py](../../src/VIEW/CLIView.py)**:
   - Adatta la visualizzazione per 4 giocatori
   - Aumenta dimensioni tabellone se necessario

3. **Modifica [src/CONTROLLER/GameController.py](../../src/CONTROLLER/GameController.py)**:
   - Gestisci turni in rotazione (1→2→3→4→1)

4. **Aggiungi Test** in [tests/test_main.py](../../tests/test_main.py):
   ```python
   def test_4_players_game():
       game = QuoridorGame(num_players=4)
       assert len(game._players) == 4
   ```

5. **Aggiorna Documentazione**:
   - Aggiungi il nuovo comando nei comandi supportati
   - Descrivi limitazioni e comportamenti attesi

---

## 🔧 Riferimenti Tecnici

### Struttura MODEL

#### QuoridorGame.py
Classe principale che gestisce la logica di gioco.

**Metodi Pubblici**:
| Metodo | Parametri | Ritorno | Descrizione |
|--------|-----------|---------|-------------|
| `move_player(coords)` | `tuple[int, int]` | `None` | Sposta giocatore corrente |
| `switch_turn()` | — | `None` | Passa turno al giocatore successivo |
| `check_victory()` | — | `bool` | Verifica se c'è un vincitore |
| `get_game_state()` | — | `dict` | Ritorna stato attuale |

#### Board.py
Rappresenta il tabellone 9×9 e gestisce celle e muri.

**Metodi Pubblici**:
| Metodo | Parametri | Ritorno | Descrizione |
|--------|-----------|---------|-------------|
| `add_wall(wall)` | `Wall` | `None` | Aggiunge muro validato |
| `get_walls()` | — | `list[Wall]` | Ritorna tutti i muri |

#### Player.py
Rappresenta un giocatore.

**Attributi**:
- `_id` (int): ID giocatore (1 o 2)
- `_position` (Cell): Posizione attuale
- `_walls_count` (int): Muri rimanenti
- `_target_row` (int): Riga di vittoria

**Metodi Pubblici**:
| Metodo | Ritorno | Descrizione |
|--------|---------|-------------|
| `get_position()` | `Cell` | Posizione corrente |
| `get_walls_count()` | `int` | Muri rimanenti |
| `use_wall()` | `None` | Decrementa contatore muri |

#### Cell.py
Rappresenta una singola cella del tabellone.

**Attributi**:
- `x` (int): Coordinata colonna (1-9)
- `y` (int): Coordinata riga (1-9)

#### Wall.py
Rappresenta un muro.

**Attributi**:
- `_start_cell` (Cell): Cella di inizio
- `_orientation` (str): `"H"` (orizzontale) o `"V"` (verticale)

#### Exception.py
Gerarchia di eccezioni personalizzate.

```
QuoridorError (base)
├── MovementError
├── WallPlacementError
├── WallDepletionError
├── TurnError
└── InvalidCommandError
```

### Struttura VIEW

#### BaseView.py
Interfaccia astratta (contratto) per tutte le viste.

#### CLIView.py
Implementazione concreta per interfaccia terminale.

**Metodi**:
| Metodo | Parametri | Descrizione |
|--------|-----------|-------------|
| `render(game_state)` | `dict` | Disegna stato del gioco |
| `get_input()` | — | Legge comando utente |

### Struttura CONTROLLER

#### GameController.py
Coordinatore tra Model e View.

**Responsabilità**:
- Parsare input utente (conversione `E5` → `(5, 5)`)
- Validare comandi
- Gestire il loop principale
- Catturare e gestire eccezioni

**Metodi Chiave**:
| Metodo | Descrizione |
|--------|-------------|
| `start_game()` | Avvia loop principale |
| `_parse_coords(coords_str)` | Converte `E5` o `E5H` in coordinate numeriche |
| `_setup_commands()` | Registra handler per comandi |

---

## 🏗️ Architettura e Design

### Decisioni Architetturali (ADR)

#### ADR-1: Perché Pattern MVC?

**Contesto**: Necessità di separare logica di gioco, presentazione e input.

**Decisione**: Adottare pattern MVC (Model-View-Controller).

**Vantaggi**:
- ✅ **Separazione responsabilità**: MODEL (logica), VIEW (grafica), CONTROLLER (coordinamento)
- ✅ **Testabilità**: Logica pura testabile senza UI
- ✅ **Estensibilità**: Facile aggiungere altre VIEW (Web, GUI)
- ✅ **Manutenibilità**: Moduli indipendenti

**Svantaggi**:
- ❌ Complessità iniziale (piccoli progetti potrebbero non necessitarla)
- ❌ Comunicazione Model↔View aggiuntiva

#### ADR-2: Perché Rich per CLI?

**Contesto**: Necessità di formattare output terminale con colori e tabelle.

**Decisione**: Usare libreria `rich`.

**Vantaggi**:
- ✅ Tabelle, colori, stili facilmente
- ✅ Comunità ampia
- ✅ Poche dipendenze

#### ADR-3: Perché Typer per Parsing Comandi?

**Contesto**: Parsing comandi CLI (move, wall, quit, etc.).

**Decisione**: Usare libreria `typer` con regex fallback.

**Vantaggi**:
- ✅ Generazione help automatica
- ✅ Type hints nativi
- ✅ Parser robusto

### Flusso di Esecuzione

```
┌─────────────────────────────────────────┐
│  1. main() inizializza MVC              │
│     - MODEL: QuoridorGame()             │
│     - VIEW: CLIView()                   │
│     - CONTROLLER: GameController()      │
└────────────┬────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│  2. controller.start_game() Loop Principale
│                                         │
│  ┌─ Mostra stato (render)              │
│  │                                     │
│  ├─ Legge input utente                │
│  │                                     │
│  ├─ Valida comando (regex + typer)   │
│  │                                     │
│  ├─ Chiama MODEL (move_player/etc)   │
│  │                                     │
│  ├─ Gestisce eccezioni                │
│  │                                     │
│  └─ Cambia turno                      │
│                                         │
│  Ripeti fino a check_victory() = True  │
└─────────────────────────────────────────┘
             ↓
┌─────────────────────────────────────────┐
│  3. Annuncia vincitore e termina       │
└─────────────────────────────────────────┘
```

### Diagramma Classi (Semplificato)

```
┌──────────────────────────────────────────────────┐
│              CONTROLLER                          │
│  ┌─────────────────────────────────────────────┐ │
│  │ GameController                              │ │
│  │ • start_game()                              │ │
│  │ • _parse_coords(coords_str)                 │ │
│  │ • _setup_commands()                         │ │
│  └─────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
           ↓                          ↓
    ┌─────────────┐          ┌─────────────────┐
    │    MODEL    │          │      VIEW       │
    ├─────────────┤          ├─────────────────┤
    │QuoridorGame │          │  BaseView       │
    │ • Board     │          │   ↑             │
    │ • Players[] │          │   │             │
    │ • Turns     │          │ CLIView         │
    │ • Winner    │          │ • render()      │
    └─────────────┘          │ • _draw_board() │
           ↓                 └─────────────────┘
    ┌─────────────┐
    │   Board     │
    ├─────────────┤
    │ • Cells[]   │
    │ • Walls[]   │
    └─────────────┘
           ↓
    ┌─────────────────────────┐
    │ Cell │ Wall │ Player    │
    └─────────────────────────┘
```

### Flow di Validazione Comandi

```
Input Utente: "move E5"
       ↓
┌──────────────────────────────────┐
│ Regex Parsing (GameController)   │  ✓ Formato valido? E5, E5H
└──────────────┬───────────────────┘
               ↓
        ┌──────────────────────────────────┐
        │ Conversione Coordinate           │  E→5, A→1 (COL_MAP)
        │ E5 → (col=5, row=5)              │
        └──────────┬───────────────────────┘
                   ↓
        ┌──────────────────────────────────┐
        │ Validazione MODEL (QuoridorGame) │  ✓ Mossa valida?
        │ move_player(5, 5)                │  ✓ Casella adiacente?
        └──────────┬───────────────────────┘
                   ↓
        ┌──────────────────────────────────┐
        │ Aggiornamento Stato              │  Posizione + Turno
        └──────────┬───────────────────────┘
                   ↓
        ┌──────────────────────────────────┐
        │ Re-render (CLIView)              │  Visualizza nuovo stato
        └──────────────────────────────────┘

Se errore → Cattura eccezione → Mostra messaggio → Richiedi input
```

---

## 📊 Gestione del Progetto

### Configurazione del Progetto

#### pyproject.toml
```toml
[project]
name = "app"
version = "0.1.0"
description = "Implementazione del gioco Quoridor a linea di comando"
requires-python = ">=3.11.9"
dependencies = [
    "rich>=13.9.4",      # Formattazione CLI
    "typer>=0.25.1",     # Parsing comandi
]
```

**Dipendenze di Sviluppo**:
- `pytest>=8.3.5` — Framework testing
- `pytest-cov>=6.0.0` — Coverage report
- `ruff>=0.11.0` — Linter & formatter

### Lint & Code Quality

#### Ruff Configuration
- **Selezionati**: E (pycodestyle), D (pydocstyle), F (Pyflakes), UP (pyupgrade), B (bugbear), SIM (simplify), I (isort)
- **Ignorati**: D203, D213, D100, D102, D107

**Eseguire Linting**:
```bash
ruff check src/
ruff format src/
```

### Testing

#### Eseguire Test
```bash
# Tutti i test
pytest

# Con coverage
pytest --cov=src

# Specifico file
pytest tests/test_main.py -v
```

#### Test Attuali
- [tests/test_main.py](../../tests/test_main.py): Test di base per logica di gioco

**Cobertura Target**: ≥ 80% per logica core

### Comandi Utili

```bash
# Installare dipendenze
pip install -e ".[dev]"

# Eseguire gioco
python -m src.main

# Linting
ruff check src/ && ruff format src/

# Testing
pytest --cov=src

# Pulire file temporanei
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

---

## 📝 Manutenibilità: Documentation as Code

### Principi Adottati

1. **Documentazione Vicina al Codice**
   - Docstring nei metodi (Python standard)
   - Commenti nelle sezioni complesse
   - README/Report.md nello stesso repository

2. **Automatizzazione**
   - Linting con `ruff`
   - Coverage tracking con `pytest-cov`
   - Type hints con annotazioni Python

3. **Revisione**
   - Documentazione parte della PR
   - Se codice cambia → documentazione cambia
   - Linter verifica docstring (ruff D*)

### Template Docstring (Google Style)

```python
def move_player(self, coords: tuple[int, int]) -> None:
    """Muove il giocatore corrente nella cella specificata.
    
    Valida il movimento secondo le regole di Quoridor.
    Il giocatore può muoversi solo di 1 cella adiacente,
    a meno che non sia bloccato da muri.
    
    Args:
        coords (tuple[int, int]): Coordinate destinazione (x, y).
        
    Raises:
        MovementError: Se il movimento non è consentito.
        
    Example:
        >>> game = QuoridorGame()
        >>> game.move_player((5, 2))
        >>> game.switch_turn()
    """
```

### Checklist Aggiornamento Documentazione

- [ ] Modifica codice implementata
- [ ] Docstring aggiornati/nuovi
- [ ] Type hints aggiunti
- [ ] Test scritti/aggiornati
- [ ] Report.md aggiornato se feature principale
- [ ] Ruff linting passato (`ruff check`)
- [ ] CHANGELOG.md aggiornato

---

## 🚧 Work in Progress & TODO

### Priorità Alta (Sprint 1)
- [x] Struttura MVC implementata
- [x] Logica movimento giocatori
- [ ] **Logica muri**: Validazione e posizionamento
- [ ] **Sistema di vittoria**: Controllo raggiungimento target
- [ ] **CLI completamente funzionante**: Tutti comandi

### Priorità Media (Sprint 2+)
...(work in progress!!)

---

## 🔗 Riferimenti Rapidi

| Elemento | Percorso |
|----------|----------|
| Logica Principale | [src/MODEL/QuoridorGame.py](../../src/MODEL/QuoridorGame.py) |
| Vista CLI | [src/VIEW/CLIView.py](../../src/VIEW/CLIView.py) |
| Controller | [src/CONTROLLER/GameController.py](../../src/CONTROLLER/GameController.py) |
| Test | [tests/test_main.py](../../tests/test_main.py) |
| Configurazione | [pyproject.toml](../../pyproject.toml) |
| Entrypoint | [src/main.py](../../src/main.py) |

---

## 📞 Note Finali

**Per Sviluppatori**: Segui il pattern MVC. Se aggiungi feature:
1. Logica → MODEL
2. Visualizzazione → VIEW
3. Coordinamento → CONTROLLER

**Per Stakeholder**: Il progetto è in Sprint 1. Logica core implementata, features avanzate in roadmap Sprint 2.

**Per Mantenitori**: Mantieni test ≥80% coverage, ruff zero warning, docstring completi.

---

**Ultima revisione**: SPRINT 1r | **Versione Documento**: 1.0 | **Data**: 2026-05-10
