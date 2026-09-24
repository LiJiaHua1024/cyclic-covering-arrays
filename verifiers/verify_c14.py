#!/usr/bin/env python3
"""Self-contained exact audit of the specific C_14, index-2, distinct-row theorem.

Uses only Python's standard library. Does not import the supplied verify14.py,
read its PASS report, or require the three missing original JSON input files.
Run: python independent_verify14.py
Optional: --solution solution14.txt --out audit.json --tables tables
"""
from __future__ import annotations
import argparse
import csv
import json
import sys
from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path

N = 14
ROW_CAP = 56
PAIRS = tuple(combinations(range(N), 2))
SOLUTION = '''10101010010100
10010101010100
01001000010010
10100101010010
01010101001010
10010010101010
10101010101010
00101001001001
01010100101001
00100100100101
01001010100101
01010010010101
01001001010101'''.splitlines()
# (i, j, state at i, state at j, coefficient), transcribed from proof_zh.md.
Q_TERMS = [
    (0,7,1,1,2), (3,13,1,1,2), (5,12,1,1,2), (7,9,0,1,2),
    (6,10,1,1,3), (2,6,1,1,1), (5,7,0,1,1), (9,13,1,1,1),
    (0,9,1,1,-2), (0,10,1,1,-2), (1,6,1,1,-2), (6,13,1,1,-2),
    (1,5,1,1,-1), (1,11,1,1,-1), (2,9,1,1,-1), (3,10,1,1,-1),
    (4,8,1,1,-1), (4,13,1,1,-1), (7,12,1,1,-1),
]
SEEDS = ('10100100100100', '10101010100100',
         '10101001010100', '10101010101010')

class AuditError(Exception):
    pass

def check(ok: bool, message: str) -> None:
    if not ok:
        raise AuditError(message)

def bit(m: int, i: int) -> int:
    return (m >> i) & 1

def text(m: int) -> str:
    # Bit i denotes x_i; do not use the conventional opposite display order.
    return ''.join(str(bit(m, i)) for i in range(N))

def mask(s: str) -> int:
    check(len(s) == N and set(s) <= {'0','1'}, f'Invalid 14-bit row: {s!r}')
    return sum((c == '1') << i for i, c in enumerate(s))

def legal(m: int) -> bool:
    rotated = ((m << 1) & ((1 << N) - 1)) | (m >> (N - 1))
    return (m & rotated) == 0

def distance(i: int, j: int) -> int:
    return min(j-i, N-(j-i))

def event_weight(i: int, j: int, a: int, b: int) -> int:
    d = distance(i, j)
    if d == 1 and a == b == 0:
        return 1
    if d == 2 and a != b:
        return 1
    if a == b == 1:
        return {3:10, 4:8, 5:2, 7:2}.get(d, 0)
    return 0

def score(m: int) -> int:
    counts = Counter((distance(i,j), bit(m,i), bit(m,j)) for i,j in PAIRS)
    return (counts[1,0,0] + counts[2,0,1] + counts[2,1,0]
            + 10*counts[3,1,1] + 8*counts[4,1,1]
            + 2*counts[5,1,1] + 2*counts[7,1,1])

def q_formula(m: int) -> int:
    p = lambda i,j: bit(m,i) * bit(m,j)
    q = lambda i,j: (1-bit(m,i)) * bit(m,j)
    return (2*(p(0,7)+p(3,13)+p(5,12)+q(7,9)) + 3*p(6,10)
            + p(2,6)+q(5,7)+p(9,13)
            - 2*(p(0,9)+p(0,10)+p(1,6)+p(6,13))
            - (p(1,5)+p(1,11)+p(2,9)+p(3,10)+p(4,8)+p(4,13)+p(7,12)))

def hit(m: int, req: tuple[int,int,int,int]) -> bool:
    i,j,a,b = req
    return bit(m,i) == a and bit(m,j) == b

def orbit(seed: str) -> set[int]:
    return {mask(seed[k:] + seed[:k]) for k in range(N)}

