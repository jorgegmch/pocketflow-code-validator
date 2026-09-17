from typing import Dict, Any

class SharedState:
    def __init__(self):
        self._data: Dict[str, Any] = {}
    def set(self, key: str, value: Any): self._data[key] = value
    def get(self, key: str, default: Any = None): return self._data.get(key, default)

class Node:
    def __init__(self, name: str):
        self.name = name
    def run(self, state: SharedState) -> str:
        return self.exec(state)
    def exec(self, state: SharedState) -> str:
        raise NotImplementedError

class Flow:
    def __init__(self, name: str):
        self.name = name
        self.nodes: Dict[str, Node] = {}
        self.state = SharedState()
        self.start_node = None

    def add_node(self, node: Node, is_start: bool = False):
        self.nodes[node.name] = node
        if is_start: self.start_node = node.name

    def run(self):
        curr = self.start_node
        while curr:
            print(f"[Flow] Ejecutando: {curr}")
            curr = self.nodes[curr].run(self.state)