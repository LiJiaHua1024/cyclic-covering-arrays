#!/usr/bin/env python3
"""Exact CP-SAT solver for general cycle Cn with tight rows."""

import argparse
import sys
from itertools import combinations
from pathlib import Path
from ortools.sat.python import cp_model


def gen_tight_masks(n):
    tight_masks = set()
    for b in range(n // 3 + 1):
        rem = n - 3 * b
        if rem % 2 == 0:
            a = rem // 2
            k = a + b
            for combo in combinations(range(k), b):
                gaps = [3 if i in combo else 2 for i in range(k)]
                for start in range(n):
                    mask = 0
                    cur = start
                    for g in gaps:
                        mask |= (1 << cur)
                        cur = (cur + g) % n
                    tight_masks.add(mask)
    return sorted(tight_masks)


def transform(mask, sign, shift, n):
    return sum(1 << ((sign * i + shift) % n) for i in range(n) if (mask >> i) & 1)


def canonical(mask, n):
    return min(transform(mask, sign, shift, n) for sign in (1, -1) for shift in range(n))


def build_model(n, m_rows, workers=8, time_limit=180):
    full = (1 << n) - 1
    allowed = gen_tight_masks(n)
    reps = [v for v in allowed if canonical(v, n) == v]

    model = cp_model.CpModel()
    x = [[model.NewBoolVar(f'x_{r}_{i}') for i in range(n)] for r in range(m_rows)]
    masks = [model.NewIntVar(0, full, f'mask_{r}') for r in range(m_rows)]

    for r in range(m_rows):
        model.Add(masks[r] == sum((1 << i) * x[r][i] for i in range(n)))
        for i in range(n):
            model.AddBoolOr((x[r][i].Not(), x[r][(i + 1) % n].Not()))

    for r in range(m_rows - 1):
        model.Add(masks[r] < masks[r + 1])

    tuples = [tuple((v >> i) & 1 for i in range(n)) for v in allowed]
    model.AddAllowedAssignments(x[0], [tuple((v >> i) & 1 for i in range(n)) for v in reps])
    for r in range(1, m_rows):
        model.AddAllowedAssignments(x[r], tuples)

    for r in range(m_rows):
        for sign in (1, -1):
            for shift in range(n):
                if r == 0 and sign == 1 and shift == 0:
                    continue
                model.Add(masks[0] <= sum((1 << ((sign * i + shift) % n)) * x[r][i] for i in range(n)))

    col = [sum(x[r][i] for r in range(m_rows)) for i in range(n)]
    for d in range(1, n // 2 + 1):
        for i in range(n):
            j = (i + d) % n
            if d == 1:
                model.Add(col[i] >= 2)
                model.Add(col[j] >= 2)
                model.Add(m_rows - col[i] - col[j] >= 2)
            else:
                both = [model.NewBoolVar(f'and_{r}_{i}_{j}') for r in range(m_rows)]
                for r, z in enumerate(both):
                    model.Add(z <= x[r][i])
                    model.Add(z <= x[r][j])
                    model.Add(z >= x[r][i] + x[r][j] - 1)
                pair = sum(both)
                model.Add(pair >= 2)
                model.Add(col[i] - pair >= 2)
                model.Add(col[j] - pair >= 2)
                model.Add(m_rows - col[i] - col[j] + pair >= 2)

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = workers
    if time_limit > 0:
        solver.parameters.max_time_in_seconds = time_limit

    status = solver.Solve(model)
    return solver, status, x


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=22)
    parser.add_argument('--rows', type=int, default=13)
    parser.add_argument('--workers', type=int, default=8)
    parser.add_argument('--time-limit', type=int, default=180)
    args = parser.parse_args()

    n = args.n
    print(f"Solving C{n} with M={args.rows} rows (tight mode)...")
    solver, status, x = build_model(n, args.rows, args.workers, args.time_limit)
    status_name = solver.StatusName(status)
    print(f"Result for C{n} M={args.rows}: {status_name} (time={solver.WallTime():.2f}s)")

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        solution_rows = [sum(solver.Value(x[r][i]) << i for i in range(n)) for r in range(args.rows)]
        print(f"Found solution with {args.rows} rows: {solution_rows}")
        out_path = Path(f"data/solution_c{n}.txt")
        with out_path.open("w", encoding="ascii") as f:
            for v in solution_rows:
                f.write(''.join(str((v >> i) & 1) for i in range(n)) + '\n')
        print(f"Written to {out_path}")


if __name__ == '__main__':
    main()
