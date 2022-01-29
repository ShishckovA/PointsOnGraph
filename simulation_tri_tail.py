from graph import Vertex, Edge, Point, Graph

from math import sqrt, factorial
import time
import itertools


def count_points(g: Graph, T=50000):
    t = 0
    ns = 0
    while t < T:
        t += g.tick()
        ns += 1
        if ns % 1000 == 0:
            print(t)
            print(len(g.get_points()))
    return len(g.get_points())

def prod(arr):
    x = 1
    for elem in arr:
        x *= elem
    return x

def build_g(t1, t2, t3, t4, t5):

    L1 = Vertex("L1")
    L2 = Vertex("L2")
    R1 = Vertex("R1")
    R2 = Vertex("R2")
    A = Vertex("A")
    B = Vertex("B")

    g = Graph()

    g.add_vertex(L1)
    g.add_vertex(L2)
    g.add_vertex(R1)
    g.add_vertex(R2)
    g.add_vertex(A)
    g.add_vertex(B)

    e1 = Edge(L1, A, t1)
    e2 = Edge(L2, A, t2)
    e3 = Edge(A, B, t3)
    e4 = Edge(B, R1, t4)
    e5 = Edge(B, R2, t5)

    g.add_edge(e1)
    g.add_edge(e2)
    g.add_edge(e3)
    g.add_edge(e4)
    g.add_edge(e5)

    g.add_point(A)

    return g


def build_tri_with_tail(t1, t2, t3, t4, t5):

    A = Vertex("A")
    B = Vertex("B")
    C = Vertex("C")
    D = Vertex("D")
    E = Vertex("E")

    g = Graph()

    g.add_vertex(A)
    g.add_vertex(B)
    g.add_vertex(C)
    g.add_vertex(D)
    g.add_vertex(E)

    e1 = Edge(A, B, t1)
    e2 = Edge(B, C, t2)
    e3 = Edge(C, A, t3)
    e4 = Edge(A, D, t4)
    e5 = Edge(D, E, t5)

    g.add_edge(e1)
    g.add_edge(e2)
    g.add_edge(e3)
    g.add_edge(e4)
    g.add_edge(e5)

    g.add_point(A)

    return g

def build_bamboo2(t1, t2, *args):
    A = Vertex("A")
    B = Vertex("B")
    C = Vertex("C")

    g = Graph()
    g.add_vertex(A)
    g.add_vertex(B)
    g.add_vertex(C)
    e1 = Edge(A, B, t1)
    e2 = Edge(B, C, t2)

    g.add_edge(e1)
    g.add_edge(e2)

    g.add_point(A)

    return g

def build(t1, t2, t3, t4, *args):
    A = Vertex("A")
    B = Vertex("B")

    g = Graph()
    g.add_vertex(A)
    g.add_vertex(B)
    e1 = Edge(A, B, t1)
    e2 = Edge(A, B, t2)
    e3 = Edge(A, B, t3)
    e4 = Edge(A, B, t4)

    g.add_edge(e1)
    g.add_edge(e2)
    g.add_edge(e3)
    g.add_edge(e4)

    g.add_point(A)

    return g

def build_tri(t1, t2, t3, *args):

    A = Vertex("A")
    B = Vertex("B")
    C = Vertex("C")
    D = Vertex("D")
    E = Vertex("E")

    g = Graph()

    g.add_vertex(A)
    g.add_vertex(B)
    g.add_vertex(C)

    e1 = Edge(A, B, t1)
    e2 = Edge(B, C, t2)
    e3 = Edge(C, A, t3)

    g.add_edge(e1)
    g.add_edge(e2)
    g.add_edge(e3)

    g.add_point(A)

    return g

N = 100
t1 = sqrt(1) * N
t2 = sqrt(2) * N
t3 = sqrt(3) * N
t4 = sqrt(5) * N
t5 = sqrt(7) * N
ts = [t1, t2, t3, t4, t5]

T = 80000000
g = build(t1, t2, t3, t4, t5)
true_n = count_points(g, T)
print(true_n)
# poly_n = T ** 4 / 192  * sum(ts) / prod(ts)
# poly_n += T ** 3 / 48 / prod(ts) * (t1 * (t2 + t3 - 1/2 * t4 + 3/2 * t5) + t2 * (t3 - 1/2 * t4 + 3/2 * t5) + t3 * (-1/2 * t4 + 3/2 * t5) + t4 * (-t4 + t5))
# print(true_n, poly_n, true_n / poly_n)

