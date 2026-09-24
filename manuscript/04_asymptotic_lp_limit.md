# Chapter 4: The Asymptotic LP Relaxation Limit: $\lim_{n \to \infty} LP(n) = 12$

## 1. Theorem Statement

**Theorem (Asymptotic Relaxation Limit)**:
$$\lim_{n \to \infty} LP(n) = 12$$
More strongly, there exist constants $C > 0$ and $0 < \theta < 1$ such that for all sufficiently large $n$:
$$12 \le LP(n) \le 12 + C \theta^n$$

---

## 2. The 2-Step Gap Markov Chain

To cover distance 7 with probability at least $1/6$ while preserving tight coverage on distances 3, 4, and 5, we construct a stationary process remembering **two consecutive gaps**.

The state space consists of pairs of consecutive gaps $s \in \{22, 23, 32, 33\}$. The transition matrix from state $ab$ to state $bc$ is defined by:
$$P = \begin{pmatrix} 5/8 & 3/8 & 0 & 0 \\ 0 & 0 & 1/2 & 1/2 \\ 3/4 & 1/4 & 0 & 0 \\ 0 & 0 & 1/2 & 1/2 \end{pmatrix}$$

### Stationary Distribution & Density
Direct computation confirms $\pi P = \pi$ for:
$$\pi = \left(\frac{2}{5}, \frac{1}{5}, \frac{1}{5}, \frac{1}{5}\right)$$
The probability that the first gap is 2 is $\pi_{22} + \pi_{23} = 3/5$, and the probability that it is 3 is $\pi_{32} + \pi_{33} = 2/5$.
The average gap length is:
$$\mathbb{E}[\text{gap}] = \frac{3}{5} \times 2 + \frac{2}{5} \times 3 = \frac{12}{5}$$
Consequently, in the stationary integer lattice process, the density of ones is:
$$\rho = \frac{5}{12}$$

---

## 3. Pairwise Probabilities at All Distances

Let $v_s(d)$ denote the conditional probability that position $d$ is 1, given that position 0 is 1 with initial 2-gap state $s$.
Let $g(s)$ be the first gap of state $s$ ($g(22)=g(23)=2$, $g(32)=g(33)=3$).
With $v_s(0) = 1$ and $v_s(d) = 0$ for $d < 0$, the recurrence is:
$$v_s(d) = \begin{cases} 0, & 0 < d < g(s) \\ 1, & d = g(s) \\ \sum_t P_{st} v_t(d - g(s)), & d > g(s) \end{cases}$$

The probability that two positions at distance $d$ are both 1 is given by:
$$p_d = \rho \sum_s \pi_s v_s(d) = \frac{2v_{22}(d) + v_{23}(d) + v_{32}(d) + v_{33}(d)}{12}$$

### Exact Rational Values
Evaluating the recurrence for small distances yields:
| $d$ | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $p_d$ | $\frac{1}{4}$ | $\frac{1}{6}$ | $\frac{1}{6}$ | $\frac{1}{6}$ | $\frac{3}{16}$ | $\frac{1}{6}$ | $\frac{65}{384}$ | $\frac{35}{192}$ | $\frac{517}{3072}$ | $\frac{89}{512}$ | $\frac{4313}{24576}$ | $\frac{2123}{12288}$ | $\frac{11327}{65536}$ |

Notice that $p_3 = p_4 = p_5 = p_7 = 1/6$, and $p_d > 1/6$ for all other $d \ge 8$ in the table.

### Global Control for All $d \ge 15$
For $d \in \{15, 16, 17\}$, exact evaluation yields:
$$\min_s v_s(15) = \frac{1655}{4096}, \quad \min_s v_s(16) = \frac{1655}{4096}, \quad \min_s v_s(17) = \frac{1681}{4096}$$
All values are strictly greater than $2/5 = 0.4$.
Since every subsequent $v_s(d)$ for $d \ge 18$ is a convex combination of previous values at $d-2$ and $d-3$, by mathematical induction:
$$v_s(d) \ge \frac{1655}{4096} > \frac{2}{5} \quad \text{for all } d \ge 15$$
Therefore, $p_d = \rho \sum_s \pi_s v_s(d) > \frac{5}{12} \times \frac{2}{5} = \frac{1}{6}$ for all $d \ge 15$.

Combining this with the table establishes:
$$\boxed{p_d \ge \frac{1}{6} \quad \text{for every } d \ge 2}$$

### Feasibility of Other Bivariate Configurations
- For non-adjacent positions ($d \ge 2$):
  - $P(10) = P(01) = \rho - p_d \ge \frac{5}{12} - \frac{1}{4} = \frac{1}{6}$.
  - $P(00) = 1 - 2\rho + p_d = 1 - \frac{10}{12} + p_d \ge \frac{2}{12} = \frac{1}{6}$.
- For adjacent positions ($d = 1$):
  - $P(11) = 0$ (forbidden constraint).
  - $P(00) = 1 - 2\rho = \frac{1}{6}$.
  - $P(01) = P(10) = \rho = \frac{5}{12} > \frac{1}{6}$.

Thus, every feasible pairwise interaction has probability at least $1/6$ under the stationary process!

---

## 4. Transfer to Finite Cycles $C_n$

We expand each gap $a \in \{2, 3\}$ into $a$ positional phases, outputting 1 only at the first phase. This yields a finite-state site transfer matrix $T$.
$T$ is irreducible and has returns of lengths 2 and 7 (which are coprime), making it aperiodic.
By the Perron-Frobenius theorem, $T^k \to \mathbf{1} \pi_{\text{site}}$ with exponential convergence rate governed by the subdominant eigenvalue $\theta < 1$.

Weighting closed paths of length $n$ by their transition probabilities normalized by $\operatorname{tr}(T^n)$ yields a rotation-invariant probability measure $\mu_n$ on legal configurations of $C_n$.
The minimum probability $c_n$ across all feasible pairwise states satisfies:
$$c_n = \frac{1}{6} + O(\theta^n)$$

Setting fractional row weights $y_r = \frac{2}{c_n} \mu_n(r)$ guarantees that every feasible requirement is covered at least twice, with total weight:
$$\sum_r y_r = \frac{2}{c_n} = 12 + O(\theta^n)$$
Variable bounds $y_r \le 1$ are satisfied for large $n$ since each closed path experiences at least $n/3$ transitions, giving $\mu_n(r) \le (3/4)^{n/3} / \operatorname{tr}(T^n) \to 0$.

Combined with the universal lower bound $LP(n) \ge 12$ (Theorem T1), this strictly establishes:
$$\lim_{n \to \infty} LP(n) = 12$$
