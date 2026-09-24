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

## 5. Remaining Open Conjectures

1. **The $C_{21}$ Frontier and the 14-Row Threshold**:
   With $N(13) = N(14) = N(15) = N(17) = N(19) = 13$, the unit integrality gap $G(n) = 1$ is invariant across all small cycles up to $n=19$.
   Is $n^* = 21$ the smallest odd cycle where $N(n^*)$ first transitions to $14$?
2. **Even Cycle Classification**:
   Does the 13-row rigidity extend to even cycles such as $C_{16}$ and $C_{18}$?
3. **Exact LP 12-Attainment**:
   While $\lim_{n \to \infty} LP(n) = 12$ is proven, does there exist an infinite family of cycles where $LP(n)$ is strictly, identically equal to 12?
   Verified independently in `verifiers/verify_c19.py`.
