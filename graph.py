from __future__ import annotations

from collections import deque
import itertools

EPS = 1e-6

class Vertex:
    def __init__(self, name="vertex"):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return str(self)


class Edge:
    def __init__(self, begin: Vertex, end: Vertex, t: float):
        self.begin = begin
        self.end = end
        self.t = t
        self.points: deque[Point] = deque()

    def __len__(self):
        return self.t

    def __str__(self):
        return f"{self.begin} -> {self.end} ({self.t:.1f})"

    def __repr__(self):
        return str(self)

    def add_point(self, p: Point):
        assert p.edge is None
        p.edge = self
        self.points.append(p)
        p.history.append(self)


class Point:
    def __init__(self, t: float = 0, history=None):
        if history is None:
            history = []
        self.edge = None
        self.t = t
        self.history = history.copy()

    def __str__(self):
        return f"Point({self.edge}, {self.t})"

    def __repr__(self):
        return str(self)

    def eta(self):
        return self.edge.t - self.t


class Graph:
    def __init__(self):
        self.g: dict[Vertex, list[Edge]] = {}

    def add_vertex(self, v: Vertex):
        if v in self.g:
            raise Exception(f"Vertex with name {v.name} is already graph")
        self.g[v] = []

    def add_edge(self, e: Edge, bidirectional=True):
        assert e.begin in self.g
        assert e.end in self.g

        self.g[e.begin].append(e)
        if bidirectional:
            reversed_e = Edge(e.end, e.begin, e.t)
            self.g[reversed_e.begin].append(reversed_e)

    def add_point(self, v: Vertex):
        if v not in self.g:
            raise Exception("Vertex is not in graph")

        for edge in self.g[v]:
            edge.add_point(Point())

    def __str__(self):
        return str(self.g)

    def get_edges(self):
        return list(itertools.chain.from_iterable(self.g.values()))

    def get_points(self):
        return [p for ls in self.g.values() for e in ls for p in e.points]


    def closest_point(self):
        return min([e.points[0] for e in self.get_edges() if e.points], key=lambda p: p.eta())


    def tick(self):
        p = self.closest_point()
        edge = p.edge
        edge.points.popleft()
        dt = p.eta()

        for p1 in self.get_points():
            if (p1.eta() - dt) < EPS:
                p1.edge.points.popleft()
                continue
            p1.t += dt
        for other_e in self.g[edge.end]:
            other_e.add_point(Point(history=p.history))
        return dt

    def skip(self, dt: float):
        dt_skip = dt
        while self.closest_point().eta() <= dt:
            dt -= self.tick()
        for p1 in self.get_points():
            assert p1.eta() >= dt
            p1.t += dt
        return dt_skip