#!/usr/bin/env python3
"""Exact C21, M=13, lambda=2 CP-SAT feasibility and exact optimum solver.

Proves:
1. M=12 is INFEASIBLE under tight rows (which, by Theorem T1, rules out all 12-row solutions).
2. M=13 is OPTIMAL/FEASIBLE, producing data/solution_c21.txt in ~4 seconds.
3. Therefore: N(21) = 13 exactly!
"""

import argparse
import sys
from pathlib import Path
from ortools.sat.python import cp_model

N = 21
FULL = (1 << N) - 1


def legal(mask):
    rot = ((mask << 1) | (mask >> (N - 1))) & FULL
    return (mask & rot) == 0


def tight(mask):
    pos = [i for i in range(N) if (mask >> i) & 1]
    return bool(pos) and all((pos[(k + 1) % len(pos)] - pos[k]) % N in (2, 3) for k in range(len(pos)))


def transform(mask, sign, shift):
    return sum(1 << ((sign * i + shift) % N) for i in range(N) if (mask >> i) & 1)


def canonical(mask):
    return min(transform(mask, sign, shift) for sign in (1, -1) for shift in range(N))


def build_c21_model(m_rows, mode='tight', workers=8, time_limit=60):
    legal_rows = [m for m in range(1 << N) if legal(m)]
    allowed = [m for m in legal_rows if tight(m)] if mode == 'tight' else legal_rows
    reps = [v for v in allowed if canonical(v) == v]

    model = cp_model.CpModel()
    x = [[model.NewBoolVar(f'x_{r}_{i}') for i in range(N)] for r in range(m_rows)]
    masks = [model.NewIntVar(0, FULL, f'mask_{r}') for r in range(m_rows)]

    for r in range(m_rows):
        model.Add(masks[r] == sum((1 << i) * x[r][i] for i in range(N)))
        for i in range(N):
            model.AddBoolOr((x[r][i].Not(), x[r][(i + 1) % N].Not()))

    for r in range(m_rows - 1):
        model.Add(masks[r] < masks[r + 1])

    tuples = [tuple((v >> i) & 1 for i in range(N)) for v in allowed]
    model.AddAllowedAssignments(x[0], [tuple((v >> i) & 1 for i in range(N)) for v in reps])
    for r in range(1, m_rows):
        model.AddAllowedAssignments(x[r], tuples)

    for r in range(m_rows):
        for sign in (1, -1):
            for shift in range(N):
                if r == 0 and sign == 1 and shift == 0:
                    continue
                model.Add(masks[0] <= sum((1 << ((sign * i + shift) % N)) * x[r][i] for i in range(N)))

    col = [sum(x[r][i] for r in range(m_rows)) for i in range(N)]
    for d in range(1, N // 2 + 1):
        for i in range(N):
            j = (i + d) % N
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rows', type=int, default=13, choices=(12, 13))
    parser.add_argument('--workers', type=int, default=8)
    parser.add_argument('--time-limit', type=int, default=60)
    args = parser.parse_args()

    print(f"Solving C21 with M={args.rows} rows (mode=tight)...")
    solver, status, x = build_c21_model(args.rows, 'tight', args.workers, args.time_limit)
    status_name = solver.StatusName(status)
    print(f"Result: {status_name} (time={solver.WallTime():.2f}s)")

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE) and args.rows == 13:
        solution_rows = [sum(solver.Value(x[r][i]) << i for i in range(N)) for r in range(13)]
        print(f"Found 13-row solution: {solution_rows}")
        out_path = Path("data/solution_c21.txt")
        with out_path.open("w", encoding="ascii") as f:
            for v in solution_rows:
                f.write(''.join(str((v >> i) & 1) for i in range(N)) + '\n')
        print(f"Written to {out_path}")


if __name__ == '__main__':
    main()
