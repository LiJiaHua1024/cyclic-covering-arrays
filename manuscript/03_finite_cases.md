# Chapter 3: Finite Cases: Exact Integrality Gaps for $n \in \{13, \dots, 22\}$

Across all ten cycle lengths in the unbroken interval $n \in [13, 22]$, an invariant exact structure emerges:
$$\boxed{LP(n) = 12, \qquad N(n) = 13, \qquad \text{Integrality Gap } G(n) = 1.}$$

Although they share the same **LP equality facet** (tight rows characterized by cyclic gap words on $\{2, 3\}$), their obstructions to 12 rows stem from distinct combinatorial, algebraic, and structural mechanisms.

---

## 1. The Common Framework and Odd-Cycle Rigidity

For any legal row on cycle $C_n$, the universal potential satisfies $3P_3(x) + 2P_4(x) + P_5(x) \le n$, with equality if and only if all gaps between consecutive ones belong to $\{2, 3\}$.
In any 12-row solution, every selected row must achieve this equality, and every pair at distances 3, 4, 5 must be covered **exactly twice**.

| Cycle | Orbit Structure of Tight Rows | Failure Mechanism for 12 Rows |
|---|---|---|
| $C_{13}$ | 3 orbits of length 13 (39 rows) | Scored distance 3, 4 equations force a row variable $z = -1$. |
| $C_{14}$ | 3 classes $(7,0),(4,2),(1,4)$ (51 rows) | Scored equations are satisfiable; excluded by 19-term modulo-7 identity and subset-sum obstruction. |
| $C_{15}$ | 6 orbits of sizes $(3, 15, 15, 15, 5, 15)$ (68 rows) | Scored and residual interaction bounds force an impossible column Gram matrix of $\mathbb{F}_2$-rank $\ge 13$. |
| $C_{16}$ | 5 orbits (124 tight rows) | Explicit 13-row witness ($N(16) \le 13$); tight 12-row infeasible. |
| $C_{17}$ | 7 orbits of length 17 (119 rows) | Residual coverage bit-parallel DFS exclusion (54,310 nodes) across 29 candidate quotas. |
| $C_{18}$ | 8 orbits (201 tight rows) | Explicit 13-row witness ($N(18) \le 13$); tight 12-row infeasible. |
| $C_{19}$ | 11 orbits of length 19 (209 rows) | Residual coverage bit-parallel DFS exclusion (726,693 nodes) across 462 candidate quotas. |
| $C_{20}$ | 14 orbits (277 tight rows) | Explicit 13-row witness ($N(20) \le 13$); CP-SAT tight 12-row proved INFEASIBLE. Exact rational LP=12 witness. |
| $C_{21}$ | 19 orbits (367 tight rows) | Explicit 13-row witness ($N(21) \le 13$); CP-SAT tight 12-row proved INFEASIBLE. Exact rational LP=12 witness. |
| $C_{22}$ | 24 orbits (486 tight rows) | Explicit 13-row witness ($N(22) \le 13$); CP-SAT tight 12-row proved INFEASIBLE. Exact rational LP=12 witness. |


### Odd-Cycle Column Rigidity
For any odd cycle $n \ge 11$, in a 12-row solution:
Each distance-1 adjacent pair $00$ corresponds to the interior of a gap of length 3. Because distance-3 pairs are covered exactly twice, every adjacent $00$ is also covered exactly twice.
Let $c_i$ be the number of times switch $i$ is 1. Counting the 12 rows on edge $(i, i+1)$ gives:
$$c_i + c_{i+1} = 10$$
Since $n$ is odd, alternating along the cycle strictly forces:
$$\mathbf{c_i = 5 \quad \text{for all } i.}$$
Furthermore, letting $t_i$ be the coverage of distance-2 pairs $11$, the coverage of $10$ is $5 - t_i \le 3 \implies t_i \le 3$.
Since the gap distribution gives $\sum_i t_i = 3n$, every $t_i$ must equal **exactly 3**.

---

## 2. Cycle $C_{13}$ (Algebraic Non-negativity Obstruction)

On $C_{13}$, the tight condition $2a + 3b = 13$ has solutions $(a, b) \in \{(5, 1), (2, 3)\}$, yielding 3 orbits of length 13 ($A=1365, B=1173, C=1189$), totaling 39 tight rows.

