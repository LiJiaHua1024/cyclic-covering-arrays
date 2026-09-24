#!/usr/bin/env python3
"""Exact rational certificates for cyclic hard-core CAFE, arbitrary fixed index.

Tests finite induction bases for ALL infinite separations and traces for every
admissible separation on cycles 11..30. No external packages or floating point.
"""
from fractions import Fraction as Q

P = (
    (Q(5, 8), Q(3, 8), Q(0), Q(0)),
    (Q(0), Q(0), Q(1, 2), Q(1, 2)),
    (Q(3, 4), Q(1, 4), Q(0), Q(0)),
    (Q(0), Q(0), Q(1, 2), Q(1, 2)),
)
PI = (Q(2, 5), Q(1, 5), Q(1, 5), Q(1, 5))
G = (2, 2, 3, 3)
RHO = Q(5, 12)
START = 11
END = 30
LAMBDAS = (1, 2, 3, 4, 5)


def stationary_certificate():
    assert all(sum(PI[s] * P[s][t] for s in range(4)) == PI[t]
               for t in range(4))
    assert sum(PI[s] * G[s] for s in range(4)) == Q(12, 5)
    assert sum(PI) == 1 and RHO == 1 / Q(12, 5)


def infinite_distance_certificate():
    v = [[Q(1)] * 4]
    for d in range(1, 18):
        v.append([
            sum((P[s][t] * v[d-G[s]][t] for t in range(4)), Q(0))
            if d >= G[s] else Q(0)
            for s in range(4)
        ])
    expected = (
        Q(1, 4), Q(1, 6), Q(1, 6), Q(1, 6), Q(3, 16), Q(1, 6),
        Q(65, 384), Q(35, 192), Q(517, 3072), Q(89, 512),
        Q(4313, 24576), Q(2123, 12288), Q(11327, 65536),
    )
    p = lambda d: RHO * sum((PI[s] * v[d][s] for s in range(4)), Q(0))
    assert tuple(p(d) for d in range(2, 15)) == expected
    assert all(Q(1, 6) <= p(d) <= Q(1, 4) for d in range(2, 18))
    assert tuple(min(v[d]) for d in (15, 16, 17)) == (
        Q(1655, 4096), Q(1655, 4096), Q(1681, 4096))
    assert tuple(max(v[d]) for d in (15, 16, 17)) == (
        Q(229, 512), Q(6961, 16384), Q(13971, 32768))
    assert all(Q(2, 5) <= value <= Q(3, 5)
               for d in (15, 16, 17) for value in v[d])
    # For every d >= 18, d-G[s] is d-2 or d-3; convexity gives the
    # inductive interval [2/5,3/5] from these three exact base levels.
    assert all(sum(P[s]) == 1 for s in range(4))
    for lam in LAMBDAS:
        for d in range(2, 18):
            pd = p(d)
            probs = (pd, RHO-pd, RHO-pd, 1-2*RHO+pd)
            assert all(6 * lam * q >= lam for q in probs)
        assert all(6 * lam * q >= lam for q in (RHO, RHO, 1-2*RHO))
    return v


def matrix_mul(a, b):
    dim = len(a)
    out = [[Q(0) for _ in range(dim)] for _ in range(dim)]
    for i in range(dim):
        for k, aik in enumerate(a[i]):
            if aik:
                for j, bkj in enumerate(b[k]):
                    if bkj:
                        out[i][j] += aik * bkj
    return out


def trace(a):
    return sum((a[i][i] for i in range(len(a))), Q(0))


def site_matrix():
    states = [(s, phase) for s in range(4) for phase in range(G[s])]
    index = {state: i for i, state in enumerate(states)}
    dim = len(states)
    t = [[Q(0) for _ in range(dim)] for _ in range(dim)]
    for (s, phase), i in index.items():
        if phase + 1 < G[s]:
            t[i][index[(s, phase + 1)]] = Q(1)
        else:
            for target, weight in enumerate(P[s]):
                t[i][index[(target, 0)]] = weight
    assert dim == 10 and all(sum(row) == 1 for row in t)
    eta = [RHO * PI[s] for s, phase in states]
    assert sum(eta) == 1
    assert all(sum(eta[i] * t[i][j] for i in range(dim)) == eta[j]
               for j in range(dim))
    e = [index[(s, 0)] for s in range(4)]
    return t, e


def finite_cycle_certificate():
    t, e = site_matrix()
    dim = len(t)
    powers = [[[Q(i == j) for j in range(dim)] for i in range(dim)]]
    for _ in range(END):
        powers.append(matrix_mul(powers[-1], t))
    total_checks = 0
    for n in range(START, END + 1):
        z = trace(powers[n])
        assert z > 0
        r = sum((powers[n][i][i] for i in e), Q(0)) / z
        for d in range(1, n // 2 + 1):
            if d == 1:
                probs = (1-2*r, r, r)
            else:
                p11 = sum((powers[d][i][j] * powers[n-d][j][i]
                           for i in e for j in e), Q(0)) / z
                probs = (1-2*r+p11, r-p11, r-p11, p11)
            assert min(probs) > 0, (n, d, probs)
            assert sum(probs) == 1
            c = min(probs)
            for lam in LAMBDAS:
                weight = Q(lam) / c
                assert all(weight * q >= lam for q in probs)
                total_checks += len(probs)
        # The global c_n, not a per-distance c, is used for the actual LP row weights.
        all_probs = [r, 1-2*r]
        for d in range(2, n // 2 + 1):
            p11 = sum((powers[d][i][j] * powers[n-d][j][i]
                       for i in e for j in e), Q(0)) / z
            all_probs.extend((1-2*r+p11, r-p11, p11))
        c_n = min(all_probs)
        assert c_n > 0
        for lam in LAMBDAS:
            scale = Q(lam) / c_n
            assert all(scale * q >= lam for q in all_probs)
        print(f"PASS n={n:2d}: all distances 1..{n//2}, "
              f"lambda=1..5, global c_n={c_n}")
    return total_checks


def main():
    stationary_certificate()
    infinite_distance_certificate()
    print("PASS exact stationary chain and all-distance induction certificate")
    count = finite_cycle_certificate()
    print(f"PASS all tests; {count} local scaled rational inequalities checked")
    print("NOTE: n>30 uses the mathematical spectral/trace proof, not enumeration.")


if __name__ == '__main__':
    main()
