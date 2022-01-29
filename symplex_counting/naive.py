def inc(ks, ts):
    ks[0] += 1
    i = 0
    while ks[i] > ts[i]:
        ks[i] = 0
        if i + 1 != len(ks):
            ks[i + 1] += 1
            i += 1
        else:
            return False
    return True


def all_comb(ts):
    ks = [0 for i in range(len(ts))]
    yield ks
    while inc(ks, ts):
        yield ks


def dot(a, b):
    return sum(ai * bi for ai, bi in zip(a, b))


def naive(l, ws):
    n = len(ws)
    ts = [int(l // w) for w in ws]
    ans = 0
    for elem in all_comb(ts):
        print(elem[-1])
        if dot(elem, ws) < l:
            ans += 1
            # print(elem, dot(elem, ws))
        elif dot(elem, ws) == l:
            ans += 0.5
    return ans



print(naive(15 * (11) ** 0.5 * 100, [1 * 100, 2 ** 0.5 * 100, 3 ** 0.5 * 100, 5 ** 0.5 * 100, 7 ** 0.5 * 100]))
