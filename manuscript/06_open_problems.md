# Chapter 6: Open Problems, Structural Barriers, and the New Frontier

## 1. The Structure of $C_{17}$ and Why Classical Reductions Failed

For $C_{17}$, tight configurations from $\{2, 3\}$-gap words correspond to $2a + 3b = 17 \implies (a, b) \in \{(7, 1), (4, 3), (1, 5)\}$.
This generates exactly **119 tight rows partitioned into 7 rotation orbits of length 17**:

| Orbit | Representative Mask | $P_2$ | $P_3$ | $P_4$ | $P_5$ | $P_6$ | $P_7$ | $P_8$ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| $A$ | 18725 | 1 | 5 | 0 | 2 | 4 | 0 | 3 |
| $B$ | 18773 | 4 | 3 | 3 | 2 | 4 | 2 | 3 |
| $C$ | 19029 | 4 | 3 | 2 | 4 | 2 | 3 | 3 |
| $D$ | 19093 | 4 | 3 | 2 | 4 | 1 | 5 | 2 |
| $E$ | 19109 | 4 | 3 | 2 | 4 | 2 | 3 | 3 |
| $F$ | 21141 | 4 | 3 | 1 | 6 | 0 | 5 | 2 |
| $G$ | 21845 | 7 | 1 | 6 | 2 | 5 | 3 | 4 |

Odd-cycle rigidity requires $\sum P_2 = 3 \times 17 = 51$, yielding:
$$a = g - 1, \qquad b + c + d + e + f = 13 - 2g$$

---

## 2. Barrier 1: Scored Distance Equations are Satisfiable on $C_{17}$

Unlike $C_{13}$ (where the scored distance equations directly forced a multiplier to equal $-1$), on $C_{17}$ there are **139 non-negative integer vectors** $(a, b, c, d, e, f, g)$ satisfying the required sum of 34 on distances 3, 4, and 5.
Furthermore, **29 vectors** also satisfy the aggregate lower bounds ($\ge 34$) on distances 6, 7, and 8.

More decisively, there exists an explicit set of **12 distinct rows**:
$$\{18761, 21797, 37450, 38229, 42325, 43602, 43689, 74900, 76074, 84644, 86674, 87210\}$$
which pairwise satisfies:
- All distance 3, 4, 5 pairs covered **exactly 2 times**;
- Every column sum $c_i = 5$;
- Every distance-2 pair covered $t_i = 3$ times.

However, this is *not* a valid covering array: its total coverage on distance 7 is only 27 (below the required 34).
This explicitly proves that **Tier 1 (scored distance equations alone) cannot exclude 12 rows on $C_{17}$**.

---

## 3. Barrier 2: The Limit of Unconstrained $\mathbb{F}_2$ Rank Arguments

Assuming all pairwise counts on distances 6, 7, 8 are in $\{2, 3\}$, and letting $E$ denote the pairs covered 3 times, the candidate Gram matrix takes the form:
$$K = (I - A(C_{17}))^2 + 2J + A(E)$$
Modulo 2, the unperturbed base matrix $I + A(\text{dist } 2)$ is invertible on $C_n$ whenever $3 \nmid n$ (such as $n=17$).

Taking the orbit count vector $(a,b,c,d,e,f,g) = (3,0,0,5,0,0,4)$ allows residual edge counts $(3, 3, 1)$ on distances 6, 7, 8 respectively.
Selecting the edge set:
$$E = \{(7,13), (8,14), (9,15), (2,9), (1,8), (3,10), (14,5)\}$$
produces a candidate matrix $K$ with:
$$\operatorname{rank}_{\mathbb{F}_2}(K) = 12$$

Thus, unlike $C_{15}$ (where *every* edge set forced rank $\ge 13$), on $C_{17}$ an unconstrained edge count argument **cannot force rank $\ge 13$**.
However, this candidate matrix $K$ is algebraically **non-realizable**: the integer vector:
$$z = (0, -1, -2, -1, 0, 1, 0, 0, 2, 2, 1, 0, 0, -1, -2, -1, 0)^T$$
satisfies:
$$z^T K z = -6 < 0$$
violating the positive-semidefiniteness required of any true Gram matrix $K = Y^T Y$.

---

## 4. Resolution of $C_{17}$ and the $C_{19}$ Frontier

The residual coverage barrier (Path 1) on $C_{17}$ has been completely resolved:
By implementing an exact, bit-parallel depth-first search traversing **54,310 nodes**, `verifiers/verify_c17.py` proves that no 12-row selection from the 119 tight rows can simultaneously achieve the pairwise lower bounds on distances 6, 7, and 8.
Thus, $N(17) = 13$ is strictly closed (Theorem T7, Chapter 3).

### Progress on $C_{19}$: Explicit 13-Row Construction

Moving to $C_{19}$, an explicit 13-row binary covering array has been constructed:
$$\begin{aligned}
\text{Rows} = \{ &152745, 150101, 337044, 305834, 86693, 169290, 173349, \\
&76361, 174738, 346410, 299604, 349522, 43349 \}
\end{aligned}$$
This witness strictly satisfies:
- All 13 rows are pairwise distinct and forbid adjacent $11$ along the 19-cycle.
- All **665 valid pairwise column interactions** across distances $d \in \{1, \dots, 9\}$ achieve coverage $\ge 2$.

