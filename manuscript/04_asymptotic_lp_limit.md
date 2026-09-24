# Chapter 4: Universal Fractional Relaxation Limit for Arbitrary Index $\lambda$: $\lim_{n \to \infty} LP_\lambda(n) = 6\lambda$

## 1. Theorem Statement

**Theorem (Universal Asymptotic Relaxation Limit for General Index $\lambda$)**:
For any fixed positive integer coverage index $\lambda \ge 1$:
$$\lim_{n \to \infty} LP_\lambda(n) = 6\lambda$$
More strongly, there exist a constant $\theta \in (0, 1)$ independent of $\lambda$, and positive constants $C_\lambda$ and $n_\lambda$, such that for all $n \ge n_\lambda$:
$$6\lambda \le LP_\lambda(n) \le 6\lambda + C_\lambda \theta^n$$

---

## 2. The 2-Step Gap Markov Chain and Exact Two-Point Bounds

To cover distance 7 with probability at least $1/6$ while preserving tight bounds across all distances, we construct a stationary process remembering **two consecutive gaps**.

The state space consists of pairs of consecutive gaps $s \in \{22, 23, 32, 33\}$. The transition matrix $P$ updating $ab \to bc$ and outputting initial gap $a$ is:
$$P = \begin{pmatrix} 5/8 & 3/8 & 0 & 0 \\ 0 & 0 & 1/2 & 1/2 \\ 3/4 & 1/4 & 0 & 0 \\ 0 & 0 & 1/2 & 1/2 \end{pmatrix}, \qquad \pi = \left(\frac{2}{5}, \frac{1}{5}, \frac{1}{5}, \frac{1}{5}\right)$$

Direct computation confirms $\pi P = \pi$. With gap lengths $g = (2, 2, 3, 3)$, the average gap length is:
$$\mathbb{E}[\text{gap}] = \sum_{s} \pi_s g(s) = \frac{12}{5} \implies \rho = \frac{1}{\mathbb{E}[\text{gap}]} = \frac{5}{12}$$

### Exact Two-Point Bounds $1/6 \le p_d \le 1/4$
Let $v_s(d)$ denote the conditional probability that position $d$ is 1, given that position 0 is 1 with initial 2-gap state $s$.
With $v_s(0) = 1$ and $v_s(d) = 0$ for $d < 0$, the recurrence is:
$$v_s(d) = \begin{cases} 0, & 0 < d < g(s) \\ 1, & d = g(s) \\ \sum_u P_{su} v_u(d - g(s)), & d > g(s) \end{cases}$$

The two-point probability is $p_d = \Pr(X_0 = X_d = 1) = \rho \sum_s \pi_s v_s(d) = \frac{2v_{22}(d) + v_{23}(d) + v_{32}(d) + v_{33}(d)}{12}$.

**Lemma 1 (Uniform Two-Point Bounds)**:
For every cyclic distance $d \ge 2$:
$$\frac{1}{6} \le p_d \le \frac{1}{4}$$

*Proof*:
Evaluating the exact rational recurrence for small distances yields:
| $d$ | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $p_d$ | $\frac{1}{4}$ | $\frac{1}{6}$ | $\frac{1}{6}$ | $\frac{1}{6}$ | $\frac{3}{16}$ | $\frac{1}{6}$ | $\frac{65}{384}$ | $\frac{35}{192}$ | $\frac{517}{3072}$ | $\frac{89}{512}$ | $\frac{4313}{24576}$ | $\frac{2123}{12288}$ | $\frac{11327}{65536}$ |

All values lie strictly in $[1/6, 1/4]$.
For the base levels $d \in \{15, 16, 17\}$, exact evaluation yields:
$$\min_s v_s(15) = \frac{1655}{4096}, \quad \min_s v_s(16) = \frac{1655}{4096}, \quad \min_s v_s(17) = \frac{1681}{4096}$$
$$\max_s v_s(15) = \frac{229}{512}, \quad \max_s v_s(16) = \frac{6961}{16384}, \quad \max_s v_s(17) = \frac{13971}{32768}$$
Thus $v_s(d) \in [2/5, 3/5]$ for all $s$ and $d \in \{15, 16, 17\}$.
For every $d \ge 18$, $v_s(d)$ is a convex combination of previous values at $d-2$ and $d-3$. By mathematical induction:
$$\frac{2}{5} \le v_s(d) \le \frac{3}{5} \quad \text{for all } d \ge 15$$
Multiplying by $\rho = 5/12$ establishes:
$$\boxed{\frac{1}{6} \le p_d \le \frac{1}{4} \quad \text{for every } d \ge 2}$$
The upper bound $p_d \le 1/4$ is mathematically indispensable: it guarantees that for non-adjacent columns, the probabilities of states $(0, 1)$ and $(1, 0)$ satisfy:
$$P(01) = P(10) = \rho - p_d = \frac{5}{12} - p_d \ge \frac{5}{12} - \frac{1}{4} = \frac{1}{6}$$
Moreover, $P(00) = 1 - 2\rho + p_d = \frac{2}{12} + p_d \ge \frac{1}{6}$.
For adjacent positions ($d = 1$), $(1, 1)$ is forbidden, while $P(00) = 1 - 2\rho = 1/6$ and $P(01) = P(10) = \rho = 5/12 > 1/6$.
Hence, **every feasible pairwise interaction has stationary probability at least $1/6$**.

