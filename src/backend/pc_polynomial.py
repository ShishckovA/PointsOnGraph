from itertools import chain, combinations
from typing import Iterable, List, Tuple, Any, Set, Optional

from backend.graph_utils import Edge, Graph

import sympy

from backend.symplex_counting.todd import build_rk


def get_graph_from_cl() -> tuple[int, int, Graph]:
    """
    Get graph from command line
    :return:
    n (int): number of vertex
    m (int): number of edges
    g (Graph): graph representation
    """
    print("Введите число вершин и число рёбер графа через пробел:")
    n, m = map(int, input("> ").split())
    g = Graph()
    ts = [sympy.Symbol(f"t_{i}") for i in range(m)]
    print(f'Введите {m} рёбер в формате "b e"')
    for i in range(m):
        b, e = map(int, input("> ").split())
        g.add_edge(Edge(b, e, ts[i]))
    return n, m, g


def powerset(iterable: Iterable) -> Iterable:
    """
    :param iterable: iterator to some container
    :return: powerset of input iterable
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def dfs(g: Graph, v: int, used: dict[int, bool]) -> None:
    """
    :param g: graph representation
    :param v: current vertex, where dfs is started
    :param used: list[bool], used[i] <=> vertex is used in dfs
    :return: None
    """
    used[v] = True
    for edge in g.g[v]:
        u = edge.end
        if not used[u]:
            dfs(g, u, used)


def is_connected(g: Graph, v: int) -> bool:
    """
    Check if graph with vertex v g is connected
    :param g: graph representation
    :param v: starting vertex for dfs
    :return: True, if graph g is connected
    False either
    """
    n = len(g.g)
    used = {i: False for i in g.g}
    dfs(g, v, used)
    return sum(used.values()) == n


def get_all_subg(g: Graph, v: int) -> set[Graph]:
    """
    List all subgraph g' for graph g, such that
    g' includes vertex v
    :param g: graph representation for subgraph listing
    :param v: vert
    :return: all subgraphs of graph g, that include vertex v
    """
    edges = [edges_with_hash[0] for edges_with_hash in g.edges.values()]
    res = set()
    for subgraph in powerset(edges):
        g1 = Graph()
        g1.add_vertex(v)
        for e1 in subgraph:
            g1.add_edge(e1)
        if is_connected(g1, v):
            res.add(g1)
    return res


def dfs2(g: Graph, c: int, f: int, used: dict[str, int],
         cs: list[dict[str, int]]) -> None:
    """
    Dfs-like helping function for finding all routes that passes
    every edge no more than 2 times. It is helpful to find
    all even routes from c to f
    :param g: graph representation
    :param c: starting vertex
    :param f: finish vertex
    :param used: number of times edge is used
    :param cs: cumulative array for result
    :return: None
    """
    if c == f:
        cs.append(used.copy())
    for edge in g.g[c]:
        u = edge.end
        if used[edge.eid] < 2:
            used[edge.eid] += 1
            dfs2(g, u, f, used, cs)
            used[edge.eid] -= 1


def unique(arr: list[dict[Any, Any]]) -> set[tuple[Any, ...]]:
    """
    Return set, containing unique elements from array arr
    :param arr: input array
    :return: unique elements from array arr
    """
    return set(
        tuple(celem)
        for celem in (
            sorted(cs.items(), key=lambda elem: elem[0]) for cs in arr
        )
    )


def all_routes(g: Graph, s: int, v: int) -> list[list[tuple[Any, Any]]]:
    """
    Compute all routes, that starts with s and finishes at v.
    Every route passes an edge no more than two times
    :param g: graph representation
    :param s: starting vertex
    :param v: end vertex
    :return: all unique routes from s to v
    """
    used = {eid: 0 for eid in g.edges}
    cs = []
    dfs2(g, s, v, used, cs)
    res = [{eid: 2 - used[eid] % 2 for eid in g.edges} for used in cs]
    res = unique(res)
    res1 = [[(g.edges[eid][0], c) for eid, c in cs] for cs in res]
    return res1


def dfs3(g: Graph, v: int, banned: str, used: dict[int, bool]) -> None:
    """
    Dfs-like function for finding an isthmus
    :param g: graph representation
    :param v: starting vertex
    :param banned: edge id for the banned edge
    :param used: showing if the edge is banned
    :return: None
    """
    used[v] = True
    for edge in g.g[v]:
        if edge.eid == banned:
            continue
        if not used[edge.end]:
            dfs3(g, edge.end, banned, used)


def get_isthmus(g: Graph, s: int, v: int) -> Optional[Edge]:
    """
    Get isthmus for vertex v, with starting vertex s
    :param g: graph representation
    :param s: starting vertex
    :param v: vertex for isthmus finding
    :return:
    Edge, if there is an isthmus near, connected with vertex v
    None either
    """
    if len(g.g[v]) == 1:
        return None
    for elem in g.g[v]:
        used = {i: False for i in g.g}
        dfs3(g, s, elem.eid, used)
        if not used[v]:
            return elem
    return None


def build(n: int, m: int, g: Graph) -> sympy.core.Expr:
    """
    Compute point counting polynomial for graph g
    :param n: number of vertex in graph g
    :param m: number of edges in graph g
    :param g: graph representation
    :return:
    Point counting polynomial for graph g. See more at
    https://link.springer.com/article/10.1134/S1560354717080032
    """
    T = sympy.Symbol("T")

    s = 0
    l = sympy.Symbol("lambda")
    ws = [sympy.Symbol(f"w_{i}") for i in range(1, m + 2)]
    Rks = [build_rk(i, l, ws[:i]) for i in range(m + 1)]

    # Computing first part
    R1 = sympy.S.Zero
    for sub_g in get_all_subg(g, s):
        ts2 = [edges[0].t * 2 for eid, edges in sub_g.edges.items()]
        Rk = Rks[len(ts2)].subs([(w, t2) for w, t2 in zip(ws, ts2)])
        res1 = sympy.S.Zero

        # Iterating through all vertex in every subgraph
        for v in sub_g.g:
            res2 = sympy.S.Zero
            for cs in all_routes(sub_g, s, v):
                res2 += Rk.subs([(l, T - sum(c * edge.t for edge, c in cs))])
            # Multiplying result with difference in difference between
            # subgraph vertex degrees
            res1 += (len(g.g[v]) - len(sub_g.g[v])) * res2
        R1 += res1

    # Computing first part -- with isthmus
    R2 = sympy.S.Zero
    for sub_g in get_all_subg(g, s):
        res3 = sympy.S.Zero

        # Iterating through all vertex in every subgraph
        for v in sub_g.g:
            ism = get_isthmus(sub_g, s, v)
            if ism is None:
                continue
            ts2 = [
                edges[0].t * 2
                for eid, edges in sub_g.edges.items()
                if eid != ism.eid
            ]
            Rk = Rks[len(ts2)].subs([(w, t2) for w, t2 in zip(ws, ts2)])
            res4 = sympy.S.Zero
            for cs in all_routes(sub_g, s, v):
                res4 += Rk.subs(
                    [
                        (
                            l,
                            T
                            - sum(
                                c * edge.t
                                for edge, c in cs
                                if edge.eid != ism.eid
                            )
                            - ism.t,
                        )
                    ]
                )
            # Here is isthmus, only +1 point at every time
            res3 += res4
        R2 += res3

    R1 = sympy.simplify(R1)
    R2 = sympy.simplify(R2)
    N = sympy.simplify(sympy.Poly(R1, T) + sympy.Poly(R2, T))
    return N


def prepare_for_showing(polynomial: sympy.Poly) -> str:
    """
    Generate string for polynomial showing
    :param polynomial: polynomial for string generation
    :return:
    String with polynomial representation
    """
    new_poly = polynomial.copy()
    v: sympy.Symbol
    for v in polynomial.free_symbols:
        if v.name != "T":
            new_poly = new_poly.subs(v, 1)

    return str(new_poly.as_expr())


def prepare_for_saving(polynomial: sympy.Poly) -> str:
    """
    Generate string for polynomial saving
    :param polynomial: polynomial for string generation
    :return:
    String with polynomial representation
    """

    return str(polynomial.as_expr())
