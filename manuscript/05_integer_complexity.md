# Chapter 5: Integer Complexity and the Asymptotic Integrality Gap for Arbitrary Index $\lambda$

While the continuous fractional relaxation remains bounded and exponentially converges to the theoretical minimum:
$$\lim_{n \to \infty} LP_\lambda(n) = 6\lambda$$
the discrete integer test suite size $N_\lambda(n)$ exhibits logarithmic divergence for any fixed coverage index $\lambda \ge 1$.

---

## 1. Theorem Statement

**Theorem (Integer Asymptotic Complexity & Unbounded Integrality Gap for Arbitrary Index $\lambda$)**:
For cycle-constrained covering arrays with arbitrary fixed index $\lambda \ge 1$:
$$N_\lambda(n) = \Theta_\lambda(\log n)$$
Consequently, the additive integrality gap grows unboundedly with cycle length:
$$G_\lambda(n) = N_\lambda(n) - LP_\lambda(n) = \Theta_\lambda(\log n) \longrightarrow \infty \quad (n \to \infty)$$

---

## 2. Information-Theoretic / Sphere-Packing Lower Bound

Consider a maximum independent set $I$ of the cycle graph $C_n$, having cardinality:
$$k = |I| = \left\lfloor \frac{n}{2} \right\rfloor$$
Because the vertices in $I$ are pairwise non-adjacent along $C_n$, every pair of factors $u, v \in I$ has all four binary configurations $\{00, 01, 10, 11\}$ legally extendible, and thus each must appear at least $\lambda$ times across the $M = N_\lambda(n)$ rows of the test suite.

Viewing the test suite as an $M \times k$ binary matrix, each vertex $v \in I$ defines a binary column code word $c_v \in \{0, 1\}^M$:
1. **Weight constraints**: No column can have Hamming weight $< \lambda$ (otherwise $11$ cannot appear $\lambda$ times) or $> M - \lambda$ (otherwise $00$ cannot appear $\lambda$ times).
2. **Hamming distance constraints**: For any distinct $u, v \in I$, the number of positions where $(c_u, c_v) = (0, 1)$ must be at least $\lambda$, and where $(c_u, c_v) = (1, 0)$ must be at least $\lambda$.
   In particular, the Hamming distance satisfies:
   $$d_H(c_u, c_v) \ge 2\lambda, \qquad d_H(c_u, \bar{c}_v) \ge 2\lambda$$

Applying the sphere-packing (Hamming) bound on the binary hypercube $\{0, 1\}^M$:
The Hamming spheres of radius $\lambda - 1$ centered at each $c_u$ and its bitwise complement $\bar{c}_u$ are pairwise disjoint.
The volume of a Hamming sphere of radius $\lambda - 1$ in $\{0, 1\}^M$ is:
$$V(M, \lambda - 1) = \sum_{j=0}^{\lambda - 1} \binom{M}{j}$$
Since there are $k$ columns and $2k$ mutually disjoint spheres of radius $\lambda - 1$:
$$2k \cdot \sum_{j=0}^{\lambda - 1} \binom{M}{j} \le 2^M$$
Taking base-2 logarithms yields the rigorous information-theoretic lower bound:
$$M \ge 1 + \log_2 k + \log_2\left(\sum_{j=0}^{\lambda - 1} \binom{M}{j}\right) = \Omega_\lambda(\log n)$$
For $\lambda = 2$, this specializes to $2k(1 + M) \le 2^M \implies M \ge 1 + \lceil \log_2(\lfloor n/2 \rfloor + 1) \rceil$.

---

## 3. Probabilistic Construction Upper Bound for General $\lambda$

To establish $N_\lambda(n) = O_\lambda(\log n)$, we apply the probabilistic method by sampling rows independently and uniformly at random from the universe of legal configurations $\mathcal{L}(C_n)$, whose cardinality is given by the Lucas number $L_n = F_{n-1} + F_{n+1} = \Theta(\phi^n)$.

### Single-Row Success Probability
For any fixed feasible pairwise requirement $(i, j, a, b)$:
- Fixing $(x_i, x_j) = (a, b)$ pins down at most 2 active switches, which in turn forbids only their adjacent neighbors (at most 4 neighboring switches).
- The remaining unconstrained vertices form a disjoint collection of paths of total length at least $n - 6$.
- By Fibonacci transfer matrix bounds, the number of legal completions is at least $F_{n-4}$.
- For all $n \ge 11$, the single-row hit probability satisfies:
  $$p = \frac{|\{x \in \mathcal{L}(C_n) : (x_i, x_j) = (a, b)\}|}{L_n} \ge \frac{F_{n-4}}{L_n} \ge \frac{1}{64}$$

