from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, OptionList, Button
from textual.widgets.option_list import Option
from textual.containers import Vertical
from editor.engine import EditorEngine


class TopicListScreen(Screen):
    def __init__(self, subject_name: str, topic_name: str):
        super().__init__()
        self.subject_name = subject_name
        self.topic_name = topic_name
        self.engine = None

    def compose(self) -> ComposeResult:
        yield Static(id="topic-info", classes="title")
        yield OptionList(
            Option("View Nodes", "view_nodes"),
            Option("Add Node", "add_node"),
            Option("Rename Topic", "rename_topic"),
            Option("Delete Topic", "delete_topic"),
            Option("Back", "back"),
            id="topic-options",
        )

    def on_mount(self) -> None:
        self.engine = EditorEngine(self.app.graph)
        subject = self.app.graph.get_subject(self.subject_name)
        if not subject:
            self.app.pop_screen()
            return
        topic = subject.get_topic(self.topic_name)
        if not topic:
            self.app.pop_screen()
            return
        self.query_one("#topic-info", Static).update(
            f"Topic: {self.topic_name} ({len(topic.nodes)} nodes)"
        )

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        value = event.option.id
        if value == "view_nodes":
            from screens.node_table import NodeTableScreen
            self.app.push_screen(NodeTableScreen(self.subject_name, self.topic_name))
        elif value == "add_node":
            from screens.dialogs import InputDialog
            def on_submit(name: str):
                if name.strip():
                    self.app.graph = self.engine.add_node(self.subject_name, self.topic_name, name.strip())
            self.app.push_screen(InputDialog("New node name:", on_submit))
        elif value == "rename_topic":
            from screens.dialogs import InputDialog
            def on_rename(name: str):
                if name.strip() and name != self.topic_name:
                    self.app.graph = self.engine.rename_topic(self.subject_name, self.topic_name, name.strip())
                    self.topic_name = name.strip()
                    self.query_one("#topic-info", Static).update(f"Topic: {self.topic_name}")
            self.app.push_screen(InputDialog(f"Rename '{self.topic_name}' to:", on_rename))
        elif value == "delete_topic":
            from screens.dialogs import ConfirmDialog
            def on_confirm():
                self.app.graph = self.engine.delete_topic(self.subject_name, self.topic_name)
                self.app.pop_screen()
            self.app.push_screen(ConfirmDialog(f"Delete topic '{self.topic_name}'?", on_confirm))
        elif value == "back":
            self.app.pop_screen()