---

## 3. Finite-State Site Matrix and Uniform Spectral-Trace Control on $C_n$

To transfer the stationary lattice process to finite cycles $C_n$, we define a 10-state positional site Markov chain:
- State space: $(s, k)$ where $s \in \{22, 23, 32, 33\}$ and $0 \le k < g(s)$.
- Transitions: if $k < g(s) - 1$, transition deterministically to $(s, k+1)$; at the boundary $k = g(s) - 1$, transition to $(u, 0)$ with probability $P_{su}$.
- Output: outputs $1$ if and only if $k = 0$.

The resulting site transition matrix $T$ is $10 \times 10$, irreducible, and aperiodic (with return loops of length 2 and 7, which are coprime).
Its stationary distribution is given explicitly by $\eta_{(s, k)} = \rho \pi_s$.
The characteristic polynomial of $T$ is:
$$\det(zI - T) = \frac{z^3(z-1)}{16}\left(16z^6 + 16z^5 + 6z^4 - 2z^3 - 2z^2 + z + 1\right)$$
By the Perron-Frobenius theorem, $1$ is a simple dominant eigenvalue, and all other eigenvalues satisfy $|\lambda_i| \le \alpha < 1$.
Therefore, for $\Pi = \mathbf{1} \eta$, there exists a constant $C < \infty$ such that:
$$\|T^m - \Pi\| \le C \alpha^m \quad \text{for all } m \ge 0$$

### Uniform Trace Estimates on Cycle $C_n$
Let $Z_n = \operatorname{tr}(T^n)$ be the partition function of closed paths of length $n$. For sufficiently large $n$, $Z_n = 1 + O(\alpha^n) > 0$.
The normalized cyclic probability measure $\mu_n$ assigns to each closed path $\omega = (z_0, \dots, z_{n-1})$ probability $Z_n^{-1} \prod_{i=0}^{n-1} T_{z_i, z_{i+1}}$, inducing a rotation-invariant measure on $\mathcal{L}(C_n)$.
Let $E$ be the diagonal indicator matrix of active sites ($k=0$). The cyclic marginals satisfy:
$$q_{1, n} = \Pr_{\mu_n}(x_0 = 1) = \frac{\operatorname{tr}(E T^n)}{Z_n} = \rho + O(\alpha^n)$$
$$q_{11, n}(d) = \Pr_{\mu_n}(x_0 = x_d = 1) = \frac{\operatorname{tr}(E T^d E T^{n-d})}{Z_n}$$

For any distance $1 \le d \le \lfloor n/2 \rfloor$, separating $T^{n-d} = \Pi + R_{n-d}$ with $\|R_{n-d}\| \le C \alpha^{n-d} \le C \alpha^{n/2}$ yields:
$$q_{11, n}(d) = \operatorname{tr}(E T^d E \Pi) + O(\alpha^{n/2}) + O(\alpha^n) = p_d + O(\alpha^{n/2})$$
Because all valid pairwise states are linear combinations of $q_{1, n}$ and $q_{11, n}(d)$, the minimum probability $c_n = \min_{e \in \mathcal{E}_n} \Pr_{\mu_n}(x \models e)$ across **all** $2n^2 - 3n$ feasible pairwise requirements satisfies the **uniform bound**:
$$c_n = \frac{1}{6} + O(\theta^n), \quad \text{where } \theta = \sqrt{\alpha} < 1$$

---

## 4. Construction of the Fractional Witness for Index $\lambda$

For any fixed integer $\lambda \ge 1$, we assign fractional weights to rows $r \in \mathcal{L}(C_n)$:
$$y_r(\lambda) = \frac{\lambda}{c_n} \mu_n(r)$$

1. **Feasibility**: For every feasible pairwise requirement $e \in \mathcal{E}_n$:
   $$\sum_{r \models e} y_r(\lambda) = \frac{\lambda}{c_n} \Pr_{\mu_n}(x \models e) \ge \frac{\lambda}{c_n} \cdot c_n = \lambda$$
2. **Objective Value**: The total fractional weight is:
   $$\sum_{r \in \mathcal{L}(C_n)} y_r(\lambda) = \frac{\lambda}{c_n} \sum_r \mu_n(r) = \frac{\lambda}{\frac{1}{6} + O(\theta^n)} = 6\lambda + O_\lambda(\theta^n)$$
3. **Variable Upper Bounds ($y_r \le 1$)**:
   Each closed path in $T$ undergoes a random gap transition at least once every 3 sites, yielding at least $n/3$ independent transitions each bounded by $3/4$.
   With at most 10 state lifts for any binary configuration:
   $$\mu_n(r) \le \frac{10}{Z_n} \left(\frac{3}{4}\right)^{n/3} \longrightarrow 0 \quad (n \to \infty)$$
   Therefore, for any fixed $\lambda$, $\max_{r} y_r(\lambda) \le 1$ holds for all sufficiently large $n \ge n_\lambda$.

Combined with the universal dual lower bound $LP_\lambda(n) \ge 6\lambda$ (Chapter 2, generalized), this establishes:
$$\boxed{\lim_{n \to \infty} LP_\lambda(n) = 6\lambda}$$
for every positive integer coverage index $\lambda \ge 1$.
