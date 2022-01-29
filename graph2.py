from __future__ import annotations

from collections import deque
import itertools
import random


class Edge:
    def __init__(self, begin: int, end: int, t: float, eid: str = None):
        self.begin = begin
        self.end = end
        self.t = t
        if eid is None:
            self.eid = Edge.random_string() 
        else:
            self.eid = eid


    def __len__(self):
        return self.t

    def __str__(self):
        return f"{self.begin} -> {self.end} ({self.t})"

    def __repr__(self):
        return str(self)

    @staticmethod
    def random_string():
        n = 10
        alph = "abcdefg1234567890"
        return "".join([random.choice(alph) for i in range(n)])

class Graph:
    def __init__(self):
        self.g: dict[int, list[Edge]] = {}
        self.edges = {}

    def add_vertex(self, v: int):
        if v in self.g:
            raise Exception(f"Vertex with name {v} is already graph")
        self.g[v] = []

    def connectors(self, v):
        return [edge for edge in self.g[v]]

    def add_edge(self, e: Edge):
        if e.begin not in self.g:
            self.add_vertex(e.begin)
        if e.end not in self.g:
            self.add_vertex(e.end)
        ind = e.eid
        self.edges[ind] = []
        self.edges[ind].append(e)
        self.g[e.begin].append(e)
        if e.begin != e.end:
            reversed_e = Edge(e.end, e.begin, e.t, ind)
            
            self.edges[ind].append(reversed_e)
            self.g[reversed_e.begin].append(reversed_e)


    def get_pair(self, edge):
        if len(self.edges[edge.eid]) == 1:
            return None
        return self.edges[edge.eid][0] if self.edges[edge.eid][0] != edge else self.edges[edge.ind][1]

    def __str__(self):
        return str(self.g)

    def __repr__(self):
        return str(self)


    def __hash__(self):
        return hash(tuple(sorted(edge for edge in self.edges)))