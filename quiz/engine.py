import random
from typing import Optional, List, Dict, Tuple
from model.graph import Graph, Subject, Topic
from util.text import semacento


class Question:
    def __init__(self, pergunta: str, respostas: List[str]):
        self.pergunta = pergunta
        self.respostas = respostas


class QuizEngine:
    def __init__(self, graph: Graph):
        self.graph = graph

    def select_question(
        self,
        subject_name: Optional[str] = None,
        topic_name: Optional[str] = None
    ) -> Optional[Question]:
        subjects = self.graph.subjects

        if subject_name:
            if subject_name not in subjects:
                return None
            subject = subjects[subject_name]
        else:
            subject = random.choice(list(subjects.values()))

        if topic_name:
            if topic_name not in subject.topics:
                return None
            topic = subject.topics[topic_name]
        else:
            topic = random.choice(list(subject.topics.values()))

        nodes = topic.nodes
        edges = topic.edges

        if not nodes or not edges:
            return None

        node_texts = list(nodes.keys())
        pergunta = random.choice(node_texts)
        pergunta_id = nodes[pergunta]

        respostas_validas = [
            destino
            for origem, destino in edges
            if origem == pergunta_id
        ]

        respostas_texto = [
            node for node, nid in nodes.items() if nid in respostas_validas
        ]

        return Question(pergunta=pergunta, respostas=respostas_texto)

    def validate(self, answer: str, question: Question) -> bool:
        for r in question.respostas:
            if semacento(answer) == semacento(r):
                return True
        return False