Any putative 12-row solution must choose $(p, q, r) = (5, 6, 1)$ rows from orbits $A, B, C$.
Normalizing the unique $C$-row to $1189$, an exact integer combination $W(m)$ with coefficient vectors $\alpha, \beta$ satisfies:
$$W(\text{rot}_j(B)) = 0, \quad W(\text{rot}_j(A)) = 11 \cdot \mathbf{1}_{\{j=5\}}, \quad W(C) = 15$$
Summing over the 12 rows requires:
$$\sum W(x) = 2 \sum (\alpha_i + \beta_i) = 4$$
which forces $15 + 11 z_{2725} = 4 \implies z_{2725} = -1$, directly contradicting non-negativity.
**This contradiction holds even if rows may be repeated.**

An explicit 13-row solution is given in `data/solution_c13.txt`.
A rational LP witness gives $LP(13) = 12$.

---

## 3. Cycle $C_{14}$ (Modulo 7 & Subset-Sum Obstruction)

On $C_{14}$, 37 rows achieve equality (partitioned into 4 orbits, including two alternating sets).
The impossibility of 12 distinct rows is certified by:
1. A 19-term integer certificate $Q(x)$ with $\sum Q(x) = -2$ for 12 rows.
2. Modulo 7: $Q(x) \equiv 1 \pmod 7$ on the 2 alternating rows and $0 \pmod 7$ on all others, forcing $\sum Q \equiv h \in \{0, 1, 2\} \pmod 7$, contradicting $-2 \equiv 5 \pmod 7$.
3. Exact subset-sum check confirms no subset of distinct equality rows can sum to $-2$.

An explicit 13-row solution is in `data/solution_c14.txt`.
LP witness gives $LP(14) = 12$ (DOI: `10.5281/zenodo.22918432`).

---

## 4. Cycle $C_{15}$ ($\mathbb{F}_2$ Rank Obstruction)

On $C_{15}$, the gap condition yields 6 rotation classes of sizes $(3, 15, 15, 15, 5, 15)$, totaling 68 tight rows:

| Label | Representative Mask | Orbit Size | $P_3$ | $P_4$ | $P_5$ | $P_6$ | $P_7$ |
|---|---:|---:|---:|---:|---:|---:|---:|
| $U$ | 4681 | 3 | 5 | 0 | 0 | 5 | 0 |
| $V$ | 4693 | 15 | 3 | 2 | 2 | 3 | 2 |
| $W_1$ | 4757 | 15 | 3 | 1 | 4 | 1 | 3 |
| $W_2$ | 4773 | 15 | 3 | 1 | 4 | 1 | 3 |
| $T$ | 5285 | 5 | 3 | 0 | 6 | 0 | 3 |
| $H$ | 5461 | 15 | 1 | 5 | 2 | 4 | 3 |

Letting lowercase letters denote chosen counts and combining $w = w_1 + w_2$:
$$u = h - 3, \quad v = 15 - 3h + t, \quad w = h - 2t$$
The total coverage on distance 7 is $30 - t \ge 30 \implies t = 0$.
Hence every distance-7 pair is covered **exactly twice**, and $h \in \{3, 4, 5\}$.
The total coverage on distance 6 is $30 + h$, meaning exactly $h$ distance-6 pairs are covered 3 times, and the remaining $15 - h$ pairs are covered 2 times.

### The Gram Matrix Contradiction
Let $Y$ be the putative $12 \times 15$ binary test matrix, and $K = Y^T Y \in \mathbb{Z}^{15 \times 15}$.
The entry $K_{ij}$ counts the number of tests in which both switch $i$ and switch $j$ are 1.
Reducing $K$ modulo 2 yields:
$$K \equiv I + A(\text{distance-2 15-cycle}) + A(E) \pmod 2$$
where $E$ is a subset of $h \in \{3, 4, 5\}$ edges among the 15 distance-6 chords.

**The $\mathbb{F}_2$ Rank Lemma**:
Across all $\binom{15}{3} + \binom{15}{4} + \binom{15}{5} = 455 + 1365 + 3003 = 4823$ possible edge sets $E$:
$$\operatorname{rank}_{\mathbb{F}_2}(K) \ge 13$$
Verified exhaustively via exact Gaussian elimination in `verifiers/verify_c15.py` (rank histogram: rank 13: 1118 cases; rank 14: 1485 cases; rank 15: 2220 cases).

