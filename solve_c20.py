#!/usr/bin/env python3
"""Exact C20 CP-SAT feasibility and exact optimum solver.

Install: pip install ortools
Run:     python solve_c20.py --rows 12 --mode tight
         python solve_c20.py --rows 13 --mode tight
         python solve_c20.py --verify data/solution_c20.txt

Mathematical guarantee:
1. By Theorem [T1], any hypothetical 12-row solution on C20 must consist
   exclusively of tight configurations (cyclic gaps in {2, 3}).
   Therefore, --rows 12 --mode tight returning INFEASIBLE strictly proves N(20) >= 13.
2. --rows 13 --mode tight returning OPTIMAL/FEASIBLE establishes N(20) <= 13.
   Together, these certify N(20) = 13 exactly.
"""

import argparse
import hashlib
from pathlib import Path

N = 20
FULL = (1 << N) - 1


def legal(mask):
    if not 0 <= mask <= FULL:
        return False
    rotated = ((mask << 1) | (mask >> (N - 1))) & FULL
    return (mask & rotated) == 0


def all_legal_rows():
    return [mask for mask in range(1 << N) if legal(mask)]


def transform(mask, sign, shift):
    return sum(1 << ((sign * i + shift) % N)
               for i in range(N) if (mask >> i) & 1)


def canonical(mask):
    return min(transform(mask, sign, shift)
               for sign in (1, -1) for shift in range(N))


def tight(mask):
    positions = [i for i in range(N) if (mask >> i) & 1]
    return bool(positions) and all(
        (positions[(k + 1) % len(positions)] - positions[k]) % N in (2, 3)
        for k in range(len(positions))
    )


def verify_rows(rows):
    """Independent, standard-library-only verifier; raises AssertionError on failure."""
    assert len(rows) == 13, f'Expected exactly 13 rows, got {len(rows)}'
    assert len(set(rows)) == 13, 'Rows must be distinct'
    assert all(legal(mask) for mask in rows), 'A row violates C20 independence'
    checked = 0
    for i in range(N):
        for j in range(i + 1, N):
            adjacent = (j == i + 1 or (i == 0 and j == N - 1))
            patterns = ((0, 0), (0, 1), (1, 0)) if adjacent else (
                (0, 0), (0, 1), (1, 0), (1, 1))
            for a, b in patterns:
                count = sum(((mask >> i) & 1) == a and
                            ((mask >> j) & 1) == b for mask in rows)
                assert count >= 2, (i, j, a, b, count)
                checked += 1
    assert checked == 740, checked
    return checked


def verify_file(filename):
    lines = Path(filename).read_text(encoding='ascii').splitlines()
    assert len(lines) == 13, f'File must have precisely 13 lines, got {len(lines)}'
    assert all(len(line) == N and set(line) <= {'0', '1'} for line in lines), (
        f'Each line must contain precisely {N} binary digits')
    rows = [sum((ch == '1') << i for i, ch in enumerate(line))
            for line in lines]
    return verify_rows(rows)


def build_model(cp_model, mode, legal_rows, m_rows):
    model = cp_model.CpModel()
    x = [[model.NewBoolVar(f'x_{r}_{i}') for i in range(N)]
         for r in range(m_rows)]
    masks = [model.NewIntVar(0, FULL, f'mask_{r}') for r in range(m_rows)]
    for r in range(m_rows):
        model.Add(masks[r] == sum((1 << i) * x[r][i] for i in range(N)))
        for i in range(N):
            model.AddBoolOr((x[r][i].Not(), x[r][(i + 1) % N].Not()))
    for r in range(m_rows - 1):
        model.Add(masks[r] < masks[r + 1])

    allowed = legal_rows if mode == 'full' else [v for v in legal_rows if tight(v)]
    reps = [v for v in allowed if canonical(v) == v]
    model.AddAllowedAssignments(x[0], [tuple((v >> i) & 1 for i in range(N))
                                       for v in reps])
    if mode == 'tight':
        tuples = [tuple((v >> i) & 1 for i in range(N)) for v in allowed]
        for r in range(1, m_rows):
            model.AddAllowedAssignments(x[r], tuples)

    for r in range(m_rows):
        for sign in (1, -1):
            for shift in range(N):
                if r == 0 and sign == 1 and shift == 0:
                    continue
                model.Add(masks[0] <= sum(
                    (1 << ((sign * i + shift) % N)) * x[r][i]
                    for i in range(N)))

    col = [sum(x[r][i] for r in range(m_rows)) for i in range(N)]
    required = 0
    for i in range(N):
        for j in range(i + 1, N):
            adjacent = j == i + 1 or (i == 0 and j == N - 1)
            if adjacent:
                model.Add(col[i] >= 2)
                model.Add(col[j] >= 2)
                model.Add(m_rows - col[i] - col[j] >= 2)
                required += 3
            else:
                both = [model.NewBoolVar(f'and_{r}_{i}_{j}')
                        for r in range(m_rows)]
                for r, z in enumerate(both):
                    model.Add(z <= x[r][i])
                    model.Add(z <= x[r][j])
                    model.Add(z >= x[r][i] + x[r][j] - 1)
                pair = sum(both)
                model.Add(pair >= 2)
                model.Add(col[i] - pair >= 2)
                model.Add(col[j] - pair >= 2)
                model.Add(m_rows - col[i] - col[j] + pair >= 2)
                required += 4

    assert len(legal_rows) == 15127
    assert required == 740
    return model, x, allowed, reps


