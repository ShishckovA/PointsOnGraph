from networkx.algorithms.polynomials import tutte_polynomial
from sympy import Symbol


def build(n, m, g):
    nxg = g.to_networkx()
    poly = tutte_polynomial(nxg)
    x = Symbol('x')

    poly = poly.subs("y", 1 + 1 / x)

    return poly
