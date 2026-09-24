# Chapter 6: Open Problems, the Boundary of $C_{17}$, and Structural Barriers

## 1. The Boundary of $C_{17}$ and Why $N(17)=13$ Remains Open

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

## 4. Resolution of $C_{17}$ and the Frontier at $C_{19}$

The residual coverage barrier (Path 1) has been completely resolved:
By implementing an exact, bit-parallel depth-first search traversing **54,310 nodes**, `verifiers/verify_c17.py` proves that no 12-row selection from the 119 tight rows can simultaneously achieve the pairwise lower bounds on distances 6, 7, and 8.
Thus, $N(17) = 13$ is strictly closed (Theorem T7, Chapter 3).

### Remaining Open Conjectures
1. **The $C_{19}$ Frontier and Integer Jump**:
   With $N(13) = N(14) = N(15) = N(17) = 13$, the unit gap $G(n) = 1$ is now verified across all small cycles up to $n=17$.
   What is the smallest cycle length $n^*$ where $N(n^*)$ first transitions to $14$? Does $C_{19}$ still have $N(19) = 13$?
2. **Exact LP 12-Attainment**:
   While $\lim_{n \to \infty} LP(n) = 12$ is proven, does there exist an infinite family of cycles where $LP(n)$ is strictly, identically equal to 12?
