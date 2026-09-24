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
| **[T4] $C_{15}$ Exact Optimum** | $n = 15$ | $LP(15) = 12, N(15) = 13$ (finite field rank certificate) | Exact rank certificate |
| **[T5] Asymptotic LP Limit** | $n \to \infty$ | $\displaystyle\lim_{n \to \infty} LP(n) = 12$, with rate $12 \le LP(n) \le 12 + C\theta^n$ | `verify_markov_chain.py` |
| **[T6] Asymptotic Gap Divergence** | $n \to \infty$ | $N(n) = \Theta(\log n) \implies G(n) = N(n) - LP(n) \to \infty$ | Coding theory / Lovász Local Lemma |

---

## 2. One-Click Mechanical Verification

All theorems with finite or Markovian certificates run in **under 5 seconds** using standard Python (zero external dependencies):

```bash
python verifiers/verify_all.py
```

To run individual verifiers:
- **Markov Chain Convergence**: `python verifiers/verify_markov_chain.py`
- **$C_{13}$ Integrality Gap**: `python verifiers/verify_c13.py`
- **$C_{14}$ Exact Certificate**: `python verifiers/verify_c14.py`

---

## 3. Repository Architecture

```text
├── theorem_ledger.md           # Single Source of Truth for all propositions
├── manuscript/                 # Full monograph chapters
│   ├── 02_universal_lower_bound.md
│   ├── 03_finite_cases.md      # C13, C14, C15 exact certificates
│   └── 04_asymptotic_lp_limit.md # 2-step gap Markov chain proof
├── verifiers/                  # Self-contained Python verifiers
│   ├── verify_all.py           # Master runner
│   ├── verify_markov_chain.py  # Rational arithmetic Markov recurrence
│   ├── verify_c13.py           # C13 exact certificate
│   └── verify_c14.py           # C14 exact certificate
├── data/                       # Concrete test suite constructions
│   ├── solution_c13.txt        # 13x13 binary matrix
│   └── solution_c14.txt        # 13x14 binary matrix
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
