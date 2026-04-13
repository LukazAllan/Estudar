from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import OptionList, Static, Button
from textual.containers import Vertical
from textual.widgets.option_list import Option


class QuizMenuScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Static("Quiz Mode", classes="title")
        yield OptionList(
            Option("All Content", "all"),
            Option("By Subject", "subject"),
            Option("By Topic", "topic"),
            Option("Exhaustive (Stub)", "exhaustive"),
            id="quiz-options",
        )
        yield Button("Back", id="back", variant="default")

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        from screens.quiz_play import QuizPlayScreen
        mode = event.option.id

        if mode == "all":
            self.app.push_screen(QuizPlayScreen(None, None))
        elif mode == "subject":
            self._select_subject(for_topic=False)
        elif mode == "topic":
            self._select_subject(for_topic=True)
        elif mode == "exhaustive":
            pass

    def _select_subject(self, for_topic: bool) -> None:
        subjects = list(self.app.graph.subjects.keys())
        screen = SubjectSelectionScreen(subjects, for_topic)
        self.app.push_screen(screen)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()


class SubjectSelectionScreen(Screen):
    def __init__(self, subjects: list[str], for_topic: bool):
        super().__init__()
        self.subjects = subjects
        self.for_topic = for_topic

    def compose(self) -> ComposeResult:
        yield Static("Select Subject", classes="title")
        options = [Option(s, s) for s in self.subjects]
        #options.append(Option("Back", "back"))
        yield OptionList(*options, id="subject-options")
        yield Button("Back", id="back", variant='default')

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        value = event.option.id
        if value == "back":
            self.app.pop_screen()
            return

        if self.for_topic:
            subject = self.app.graph.get_subject(value)
            topics = list(subject.topics.keys())
            screen = TopicSelectionScreen(value, topics)
            self.app.push_screen(screen)
        else:
            from screens.quiz_play import QuizPlayScreen
            self.app.push_screen(QuizPlayScreen(value, None))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()


class TopicSelectionScreen(Screen):
    def __init__(self, subject_name: str, topics: list[str]):
        super().__init__()
        self.subject_name = subject_name
        self.topics = topics

    def compose(self) -> ComposeResult:
        yield Static(f"Select Topic in {self.subject_name}", classes="title")
        options = [Option(t, t) for t in self.topics]
        #options.append(Option("Back", "back"))
        yield OptionList(*options, id="topic-options")
        yield Button("Back", "default", id="back")

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        value = event.option.id
        if value == "back":
            self.app.pop_screen()
            return
        from screens.quiz_play import QuizPlayScreen
        self.app.push_screen(QuizPlayScreen(self.subject_name, value))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()