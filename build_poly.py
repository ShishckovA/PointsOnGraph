#!/usr/bin/env python
# coding: utf-8

# In[1]:


from itertools import chain, combinations

from graph2 import *

import sympy

from symplex_counting.todd import build_rk

# multiedge
# n, m = 2, 4
# g = Graph()
# ts = [sympy.Symbol(f"t_{i}") for i in range(m)]
# T = sympy.Symbol("T")
# g.add_edge(Edge(0, 1, ts[0]))
# g.add_edge(Edge(0, 1, ts[1]))
# g.add_edge(Edge(0, 1, ts[2]))
# g.add_edge(Edge(0, 1, ts[3]))
# print(g)

# bamboo-2
# n, m = 3, 2
# g = Graph()
# ts = [sympy.Symbol(f"t_{i}") for i in range(m)]
# T = sympy.Symbol("T")
# g.add_edge(Edge(0, 1, ts[0]))
# g.add_edge(Edge(1, 2, ts[1]))
# print(g)

# tail-tri
n, m = 5, 5
g = Graph()
ts = [sympy.Symbol(f"t_{i}") for i in range(1, m + 1)]
T = sympy.Symbol("T")
g.add_edge(Edge(0, 1, ts[0]))
g.add_edge(Edge(2, 0, ts[1]))
g.add_edge(Edge(1, 2, ts[2]))
g.add_edge(Edge(0, 3, ts[3]))
g.add_edge(Edge(3, 4, ts[4]))
print(g)

# tri
# n, m = 3, 3
# g = Graph()
# ts = [sympy.Symbol(f"t_{i}") for i in range(m)]
# T = sympy.Symbol("T")
# g.add_edge(Edge(0, 1, ts[0]))
# g.add_edge(Edge(1, 2, ts[1]))
# g.add_edge(Edge(2, 0, ts[2]))
# print(g)

# single-edge
# n, m = 2, 1
# g = Graph()
# ts = [sympy.Symbol(f"t_{i}") for i in range(m)]
# T = sympy.Symbol("T")
# g.add_edge(Edge(0, 1, ts[0]))
# print(g)


# In[2]:


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
    return set(tuple(celem) for celem in (sorted(
            cs.items(), key=lambda elem: elem[0]
        ) for cs in arr)
    )



def all_routes(g, s, v):
    used = {eid: 0 for eid in g.edges}
    cs = []
    dfs2(g, s, v, used, cs)
    res = [{
        eid: 2 - used[eid] % 2 for eid in g.edges
    } for used in cs]
    res = unique(res)
    res1 = [[(g.edges[eid][0], c) for eid, c in cs] for cs in res]
    return res1


# In[3]:


for elem in all_routes(g, 0, 1):
    print(elem)


# In[4]:


s = 0
l = sympy.Symbol("lambda")
ws = [sympy.Symbol(f"w_{i}") for i in range(1, m + 2)]
Rks = [build_rk(i, l, ws[:i]) for i in range(m + 1)]


# In[5]:


print(Rks)


# In[6]:


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


# In[7]:


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
        ts2 = [edges[0].t * 2 for eid, edges in sub_g.edges.items() if eid != ism.eid]
        Rk = Rks[len(ts2)].subs([(w, t2) for w, t2 in zip(ws, ts2)])
        res4 = sympy.S.Zero
        for cs in all_routes(sub_g, s, v):
            res4 += Rk.subs([(l,  T - sum(c * edge.t for edge, c in cs if edge.eid != ism.eid) - ism.t)])
        res3 += res4
    R2 += res3


# In[8]:


R1 = sympy.simplify(R1)
R2 = sympy.simplify(R2)
N = sympy.simplify(sympy.Poly(R1, T) + sympy.Poly(R2, T))
N


# In[9]:


# display(sympy.simplify(sympy.Poly(R1, T)), sympy.simplify(sympy.Poly(R2, T)))


# In[10]:


k = 10
t1 = sympy.S.One * k
t2 = sympy.sqrt(2) * k
t3 = sympy.sqrt(3) * k
t4 = sympy.sqrt(5) * k
t5 = sympy.sqrt(7) * k

tvals = [t1, t2, t3, t4, t5]

Tc = 500


# In[11]:


N.subs([
    (T, Tc)
]).subs(zip(ts, tvals)).evalf()


# In[12]:


print(sympy.latex(N))


# In[13]:


R1_p = sympy.S.Zero
for sub_g in get_all_subg(g, s):
    ts2 = [edges[0].t * 2 for eid, edges in sub_g.edges.items()]
    Rk = Rks[len(ts2)].subs([(w, t2) for w, t2 in zip(ws, ts2)])
    res1 = sympy.S.Zero
    for v in sub_g.g:
        res2 = sympy.S.Zero
        for cs in all_routes(sub_g, s, v):
            res2 += Rk.subs([(l, T + sum(c * edge.t for edge, c in cs if c == 1))])
        res1 += (len(g.g[v]) - len(sub_g.g[v])) * res2
    R1_p += res1


R2_p = sympy.S.Zero
for sub_g in get_all_subg(g, s):
    res3 = sympy.S.Zero
    for v in sub_g.g:
        ism = get_isthmus(sub_g, s, v)
        if ism is None:
            continue
        ts2 = [edges[0].t * 2 for eid, edges in sub_g.edges.items() if eid != ism.eid]
        Rk = Rks[len(ts2)].subs([(w, t2) for w, t2 in zip(ws, ts2)])
        res4 = sympy.S.Zero
        for cs in all_routes(sub_g, s, v):
            res4 += Rk.subs([(l,  T + sum(c * edge.t for edge, c in cs if edge.eid != ism.eid and c == 1) - ism.t)])
        res3 += res4
    R2_p += res3

R1_p = sympy.simplify(R1_p)
R2_p = sympy.simplify(R2_p)
N_p = sympy.Poly(sympy.simplify(R1_p + R2_p), T)

N_p.subs([
    (T, Tc)
]).subs(zip(ts, tvals)).evalf()


# In[14]:


display(N_p)


# In[ ]:




