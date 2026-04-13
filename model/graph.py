from dataclasses import dataclass, field
from typing import Dict, List, Optional
import copy


@dataclass(frozen=True)
class Edge:
    source: int
    target: int


@dataclass(frozen=True)
class Node:
    text: str
    id: int 


@dataclass(frozen=True)
class Topic:
    name: str
    nodes: Dict[str, int] = field(default_factory=dict)
    edges: List[List[int]] = field(default_factory=list)

    def add_node(self, text: str, node_id: int) -> 'Topic':
        new_nodes = dict(self.nodes)
        new_nodes[text] = node_id
        return Topic(name=self.name, nodes=new_nodes, edges=list(self.edges))

    def remove_node(self, text: str) -> 'Topic':
        node_id = self.nodes.get(text)
        if node_id is None:
            return self
        new_nodes = {k: v for k, v in self.nodes.items() if k != text}
        new_edges = [e for e in self.edges if e[0] != node_id and e[1] != node_id]
        return Topic(name=self.name, nodes=new_nodes, edges=new_edges)

    def rename_node(self, old_text: str, new_text: str) -> 'Topic':
        if old_text not in self.nodes:
            return self
        node_id = self.nodes[old_text]
        new_nodes = dict(self.nodes)
        del new_nodes[old_text]
        new_nodes[new_text] = node_id
        return Topic(name=self.name, nodes=new_nodes, edges=list(self.edges))

    def add_edge(self, source_id: int, target_id: int) -> 'Topic':
        new_edges = list(self.edges)
        if [source_id, target_id] not in new_edges:
            new_edges.append([source_id, target_id])
        return Topic(name=self.name, nodes=dict(self.nodes), edges=new_edges)

    def remove_edge(self, source_id: int, target_id: int) -> 'Topic':
        new_edges = [e for e in self.edges if e != [source_id, target_id]]
        return Topic(name=self.name, nodes=dict(self.nodes), edges=new_edges)


@dataclass(frozen=True)
class Subject:
    name: str
    topics: Dict[str, Topic] = field(default_factory=dict)

    def add_topic(self, name: str) -> 'Subject':
        new_topics = dict(self.topics)
        new_topics[name] = Topic(name=name)
        return Subject(name=self.name, topics=new_topics)

    def remove_topic(self, name: str) -> 'Subject':
        new_topics = {k: v for k, v in self.topics.items() if k != name}
        return Subject(name=self.name, topics=new_topics)

    def rename_topic(self, old_name: str, new_name: str) -> 'Subject':
        if old_name not in self.topics:
            return self
        topic = self.topics[old_name]
        new_topics = dict(self.topics)
        del new_topics[old_name]
        new_topics[new_name] = Topic(name=new_name, nodes=dict(topic.nodes), edges=list(topic.edges))
        return Subject(name=self.name, topics=new_topics)

    def get_topic(self, name: str) -> Optional[Topic]:
        return self.topics.get(name)

    def update_topic(self, topic: Topic) -> 'Subject':
        new_topics = dict(self.topics)
        new_topics[topic.name] = topic
        return Subject(name=self.name, topics=new_topics)


@dataclass(frozen=True)
class Graph:
    subjects: Dict[str, Subject] = field(default_factory=dict)

    def add_subject(self, name: str) -> 'Graph':
        new_subjects = dict(self.subjects)
        new_subjects[name] = Subject(name=name)
        return Graph(subjects=new_subjects)

    def remove_subject(self, name: str) -> 'Graph':
        new_subjects = {k: v for k, v in self.subjects.items() if k != name}
        return Graph(subjects=new_subjects)

    def rename_subject(self, old_name: str, new_name: str) -> 'Graph':
        if old_name not in self.subjects:
            return self
        subject = self.subjects[old_name]
        new_subjects = dict(self.subjects)
        del new_subjects[old_name]
        new_subjects[new_name] = Subject(name=new_name, topics=dict(subject.topics))
        return Graph(subjects=new_subjects)

    def get_subject(self, name: str) -> Optional[Subject]:
        return self.subjects.get(name)

    def update_subject(self, subject: Subject) -> 'Graph':
        new_subjects = dict(self.subjects)
        new_subjects[subject.name] = subject
        return Graph(subjects=new_subjects)

    def to_dict(self) -> dict:
        result = {}
        for subject_name, subject in self.subjects.items():
            result[subject_name] = {}
            for topic_name, topic in subject.topics.items():
                result[subject_name][topic_name] = {
                    "nodes": dict(topic.nodes),
                    "edges": list(topic.edges)
                }
        return result

    @classmethod
    def from_dict(cls, data: dict) -> 'Graph':
        subjects = {}
        for subject_name, subject_data in data.items():
            topics = {}
            for topic_name, topic_data in subject_data.items():
                topics[topic_name] = Topic(
                    name=topic_name,
                    nodes=dict(topic_data.get("nodes", {})),
                    edges=list(topic_data.get("edges", []))
                )
            subjects[subject_name] = Subject(name=subject_name, topics=topics)
        return cls(subjects=subjects)