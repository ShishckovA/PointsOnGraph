from math import factorial
import sympy as sym

def td(s, ws):
    z = sym.Symbol("z") 
    formula = sym.S.One
    for wi in ws:
        formula *= wi * z / (1 - sym.exp(-wi * z))
    mcloren = sym.Poly(formula.series(z, x0=0, n=s + 1).removeO(), z)
    result = mcloren.all_coeffs()[::-1]
    return result[-1]


def build_rk(k, l, ws):
    print(k)
    p1 = 1
    for wi in ws:
        p1 /= wi
    s1 = 0
    for s in range(k + 1):
        to_add = l ** s / factorial(s) * td(k - s, ws)
        s1 += to_add
    return p1 * s1

# k = 5
# ws = [sym.Symbol(f"w_{i + 1}") for i in range(k)]
# l = sym.Symbol("lambda")
# rk = (build_rk(k, l, ws))
# result = rk.subs({"lambda": sym.sqrt(11) * 15 * 100, "w_1": 1 * 100, "w_2": sym.sqrt(2) * 100, "w_3": sym.sqrt(3) * 100, "w_4": sym.sqrt(5) * 100, "w_5": sym.sqrt(7) * 100}).evalf()
# print(result)