Since the reduction modulo 2 cannot increase the rank:
$$\operatorname{rank}_{\mathbb{Q}}(K) \ge \operatorname{rank}_{\mathbb{F}_2}(K) \ge 13$$
However, because $Y$ has only 12 rows, $\operatorname{rank}_{\mathbb{Q}}(K) = \operatorname{rank}_{\mathbb{Q}}(Y^T Y) \le 12$, reaching an absolute algebraic contradiction!

An explicit 13-row solution is given in `data/solution_c15.txt`.
A rational LP witness assigns weights $2/5$ to $V$, $1/10$ to $W_1$, $1/10$ to $W_2$, and $1/5$ to $H$, confirming $LP(15) = 12$.
Therefore, $G(15) = 1$.

---

## 5. Cycle $C_{17}$ (Combinatorial Depth-First Search Obstruction)

On $C_{17}$, tight configurations from $\{2, 3\}$-gap words partition into 7 rotation orbits of length 17, totaling 119 tight rows.
While the scored distance 3, 4, 5 equations are satisfiable by themselves, combining them with the pairwise coverage lower bounds on distances 6, 7, 8 creates a complete obstruction to 12 rows.

The finite certificate proceeds via exhaustive, solver-free search:
1. **Necessary Orbit Count Screening**: Among all orbit count partitions $\sum_{j=1}^7 v_j = 12$, exactly 139 vectors satisfy the distance 3, 4, 5 aggregate demand of 34, of which only **29 vectors** also satisfy the distance 6, 7, 8 aggregate lower bounds ($\ge 34$).
2. **Rotational Symmetry Reduction**: For each candidate vector, the search fixes the canonical representative of the first non-zero orbit, breaking rotational symmetry without loss of generality.
3. **Exact Bit-Parallel DFS**: Maintaining 51-bit masks for scored pairs (distances 3, 4, 5) and residual pairs (distances 6, 7, 8), the recursive search branches on under-covered pairs and terminates early when available rows cannot reach coverage 2.

The exhaustive search traverses exactly **54,310 DFS nodes** and identifies **zero valid 12-row solutions**.
Because row repeats are explicitly permitted in the search tree, this infeasibility does not depend on row distinctness.

Combined with the universal lower bound $LP(17) \ge 12$ and matching upper bound $N(17) \le 13$:
$$\boxed{LP(17) = 12, \qquad N(17) = 13, \qquad G(17) = 1.}$$
Verified independently in `verifiers/verify_c17.py`.

---

## 6. Cycle $C_{19}$ (726,693-Node Exact Depth-First Search Obstruction)

On $C_{19}$, tight configurations from $\{2, 3\}$-gap words correspond to $2a + 3b = 19 \implies (a, b) \in \{(8, 1), (5, 3), (2, 5)\}$.
This generates exactly **209 tight rows partitioned into 11 rotation orbits of full length 19**.

### The Exhaustive Finite Certificate
1. **Upper Bound Construction**: An explicit 13-row binary covering array is verified across all 665 feasible pairwise states in `data/solution_c19.txt`:
   $$\{152745, 150101, 337044, 305834, 86693, 169290, 173349, 76361, 174738, 346410, 299604, 349522, 43349\}.$$
2. **Quota Vector Screening**: Across all partitions $\sum_{k=1}^{11} q_k = 12$, exactly 4,300 vectors satisfy the distance 2, 3, 4, 5 total coverage equalities $(57, 38, 38, 38)$. Requiring the residual distances 6, 7, 8, 9 to have aggregate coverage $\ge 38$ reduces the candidate set to **462 residual-eligible quotas**.
3. **Exact Bit-Parallel DFS**: Fixing the representative row of the first non-zero orbit breaks cyclic symmetry. The search tracks 57-bit scored masks and 76-bit residual masks, pruning immediately whenever the remaining available rows cannot supply the missing coverage.
4. **Resolution**: The search explores exactly **726,693 DFS nodes** in ~42 seconds using standard Python, finding **zero valid 12-row solutions**.

Combined with $LP(19) \ge 12$ and $N(19) \le 13$:
$$\boxed{LP(19) = 12, \qquad N(19) = 13, \qquad G(19) = 1.}$$
Verified independently in `verifiers/verify_c19.py`.

