from typing import Callable

from PyQt5.QtCore import QThread


class Node:
    def __init__(self, x: float, y: float, name: str):
        self.x = x
        self.y = y
        self.name = name

    def get_node_string(self):
        return f"{self.x} {self.y} {self.name}"

    @staticmethod
    def from_string(string: str):
        x, y, name = string.split()
        return Node(float(x), float(y), name)


class Edge:
    def __init__(self, node1: Node, node2: Node):
        self.node1 = node1
        self.node2 = node2

    def get_edge_string(self):
        return f"{self.node1.name} {self.node2.name}"


class AThread(QThread):
    def __init__(self, parent=None, function: Callable = None, *args, **kwargs):
        super().__init__(parent)
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.result = None
        self.ok = False

    def run(self):
        try:
            self.result = self.function(*self.args, **self.kwargs)
            self.ok = True
        except Exception as e:
            self.result = e
            self.ok = False
