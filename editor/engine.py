from typing import Optional, Literal, List
from model.graph import Graph, Subject, Topic, Node, Edge


class EditorEngine:
    def __init__(self, graph: Graph):
        self.graph = graph

    def add_subject(self, name: str) -> Graph:
        return self.graph.add_subject(name)

    def rename_subject(self, old: str, new: str) -> Graph:
        return self.graph.rename_subject(old, new)

    def delete_subject(self, name: str) -> Graph:
        return self.graph.remove_subject(name)

    def add_topic(self, subject: str, name: str) -> Graph:
        subj = self.graph.get_subject(subject)
        if not subj:
            return self.graph
        new_subj = subj.add_topic(name)
        return self.graph.update_subject(new_subj)

    def rename_topic(self, subject: str, old: str, new: str) -> Graph:
        subj = self.graph.get_subject(subject)
        if not subj:
            return self.graph
        new_subj = subj.rename_topic(old, new)
        return self.graph.update_subject(new_subj)

    def delete_topic(self, subject: str, name: str) -> Graph:
        subj = self.graph.get_subject(subject)
        if not subj:
            return self.graph
        new_subj = subj.remove_topic(name)
        return self.graph.update_subject(new_subj)

    def add_node(self, subject: str, topic: str, text: str, nid: Optional[int] = None) -> Graph:
        subj = self.graph.get_subject(subject)
        if not subj:
            return self.graph
        topic_obj = subj.get_topic(topic)
        if not topic_obj:
            return self.graph

        if nid is None:
            nid = max(topic_obj.nodes.values(), default=0) + 1

        new_topic = topic_obj.add_node(text, nid)
        new_subj = subj.update_topic(new_topic)
        return self.graph.update_subject(new_subj)

    def rename_node(self, subject: str, topic: str, old_text: str, new_text: str) -> Graph:
        subj = self.graph.get_subject(subject)
        if not subj:
            return self.graph
        topic_obj = subj.get_topic(topic)
        if not topic_obj:
            return self.graph

        new_topic = topic_obj.rename_node(old_text, new_text)
        new_subj = subj.update_topic(new_topic)
        return self.graph.update_subject(new_subj)

    def delete_node(self, subject: str, topic: str, text: str) -> Graph:
        subj = self.graph.get_subject(subject)
        if not subj:
            return self.graph
        topic_obj = subj.get_topic(topic)
        if not topic_obj:
            return self.graph

        new_topic = topic_obj.remove_node(text)
        new_subj = subj.update_topic(new_topic)
        return self.graph.update_subject(new_subj)

    def connect(
        self,
        subject: str,
        topic: str,
        src_text: str,
        dst_text: str,
        direction: Literal["P", "R"]
    ) -> Graph:
        subj = self.graph.get_subject(subject)
        if not subj:
            return self.graph
        topic_obj = subj.get_topic(topic)
        if not topic_obj:
            return self.graph

        src_id = topic_obj.nodes.get(src_text)
        dst_id = topic_obj.nodes.get(dst_text)
        if src_id is None or dst_id is None:
            return self.graph

        if direction == "P":
            new_topic = topic_obj.add_edge(src_id, dst_id)
        else:
            new_topic = topic_obj.add_edge(dst_id, src_id)

        new_subj = subj.update_topic(new_topic)
        return self.graph.update_subject(new_subj)

    def disconnect(
        self,
        subject: str,
        topic: str,
        src_text: str,
        dst_text: str
    ) -> Graph:
        subj = self.graph.get_subject(subject)
        if not subj:
            return self.graph
        topic_obj = subj.get_topic(topic)
        if not topic_obj:
            return self.graph

        src_id = topic_obj.nodes.get(src_text)
        dst_id = topic_obj.nodes.get(dst_text)
        if src_id is None or dst_id is None:
            return self.graph

        new_topic = topic_obj.remove_edge(src_id, dst_id)
        new_subj = subj.update_topic(new_topic)
        return self.graph.update_subject(new_subj)

    def batch_connect(
        self,
        subject: str,
        topic: str,
        src_text: str,
        dst_texts: List[str],
        direction: Literal["P", "R", "PR"]
    ) -> Graph:
        subj = self.graph.get_subject(subject)
        if not subj:
            return self.graph
        topic_obj = subj.get_topic(topic)
        if not topic_obj:
            return self.graph

        src_id = topic_obj.nodes.get(src_text)
        if src_id is None:
            return self.graph

        new_edges = list(topic_obj.edges)

        if direction in ("P", "PR"):
            for dst_text in dst_texts:
                dst_id = topic_obj.nodes.get(dst_text)
                if dst_id is not None:
                    edge = [src_id, dst_id]
                    if edge not in new_edges:
                        new_edges.append(edge)

        if direction in ("R", "PR"):
            for dst_text in dst_texts:
                dst_id = topic_obj.nodes.get(dst_text)
                if dst_id is not None:
                    edge = [dst_id, src_id]
                    if edge not in new_edges:
                        new_edges.append(edge)

        new_topic = Topic(name=topic_obj.name, nodes=dict(topic_obj.nodes), edges=new_edges)
        new_subj = subj.update_topic(new_topic)
        return self.graph.update_subject(new_subj)