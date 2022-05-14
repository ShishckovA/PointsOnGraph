from networkx.algorithms.polynomials import tutte_polynomial


def build(n, m, g):
    nxg = g.to_networkx()
    poly = tutte_polynomial(nxg)
    poly = poly.subs("x", 1)

    return poly