Combined with the universal potential lower bound $LP(19) \ge 12$, this establishes:
$$\boxed{12 \le LP(19) \le N(19) \le 13.}$$

**Immediate Consequence for the Odd-Cycle Jump Threshold**:
Because $N(13) = N(14) = N(15) = N(17) = 13$ and $N(19) \le 13$, the smallest odd cycle length $n^*$ where the integer optimum first exceeds 13 must satisfy:
$$\boxed{n^*_{\text{odd}} \ge 21.}$$
Thus, $n=19$ is **not** the jump threshold.

### Full Closure of $C_{19}$: 726,693-Node DFS Exclusion
The 12-row exclusion on $C_{19}$ has been completely resolved:
By implementing an exact, bit-parallel depth-first search traversing **726,693 nodes**, `verifiers/verify_c19.py` proves that no 12-row selection from the 209 tight rows can simultaneously achieve the pairwise coverage conditions.
Thus, $N(19) = 13$ is strictly closed:
$$\boxed{LP(19) = 12, \qquad N(19) = 13, \qquad G(19) = 1.}$$

---

## 5. The Continuous Plateau $[13, 21]$ and Resolution of $C_{20}, C_{21}$

### Full Closure of Even Cycles and $C_{21}$
Explicit 13-row binary covering arrays have been established and mechanically verified for $C_{16}$ (464 valid pairs), $C_{18}$ (594 valid pairs), $C_{20}$ (740 valid pairs), and $C_{21}$ (819 valid pairs), recorded in `data/solution_c16.txt`, `data/solution_c18.txt`, `data/solution_c20.txt`, and `data/solution_c21.txt`.

Furthermore, by Theorem T1, any putative 12-row solution on $C_{20}$ (277 tight rows) or $C_{21}$ (367 tight rows) must consist exclusively of tight configurations.
Exact CP-SAT models with dihedral symmetry breaking prove:
- `solve_c20.py --rows 12 --mode tight`: **INFEASIBLE** (0.89s) $\implies N(20) = 13$.
- `solve_c21.py --rows 12`: **INFEASIBLE** (0.80s) $\implies N(21) = 13$.

Moreover, exact rational LP witnesses of total weight 12 are constructed and verified in pure fractional arithmetic:
- $C_{20}$: 5 rotation orbits of length 20, weights $\left(\frac{4}{35}, \frac{4}{35}, \frac{2}{35}, \frac{1}{7}, \frac{6}{35}\right)$, total weight 12 $\implies LP(20) = 12$.
- $C_{21}$: 4 rotation orbits (sizes 3, 21, 21, 21), weights $\left(\frac{5}{17}, \frac{2}{17}, \frac{6}{17}, \frac{1}{17}\right)$, total weight 12 $\implies LP(21) = 12$.

### The 9-Integer Plateau and Global Jump Threshold
Combining all exact results establishes that **every integer in the 9-element range $n \in [13, 21]$ has $N(n) = 13$**:
$$\boxed{N(13) = N(14) = N(15) = N(16) = N(17) = N(18) = N(19) = N(20) = N(21) = 13.}$$
Consequently, the global jump threshold where the integer optimum first exceeds 13 is pushed to:
$$\boxed{n^*_{\text{global}} \ge 22.}$$

---

## 6. The Dual Column-Code Perspective $L(M)$ and Open Frontiers

Rather than incrementing the cycle length $n$ point-by-point, the fundamental structural problem is formulated dually in terms of **column code capacity**:

**Definition (Maximum Cycle Capacity $L(M)$)**:
For a fixed integer budget of $M$ test rows, define $L(M)$ as the maximum cycle length $n$ such that $C_n$ admits a valid binary covering array of $M$ rows:
$$L(M) = \max \{n \in \mathbb{N} : N(n) \le M\}$$

From our exact theorems:
- For $M \le 11$: $L(M) = 6$ (by Theorem T1, $N(n) \ge 12$ for all $n \ge 7$).
- For $M = 12$: $L(12) = 12$ (since $N(12) \le 12$, and for all $n \ge 13$, $N(n) \ge 13$).
- For $M = 13$: We have rigorously established:
  $$\boxed{L(13) \ge 21.}$$

### Open Problems and Conjectures

1. **Exact Determination of $L(13)$ and the Jump Threshold**:
   Is $L(13) = 21$ (meaning $n^*_{\text{global}} = 22$ is the exact jump point where $N(22) = 14$), or does $L(13) \ge 22$?
   This is equivalent to determining whether the space of legal independent sets on $C_{22}$ can support 13 mutually covering rows.

2. **Finite Attainment of the Fractional Constant $\lim LP(n) = 12$**:
   While we have established exact rational certificates with $LP(n) = 12$ for $n \in \{13, 14, 15, 16, 17, 18, 19, 20, 21\}$, does $LP(n) = 12$ hold identically for **all** $n \ge 13$?
   Or do there exist cycle lengths where the fractional optimum strictly exceeds 12 before decaying exponentially back toward 12?

3. **Asymptotic Constant of Integer Complexity**:
   Theorem T6 establishes $N_\lambda(n) = \Theta_\lambda(\log n)$ for all $\lambda \ge 1$.
   What is the exact asymptotic leading constant:
   $$c(\lambda) = \lim_{n \to \infty} \frac{N_\lambda(n)}{\log_2 n} ?$$
   Does $c(2)$ equal 1, or is it strictly larger due to the cyclic adjacent-exclusion constraint?
