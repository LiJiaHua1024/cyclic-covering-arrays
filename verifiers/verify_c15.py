#!/usr/bin/env python3
"""Exact, solver-free verifier for the C15 integrality gap and GF(2) rank certificate.

Verifies:
1. Classification of all 68 tight rows from {2,3}-gap words into 6 rotation orbits.
2. The GF(2) rank certificate across all 4823 edge combinations, proving rank >= 13.
3. Rational LP=12 witness using exact fractions on all pairwise demands.
4. Explicit 13-row integer solution validity and coverage >= 2.
"""

from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
import sys

N = 15
FULL = (1 << N) - 1

def bit(m, i):
    return (m >> (i % N)) & 1

def rotate(m, k):
    return ((m << k) | (m >> (N-k))) & FULL

def orbit(m):
    return {rotate(m, k) for k in range(N)}

def legal(m):
    return 0 <= m <= FULL and all(
        not (bit(m, i) and bit(m, i+1)) for i in range(N)
    )

def pd(m, d):
    return sum(bit(m, i) * bit(m, i+d) for i in range(N))

def tight_from_gaps():
    ans = set()
    for length in (5, 6, 7):
        for gaps in product((2, 3), repeat=length):
            if sum(gaps) != N:
                continue
            positions, place = [0], 0
            for gap in gaps[:-1]:
                place += gap
                positions.append(place)
            row = sum(1 << i for i in positions)
            ans.update(orbit(row))
    return ans

def check_orbits():
    reps = (4681, 4693, 4757, 4773, 5285, 5461)
    sizes = (3, 15, 15, 15, 5, 15)
    profiles = (
        (5,0,0,5,0), (3,2,2,3,2), (3,1,4,1,3),
        (3,1,4,1,3), (3,0,6,0,3), (1,5,2,4,3)
    )
    classes = [orbit(m) for m in reps]
    assert [len(c) for c in classes] == list(sizes), "Orbit size mismatch"
    assert all(classes[i].isdisjoint(classes[j])
               for i in range(6) for j in range(i+1, 6)), "Orbits not disjoint"
    assert set().union(*classes) == tight_from_gaps(), "Orbits do not cover all tight rows"
    assert [tuple(pd(m, d) for d in (3,4,5,6,7))
            for m in reps] == list(profiles), "Profile mismatch"
    assert len(tight_from_gaps()) == 68, "Tight row count != 68"
    assert all(legal(m) for m in tight_from_gaps()), "Illegal tight row"

def rank_gf2(rows):
    rows = rows[:]
    rank = 0
    for col in range(N):
        pivot = next((r for r in range(rank, N)
                      if (rows[r] >> col) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for r in range(N):
            if r != rank and ((rows[r] >> col) & 1):
                rows[r] ^= rows[rank]
        rank += 1
    return rank

def check_rank_certificate():
    baseline = [
        (1 << i) | (1 << ((i+2) % N)) | (1 << ((i-2) % N))
        for i in range(N)
    ]
    histogram = Counter()
    for size in (3, 4, 5):
        for chosen in combinations(range(N), size):
            rows = baseline[:]
            for i in chosen:
                j = (i+6) % N
                rows[i] ^= 1 << j
                rows[j] ^= 1 << i
            rank = rank_gf2(rows)
            assert rank >= 13, f"Rank {rank} < 13 for chosen={chosen}"
            histogram[(size, rank)] += 1
    assert sum(histogram.values()) == 4823, f"Expected 4823 cases, got {sum(histogram.values())}"
    return histogram

def check_upper_and_lp():
    upper = [
        5285,5449,9514,9557,10834,10901,10921,
        18724,18762,21060,21162,21650,21842
    ]
    assert len(upper) == len(set(upper)) == 13, "Upper bound not 13 distinct rows"
    assert all(legal(m) for m in upper), "Illegal upper row"

    weights = {}
    for rep, weight in (
        (4693,Q(2,5)), (4757,Q(1,10)),
        (4773,Q(1,10)), (5461,Q(1,5))
    ):
        for m in orbit(rep):
            assert m not in weights
            weights[m] = weight
    assert sum(weights.values()) == 12, "LP total weight != 12"
    assert all(legal(m) and 0 <= w <= 1
               for m,w in weights.items()), "Invalid LP weights"

    for i,j in combinations(range(N), 2):
        adjacent = j == i+1 or (i,j) == (0,N-1)
        for a,b in product((0,1), repeat=2):
            if adjacent and a == b == 1:
                continue
            match = lambda m: bit(m,i) == a and bit(m,j) == b
            assert sum(match(m) for m in upper) >= 2, f"Upper fails pair ({i},{j}) = ({a},{b})"
            assert sum(w for m,w in weights.items()
                       if match(m)) >= 2, f"LP fails pair ({i},{j}) = ({a},{b})"

if __name__ == "__main__":
    check_orbits()
    histogram = check_rank_certificate()
    check_upper_and_lp()
    print("PASS: C15 exact orbit classification (68 tight rows);")
    print("      GF(2) rank certificate (all 4823 cases rank >= 13);")
    print("      rational LP=12 witness; explicit 13-row upper bound.")
    print("      Rank histogram:", dict(sorted(histogram.items())))
