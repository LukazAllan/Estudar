from typing import Callable
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Static, Input, Button, Checkbox, RadioSet, RadioButton, Label
from textual.containers import Vertical, Horizontal


class InputDialog(ModalScreen[str]):
    def __init__(self, prompt: str, callback: Callable[[str], None]):
        super().__init__()
        self.prompt = prompt
        self.callback = callback

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static(self.prompt, classes="dialog-title"),
            Input(id="dialog-input", placeholder="Type here..."),
            Horizontal(
                Button("Confirm", id="confirm", variant="primary"),
                Button("Cancel", id="cancel", variant="default"),
                classes="button-row",
            ),
            classes="dialog",
        )

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.callback(event.value.strip())
        self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            input_widget = self.query_one("#dialog-input", Input)
            self.callback(input_widget.value.strip())
        self.app.pop_screen()


class ConfirmDialog(ModalScreen[bool]):
    def __init__(self, message: str, on_confirm: Callable[[], None]):
        super().__init__()
        self.message = message
        self.on_confirm = on_confirm

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static(self.message, classes="dialog-title"),
            Horizontal(
                Button("Yes", id="yes", variant="primary"),
                Button("No", id="no", variant="default"),
                classes="button-row",
            ),
            classes="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            self.on_confirm()
        self.app.pop_screen()


class BatchConnectDialog(ModalScreen[None]):
    def __init__(self, graph, subject_name: str, topic_name: str, node_text: str):
        super().__init__()
        self.graph = graph
        self.subject_name = subject_name
        self.topic_name = topic_name
        self.node_text = node_text

    def compose(self) -> ComposeResult:
        from editor.engine import EditorEngine

        subject = self.graph.get_subject(self.subject_name)
        topic = subject.get_topic(self.topic_name)
        nodes = [t for t in topic.nodes.keys() if t != self.node_text]

        yield Vertical(
            Static(f"Batch connect '{self.node_text}'", classes="dialog-title"),
            *[Checkbox(n, id=f"cb-{i}") for i, n in enumerate(nodes)],
            RadioSet(
                RadioButton("P", id="dir-p", value=True),
                RadioButton("R", id="dir-r"),
                RadioButton("PR", id="dir-pr"),
                id="direction",
            ),
            Horizontal(
                Button("Confirm", id="confirm", variant="primary"),
                Button("Cancel", id="cancel", variant="default"),
                classes="button-row",
            ),
            classes="dialog",
            id="batch-dialog",
        )

    def on_mount(self) -> None:
        pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "confirm":
            from editor.engine import EditorEngine
            engine = EditorEngine(self.app.graph)

            selected = []
            for child in self.query(Checkbox):
                if child.value:
                    selected.append(child.label)

            direction = "PR"
            radio_set = self.query_one("#direction", RadioSet)
            if radio_set.pressed_button:
                dir_id = radio_set.pressed_button.id
                if dir_id == "dir-p":
                    direction = "P"
                elif dir_id == "dir-r":
                    direction = "R"

            if selected:
                self.app.graph = engine.batch_connect(
                    self.subject_name, self.topic_name, self.node_text, selected, direction
                )
        self.app.pop_screen()


class RemoveEdgeDialog(ModalScreen[None]):
    def __init__(self, subject_name: str, topic_name: str, node_text: str, edges: list):
        super().__init__()
        self.subject_name = subject_name
        self.topic_name = topic_name
        self.node_text = node_text
        self.edges = edges

    def compose(self) -> ComposeResult:
        from textual.widgets.option_list import Option
        yield Vertical(
            Static("Select edge to remove", classes="dialog-title"),
            *[Checkbox(label, id=f"edge-{i}") for i, (opt) in enumerate(self.edges)],
            Horizontal(
                Button("Remove", id="remove", variant="error"),
                Button("Cancel", id="cancel", variant="default"),
                classes="button-row",
            ),
            classes="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "remove":
            from editor.engine import EditorEngine
            engine = EditorEngine(self.app.graph)
            for child in self.query(Checkbox):
                if child.value:
                    parts = child.label.split(" → ", 1)
                    if len(parts) == 2:
                        self.app.graph = engine.disconnect(
                            self.subject_name, self.topic_name, parts[0], parts[1]
                        )
        self.app.pop_screen()