# Estudar - Quiz and Study Tool

A terminal-based quiz and study application with a Textual User Interface (TUI).

## Features

- **Quiz Mode**: Test your knowledge with questions from various subjects
- **Editor Mode**: Create and edit your own quiz content
- **Textual TUI**: Built on the [Textual](https://textual.textualize.io/) framework
- **Keyboard-driven**: vim-like keybindings, clickable buttons, mouse support
- **Auto-save**: Changes are automatically saved on exit

## Installation

```bash
pip install -r requirements.txt
```

Dependencies:
- `textual` - TUI framework (v0.44+)
- `commentjson` - JSON with comments support
- `wcwidth` - Wide character width calculation

## Usage

```bash
python main.py
```

## Controls

| Key | Action |
|-----|--------|
| `Tab` | Next widget |
| `Shift+Tab` | Previous widget |
| `Enter` | Select / Confirm |
| `ESC` | Back / Cancel |
| `Ctrl+Q` | Save and Quit |

Mouse is fully supported - click buttons, select options, scroll lists.

## Data Structure

The application stores data in `base.json` with the following structure:

```json
{
  "Subject": {
    "Topic": {
      "nodes": {"text": id},
      "edges": [[source_id, target_id]]
    }
  }
}
```

## Known Limitations

- Exhaustive quiz mode is a stub (not fully implemented)
- No automated test suite
- Spaced-repetition scheduling not implemented

## Architecture

```
main.py
 └─ textual_app.QuizApp (Textual App)
      ├─ screens/MainMenuScreen
      ├─ screens/QuizMenuScreen
      ├─ screens/QuizPlayScreen
      ├─ screens/EditorMenuScreen
      ├─ screens/SubjectListScreen
      ├─ screens/TopicListScreen
      ├─ screens/NodeTableScreen
      ├─ screens/NodeDetailScreen
      └─ screens/dialogs (InputDialog, ConfirmDialog, BatchConnectDialog)
quiz.engine.QuizEngine   (pure logic, no UI)
editor.engine.EditorEngine (pure logic, no UI)
storage.json_store.JsonStore
model.graph.Graph / Subject / Topic / Node / Edge
util.text.semacento, cls, wrap, cor
```