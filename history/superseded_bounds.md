# Historical Bounds and Evolution Log

This directory archives superseded bounds and intermediate computational milestones for historical provenance.

---

## 1. Luna's Initial Bound: $LP(n) \le 80$
- **Origin**: Early stage heuristic Markovian construction.
- **Status**: Obsolete.
- **Superseded by**: The exact limit theorem $\lim_{n \to \infty} LP(n) = 12$.

---

## 2. Elementary Global Bound: $LP(n) \le 36$
- **Origin**: Direct combinatorial counting across all feasible states for $n \ge 10$.
- **Status**: Retained as a simple, non-asymptotic elementary upper bound for finite $n$.

---

## 3. Intermediate Asymptotic Bound: $\limsup_{n \to \infty} LP(n) \le 144/11 \approx 13.0909$
- **Origin**: 1-step gap Markov chain on $\{2, 3\}$.
- **Status**: Definitively superseded.
- **Reason**: The 1-step chain had a coverage defect at distance 7 ($p_7 = 11/72 < 1/6$).
  The new 2-step gap chain on $\{22, 23, 32, 33\}$ resolved the distance-7 defect, achieving $p_7 = 1/6$ and $p_d \ge 1/6$ for all $d \ge 2$, proving $\lim_{n \to \infty} LP(n) = 12$.