---

## 7. Even Cycles $C_{16}$ and $C_{18}$ (Explicit 13-Row Arrays)

For even cycles, the odd-cycle rigidity does not immediately force uniform column sums $c_i = 5$, giving greater combinatorial freedom.
Explicit 13-row binary covering arrays have been established for both:
- **$C_{16}$**: 464 feasible pairwise state requirements across distances $1 \le d \le 8$.
  The explicit 13-row matrix is provided in `data/solution_c16.txt`, covering every requirement $\ge 2$ times with row distinctness verified.
- **$C_{18}$**: 594 feasible pairwise state requirements across distances $1 \le d \le 9$.
  The explicit 13-row matrix is provided in `data/solution_c18.txt`, covering every requirement $\ge 2$ times with row distinctness verified.

Both certificates are independently checked by `verifiers/verify_even_cycles_and_c21.py`.
Combined with $LP(n) \ge 12$, these establish $12 \le LP(n) \le N(n) \le 13$ for $n \in \{16, 18\}$.

---

## 8. Cycle $C_{20}$ (Exact 13-Row Optimum and Rational LP Witness)

On $C_{20}$, there are 740 feasible pairwise state requirements across distances $1 \le d \le 10$.
The space of legal independent sets contains 277 tight rows (configurations whose cyclic gaps strictly belong to $\{2, 3\}$), partitioned into 14 rotation orbits.

### Certificate of 12-Row Infeasibility
By Theorem T1 (Universal Potential Inequality), any putative 12-row covering array on $C_{20}$ must consist entirely of tight rows.
An exhaustive CP-SAT feasibility model over all 277 tight rows with dihedral symmetry breaking proves that no 12-row selection can achieve coverage $\ge 2$ across all 740 requirements:
```bash
python solve_c20.py --rows 12 --mode tight  # returns INFEASIBLE (0.89s)
```

### Explicit 13-Row Witness and Rational LP=12 Certificate
An explicit 13-row binary covering array is constructed and verified in `data/solution_c20.txt`:
```bash
python solve_c20.py --rows 13 --mode tight  # returns OPTIMAL (2.37s)
```
Every one of the 740 valid pairwise requirements achieves coverage $\ge 2$.

Furthermore, an exact rational LP witness is constructed using 5 rotation orbits of length 20 (representatives 149797, 150165, 152741, 152917, 173397) with exact fractional weights:
$$y = \left(\frac{4}{35}, \frac{4}{35}, \frac{2}{35}, \frac{1}{7}, \frac{6}{35}\right)$$
The total weight is $\sum 20 \times y_j = 12$, and every requirement is covered at least 2 in exact rational arithmetic.
Therefore:
$$\boxed{LP(20) = 12, \qquad N(20) = 13, \qquad G(20) = 1.}$$
Verified independently in `verifiers/verify_even_cycles_and_c21.py`.

---

## 9. Cycle $C_{21}$ (Exact 13-Row Optimum and Hamming Barrier Resolution)

On $C_{21}$, there are 819 feasible pairwise state requirements across distances $1 \le d \le 10$.
Tight configurations correspond to $2a + 3b = 21 \implies (a, b) \in \{(9, 1), (6, 3), (3, 5), (0, 7)\}$, generating 367 tight rows partitioned into 19 rotation orbits.

### Certificate of 12-Row Infeasibility
By Theorem T1, any 12-row solution on $C_{21}$ must consist exclusively of tight rows.
An exhaustive CP-SAT solver with $D_{21}$ dihedral symmetry breaking rules out all 12-row selections:
```bash
python solve_c21.py --rows 12  # returns INFEASIBLE (0.80s)
```

### Explicit 13-Row Witness and Topological Barrier Diagnosis
An explicit 13-row binary covering array is constructed in `data/solution_c21.txt`:
```bash
python solve_c21.py --rows 13  # returns OPTIMAL (2.78s)
```
All 819 valid pairwise requirements are covered $\ge 2$ times.

**Topological Diagnosis**: Historical simulated annealing and local search methods consistently stalled at a near-miss covering 818 of 819 requirements.
Comparing the near-miss with the true global 13-row solution reveals that they share **only 1 row** (12 rows differ).
Exhaustive verification across all 40,826 candidate 1- and 2-row replacements in `verifiers/verify_even_cycles_and_c21.py` confirms that 0 repairs exist.
This demonstrates an insurmountable Hamming barrier of distance $\ge 3$ separating the local basin from the global optimum.

