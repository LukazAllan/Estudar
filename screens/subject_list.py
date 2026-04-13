from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, OptionList, Button
from textual.widgets.option_list import Option
from textual.containers import Vertical
from editor.engine import EditorEngine


class SubjectListScreen(Screen):
    def __init__(self, subject_name: str):
        super().__init__()
        self.subject_name = subject_name
        self.engine = None

    def compose(self) -> ComposeResult:
        yield Static(id="subject-name", classes="title")
        yield OptionList(id="topic-list")
        yield Vertical(
            Button("Add Topic", id="add-topic", variant="primary"),
            Button("Rename Subject", id="rename-subject", variant="default"),
            Button("Delete Subject", id="delete-subject", variant="error"),
            Button("Back", id="back", variant="default"),
            classes="button-row",
        )

    def on_mount(self) -> None:
        self.engine = EditorEngine(self.app.graph)
        self._refresh_topics()

    def _refresh_topics(self) -> None:
        subject = self.app.graph.get_subject(self.subject_name)
        if not subject:
            self.app.pop_screen()
            return
        self.query_one("#subject-name", Static).update(f"Subject: {self.subject_name}")
        topics = list(subject.topics.keys())
        options = [Option(t, t) for t in topics]
        self.query_one("#topic-list", OptionList).clear_options()
        for opt in options:
            self.query_one("#topic-list", OptionList).add_option(opt)

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        from screens.topic_list import TopicListScreen
        self.app.push_screen(TopicListScreen(self.subject_name, event.option.id))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add-topic":
            from screens.dialogs import InputDialog
            def on_submit(name: str):
                if name.strip():
                    self.app.graph = self.engine.add_topic(self.subject_name, name.strip())
                    self._refresh_topics()
            self.app.push_screen(InputDialog("New topic name:", on_submit))
        elif event.button.id == "rename-subject":
            from screens.dialogs import InputDialog
            def on_rename(name: str):
                if name.strip() and name != self.subject_name:
                    self.app.graph = self.engine.rename_subject(self.subject_name, name.strip())
                    self.subject_name = name.strip()
                    self._refresh_topics()
            self.app.push_screen(InputDialog(f"Rename '{self.subject_name}' to:", on_rename))
        elif event.button.id == "delete-subject":
            from screens.dialogs import ConfirmDialog
            def on_confirm():
                self.app.graph = self.engine.delete_subject(self.subject_name)
                self.app.pop_screen()
            self.app.push_screen(ConfirmDialog(f"Delete '{self.subject_name}'?", on_confirm))
        elif event.button.id == "back":
            self.app.pop_screen()