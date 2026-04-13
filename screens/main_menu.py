from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Static
from textual.containers import Horizontal, Vertical


class MainMenuScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("📚 Estudar", classes="title")
        yield Static("Quiz & Study Tool", classes="info-text")
        yield Vertical(
            Button("Quiz", id="quiz", variant="primary"),
            Button("Editor", id="editor", variant="default"),
            Button("Quit", id="quit", variant="error"),
            classes="button-row",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quiz":
            from screens.quiz_menu import QuizMenuScreen
            self.app.push_screen(QuizMenuScreen())
        elif event.button.id == "editor":
            from screens.editor_menu import EditorMenuScreen
            EDITOR = EditorMenuScreen()
            self.app.push_screen(EDITOR)
        elif event.button.id == "quit":
            self.app.action_save_and_exit()
