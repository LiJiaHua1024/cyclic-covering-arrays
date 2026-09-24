# Chapter 2: Universal Scoring Inequality and Lower Bound

## 1. Theorem Statement

**Theorem (Universal Local Potential Inequality)**:
For every legal cyclic binary configuration $x$ on cycle $C_n$ with $n \ge 11$:
$$3P_3(x) + 2P_4(x) + P_5(x) \le n$$
where $P_d(x) = \sum_{i=0}^{n-1} x_i x_{(i+d) \bmod n}$.

Equality holds if and only if every cyclic gap between consecutive active switches (ones) is either 2 or 3.

---

## 2. Mathematical Proof

If the configuration is empty, the score is 0, which trivially satisfies $0 \le n$.

For a nonempty legal configuration, list its active positions in cyclic order. Let $g_1, \dots, g_s$ be the cyclic distances between successive ones.
Since adjacent ones are prohibited, $g_i \ge 2$, and $\sum_{i=1}^s g_i = n$.

A pair of ones with forward cyclic distance at most 5 must either be:
1. **Consecutive** (a single gap of length 3, 4, or 5); or
2. **Separated by exactly one intervening one** (two successive gaps summing to 4 or 5: $2+2$, $2+3$, or $3+2$).

Three gaps already sum to at least $2 + 2 + 2 = 6$. Because $n \ge 11$, these cases partition all directed pairs at distances 3, 4, and 5 without overlap.
Hence, the total score can be written as:
$$\text{Score}(x) = 3 \#(g_i=3) + 2 \#(g_i=4) + \#(g_i=5) + \sum_{i=1}^s f(g_i, g_{i+1})$$
where the local transition bonus is:
$$f(2,2) = 2, \quad f(2,3) = f(3,2) = 1, \quad f(u,v) = 0 \text{ otherwise.}$$

For every ordered pair of adjacent gaps $(u, v)$:
$$f(u, v) \le \mathbf{1}_{\{u=2\}} + \mathbf{1}_{\{v=2\}}$$
Summing over the cyclic indices, $\sum_{i=1}^s f(g_i, g_{i+1}) \le 2 \#(g_i=2)$.
Therefore:
$$\text{Score}(x) \le 2 \#(g_i=2) + 3 \#(g_i=3) + 2 \#(g_i=4) + \#(g_i=5) \le \sum_{i=1}^s g_i = n$$

---

## 3. Corollary: Universal Lower Bound for All $n \ge 11$

For $n \ge 11$, the three sets of unordered pairs of cyclic distances 3, 4, and 5 are mutually disjoint and contain $n$ pairs each.
In an index-2 constrained covering array, each of these $3n$ pairs must be covered at least twice.
Weighting their coverage requirements with coefficients 3, 2, and 1, the total required weighted demand across the test suite is:
$$\text{Total Demand} = 2 \times (3n + 2n + n) = 12n$$

By the scoring inequality, each legal row contributes at most $n$ to this sum.
Consequently, for any valid test suite $\mathcal{T}$ (fractional or integer):
$$\sum_{x \in \mathcal{T}} \text{Score}(x) \ge 12n \implies |\mathcal{T}| \ge 12$$

Thus, for all $n \ge 11$:
$$\boxed{LP(n) \ge 12 \quad \text{and} \quad N(n) \ge 12}$$
Moreover, any 12-row integer solution must consist entirely of tight configurations (gaps in $\{2, 3\}$ only) and cover each pair at distances 3, 4, 5 *exactly* twice.
