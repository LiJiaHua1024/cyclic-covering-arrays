#!/usr/bin/env python3
"""Solver-free, self-contained C19 exact-value certificate (Python 3 stdlib)."""
from itertools import combinations, product
from time import perf_counter

N = 19
FULL = (1 << N) - 1
UPPER = (
    152745, 150101, 337044, 305834, 86693, 169290, 173349,
    76361, 174738, 346410, 299604, 349522, 43349,
)
EXPECTED_REPS = (
    74901, 74917, 75045, 75093, 76117, 76373,
    76437, 76453, 84565, 84629, 87381,
)


def bit(mask, i):
    return (mask >> (i % N)) & 1


def rotate(mask, k):
    return ((mask << k) | (mask >> (N - k))) & FULL


def incidence(mask, d):
    return sum(1 << i for i in range(N) if bit(mask, i) and bit(mask, i + d))


def valid_suite(suite):
    if len(suite) != len(set(suite)):
        return False
    for mask in suite:
        if mask < 0 or mask > FULL:
            return False
        if any(bit(mask, i) and bit(mask, i + 1) for i in range(N)):
            return False
    for d in range(1, N // 2 + 1):
        for i in range(N):
            for a, b in product((0, 1), repeat=2):
                if d == 1 and a == b == 1:
                    continue
                count = sum(bit(mask, i) == a and bit(mask, i + d) == b
                            for mask in suite)
                if count < 2:
                    return False
    return True


def tight_rows():
    ans = set()
    for length in (7, 8, 9):
        for gaps in product((2, 3), repeat=length):
            if sum(gaps) != N:
                continue
            positions = [0]
            for gap in gaps[:-1]:
                positions.append(positions[-1] + gap)
            base = sum(1 << i for i in positions)
            ans.update(rotate(base, k) for k in range(N))
    return sorted(ans)


def main():
    assert len(UPPER) == 13 and valid_suite(UPPER)
    rows = tight_rows()
    assert len(rows) == 209
    remaining = set(rows)
    classes = []
    while remaining:
        rep = min(remaining)
        orbit = {rotate(rep, k) for k in range(N)}
        assert orbit <= remaining and len(orbit) == N
        classes.append((rep, orbit))
        remaining -= orbit
    assert tuple(rep for rep, _ in classes) == EXPECTED_REPS

    row_index = {mask: j for j, mask in enumerate(rows)}
    group = [next(k for k, (_, orbit) in enumerate(classes) if m in orbit)
             for m in rows]
    profiles = [tuple(incidence(rep, d).bit_count() for d in range(2, 10))
                for rep, _ in classes]
    scored = [sum(incidence(mask, d) << (N * (d - 3))
                  for d in (3, 4, 5)) for mask in rows]
    residual = [sum(incidence(mask, d) << (N * (d - 6))
                    for d in (6, 7, 8, 9)) for mask in rows]

    scored_quota_count = 0
    quotas = []
    for dividers in combinations(range(22), 10):
        cuts = (-1,) + dividers + (22,)
        q = tuple(cuts[k + 1] - cuts[k] - 1 for k in range(11))
        totals = [sum(q[k] * profiles[k][d] for k in range(11))
                  for d in range(8)]
        if totals[:4] != [57, 38, 38, 38]:
            continue
        scored_quota_count += 1
        if all(v >= 38 for v in totals[4:]):
            quotas.append(q)
    assert scored_quota_count == 4300 and len(quotas) == 462

    all_scored = (1 << 57) - 1
    all_residual = (1 << 76) - 1
    nodes = 0

    for quota in quotas:
        allowed = [j for j in range(209) if quota[group[j]]]
        scored_column = [tuple(j for j in allowed if scored[j] >> p & 1)
                         for p in range(57)]
        residual_column = [tuple(j for j in allowed if residual[j] >> p & 1)
                         for p in range(76)]
        first_group = next(k for k, v in enumerate(quota) if v)
        seed = row_index[classes[first_group][0]]
        used = [0] * 11
        used[first_group] = 1
        selected = [seed]

        def dfs(s_once, s_twice, r_once, r_twice, chosen_bits):
            nonlocal nodes
            nodes += 1
            if len(selected) == 12:
                if s_twice == all_scored and r_twice == all_residual:
                    return tuple(rows[j] for j in selected)
                return None

            available = {j for j in allowed
                         if not (chosen_bits >> j & 1)
                         and used[group[j]] < quota[group[j]]
                         and not (scored[j] & s_twice)}
            best = None
            for p in range(57):
                if s_twice >> p & 1:
                    continue
                options = [j for j in scored_column[p] if j in available]
                need = 1 if s_once >> p & 1 else 2
                if len(options) < need:
                    return None
                if best is None or len(options) < len(best):
                    best = options
                if len(best) == 1:
                    break
            if best is None:
                return None
            for p in range(76):
                if r_twice >> p & 1:
                    continue
                options = [j for j in residual_column[p] if j in available]
                need = 1 if r_once >> p & 1 else 2
                if len(options) < need:
                    return None
                if len(options) < len(best):
                    best = options
                if len(best) == 1:
                    break

            for j in best:
                used[group[j]] += 1
                selected.append(j)
                s, r = scored[j], residual[j]
                result = dfs(s_once | s, s_twice | (s_once & s),
                             r_once | r, r_twice | (r_once & r),
                             chosen_bits | (1 << j))
                if result is not None:
                    return result
                selected.pop()
                used[group[j]] -= 1
            return None

        s, r = scored[seed], residual[seed]
        witness = dfs(s, 0, r, 0, 1 << seed)
        if witness is not None:
            print('Necessary-condition 12-row candidate:', witness)
            print('Full covering-array validity:', valid_suite(witness))
            print('DFS nodes:', nodes)
            return

    print('Tight rows:', len(rows), '; rotation orbits:', len(classes))
    print('Scored quotas:', scored_quota_count,
          '; residual-eligible quotas:', len(quotas))
    print('DFS nodes:', nodes)
    print('Verified 13-row witness:', UPPER)
    print('PASS: no 12-row solution on C19; N(19) = 13')


if __name__ == '__main__':
    start = perf_counter()
    main()
    print('Elapsed seconds:', round(perf_counter() - start, 2))
