from itertools import chain, combinations

from backend.graph_utils import Edge, Graph

import sympy

from backend.symplex_counting.todd import build_rk


def get_graph_from_cl():
    print("Введите число вершин и число рёбер графа через пробел:")
    n, m = map(int, input("> ").split())
    g = Graph()
    ts = [sympy.Symbol(f"t_{i}") for i in range(m)]
    print(f'Введите {m} рёбер в формате "b e"')
    for i in range(m):
        b, e = map(int, input("> ").split())
        g.add_edge(Edge(b, e, ts[i]))
    return n, m, g


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def dfs(g, v, used):
    used[v] = True
    for edge in g.g[v]:
        u = edge.end
        if not used[u]:
            dfs(g, u, used)


def is_connected(g, v):
    n = len(g.g)
    used = {i: False for i in g.g}
    dfs(g, v, used)
    return sum(used.values()) == n


def get_all_subg(g, v):
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


def dfs2(g, c, f, used, cs):
    if c == f:
        cs.append(used.copy())
    for edge in g.g[c]:
        u = edge.end
        if used[edge.eid] < 2:
            used[edge.eid] += 1
            dfs2(g, u, f, used, cs)
            used[edge.eid] -= 1


def unique(arr):
    return set(
        tuple(celem)
        for celem in (
            sorted(cs.items(), key=lambda elem: elem[0]) for cs in arr
        )
    )


def all_routes(g, s, v):
    used = {eid: 0 for eid in g.edges}
    cs = []
    dfs2(g, s, v, used, cs)
    res = [{eid: 2 - used[eid] % 2 for eid in g.edges} for used in cs]
    res = unique(res)
    res1 = [[(g.edges[eid][0], c) for eid, c in cs] for cs in res]
    return res1


def dfs3(g, v, banned, used):
    used[v] = True
    for edge in g.g[v]:
        if edge.eid == banned:
            continue
        if not used[edge.end]:
            dfs3(g, edge.end, banned, used)


def get_isthmus(g, s, v):
    if len(g.g[v]) == 1:
        return None
    for elem in g.g[v]:
        used = {i: False for i in g.g}
        dfs3(g, s, elem.eid, used)
        if not used[v]:
            return elem
    return None


def build(n, m, g):
    T = sympy.Symbol("T")

    s = 0
    l = sympy.Symbol("lambda")
    ws = [sympy.Symbol(f"w_{i}") for i in range(1, m + 2)]
    Rks = [build_rk(i, l, ws[:i]) for i in range(m + 1)]

    R1 = sympy.S.Zero
    for sub_g in get_all_subg(g, s):
        ts2 = [edges[0].t * 2 for eid, edges in sub_g.edges.items()]
        Rk = Rks[len(ts2)].subs([(w, t2) for w, t2 in zip(ws, ts2)])
        res1 = sympy.S.Zero
        for v in sub_g.g:
            res2 = sympy.S.Zero
            for cs in all_routes(sub_g, s, v):
                res2 += Rk.subs([(l, T - sum(c * edge.t for edge, c in cs))])
            res1 += (len(g.g[v]) - len(sub_g.g[v])) * res2
        R1 += res1

    R2 = sympy.S.Zero
    for sub_g in get_all_subg(g, s):
        res3 = sympy.S.Zero
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
            res3 += res4
        R2 += res3

    R1 = sympy.simplify(R1)
    R2 = sympy.simplify(R2)
    N = sympy.simplify(sympy.Poly(R1, T) + sympy.Poly(R2, T))
    return N


def prepare_for_showing(polynomial: sympy.Poly):
    new_poly = polynomial.copy()
    for v in polynomial.free_symbols:
        if v.name != "T":
            new_poly = new_poly.subs(v, 1)

    return str(new_poly.as_expr())


def prepare_for_saving(polynomial: sympy.Poly):
    return str(polynomial.as_expr())
