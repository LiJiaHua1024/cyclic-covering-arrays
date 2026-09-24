#!/usr/bin/env python3
"""C17: exact 12-row exclusion, Python standard library only."""
from itertools import combinations, product

N = 17
FULL = (1 << N) - 1

def rotate(mask, shift):
    return ((mask << shift) | (mask >> (N - shift))) & FULL

def tight_rows():
    found = set()
    for length in (6, 7, 8):
        for gaps in product((2, 3), repeat=length):
            if sum(gaps) != N:
                continue
            positions = [0]
            for gap in gaps[:-1]:
                positions.append(positions[-1] + gap)
            base = sum(1 << i for i in positions)
            found.update(rotate(base, k) for k in range(N))
    return sorted(found)

def incidence(mask, d):
    return sum(1 << i for i in range(N)
               if (mask >> i & 1) and (mask >> ((i + d) % N) & 1))

def solve():
    rows = tight_rows()
    assert len(rows) == 119
    remaining = set(rows)
    orbits = []
    while remaining:
        rep = min(remaining)
        orb = {rotate(rep, k) for k in range(N)}
        assert len(orb) == 17 and orb <= remaining
        orbits.append((rep, orb))
        remaining -= orb
    assert [rep for rep, _ in orbits] == [
        18725, 18773, 19029, 19093, 19109, 21141, 21845
    ]
    group = [next(k for k, (_, orb) in enumerate(orbits) if m in orb)
             for m in rows]
    row_index = {m: i for i, m in enumerate(rows)}
    masks = [[incidence(m, d) for d in range(2, 9)] for m in rows]
    profiles = [[x.bit_count() for x in masks[row_index[rep]]]
                for rep, _ in orbits]
    assert profiles == [
        [1, 5, 0, 2, 4, 0, 3], [4, 3, 3, 2, 4, 2, 3],
        [4, 3, 2, 4, 2, 3, 3], [4, 3, 2, 4, 1, 5, 2],
        [4, 3, 2, 4, 2, 3, 3], [4, 3, 1, 6, 0, 5, 2],
        [7, 1, 6, 2, 5, 3, 4]
    ]
    scored = [sum(masks[j][d - 2] << (N * (d - 3)) for d in (3, 4, 5))
              for j in range(119)]
    residual = [sum(masks[j][d - 2] << (N * (d - 6)) for d in (6, 7, 8))
                for j in range(119)]
    all_pairs = (1 << (3 * N)) - 1
    scored_vectors = 0
    candidates = []
    for dividers in combinations(range(18), 6):
        cuts = (-1,) + dividers + (18,)
        v = tuple(cuts[i + 1] - cuts[i] - 1 for i in range(7))
        totals = [sum(v[k] * profiles[k][d] for k in range(7))
                  for d in range(7)]
        if totals[1:4] != [34, 34, 34]:
            continue
        scored_vectors += 1
        if totals[0] == 51 and min(totals[4:]) >= 34:
            candidates.append(v)
    assert scored_vectors == 139 and len(candidates) == 29

    nodes = 0
    for quota in candidates:
        allowed = [j for j in range(119) if quota[group[j]]]
        columns = [tuple(j for j in allowed if scored[j] >> p & 1)
                   for p in range(3 * N)]
        first_group = next(k for k, q in enumerate(quota) if q)
        first = row_index[orbits[first_group][0]]
        used = [0] * 7
        used[first_group] = 1

        def search(sc_once, sc_twice, rs_once, rs_twice, depth):
            nonlocal nodes
            nodes += 1
            if depth == 12:
                return sc_twice == all_pairs and rs_twice == all_pairs
            active = {j for j in allowed
                      if used[group[j]] < quota[group[j]]
                      and not (scored[j] & sc_twice)}
            best = None
            for p in range(3 * N):
                if sc_twice >> p & 1:
                    continue
                options = [j for j in columns[p] if j in active]
                need = 1 if sc_once >> p & 1 else 2
                if len(options) < need:
                    return False
                if best is None or len(options) < len(best):
                    best = options
                if len(best) == 1:
                    break
            if best is None:
                return False
            for j in best:
                used[group[j]] += 1
                s, r = scored[j], residual[j]
                if search(sc_once | s, sc_twice | (sc_once & s),
                          rs_once | r, rs_twice | (rs_once & r), depth + 1):
                    return True
                used[group[j]] -= 1
            return False

        s, r = scored[first], residual[first]
        if search(s, 0, r, 0, 1):
            raise AssertionError('Found 12 rows: quota=' + repr(quota))
    assert nodes == 54310, nodes
    print('PASS: 119 tight rows; 139 scored orbit vectors;'
          ' 29 residual candidates; 54310 DFS nodes; no 12-row solution')

if __name__ == '__main__':
    solve()
