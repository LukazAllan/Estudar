# Spec: Estudar - Educational Quiz & Editor System

## Overview
A terminal-based educational tool for studying through quiz games and managing question banks. Built in Python with a JSON-based knowledge graph structure.

---

## Architecture

### Core Modules
| File | Purpose |
|------|---------|
| `main.py` | Entry point - main menu dispatcher |
| `perguntas.py` | Quiz game engine |
| `editor.py` | Visual editor for question bank |
| `canivete.py` | Utility functions (text normalization, colors, I/O helpers) |

### Data Structure (`base.json`)
Hierarchical knowledge graph:
```
Subject (Matéria)
  └── Topic (Assunto)
        ├── nodes: { "concept_text": numeric_id }
        └── edges: [ [source_id, target_id] ]  # directed: question → answer
```

**Example**: "classificação" (id:1) → "Processo de organização..." (id:2)

---

## Features

### Quiz Game (`perguntas.py`)
- **Modes**: All content / By Subject / By Topic / Exhaustive (visit all nodes)
- **Gameplay**: Random question from selected scope → user types answer → fuzzy match (accent-insensitive)
- **Scoring**: Tracks round & correct answers
- **Navigation**: Interactive menus via `questionary`

### Editor (`editor.py`)
Full CRUD for the knowledge graph:
- **Subjects**: Add / Rename / Delete / Navigate
- **Topics**: Add / Rename / Delete / Navigate  
- **Nodes**: Add / Edit / Delete / View connections
- **Edges**: Connect nodes (P=question, R=answer) / Remove edges / View connections
- **Batch connect**: Checkbox multi-select for linking one node to many
- **Auto-save**: On exit (Ctrl+C or menu) or error

### Utilities (`canivete.py`)
- `semacento()` - Remove accents + lowercase for fuzzy matching
- `cor()` - ANSI color codes per subject
- `cls()` - Cross-platform clear screen
- `rinput()` - Validated input loops
- `tit()` - Print formatted titles

---

## Dependencies
```
questionary  >= 2.1.1   # Interactive prompts
commentjson  >= 0.x     # JSON with comments support
lark-parser  >= 0.7.8   # (transitive)
wcwidth      >= 0.x     # Terminal width calculations
prompt-toolkit >= 3.x   # (transitive)
```

---

## Data Format Details

### Node
```json
"concept or question text": numeric_id
```
- IDs are unique per topic, auto-suggested as `max_id + 1`
- Both questions and answers are stored as nodes

### Edge
```json
[source_id, target_id]
```
- Directed: source = question, target = valid answer
- Multiple valid answers per question supported

---

## Usage

```bash
# Run quiz
python main.py
# → Option 2: Jogo de Perguntas

# Run editor
python main.py  
# → Option 1: Editor
# Or directly: python editor.py
```

---

## Key Algorithms

### Question Selection (`escolher_pergunta`)
1. Pick random topic (or filtered)
2. Pick random edge from topic's edges
3. Source node = question, collect all targets = valid answers
4. Map IDs back to text for display

### Answer Validation (`validar_pergunta`)
```python
semacento(user_input) == semacento(valid_answer)
```
Case + accent insensitive comparison.

---

## Extending

### Add New Subject
1. Editor → "Adicionar Matéria"
2. Editor → Navigate → "Adicionar Assunto"
3. Editor → "Adicionar Nó" for concepts
4. Editor → "Conectar Nó" to create Q→A edges

### Add Colors
Edit `canivete.py:cor()` dict with subject name → ANSI code.

---

## Known Limitations
- `to_all_nodes()` (exhaustive mode) - stub implementation
- No spaced repetition / scheduling
- Single JSON file (no multi-file / import-export)
- No web / GUI interface