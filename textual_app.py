from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, Static, OptionList, ListView, ListItem, Label
from textual.screen import Screen
from model.graph import Graph
from storage.json_store import load, save
from screens.main_menu import MainMenuScreen


class QuizApp(App):
    CSS_PATH = "app.tcss"
    BINDINGS = [
        Binding("ctrl+q", "save_and_exit", "Save & Quit"),
    ]

    graph_path: str = "base.json"
    graph: Graph = load(graph_path)

    def on_mount(self) -> None:
        self.push_screen(MainMenuScreen())

    def action_save_and_exit(self) -> None:
        save(self.graph, self.graph_path)
        self.exit()

    async def on_screen_resume(self) -> None:
        pass