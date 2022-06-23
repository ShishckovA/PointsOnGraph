from __future__ import annotations

import random
from typing import Union, Optional

import sympy
import networkx as nx


class Edge:
    """
    Edge representation in polynomial counting
    Has unique id, eid, eid is repeated only in reversed edges
    """
    def __init__(self, begin: int, end: int, t: Union[float, int, sympy.Symbol],
                 eid: Optional[str] = None):
        """
        Constructor for edge
        :param begin: vertex index for edge first end
        :param end: vertex index for edge second end
        :param t: edge length, can be any number or symbol
        :param eid: edge unique id. If None, a new eid is generated
        """
        self.begin = begin
        self.end = end
        self.t = t
        if eid is None:
            self.eid = Edge.random_string()
        else:
            self.eid = eid

    def __len__(self) -> Union[float, int, sympy.Symbol]:
        return self.t

    def __str__(self) -> str:
        return f"{self.begin} -> {self.end} ({self.t})"

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def random_string() -> str:
        """
        Generate random string for eid
        :return:
        """
        n = 10
        alph = "abcdefg1234567890"
        return "".join([random.choice(alph) for i in range(n)])


class Graph:
    """
    Graph representation for polynomial computing.
    Has list-of-edge dict in Graph.g and set of unique edges in
    Graph.edges (for iterating through edges)
    """
    def __init__(self):
        self.g: dict[int, list[Edge]] = {}
        self.edges = {}

    def add_vertex(self, v: int):
        if v in self.g:
            raise Exception(f"Vertex with name {v} is already graph")
        self.g[v] = []

    def connectors(self, v: int) -> list[Edge]:
        """
        Get all edges which is connected with vertex v
        :param v: vertex to find connectors
        :return: list of edges, where edge.begin == v or edge.end == v
        """
        return [edge for edge in self.g[v]]

    def add_edge(self, e: Edge) -> None:
        """
        Adds edge into a graph instance. Also adds a reverse edge
        with same eid.
        :param e: Edge to add
        :return: None
        """
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

    def get_pair(self, edge) -> Optional[Edge]:
        """
        Get edge pair for some edge (reversed)
        :param edge: edge to find a pair
        :return: reversed edge, or None if edge has no pair
        (i.e. a loop)
        """
        if len(self.edges[edge.eid]) == 1:
            return None
        return (
            self.edges[edge.eid][0]
            if self.edges[edge.eid][0] != edge
            else self.edges[edge.ind][1]
        )

    def __str__(self) -> str:
        return str(self.g)

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(tuple(sorted(edge for edge in self.edges)))

    def to_networkx(self) -> nx.Graph():
        """
        Convert a graph into NetworkX instance.
        :return: nx representation for a graph
        """
        G = nx.Graph()
        edge_set = {}
        G.add_nodes_from(self.g.keys())
        for edges_with_id in self.edges.values():
            edge = edges_with_id[0]
            G.add_edge(edge.begin, edge.end, eid=edge.eid)
        return G


def get_symbols(num_edges: int) -> list[sympy.Symbol]:
    """
    Generate symbols for edges length
    :param num_edges: number of edge, and symbols to generate
    :return:
    """
    return [sympy.Symbol(f"t_{i}") for i in range(num_edges)]


def get_multiedge(m=4) -> tuple[int, int, Graph]:
    """
    Graph example: multiedge
    m edges between two vertices
    List of edges representation:
    0 1
    0 1
    0 1
    ... (m times)
    :param m: number of edges
    between 2 vertices
    :return:
    """
    n = 2
    g = Graph()
    ts = get_symbols(m)
    for i in range(m):
        g.add_edge(Edge(0, 1, ts[i]))
    return n, m, g


def get_bamboo_len_2() -> tuple[int, int, Graph]:
    """
    Graph example: bamboo of len 2
    3 nodes in a row
    List of edges representation:
    0 1
    1 2
    :return:
    n -- number of vertices
    m -- number of edges
    n -- graph representation
    """
    n, m = 3, 2
    g = Graph()
    ts = get_symbols(m)
    g.add_edge(Edge(0, 1, ts[0]))
    g.add_edge(Edge(1, 2, ts[1]))
    return n, m, g


def get_triangle_with_tail() -> tuple[int, int, Graph]:
    """
    Graph example: trianngle with tail
    Triangle graph with a tail (len 2) in one vertex
    List of edges representation:
    0 1
    0 2
    1 2
    0 3
    3 4
    :return:
    n -- number of vertices
    m -- number of edges
    n -- graph representation
    """
    n, m = 5, 5
    g = Graph()
    ts = get_symbols(m)
    g.add_edge(Edge(0, 1, ts[0]))
    g.add_edge(Edge(2, 0, ts[1]))
    g.add_edge(Edge(1, 2, ts[2]))
    g.add_edge(Edge(0, 3, ts[3]))
    g.add_edge(Edge(3, 4, ts[4]))
    return n, m, g


def get_triangle() -> tuple[int, int, Graph]:
    """
    Graph example: triangle
    Triangle graph
    List of edges representation:
    0 1
    0 2
    1 2
    :return:
    n -- number of vertices
    m -- number of edges
    n -- graph representation
    """
    n, m = 3, 3
    g = Graph()
    ts = get_symbols(m)
    g.add_edge(Edge(0, 1, ts[0]))
    g.add_edge(Edge(1, 2, ts[1]))
    g.add_edge(Edge(2, 0, ts[2]))
    return n, m, g


def get_H() -> tuple[int, int, Graph]:
    """
    Graph example: H graph
    A graph that looks like a capital H letter
    List of edges representation:
    0 1
    0 2
    0 3
    3 4
    3 5
    :return:
    n -- number of vertices
    m -- number of edges
    n -- graph representation
    """
    n, m = 6, 5
    g = Graph()
    ts = get_symbols(m)
    T = sympy.Symbol("T")
    g.add_edge(Edge(0, 1, ts[0]))
    g.add_edge(Edge(0, 2, ts[1]))
    g.add_edge(Edge(0, 3, ts[2]))
    g.add_edge(Edge(3, 4, ts[3]))
    g.add_edge(Edge(3, 5, ts[4]))
    return n, m, g


def get_single_edge() -> tuple[int, int, Graph]:
    """
    Graph example: Single edge
    One edge between two nodes
    List of edges representation:
    0 1
    0 2
    0 3
    3 4
    3 5
    :return:
    n -- number of vertices
    m -- number of edges
    n -- graph representation
    """
    return get_multiedge(1)
