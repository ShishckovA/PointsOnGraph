from __future__ import annotations

from typing import Callable, Any

from PyQt5.QtCore import QThread


class Node:
    """
    Represents node in graph window
    A position is stored in (x, y) field, name is node title
    for showing
    """
    def __init__(self, x: float, y: float, name: str):
        """
        Node constructor
        :param x: node x-coordinate (in [0, 1))
        :param y: node y-coordinate (in [0, 1))
        :param name: node title
        """
        self.x = x
        self.y = y
        self.name = name

    def get_node_string(self) -> str:
        """
        Generate string for node saving
        :return: string representing a node
        """
        return f"{self.x} {self.y} {self.name}"

    @staticmethod
    def from_string(string: str) -> Node:
        """
        Static method from node deserialization
        :param string: string from mode deserialization
        :return: Node
        """
        x, y, name = string.split()
        return Node(float(x), float(y), name)


class Edge:
    """
    Represents edge in graph window
    Two ends of edge (Nodes) are stored in node1 and node field
    name is a name for edge labeling and variable in
    polynomials (length)
    """
    def __init__(self, node1: Node, node2: Node, name: str):
        """
        Edge constructor
        :param node1: first end of node
        :param node2: second end of node
        :param name: node label
        """
        self.node1 = node1
        self.node2 = node2
        self.name = name

    def get_edge_string(self) -> str:
        """
        Generate string for edge saving
        :return: string representing a edge
        """
        return f"{self.node1.name} {self.node2.name} {self.name}"

    def __eq__(self, other: Any) -> bool:
        """
        Equal operator
        :param other:
        :return:
        True if ids of self and other are equal
        """
        return id(self) == id(other)


class AThread(QThread):
    """
    A thread for subtask. Derived from PyQT QThread
    """
    def __init__(self, parent=None, function: Callable = None, *args, **kwargs):
        """
        Constructor for AThread. Used to set function and it's args
        :param parent:
        :param function: a function to calculate
        :param args: function args
        :param kwargs: function keyword args
        """
        super().__init__(parent)
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.result = None
        self.ok = False

    def run(self):
        """
        Start computing a function. If success, a result is stored
        in Athread.result and Athread.ok is True. Else, exception is stored
        in Athread.result, and Athread.ok is False.
        :return: None
        """
        try:
            self.result = self.function(*self.args, **self.kwargs)
            self.ok = True
        except Exception as e:
            self.result = e
            self.ok = False
