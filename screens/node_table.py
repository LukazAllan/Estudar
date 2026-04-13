from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, DataTable, Button
from textual.containers import Vertical


class NodeTableScreen(Screen):
    def __init__(self, subject_name: str, topic_name: str):
        super().__init__()
        self.subject_name = subject_name
        self.topic_name = topic_name

    def compose(self) -> ComposeResult:
        yield Static(id="table-title", classes="title")
        yield DataTable(id="node-table")
        yield Button("Back", id="back", variant="default")

    def on_mount(self) -> None:
        subject = self.app.graph.get_subject(self.subject_name)
        if not subject:
            self.app.pop_screen()
            return
        topic = subject.get_topic(self.topic_name)
        if not topic:
            self.app.pop_screen()
            return

        self.query_one("#table-title", Static).update(f"Nodes in {self.topic_name}")
        table = self.query_one("#node-table", DataTable)
        table.clear(columns=True)
        table.add_columns("Node", "ID")

        for text, nid in topic.nodes.items():
            table.add_row(text, str(nid))

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        row = event.row
        node_text = row.cells[0]
        from screens.node_detail import NodeDetailScreen
        self.app.push_screen(NodeDetailScreen(self.subject_name, self.topic_name, node_text))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()