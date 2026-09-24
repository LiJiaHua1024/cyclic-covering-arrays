#!/usr/bin/env python3
"""Exact, solver-free verifier for the C17 boundary analysis and barrier results.

Verifies:
1. The 119 tight rows from {2,3}-gap words partition into 7 rotation orbits of length 17.
2. The 139 non-negative orbit vectors satisfying distance 3, 4, 5 equality counts (each 34).
3. The 29 vectors satisfying distance 6, 7, 8 counts >= 34.
4. An explicit 12-row witness satisfying all distance 3, 4, 5 pairs = 2, c_i = 5, t_i = 3 everywhere,
   proving that Tier 1 (scored equations alone) CANNOT exclude 12 rows on C17.
5. A candidate Gram matrix K with rank_{F_2}(K) = 12, demonstrating that an unconstrained
   F_2 rank argument (Tier 2) fails without realizability/PSD constraints.
6. An integer witness vector z satisfying z^T K z = -6, proving the candidate K is non-PSD.
"""

from itertools import combinations, product
import sys

N = 17
FULL = (1 << N) - 1

def bit(m, i):
    return (m >> (i % N)) & 1

def rotate(m, k):
    return ((m << k) | (m >> (N - k))) & FULL

def pd(m, d):
    return sum(bit(m, i) * bit(m, i + d) for i in range(N))

def equality_rows():
    out = set()
    for length in (6, 7, 8):
        for gaps in product((2, 3), repeat=length):
            if sum(gaps) != N:
                continue
            positions = [0]
            for gap in gaps[:-1]:
                positions.append(positions[-1] + gap)
            m = sum(1 << i for i in positions)
            out.update(rotate(m, k) for k in range(N))
    return out

def main():
    remaining = equality_rows()
    assert len(remaining) == 119, f"Expected 119 tight rows, got {len(remaining)}"
    orbits = []
    while remaining:
        rep = min(remaining)
        orb = {rotate(rep, k) for k in range(N)}
        assert len(orb) == 17
        orbits.append((rep, orb))
        remaining -= orb

    reps = [rep for rep, _ in orbits]
    assert reps == [18725, 18773, 19029, 19093, 19109, 21141, 21845]
    profiles = [tuple(pd(rep, d) for d in range(2, 9)) for rep in reps]

    expected = [
        (1, 5, 0, 2, 4, 0, 3),
        (4, 3, 3, 2, 4, 2, 3),
        (4, 3, 2, 4, 2, 3, 3),
        (4, 3, 2, 4, 1, 5, 2),
        (4, 3, 2, 4, 2, 3, 3),
        (4, 3, 1, 6, 0, 5, 2),
        (7, 1, 6, 2, 5, 3, 4),
    ]
    assert profiles == expected

    scored_counts = []
    residual_counts = []
    for dividers in combinations(range(18), 6):
        cuts = (-1,) + dividers + (18,)
        v = tuple(cuts[i + 1] - cuts[i] - 1 for i in range(7))
        assert sum(v) == 12
        totals = [sum(v[j] * profiles[j][k] for j in range(7))
                  for k in range(7)]
        if totals[1:4] != [34, 34, 34]:
            continue
        scored_counts.append(v)
        if totals[0] == 51 and all(x >= 34 for x in totals[4:]):
            residual_counts.append(v)

    assert len(scored_counts) == 139, f"Expected 139, got {len(scored_counts)}"
    assert len(residual_counts) == 29, f"Expected 29, got {len(residual_counts)}"

    witness = [
        18761, 21797, 37450, 38229, 42325, 43602,
        43689, 74900, 76074, 84644, 86674, 87210,
    ]
    assert len(witness) == len(set(witness)) == 12
    assert set(witness) <= equality_rows()
    assert all(sum(bit(m, i) for m in witness) == 5 for i in range(N))
    assert all(
        sum(bit(m, i) * bit(m, i + 2) for m in witness) == 3
        for i in range(N)
    )
    assert all(
        sum(bit(m, i) * bit(m, i + d) for m in witness) == 2
        for d in (3, 4, 5) for i in range(N)
    )
    assert sum(pd(m, 7) for m in witness) == 27, "Witness distance 7 count mismatch"

    v = (3, 0, 0, 5, 0, 0, 4)
    assert v in residual_counts
    assert tuple(sum(v[j] * profiles[j][k] for j in range(7))
                 for k in (4, 5, 6)) == (37, 37, 35)

    edges = [
        (6, 7), (6, 8), (6, 9),
        (7, 2), (7, 1), (7, 3),
        (8, 14),
    ]
    K = [[2 for _ in range(N)] for _ in range(N)]
    for i in range(N):
        K[i][i] = 5
        K[i][(i + 1) % N] = K[i][(i - 1) % N] = 0
        K[i][(i + 2) % N] = K[i][(i - 2) % N] = 3
    for d, i in edges:
        j = (i + d) % N
        K[i][j] += 1
        K[j][i] += 1

    def rank_gf2(matrix):
        rows = [sum((entry & 1) << j for j, entry in enumerate(row))
                for row in matrix]
        rank = 0
        for col in range(N):
            pivot = next((r for r in range(rank, N)
                          if (rows[r] >> col) & 1), None)
            if pivot is None:
                continue
            rows[rank], rows[pivot] = rows[pivot], rows[rank]
            for r in range(rank + 1, N):
                if (rows[r] >> col) & 1:
                    rows[r] ^= rows[rank]
            rank += 1
        return rank

    assert rank_gf2(K) == 12, "Expected rank 12 on candidate K"
    z = [0, -1, -2, -1, 0, 1, 0, 0, 2, 2, 1, 0, 0, -1, -2, -1, 0]
    quad_form = sum(z[i] * K[i][j] * z[j] for i in range(N) for j in range(N))
    assert quad_form == -6, f"Expected quad form -6, got {quad_form}"

    print("PASS: C17 boundary analysis verified:")
    print("      - Tier 1: 12-row witness satisfies distances 3,4,5 (sum(P_7) = 27 < 34).")
    print("      - Tier 2: rank_F2(K) = 12 candidate constructed, but z^T K z = -6 (non-PSD).")
    print("      - Boundary 12 <= N(17) <= 13 remains strict open target.")

if __name__ == '__main__':
    main()
