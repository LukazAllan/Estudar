# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-04-13

### Added

- **Textual TUI**: Replaced the `questionary`-based CLI with a full Textual TUI application (`textual_app.py`) with multiple screens.
- **Graph domain model** (`model/graph.py`): Immutable, frozen dataclass-based model with `Graph`, `Subject`, `Topic`, `Node`, and `Edge` entities and pure transformation methods.
- **Editor engine** (`editor/engine.py`): Business logic layer for CRUD on subjects, topics, nodes, and edges (including batch connect).
- **Quiz engine** (`quiz/engine.py`): Question selection and answer validation logic extracted from the old `perguntas.py`.
- **Screens package** (`screens/`):
  - `main_menu.py` — Main navigation screen.
  - `subject_list.py` — Subject browsing and management.
  - `topic_list.py` — Topic browsing and management.
  - `node_detail.py` — Node detail view with edge navigation.
  - `node_table.py` — Node listing table.
  - `editor_menu.py` — Editor actions menu.
  - `quiz_menu.py` — Quiz mode selection (all / by subject / by topic).
  - `quiz_play.py` — In-terminal quiz gameplay screen.
  - `dialogs.py` — Reusable modal dialogs (input, confirm, batch connect, remove edge).
- **Utility modules**:
  - `util/text.py` — Accent-stripping and text helpers (migrated from `canivete.py`).
  - `util/keys.py` — Key binding helpers.
- **JSON storage layer** (`storage/json_store.py`): Load/save the knowledge base to `base.json`.
- **App stylesheet** (`app.tcss`): Textual CSS for the TUI layout and theming.
- **Project metadata** (`pyproject.toml`): Python package config with `textual`, `commentjson`, and `wcwidth` dependencies.
- **`requirements.txt`**: Pinned runtime dependencies.
- **`README.md`**, **`spec.md`**, **`this.md`**: Project documentation and specification.

### Changed

- **`main.py`**: Entry point now launches the Textual `QuizApp` instead of the old `questionary` menu loop.
- **`base.json`**: Schema unchanged but data restructured/reformatted for the new model layer.

### Removed

- **`editor.py`**: Replaced by `editor/engine.py` + Textual screens.
- **`perguntas.py`**: Replaced by `quiz/engine.py` + `screens/quiz_menu.py` + `screens/quiz_play.py`.
- **`canivete.py`**: Replaced by `util/text.py`.