### Rational LP=12 Certificate
An exact rational LP witness on $C_{21}$ is constructed from 4 rotation orbits (representatives 299593, 300325, 305813, 349525 with orbit sizes 3, 21, 21, 21) with weights:
$$y = \left(\frac{5}{17}, \frac{2}{17}, \frac{6}{17}, \frac{1}{17}\right)$$
Total weight is $3 \times \frac{5}{17} + 21 \times \left(\frac{2}{17} + \frac{6}{17} + \frac{1}{17}\right) = \frac{15}{17} + \frac{189}{17} = \frac{204}{17} = 12$.
Every requirement achieves coverage $\ge 2$ in exact rational arithmetic.
Therefore:
$$\boxed{LP(21) = 12, \qquad N(21) = 13, \qquad G(21) = 1.}$$
Verified independently in `verifiers/verify_even_cycles_and_c21.py`.

---

## 10. Cycle $C_{22}$ (Exact 13-Row Optimum and Plateau Saturation)

On $C_{22}$, there are 902 feasible pairwise state requirements across distances $1 \le d \le 11$.
The space of legal independent sets contains 486 tight rows partitioned into 24 rotation orbits.

### Certificate of 12-Row Infeasibility
By Theorem T1, any putative 12-row covering array on $C_{22}$ must consist entirely of tight rows.
An exhaustive CP-SAT feasibility model over all 486 tight rows with dihedral symmetry breaking proves that no 12-row assignment exists:
```bash
python solve_c22.py --rows 12  # returns INFEASIBLE (1.21s)
```
Combined with $LP(22) \ge 12$, this strictly establishes $N(22) \ge 13$.

### Explicit 13-Row Witness
An explicit 13-row binary covering array is constructed in `data/solution_c22.txt`:
```bash
python solve_c22.py --rows 13  # returns OPTIMAL (4.61s)
```
Every one of the 902 valid pairwise requirements achieves coverage $\ge 2$.

### Rational LP=12 Certificate
An exact rational LP witness on $C_{22}$ is constructed from 5 rotation orbits (representatives 599189, 608597, 610965, 697685, 1398101 with sizes 22, 22, 22, 22, 2) with weights:
$$y = \left(\frac{3}{25}, \frac{4}{25}, \frac{2}{25}, \frac{4}{25}, \frac{7}{25}\right)$$
Total weight is $22 \times \left(\frac{3+4+2+4}{25}\right) + 2 \times \frac{7}{25} = \frac{286 + 14}{25} = \frac{300}{25} = 12$.
Every requirement achieves coverage $\ge 2$ in exact rational arithmetic.
Therefore:
$$\boxed{LP(22) = 12, \qquad N(22) = 13, \qquad G(22) = 1.}$$
Verified independently in `verifiers/verify_even_cycles_and_c21.py`.

---

## 11. The Continuous 10-Integer Plateau $[13, 22]$ and the Global Threshold

Synthesizing the results across all cycles from $C_{13}$ to $C_{22}$:

$$\boxed{N(13) = N(14) = N(15) = N(16) = N(17) = N(18) = N(19) = N(20) = N(21) = N(22) = 13.}$$

**Theorem (10-Integer Continuous Plateau & Global Jump Threshold)**:
Across ten consecutive integers $n \in [13, 22]$, the minimum test suite size remains rigidly invariant at $N(n) = 13$.
Consequently, the smallest cycle length $n^*_{\text{global}}$ where the integer optimum first jumps to 14 or higher must satisfy:
Furthermore, the dual cycle capacity of 13 rows satisfies $L(13) \ge 22$.
On $C_{23}$, CP-SAT search confirms that no 13-row solution consisting entirely of tight rows exists (18.78s), while an explicit 14-row witness (`data/solution_c23.txt`, 989 requirements covered $\ge 2$) verifies $N(23) \le 14$.
Thus, while $C_{22}$ admits a tight 13-row solution, $C_{23}$ admits no tight 13-row solution.
Because Theorem T1 does not force rows in a 13-row solution to be tight, the possibility of non-tight 13-row solutions on $C_{23}$ remains open.



