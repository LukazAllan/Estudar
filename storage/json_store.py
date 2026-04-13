import os
import tempfile
from commentjson import load as cjson_load, dump as cjson_dump
from model.graph import Graph


def load(path: str) -> Graph:
    with open(path, encoding="utf-8") as f:
        data = cjson_load(f)
    return Graph.from_dict(data)


def save(graph: Graph, path: str) -> None:
    dirname = os.path.dirname(path) or "."
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=dirname,
        delete=False,
        suffix=".tmp"
    ) as tmp:
        cjson_dump(graph.to_dict(), tmp, indent=4, ensure_ascii=False)
        tmp_path = tmp.name
    os.replace(tmp_path, path)