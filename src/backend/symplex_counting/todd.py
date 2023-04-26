from math import factorial
from typing import Union

import sympy as sym
from sympy import bernoulli

from pre_calc import pre_calc


def td(s: int, ws: list[Union[float, int, sym.Symbol]]):
    res = pre_calc(s, len(ws))
    if res is not None:
        return res
    x = sym.Symbol("x")
    res = sym.Poly(1, x)

    for i in range(len(ws)):
        cp = charpoly(s + 1, x, ws[i])
        res *= cp
        res = drop_order_higher_than(s, x, res)

    cfs = res.all_coeffs()

    if s + 1 > len(cfs):
        return sym.S.Zero

    return cfs[-s - 1]


def charpoly(n: int, x, gam):
    if n == 0:
        return sym.Poly(sym.S.One, x)
    else:
        res = sym.Poly(sym.S.One + gam * x, x)
        for i in range(1, n + 1):
            res += bernoulli(i) / factorial(i) * gam ** i * x ** i
        return res


def drop_order_higher_than(k: int, x: sym.Symbol, polynom: sym.Poly):
    return sym.Poly(sum(c * x ** i for i, c in enumerate(polynom.all_coeffs()[::-1]) if i <= k), x)


def build_rk(k: int, l: Union[float, int, sym.Symbol], ws: list[Union[float, sym.Symbol]]):
    p1 = 1
    for wi in ws:
        p1 /= wi
    s1 = 0
    for s in range(k + 1):
        to_add = l ** s / factorial(s) * td(k - s, ws)
        s1 += to_add
    return p1 * s1
