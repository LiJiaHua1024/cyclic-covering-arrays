# Chapter 5: Integer Complexity and the Asymptotic Integrality Gap

While the continuous fractional relaxation remains bounded and exponentially converges to the theoretical minimum:
$$\lim_{n \to \infty} LP(n) = 12$$
the discrete integer test suite size $N(n)$ exhibits logarithmic divergence.

---

## 1. Theorem Statement

**Theorem (Integer Asymptotic Complexity & Unbounded Gap)**:
For cycle-constrained covering arrays with index $\lambda = 2$:
$$N(n) = \Theta(\log n)$$
Consequently, the additive integrality gap grows unboundedly with cycle length:
$$G(n) = N(n) - LP(n) = \Theta(\log n) \to \infty$$

---

## 2. Information-Theoretic / Coding Lower Bound

Consider a maximum independent set $I$ of the cycle $C_n$, having cardinality:
$$k = |I| = \left\lfloor \frac{n}{2} \right\rfloor$$
Because the vertices in $I$ are pairwise non-adjacent, every pair of factors in $I$ must cover all four binary configurations $\{00, 01, 10, 11\}$.

Let $M = N(n)$ be the number of test rows, and consider the $k$ binary columns of length $M$ corresponding to the vertices in $I$:
1. **No constant columns**: A column cannot be all-zero or all-one, as that would preclude coverage of $11$ or $00$ respectively.
2. **No identical or complementary columns**:
   - If two columns are identical, they can never produce states $01$ or $10$.
   - If two columns are bitwise complementary ($c_1 = \bar{c}_2$), they can never produce states $00$ or $11$.

Therefore, the columns corresponding to $I$ must be pairwise non-constant, distinct, and non-complementary.
Partitioning the $2^M - 2$ non-constant binary vectors of length $M$ into complementary pairs $\{v, \bar{v}\}$ yields at most $2^{M-1} - 1$ distinct pairs.

Hence, we must have:
$$k \le 2^{M-1} - 1 \implies 2^{M-1} \ge \left\lfloor \frac{n}{2} \right\rfloor + 1$$
Taking base-2 logarithms:
$$M \ge 1 + \left\lceil \log_2\left(\left\lfloor \frac{n}{2} \right\rfloor + 1\right) \right\rceil = \Omega(\log n)$$

---

## 3. Probabilistic / Random Construction Upper Bound

To show $N(n) = O(\log n)$, we consider the random selection of rows from the universe of legal configurations $\mathcal{L}(C_n)$, whose size is given by the Lucas number $L_n = F_{n-1} + F_{n+1} \approx \phi^n$.

For any fixed feasible pairwise requirement $(i, j, a, b)$:
- Specifying $(x_i, x_j) = (a, b)$ restricts at most 2 active switches, which in turn forbids at most their adjacent neighbors (at most 4 neighboring switches).
- The remaining unrestricted vertices form a disjoint union of path graphs.
- Direct Fibonacci counting shows that the number of legal completions is at least $F_{n-4}$.
- The ratio of legal completions to the total universe satisfies:
  $$\frac{F_{n-4}}{L_n} > \frac{1}{40} \quad \text{for all } n \ge 7$$

Thus, under uniform random sampling of rows, the probability that a single chosen row covers a specific feasible requirement is at least $p \ge 1/40$.
For a randomly chosen suite of $M$ rows, the probability that a specific requirement fails to achieve coverage at least 2 is bounded by Chernoff / binomial tail bounds:
$$\mathbb{P}(\text{Coverage}(i, j, a, b) < 2) \le (1 + M p) (1 - p)^{M-1} \le (1 + M) \exp(-c M)$$

The total number of feasible requirements is $D_n = 2n^2 - 3n$.
By the union bound across all $D_n$ requirements:
$$\mathbb{P}(\text{Failure}) \le (2n^2 - 3n) (1 + M) \exp(-c M)$$
Choosing $M = C \log n$ for a sufficiently large constant $C$ drives this failure probability strictly below 1:
$$\mathbb{P}(\text{Failure}) < 1$$
By the probabilistic method (or via the Lovász Local Lemma for explicit dependency graphs), there exists a valid integer test suite of size $O(\log n)$.

---

## 4. The Qualitative Contrast

This establishes the fundamental asymptotic divergence between the continuous relaxation and the discrete integer problem:

$$\begin{aligned}
LP(n) &= 12 + O(\theta^n) \longrightarrow 12 \quad (O(1) \text{ bounded}) \\
N(n) &= \Theta(\log n) \longrightarrow \infty \\
G(n) &= N(n) - LP(n) = \Theta(\log n) \longrightarrow \infty
\end{aligned}$$

The integrality gap does not vanish or remain constant in the large-scale limit; rather, it grows logarithmically with dimension $n$.

---

## 5. Context and Connection to Classical Literature

The logarithmic scaling of discrete covering arrays is rooted in the classical extremal set theory of Rényi (1971), Katona (1973), and Kleitman & Spencer (1973). For unconstrained binary covering arrays of strength 2, it is well known that $N \sim \frac{1}{2} \log_2 n$.

In the presence of cyclic exclusion constraints, our result proves that:
1. The logarithmic integer scaling $N(n) = \Theta(\log n)$ continues to hold despite the exclusion of adjacent ones.
2. Crucially, while the integer testing suite must grow logarithmically, the fractional relaxation remains **strictly bounded** and exponentially rapidly stabilizes at $\lim_{n \to \infty} LP(n) = 12$.
3. Consequently, the unit gap $G(n) = 1$ observed on small finite cycles ($C_{13}, C_{14}, C_{15}$) is a localized finite phenomenon: as $n \to \infty$, the true integrality gap diverges to infinity.