def audit(strings: list[str], tables: Path | None = None) -> dict:
    rows = [mask(s) for s in strings]
    check(len(rows) == 13, 'Expected exactly 13 construction rows')
    check(len(set(rows)) == len(rows), 'Duplicate complete row')
    check(all(legal(m) for m in rows), 'Illegal adjacency, including edge (13,0)')

    # Verify the bit-mask legality test against a separately written test on the
    # entire binary domain; then enumerate every legal configuration.
    for m in range(1 << N):
        direct = all(bit(m,i) + bit(m,(i+1)%N) <= 1 for i in range(N))
        check(legal(m) == direct, 'Bit-mask / direct legality disagreement')
    universe = [m for m in range(1 << N) if legal(m)]
    reqs = sorted({(i,j,bit(m,i),bit(m,j)) for m in universe for i,j in PAIRS})
    formula_reqs = {(i,j,a,b) for i,j in PAIRS for a in (0,1) for b in (0,1)
                    if not (distance(i,j)==1 and a==b==1)}
    check(set(reqs) == formula_reqs, 'Projection / closed-form demand disagreement')
    check(len(universe)==843 and len(reqs)==350, 'Unexpected domain counts')
    witnesses = {r:[k+1 for k,m in enumerate(rows) if hit(m,r)] for r in reqs}
    counts = {r:len(ids) for r,ids in witnesses.items()}
    check(min(counts.values()) >= 2, 'Some extendible interaction has coverage < 2')
    erasure_minima = [min(counts[r]-int(hit(m,r)) for r in reqs) for m in rows]
    check(min(erasure_minima) >= 1, 'Single-row erasure property fails')

    scores = {m:score(m) for m in universe}
    for m in universe:
        check(scores[m] == sum(event_weight(i,j,bit(m,i),bit(m,j)) for i,j in PAIRS),
              'Two definitions of S disagree')
    check(max(scores.values()) <= ROW_CAP, 'False all-row score cap')
    weights = {r:event_weight(*r) for r in reqs}
    check(all(w >= 0 for w in weights.values()), 'Negative lower-bound weight')
    demand = 2 * sum(weights.values())
    check(ROW_CAP > 0 and demand % ROW_CAP == 0, 'Equality argument not applicable')
    equality_n = demand // ROW_CAP
    check(equality_n == 12, 'Unexpected preliminary lower bound')
    tight = [m for m in universe if scores[m] == ROW_CAP]
    check(len(tight) == 37, 'Unexpected equality-row count')
    orbits = [orbit(s) for s in SEEDS]
    check(sum(map(len,orbits)) == len(set().union(*orbits)) == len(tight),
          'Orbit description overlaps or has wrong size')
    check(set().union(*orbits) == set(tight), 'Orbit list is not the full equality set')

    # At N=12 every positively weighted INDIVIDUAL interaction must be covered
    # exactly twice. Thus any supported integer combination has forced sum
    # twice the sum of its coefficients, even if some coefficients are negative.
    check(len({t[:4] for t in Q_TERMS}) == len(Q_TERMS), 'Duplicate Q term')
    check(all(t[:4] in weights and weights[t[:4]]>0 for t in Q_TERMS),
          'Q uses an interaction outside the positive-weight support')
    for m in universe:
        check(q_formula(m) == sum(c for i,j,a,b,c in Q_TERMS if hit(m,(i,j,a,b))),
              'Literal Q formula / coefficient list disagreement')
    coefficient_sum = sum(t[4] for t in Q_TERMS)
    forced_q_sum = 2 * coefficient_sum
    alternators = {mask('10101010101010'), mask('01010101010101')}
    check(alternators <= set(tight), 'Alternating rows are not equality rows')
    check(all(q_formula(m)%7 == int(m in alternators) for m in tight),
          'Original modulo-7 identity fails')
    possible_h = set(range(len(alternators)+1))  # distinct complete rows
    check(forced_q_sum%7 not in {h%7 for h in possible_h},
          'Modulo-7 identity yields no contradiction')

    # Additional simplification found in this audit: on the 37 equality rows,
    # Q is 0 on 34, -7 on one, and +1 on each alternating row.
    expected_nonzero = {mask('01001010100101'):-7,
                        mask('10101010101010'):1,
                        mask('01010101010101'):1}
    check(all(q_formula(m) == expected_nonzero.get(m,0) for m in tight),
          'Exact three-row Q simplification fails')
    subset_sums = {0}
    for m in tight:
        value = q_formula(m)
        subset_sums |= {s+value for s in tuple(subset_sums)}
    check(forced_q_sum not in subset_sums,
          'Exact subset-sum check yields no contradiction')
    strict_lower = equality_n + 1
    check(strict_lower == len(rows), 'Proven upper and lower bounds do not coincide')

    # New symmetric LP witness, not the absent original 28-row witness.
    # Each row in an orbit gets its indicated rational mass. No LP solver is used.
    orbit_masses = (Fraction(3,14),Fraction(5,14),Fraction(3,7),Fraction(1,2))
    masses = {m:f for orb,f in zip(orbits,orbit_masses) for m in orb}
    check(all(0 < f <= 1 for f in masses.values()), 'Invalid LP variable bounds')
    lp_total = sum(masses.values(), Fraction())
    lp_min = min(sum((f for m,f in masses.items() if hit(m,r)),Fraction()) for r in reqs)
    check(lp_total == equality_n and lp_min >= 2, 'New rational LP witness fails')
    lp_rows = [{'row':text(m),'numerator':f.numerator,'denominator':f.denominator}
               for m,f in sorted(masses.items(),key=lambda item:text(item[0]))]

    report = {
        'status':'PASS', 'n':N, 'binary_rows_examined':1<<N,
        'legal_rows':len(universe), 'extendible_requirements':len(reqs),
        'construction_size':len(rows), 'row_distinct':True,
        'minimum_coverage':min(counts.values()),
        'coverage_histogram':dict(sorted(Counter(counts.values()).items())),
        'single_row_erasure_minima':erasure_minima,
        'weighted_demand':demand, 'row_score_cap':max(scores.values()),
        'tight_rows':len(tight), 'tight_orbit_sizes':list(map(len,orbits)),
        'Q_terms':len(Q_TERMS), 'Q_coefficient_sum':coefficient_sum,
        'forced_Q_sum_if_12_rows':forced_q_sum,
        'tight_Q_histogram':dict(sorted(Counter(q_formula(m) for m in tight).items())),
        'nonzero_Q_rows':{text(m):v for m,v in expected_nonzero.items()},
        'all_possible_Q_sums_for_distinct_subsets_of_tight_rows':sorted(subset_sums),
        'original_modulo_7_certificate':'PASS', 'exact_three_row_simplification':'PASS',
        'strict_lower_bound':strict_lower, 'upper_bound':len(rows),
        'optimum':strict_lower, 'gap':len(rows)-strict_lower,
        'new_symmetric_LP_witness':{'objective':str(lp_total),'support_size':len(masses),
                                    'minimum_coverage':str(lp_min)},
        'example_first_and_third_switch':{
            f'{a}{b}':witnesses[0,2,a,b] for a in (0,1) for b in (0,1)},
        'verification_arithmetic':'integers; Fraction for the separate LP witness',
        'uses_optimization_solver':False,
        'imports_supplied_verifier':False,
        'reads_supplied_PASS_report':False,
    }
    if tables is not None:
        tables.mkdir(parents=True,exist_ok=True)
        with (tables/'coverage.tsv').open('w',newline='',encoding='utf-8') as f:
            writer=csv.writer(f,delimiter='\t')
            writer.writerow(('i','j','a','b','coverage','test_ids_1_based'))
            for r in reqs:
                writer.writerow((*r,counts[r],','.join(map(str,witnesses[r]))))
        with (tables/'all_legal_rows.tsv').open('w',newline='',encoding='utf-8') as f:
            writer=csv.writer(f,delimiter='\t')
            writer.writerow(('x0_to_x13','ones','S','tight','Q','Q_mod_7'))
            for m in sorted(universe,key=text):
                writer.writerow((text(m),m.bit_count(),scores[m],int(m in tight),
                                 q_formula(m),q_formula(m)%7))
        lp={'provenance':'New symmetric 37-row witness reconstructed in this audit; '
                          'not the absent original 28-row witness.',
            'n':N,'index':2,'rows':lp_rows}
        (tables/'new_symmetric_lp_witness14.json').write_text(
            json.dumps(lp,indent=2)+'\n',encoding='utf-8')
    return report

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--solution',type=Path)
    parser.add_argument('--out',type=Path)
    parser.add_argument('--tables',type=Path)
    args=parser.parse_args()
    try:
        rows = args.solution.read_text(encoding='utf-8').split() if args.solution else SOLUTION
        report=audit(rows,args.tables)
        output=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
        if args.out:
            args.out.parent.mkdir(parents=True,exist_ok=True)
            args.out.write_text(output,encoding='utf-8')
        print(output,end='')
        return 0
    except (AuditError,OSError,ValueError,KeyError,TypeError) as exc:
        print(f'FAIL: {exc}',file=sys.stderr)
        return 1

if __name__=='__main__':
    raise SystemExit(main())
