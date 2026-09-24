# Exact Bounds, Integrality Gaps, and Asymptotic Limits for Cyclic Constrained Covering Arrays

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Verification: PASS](https://img.shields.io/badge/Verification-ALL%20PASS-brightgreen.svg)]()

This repository contains the unified research monograph, exact mechanical certificates, and verification software for index-2 ($\lambda=2$) constrained covering arrays on cycle topologies $C_n$ avoiding adjacent active switches.

---

## 1. Executive Summary of Core Theorems

| Proposition | Scope | Main Mathematical Statement | Verification |
|---|---|---|---|
| **[T1] Universal Lower Bound** | All $n \ge 11$ | $3P_3(x) + 2P_4(x) + P_5(x) \le n \implies LP(n) \ge 12, N(n) \ge 12$ | Exact potential proof |
| **[T2] $C_{13}$ Integrality Gap** | $n = 13$ | $LP(13) = 12, N(13) = 13$ (infeasible even with row repeats) | `verify_c13.py` |
| **[T3] $C_{14}$ Exact Optimum** | $n = 14$ | $LP(14) = 12, N(14) = 13$ (modulo 7 & subset-sum obstruction) | `verify_c14.py` (DOI: `10.5281/zenodo.22918432`) |
| **[T4] $C_{15}$ Exact Optimum** | $n = 15$ | $LP(15) = 12, N(15) = 13$ ($\mathbb{F}_2$ rank obstruction on Gram matrix) | `verify_c15.py` |
| **[T5] Asymptotic LP Limit** | $n \to \infty$ | $\displaystyle\lim_{n \to \infty} LP(n) = 12$, with rate $12 \le LP(n) \le 12 + C\theta^n$ | `verify_markov_chain.py` |
| **[T6] Asymptotic Gap Divergence** | $n \to \infty$ | $N(n) = \Theta(\log n) \implies G(n) = N(n) - LP(n) \to \infty$ | Coding theory / Lovász Local Lemma |
| **[T7] $C_{17}$ Exact Optimum** | $n = 17$ | $LP(17) = 12, N(17) = 13$ (54,310-node exact DFS exclusion) | `verify_c17.py` |
| **[T8] $C_{19}$ Exact Optimum** | $n = 19$ | $LP(19) = 12, N(19) = 13$ (726,693-node exact DFS exclusion); odd jump threshold $n^* \ge 21$ | `verify_c19.py` |
| **[T9] Continuous Plateau $[13, 21]$** | $n \in [13, 21]$ | $N(n) = 13$ for all 9 consecutive integers ($C_{16}, C_{18}, C_{20}, C_{21}$ exact witnesses); global threshold $n^* \ge 22$ | `verify_even_cycles_and_c21.py` |
| **[T10] $C_{21}$ Exact Optimum** | $n = 21$ | $LP(21) = 12, N(21) = 13$ (CP-SAT tight exclusion & explicit 13-row witness) | `verify_even_cycles_and_c21.py`, `solve_c21.py` |
| **[T11] $C_{20}$ Exact Optimum** | $n = 20$ | $LP(20) = 12, N(20) = 13$ (CP-SAT tight exclusion & explicit 13-row witness) | `verify_even_cycles_and_c21.py`, `solve_c20.py` |

---

## 2. One-Click Mechanical Verification

All theorems with finite or Markovian certificates run using standard Python (zero external dependencies):

```bash
python verifiers/verify_all.py
```

To run individual verifiers:
- **Markov Chain Convergence**: `python verifiers/verify_markov_chain.py`
- **$C_{13}$ Integrality Gap**: `python verifiers/verify_c13.py`
- **$C_{14}$ Exact Certificate**: `python verifiers/verify_c14.py`
- **$C_{15}$ $\mathbb{F}_2$ Rank Certificate**: `python verifiers/verify_c15.py`
- **$C_{17}$ Exact DFS Certificate**: `python verifiers/verify_c17.py`
- **$C_{19}$ Exact DFS Certificate**: `python verifiers/verify_c19.py`
- **Even Cycles ($C_{16}, C_{18}, C_{20}$) & $C_{21}$ 13-Row Bounds**: `python verifiers/verify_even_cycles_and_c21.py`
- **$C_{20}$ Exact CP-SAT Solver**: `python solve_c20.py --mode tight`
- **$C_{21}$ Exact CP-SAT Solver**: `python solve_c21.py`

---

## 3. Repository Architecture

```text
├── theorem_ledger.md           # Single Source of Truth for all propositions
├── solve_c20.py                # C20 exact CP-SAT solver and verifier
├── manuscript/                 # Full monograph chapters
│   ├── 01_introduction.md      # Model, Lucas numbers, D_n, and small n infeasibility
│   ├── 02_universal_lower_bound.md # Universal potential inequality (LP >= 12)
│   ├── 03_finite_cases.md      # C13, C14, C15, C17, C19 exact certificates & obstructions
│   ├── 04_asymptotic_lp_limit.md # 2-step gap Markov chain proof (lim LP = 12)
│   ├── 05_integer_complexity.md # N(n) = Theta(log n) and unbounded gap divergence
│   └── 06_open_problems.md     # Plateau [13, 20], C21 frontier, and threshold n* >= 21
├── verifiers/                  # Self-contained Python verifiers
│   ├── verify_all.py           # Master runner (runs all 7 verifiers)
│   ├── verify_markov_chain.py  # Rational arithmetic Markov recurrence
│   ├── verify_c13.py           # C13 exact certificate
│   ├── verify_c14.py           # C14 exact certificate
│   ├── verify_c15.py           # C15 GF(2) rank certificate
│   ├── verify_c17.py           # C17 exact 54,310-node DFS exclusion
│   ├── verify_c17_boundary.py  # C17 barrier analysis (witness & Gram non-PSD)
│   ├── verify_c19.py           # C19 exact 726,693-node DFS exclusion
│   └── verify_even_cycles_and_c21.py # C16, C18, C20, C21 suites & 2-row repair check
├── data/                       # Concrete test suite constructions
│   ├── solution_c13.txt        # 13x13 binary matrix
│   ├── solution_c14.txt        # 13x14 binary matrix
│   ├── solution_c15.txt        # 13x15 binary matrix
│   ├── solution_c16.txt        # 13x16 binary matrix
│   ├── solution_c17.txt        # (derived from verify_c17 upper bound)
│   ├── solution_c18.txt        # 13x18 binary matrix
│   ├── solution_c19.txt        # 13x19 binary matrix
│   ├── solution_c20.txt        # 13x20 binary matrix
│   └── solution_c21.txt        # 14x21 binary matrix
└── history/                    # Superseded bounds (80, 36, 144/11)
```

---

## 4. Citation

```bibtex
@misc{li2026_cyclic_covering_monograph,
  author       = {Jiahua Li},
  title        = {Exact Bounds, Integrality Gaps, and Asymptotic Limits for Cyclic Constrained Covering Arrays},
  year         = {2026},
  publisher    = {GitHub},
  howpublished = {\url{https://github.com/LiJiaHua1024/cyclic-covering-arrays}}
}
```

## 5. License

This project is licensed under the [MIT License](LICENSE).
