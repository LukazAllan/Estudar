from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Input, Button
from textual.containers import Vertical
from quiz.engine import QuizEngine
from util.text import semacento


class QuizPlayScreen(Screen):
    def __init__(self, subject: str | None, topic: str | None):
        super().__init__()
        self.subject = subject
        self.topic = topic
        self.engine = None
        self.round_num = 1
        self.score = 0
        self.question = None
        self.state = "question"

    def compose(self) -> ComposeResult:
        yield Static("Quiz", classes="title")
        yield Static(id="info", classes="info-text")
        yield Static(id="question", classes="quiz-question")
        yield Input(placeholder="Your answer...", id="answer-input")
        yield Static(id="result", classes="info-text")
        yield Vertical(
            Button("Continue", id="continue", variant="primary"),
            Button("Quit", id="quit", variant="error"),
            id="result-buttons",
        )

    def on_mount(self) -> None:
        self.engine = QuizEngine(self.app.graph)
        self._new_question()

    def _new_question(self) -> None:
        self.question = self.engine.select_question(self.subject, self.topic)
        if not self.question:
            self.query_one("#question", Static).update("No questions available.")
            self.query_one("#answer-input", Input).disabled = True
            self.query_one("#result-buttons").display = False
            return

        self.state = "question"
        info_question = f"Assunto: {self.subject} | Tópico: {self.topic if self.topic else 'Todos'}"
        info_points = f"Rodada: {self.round_num} | Pontuação: {self.score}"
        info = f'{info_points:^{len(info_question)}}'
        self.query_one("#info", Static).update(
            f"{info_question}\n{info}"
        )
        self.query_one("#question", Static).update(self.question.pergunta)
        self.query_one("#answer-input", Input).value = ""
        self.query_one("#answer-input", Input).disabled = False
        self.query_one("#answer-input", Input).focus()
        self.query_one("#result", Static).update("")
        self.query_one("#result-buttons").display = False

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if self.state != "question" or not self.question:
            return

        answer = event.value.strip()
        if not answer:
            return

        correct = self.engine.validate(answer, self.question)
        self.round_num += 1
        if correct:
            self.score += 1
            self.query_one("#result", Static).update("✅ CORRETO!")
            self.query_one("#result", Static).classes = "result-correct"
        else:
            corretas = " | ".join(self.question.respostas)
            self.query_one("#result", Static).update(f"❌ ERRADO! Respostas: {corretas}")
            self.query_one("#result", Static).classes = "result-wrong"

        self.state = "result"
        self.query_one("#answer-input", Input).disabled = True
        self.query_one("#result-buttons").display = True

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "continue":
            self._new_question()
        elif event.button.id == "quit":
            self.app.pop_screen()