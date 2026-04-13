# Spec: Estudar - Educational Quiz & Editor System (TUI)

## Overview
A terminal-based educational tool for studying through quiz games and managing question banks. Built in Python with a **custom Textual User Interface (TUI)** — no external `questionary` dependency. Uses a JSON-based knowledge graph for content.

---

## Architecture

### Core Modules
| File | Purpose |
|------|---------|
| `main.py` | Entry point – launches the TUI application |
| `tui/app.py` | Main TUI application class (screen manager, key bindings) |
| `tui/screens/` | Individual screens (menu, quiz, editor, dialogs) |
| `tui/widgets/` | Reusable widgets (lists, forms, tables, popups) |
| `quiz/engine.py` | Quiz logic: question selection, scoring, validation |
| `editor/engine.py` | Editor logic: CRUD operations on the knowledge graph |
| `storage/json_store.py` | Load / save `base.json` (commentjson) |
| `model/graph.py` | In-memory graph representation (subjects → topics → nodes/edges) |
| `util/text.py` | `semacento()`, `cls()`, `wrap()`, color helpers |
| `util/keys.py` | Key constants & input helpers |

### Data Structure (`base.json`)
Hierarchical knowledge graph:
```
Subject (Matéria)
  └── Topic (Assunto)
        ├── nodes: { "concept_text": numeric_id }
        └── edges: [ [source_id, target_id] ]   # directed: question → answer
```

**Example**: `"classificação": 1  →  "Processo de organização...": 2` stored as edge `[2, 1]`.

---

## Features

### 1. TUI Framework (custom, no questionary)
- **Screen stack** – push/pop screens, ESC to go back
- **Keyboard-driven** – vim-like bindings (j/k, Enter, ESC, / for search)
- **Widgets**: `MenuList`, `InputBox`, `ConfirmDialog`, `TableView`, `CheckboxList`
- **Responsive layout** – adapts to terminal width/height via `os.get_terminal_size()`
- **Colors** – per-subject ANSI themes (defined in `util/text.py:cor()`)

### 2. Quiz Game (`quiz/engine.py`)
- **Modes**: All content / By Subject / By Topic / Exhaustive (visit all nodes)
- **Gameplay loop**:
  1. Pick random edge in scope → source node = question
  2. Collect all target nodes = valid answers
  3. Render question screen → user types answer → `semacento()` fuzzy match
  4. Show result (green/red) → prompt “Continue? (Enter) / Quit (q)”
- **Scoring**: round counter + correct answers
- **Navigation**: `ESC` returns to main menu at any prompt

### 3. Editor (`editor/engine.py`)
Full CRUD for the knowledge graph, all via TUI screens:
- **Subjects**: List → Add / Rename / Delete
- **Topics** (inside subject): List → Add / Rename / Delete
- **Nodes** (inside topic): TableView → Add / Edit / Delete / View connections
- **Edges**: From node detail → Connect (P=question, R=answer) / Remove edges / Batch connect (CheckboxList)
- **Auto-save**: On screen pop (ESC) or explicit “Save & Quit”; also on Ctrl+C / unhandled exception

### 4. Persistence (`storage/json_store.py`)
- `load()` → parses `base.json` with `commentjson` (supports trailing commas, comments)
- `save(graph)` → writes pretty-printed UTF-8 JSON, atomic write (temp file + rename)

### 5. Utilities (`util/text.py`)
- `semacento(str) → str` – lower-case + strip accents for fuzzy matching
- `cls()` – cross-platform clear screen (fallback for raw TUI redraw)
- `wrap(text, width)` – word-wrap for description panels
- `cor(subject) → ANSI_CODE` – colour per subject

---

## Dependencies
```
commentjson >= 0.x      # JSON with comments
wcwidth    >= 0.x       # Unicode width for column alignment
# stdlib only otherwise: curses (or `blessed`/`rich` if preferred), json, os, sys, random, pathlib
```
> **No `questionary`, `prompt_toolkit`, or `lark-parser`.**  
> TUI built on `curses` (stdlib) or optionally `rich`/`textual` if you want higher-level widgets.

---

## Data Format Details

### Node
```json
"concept or question text": numeric_id
```
- IDs unique per topic; editor auto-suggests `max_id + 1`.

### Edge
```json
[source_id, target_id]
```
- Directed: source = question, target = valid answer.
- Multiple targets per source allowed (multiple correct answers).

---

## Usage

```bash
# Launch TUI (main menu)
python main.py

# Direct quiz (optional CLI flags later)
python -m quiz.engine --subject biologia --topic taxonomia

# Direct editor
python -m editor.engine
```

---

## Key Algorithms

### Question Selection (`quiz.engine.select_question`)
1. Filter edges by scope (subject/topic/all).
2. `random.choice(edges)` → `source_id`.
3. Resolve `source_id → question_text` via reverse node map.
4. Collect all `target_id` for that source → map to answer texts.

### Answer Validation (`quiz.engine.validate`)
```python
semacento(user_input) == semacento(valid_answer)
```
Case + accent insensitive.

### Graph Mutations (`editor.engine`)
- All mutations return new graph (immutable-style) → easy undo/redo later.
- Edge addition checks for duplicates before append.

---

## Extending

### Add New Subject / Topic / Node
Use the Editor TUI – no code changes.

### Add Colours
Edit `util/text.py:cor()` dict: `"nova matéria": "\033[1;35;40m"`.

### Swap TUI Backend
Replace `tui/app.py` + widgets with `textual` or `rich` – engine/storage layers unchanged.

---

## Known Limitations
- `Exhaustive` mode (visit all nodes) – not yet implemented.
- No spaced-repetition scheduling.
- Single `base.json` file (no import/export, no multi-file projects).
- No mouse support (keyboard-only).
- No automated tests yet.