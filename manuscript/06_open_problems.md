# Chapter 6: Open Problems and Boundary of $C_{17}$

## 1. The Boundary of $C_{17}$

For $C_{17}$, tight configurations from $\{2, 3\}$-gap words correspond to $2a + 3b = 17 \implies (a, b) \in \{(7, 1), (4, 3), (1, 5)\}$.
This generates exactly **119 tight rows partitioned into 7 rotation orbits of length 17**.

Preliminary MILP searches suggest that no 12-row integer solution exists, and an explicit 13-row solution is available.
However, because no finite linear contradiction (as in $C_{13}$) or checkable rank certificate (as in $C_{15}$) has been established, we strictly state:
$$12 \le N(17) \le 13$$
and classify $G(17) = 1$ as an open problem pending an independent, solver-free certificate.

---

## 2. A 3-Tier Classification Criterion on the LP Equality Facet

Rather than speculating whether all odd cycles exhibit integrality gaps, the structural analysis across $C_{13}, C_{14}, C_{15}$ establishes a rigorous diagnostic hierarchy for 12-row existence:

1. **Tier 1: Scored Distance Equations Contradict Non-negativity**:
   As in $C_{13}$, the linear equations for distances 3, 4, 5 alone force a row multiplier to be negative, without examining other bivariate states.
2. **Tier 2: Residual Interaction Bounds Force an Impossible Gram Matrix**:
   As in $C_{15}$, the scored equations admit integer solutions, but the rigidity of residual pair counts forces a column Gram matrix $K = Y^T Y$ with $\operatorname{rank}_{\mathbb{F}_2}(K) \ge 13$, contradicting the 12-row budget.
3. **Tier 3: Higher-Order Coverage Obstructions**:
   As in $C_{14}$, the scored distances and simple Gram matrices do not directly fail; deeper modular obstructions and distinct-row capacity constraints obstruct 12 rows.

---

## 3. Asymptotic Conjectures

- **Exact 12-Attainment**: Does there exist an infinite subsequence of cycle lengths $n_k$ for which $LP(n_k)$ strictly equals 12?
- **Integer Transition**: At what critical cycle length $n$ does the integer optimum first jump from $N(n) = 13$ to $N(n) = 14$?