def solve(args):
    try:
        from ortools.sat.python import cp_model
    except ImportError as exc:
        raise SystemExit('Install OR-Tools first: pip install ortools') from exc

    legal_rows = all_legal_rows()
    assert len(legal_rows) == 15127
    model, x, allowed, reps = build_model(cp_model, args.mode, legal_rows, args.rows)

    try:
        raw_proto = model.Proto().SerializeToString(deterministic=True)
    except AttributeError:
        raw_proto = str(model.Proto()).encode('utf-8')
    digest = hashlib.sha256(raw_proto).hexdigest()

    Path('data').mkdir(exist_ok=True)
    logfile = Path('data') / f'search_c20_{args.mode}_m{args.rows}.log'
    print(f'Rows={args.rows}; Mode={args.mode}; legal={len(legal_rows)}; allowed={len(allowed)}; '
          f'canonical first-row choices={len(reps)}; model SHA256={digest}')

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = 0
    solver.parameters.log_search_progress = True
    solver.parameters.log_to_stdout = False
    if args.time_limit > 0:
        solver.parameters.max_time_in_seconds = args.time_limit

    with logfile.open('w', encoding='utf-8') as log:
        log.write(f'C20 exact feasibility test for M={args.rows}\n'
                  f'mode={args.mode}\nmodel_sha256={digest}\n'
                  f'allowed_rows={len(allowed)}; first_row_reps={len(reps)}\n'
                  f'time_limit_seconds={args.time_limit}; '
                  f'num_search_workers={args.workers}; random_seed=0\n'
                  f'{model.ModelStats()}\n')
        solver.log_callback = lambda text: (log.write(text), log.flush())
        status = solver.Solve(model)
        label = solver.StatusName(status)
        log.write(f'FINAL STATUS: {label}\n{solver.ResponseStats()}\n')

    print(f'{label}; branches={solver.NumBranches()}; '
          f'conflicts={solver.NumConflicts()}; '
          f'wall_time={solver.WallTime():.3f}s; log={logfile}')

    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        rows = [sum(solver.Value(x[r][i]) << i for i in range(N))
                for r in range(args.rows)]
        if args.rows == 13:
            assert verify_rows(rows) == 740
            outfile = Path('data/solution_c20.txt')
            outfile.write_text(''.join(''.join(str((v >> i) & 1)
                                             for i in range(N)) + '\n'
                                       for v in rows), encoding='ascii')
            assert verify_file(outfile) == 740
            print(f'SAT: independent verification passed; witness={outfile}')
        else:
            print(f'SAT: feasible solution of size {args.rows} found: {rows}')
    elif status == cp_model.INFEASIBLE:
        if args.rows == 12 and args.mode == 'tight':
            print('INFEASIBLE: all 277 tight rows excluded for M=12. '
                  'By Theorem [T1], this strictly establishes N(20) >= 13.')
        elif args.mode == 'full':
            print(f'INFEASIBLE: no {args.rows}-row solution exists on C20.')
        else:
            print(f'INFEASIBLE only for tight rows with M={args.rows}.')
    else:
        print('UNKNOWN: neither SAT nor UNSAT was established.')
        raise SystemExit(2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rows', type=int, default=13, choices=(12, 13),
                        help='Number of rows to test (12 or 13, default: 13).')
    parser.add_argument('--mode', choices=('full', 'tight'), default='tight',
                        help='Search mode: tight (gap in {2,3}) or full (all independent sets).')
    parser.add_argument('--time-limit', type=float, default=60,
                        help='Seconds; 0 means no time limit.')
    parser.add_argument('--workers', type=int, default=8,
                        help='Number of CP-SAT search workers (default: 8).')
    parser.add_argument('--verify', metavar='PATH', help='Verify a matrix; no OR-Tools needed.')
    args = parser.parse_args()
    if args.verify:
        print(f'PASS: {verify_file(args.verify)} valid ordered pair-states')
    else:
        assert args.time_limit >= 0
        solve(args)


if __name__ == '__main__':
    main()
