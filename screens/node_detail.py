from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, OptionList, Button
from textual.widgets.option_list import Option
from textual.containers import Vertical
from editor.engine import EditorEngine


class NodeDetailScreen(Screen):
    def __init__(self, subject_name: str, topic_name: str, node_text: str):
        super().__init__()
        self.subject_name = subject_name
        self.topic_name = topic_name
        self.node_text = node_text
        self.engine = None

    def compose(self) -> ComposeResult:
        yield Static(id="node-title", classes="title")
        yield Static(id="connections", classes="info-text")
        yield OptionList(
            Option("Edit Node", "edit_node"),
            Option("Delete Node", "delete_node"),
            Option("Connect Node", "connect_node"),
            Option("Batch Connect", "batch_connect"),
            Option("Remove Edge", "remove_edge"),
            Option("View Connections", "view_connections"),
            Option("Back", "back"),
            id="node-options",
        )

    def on_mount(self) -> None:
        self.engine = EditorEngine(self.app.graph)
        self._refresh()

    def _refresh(self) -> None:
        subject = self.app.graph.get_subject(self.subject_name)
        if not subject:
            self.app.pop_screen()
            return
        topic = subject.get_topic(self.topic_name)
        if not topic:
            self.app.pop_screen()
            return

        node_id = topic.nodes.get(self.node_text)
        if node_id is None:
            self.app.pop_screen()
            return

        conns = []
        for src_id, dst_id in topic.edges:
            if src_id == node_id:
                for t, nid in topic.nodes.items():
                    if nid == dst_id:
                        conns.append(f"  → {t} (P)")
                        break
            elif dst_id == node_id:
                for t, nid in topic.nodes.items():
                    if nid == src_id:
                        conns.append(f"  ← {t} (R)")
                        break

        self.query_one("#node-title", Static).update(
            f"Node: {self.node_text} (ID: {node_id})"
        )
        self.query_one("#connections", Static).update(
            "\n".join(conns) if conns else "No connections"
        )

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        value = event.option.id
        if value == "edit_node":
            from screens.dialogs import InputDialog
            def on_edit(name: str):
                if name.strip() and name != self.node_text:
                    self.app.graph = self.engine.rename_node(
                        self.subject_name, self.topic_name, self.node_text, name.strip()
                    )
                    self.node_text = name.strip()
                    self._refresh()
            self.app.push_screen(InputDialog(f"Rename '{self.node_text}' to:", on_edit))
        elif value == "delete_node":
            from screens.dialogs import ConfirmDialog
            def on_delete():
                self.app.graph = self.engine.delete_node(
                    self.subject_name, self.topic_name, self.node_text
                )
                self.app.pop_screen()
            self.app.push_screen(ConfirmDialog(f"Delete '{self.node_text}'?", on_delete))
        elif value == "connect_node":
            self._show_connect_screen()
        elif value == "batch_connect":
            from screens.dialogs import BatchConnectDialog
            self.app.push_screen(BatchConnectDialog(
                self.app.graph, self.subject_name, self.topic_name, self.node_text
            ))
        elif value == "remove_edge":
            self._show_remove_edge()
        elif value == "view_connections":
            pass
        elif value == "back":
            self.app.pop_screen()

    def _show_connect_screen(self) -> None:
        subject = self.app.graph.get_subject(self.subject_name)
        topic = subject.get_topic(self.topic_name)
        nodes = [t for t in topic.nodes.keys() if t != self.node_text]
        screen = ConnectNodeScreen(self.subject_name, self.topic_name, self.node_text, nodes)
        self.app.push_screen(screen)

    def _show_remove_edge(self) -> None:
        subject = self.app.graph.get_subject(self.subject_name)
        topic = subject.get_topic(self.topic_name)
        node_id = topic.nodes.get(self.node_text)

        edges = []
        for src_id, dst_id in topic.edges:
            if src_id == node_id or dst_id == node_id:
                src_t = next((t for t, nid in topic.nodes.items() if nid == src_id), "?")
                dst_t = next((t for t, nid in topic.nodes.items() if nid == dst_id), "?")
                edges.append(Option(f"{src_t} → {dst_t}", f"{src_t}|{dst_t}"))

        if not edges:
            return

        from screens.dialogs import RemoveEdgeDialog
        self.app.push_screen(RemoveEdgeDialog(
            self.subject_name, self.topic_name, self.node_text, edges
        ))


class ConnectNodeScreen(Screen):
    def __init__(self, subject_name: str, topic_name: str, node_text: str, nodes: list[str]):
        super().__init__()
        self.subject_name = subject_name
        self.topic_name = topic_name
        self.node_text = node_text
        self.nodes = nodes
        self.engine = None

    def compose(self) -> ComposeResult:
        yield Static("Connect Node", classes="title")
        yield OptionList(id="target-nodes")
        yield Static("Press P, R or ESC", classes="info-text")

    def on_mount(self) -> None:
        self.engine = EditorEngine(self.app.graph)
        ol = self.query_one("#target-nodes", OptionList)
        for n in self.nodes:
            ol.add_option(Option(n, n))

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        self._connect(event.option.id, "P")

    def _connect(self, target: str, direction: str) -> None:
        self.app.graph = self.engine.connect(
            self.subject_name, self.topic_name, self.node_text, target, direction
        )
        self.app.pop_screen()

    def on_key(self, event) -> None:
        key = event.key
        ol = self.query_one("#target-nodes", OptionList)
        if key == "p" and ol.highlighted:
            self._connect(ol.get_option_at_index(ol.highlighted).id, "P")
        elif key == "r" and ol.highlighted:
            self._connect(ol.get_option_at_index(ol.highlighted).id, "R")
        elif key == "escape":
            self.app.pop_screen()