### Chernoff Tail Bound Across $M$ Independent Trials
Let $X \sim \operatorname{Bin}(M, p)$ be the number of rows covering a fixed requirement $(i, j, a, b)$.
The probability that this requirement is covered fewer than $\lambda$ times is:
$$\mathbb{P}(X < \lambda) = \sum_{j=0}^{\lambda - 1} \binom{M}{j} p^j (1 - p)^{M - j} \le \binom{M}{\lambda - 1} (1 - p)^{M - \lambda + 1} \le M^{\lambda - 1} \exp(-p(M - \lambda + 1))$$
The total number of feasible requirements on $C_n$ is $D_n = 2n^2 - 3n < 2n^2$.
By the union bound across all $D_n$ requirements:
$$\mathbb{P}(\text{Coverage Failure}) \le 2n^2 M^{\lambda - 1} \exp(-p(M - \lambda + 1))$$

### Pairwise Distinctness of Selected Rows
Because rows are sampled from the exponentially large universe $|\mathcal{L}(C_n)| = L_n = \Theta(\phi^n)$, the probability of selecting duplicate rows satisfies:
$$\mathbb{P}(\text{Duplicate Rows}) \le \binom{M}{2} \frac{1}{L_n} \le \frac{M^2}{2 \phi^n} \longrightarrow 0 \quad (n \to \infty)$$

Combining both failure modes via the union bound:
$$\mathbb{P}(\text{Failure}) \le 2n^2 M^{\lambda - 1} \exp(-p(M - \lambda + 1)) + \frac{M^2}{2 \phi^n}$$
Setting $M = \left\lceil \frac{2}{p} \ln n + \frac{\lambda - 1}{p} \ln \ln n + C_\lambda \right\rceil$ ensures that:
$$\mathbb{P}(\text{Failure}) < 1$$
for all sufficiently large $n$.
By the probabilistic method, there exists a valid covering array of size $M = O_\lambda(\log n)$ with **strictly distinct rows**.

---

## 4. The Qualitative Contrast

This establishes the universal asymptotic divergence between the continuous relaxation and the discrete integer problem for every index $\lambda \ge 1$:

$$\begin{aligned}
LP_\lambda(n) &= 6\lambda + O_\lambda(\theta^n) \longrightarrow 6\lambda \quad (O(1) \text{ bounded}) \\
N_\lambda(n) &= \Theta_\lambda(\log n) \longrightarrow \infty \\
G_\lambda(n) &= N_\lambda(n) - LP_\lambda(n) = \Theta_\lambda(\log n) \longrightarrow \infty
\end{aligned}$$

The integrality gap does not vanish or remain constant in the large-scale limit; rather, it diverges logarithmically with dimension $n$ for all $\lambda \ge 1$.

---

## 5. Connection to CAFE Literature

In the terminology of Danziger, Mendelsohn, Moura, and Stevens (*Covering arrays avoiding forbidden edges*, Theoretical Computer Science, 410(8-10):746–758, 2009), this problem corresponds to a **CAFE** (Covering Array Avoiding Forbidden Edges) of strength 2, index $\lambda$, on the binary hypercube with forbidden edge graph $G = C_n$.

Our results establish three foundational properties for cyclic CAFE:
1. **Universal LP Lower Bound**: The local scoring potential proves that $LP_\lambda(C_n) \ge 6\lambda$ for all $n \ge 11$, showing that cyclic constraints enforce an absolute fractional floor proportional to $6\lambda$.
2. **Exponentially Rapid Asymptotic Saturation**: The 2-step Markov chain and transfer matrix trace bounds prove that the fractional relaxation saturates at $6\lambda$ exponentially fast: $LP_\lambda(C_n) = 6\lambda + O_\lambda(\theta^n)$.
3. **Fractional–Integral Separation**: While the LP relaxation remains flat at $6\lambda$, the integer testing complexity $N_\lambda(C_n) = \Theta_\lambda(\log n)$ diverges, proving that cyclic CAFE exhibits an unbounded integrality gap $G_\lambda(C_n) \to \infty$.
