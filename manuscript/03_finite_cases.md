# Chapter 3: Finite Cases: Exact Integrality Gaps for $n \in \{13, 14, 15, 17, 19\}$

Across the five cycle lengths $n \in \{13, 14, 15, 17, 19\}$, an invariant exact structure emerges:
$$\boxed{LP(n) = 12, \qquad N(n) = 13, \qquad \text{Integrality Gap } G(n) = 1.}$$

Although they share the same **LP equality facet** (tight rows characterized by cyclic gap words on $\{2, 3\}$), their obstructions to 12 rows stem from distinct combinatorial and algebraic mechanisms.

---

## 1. The Common Framework and Odd-Cycle Rigidity

For any legal row on cycle $C_n$, the universal potential satisfies $3P_3(x) + 2P_4(x) + P_5(x) \le n$, with equality if and only if all gaps between consecutive ones belong to $\{2, 3\}$.
In any 12-row solution, every selected row must achieve this equality, and every pair at distances 3, 4, 5 must be covered **exactly twice**.

| Cycle | Orbit Structure of Tight Rows | Failure Mechanism for 12 Rows |
|---|---|---|
| $C_{13}$ | 3 orbits of length 13 (39 rows) | Scored distance 3, 4 equations force a row variable $z = -1$. |
| $C_{14}$ | 3 classes $(7,0),(4,2),(1,4)$ (51 rows) | Scored equations are satisfiable; excluded by 19-term modulo-7 identity and subset-sum obstruction. |
| $C_{15}$ | 6 orbits of sizes $(3, 15, 15, 15, 5, 15)$ (68 rows) | Scored and residual interaction bounds force an impossible column Gram matrix of $\mathbb{F}_2$-rank $\ge 13$. |
| $C_{17}$ | 7 orbits of length 17 (119 rows) | Residual coverage bit-parallel DFS exclusion (54,310 nodes) across 29 candidate quotas. |
| $C_{19}$ | 11 orbits of length 19 (209 rows) | Residual coverage bit-parallel DFS exclusion (726,693 nodes) across 462 candidate quotas. |

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
