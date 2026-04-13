from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, OptionList, Button
from textual.widgets.option_list import Option
from textual.containers import Vertical
from editor.engine import EditorEngine


class EditorMenuScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("Editor", classes="title")
        yield OptionList(id="subject-list")
        yield Vertical(
            Button("Add Subject", id="add-subject", variant="primary"),
            Button("Back", id="back", variant="default"),
            classes="button-row",
        )

    def on_mount(self) -> None:
        self._refresh_subjects()

    def _refresh_subjects(self) -> None:
        subjects = list(self.app.graph.subjects.keys())
        options = [Option(s, s) for s in subjects]
        self.query_one("#subject-list", OptionList).clear_options()
        for opt in options:
            self.query_one("#subject-list", OptionList).add_option(opt)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        value = event.option.id
        from screens.subject_list import SubjectListScreen
        self.app.push_screen(SubjectListScreen(value))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-subject":
            from screens.dialogs import InputDialog
            def on_submit(name: str):
                if name.strip():
                    engine = EditorEngine(self.app.graph)
                    self.app.graph = engine.add_subject(name.strip())
                    self._refresh_subjects()
            self.app.push_screen(InputDialog("New subject name:", on_submit))
        elif event.button.id == "back":
            self.app.pop_screen()