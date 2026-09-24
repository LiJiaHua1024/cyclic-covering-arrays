# Chapter 1: Introduction and Mathematical Model

## 1. Problem Definition

Let $C_n$ denote the undirected cycle graph on $n$ vertices labeled $0, 1, \dots, n-1$, with edges $(i, i+1)$ for $0 \le i < n-1$ and the wrap-around edge $(n-1, 0)$.
We consider combinatorial interaction testing on $n$ binary factors $x = (x_0, x_1, \dots, x_{n-1}) \in \{0, 1\}^n$ subject to **adjacent exclusion constraints**:
$$x_i + x_{(i+1) \bmod n} \le 1 \quad (0 \le i < n)$$

A binary vector $x$ satisfying this condition corresponds to an **independent set** of the cycle graph $C_n$.
The set of all legal test configurations is denoted by $\mathcal{L}(C_n)$.
The cardinality $|\mathcal{L}(C_n)|$ is given by the Lucas numbers:
$$L_n = F_{n-1} + F_{n+1}$$
where $F_0 = 0, F_1 = 1, F_2 = 1, \dots$ are the Fibonacci numbers.

---

## 2. Coverage Requirements ($\lambda = 2$)

In combinatorial testing of strength 2 and index $\lambda = 2$, every pairwise interaction $(x_i, x_j) = (a, b)$ that can legitimately appear in some legal configuration must be covered at least twice across the test suite:

- For **adjacent pairs** (distance 1 on $C_n$), the state $(1, 1)$ is forbidden. The 3 feasible states are $(0, 0), (0, 1), (1, 0)$.
- For **non-adjacent pairs** (distance $d \ge 2$), all 4 states $(0, 0), (0, 1), (1, 0), (1, 1)$ are feasible.

The total number of extendible 2-way requirements on $C_n$ is:
$$D_n = 3n + 4\left(\binom{n}{2} - n\right) = 2n^2 - 3n$$

| $n$ | Universe Size $|\mathcal{L}(C_n)| = L_n$ | Demand Count $D_n = 2n^2 - 3n$ | Feasibility Status |
|---:|---:|---:|:---|
| 4 | 7 | 20 | Infeasible ($\lambda=2$) |
| 5 | 11 | 35 | Infeasible ($\lambda=2$) |
| 6 | 18 | 54 | Infeasible ($\lambda=2$) |
| 7 | 29 | 77 | Feasible |
| 8 | 47 | 104 | Feasible |
| ... | ... | ... | ... |
| 13 | 521 | 299 | Feasible ($LP=12, N=13$) |
| 14 | 843 | 350 | Feasible ($LP=12, N=13$) |
| 15 | 1364 | 405 | Feasible ($LP=12, N=13$) |

### Infeasibility for $n \in \{4, 5, 6\}$
For $n \in \{4, 5, 6\}$, certain feasible $11$ states can only be extended by a **unique** legal configuration:
- On $C_4$: pair $(0, 2) = (1, 1) \implies (1, 0, 1, 0)$ is the unique extension.
- On $C_5$: pair $(0, 2) = (1, 1) \implies (1, 0, 1, 0, 0)$ is the unique extension.
- On $C_6$: pair $(0, 3) = (1, 1) \implies (1, 0, 0, 1, 0, 0)$ is the unique extension.

Because complete test configurations must be distinct (or row capacity $y_r \le 1$), these states cannot be covered twice. Hence, $LP(n) = N(n) = +\infty$ for $n \le 6$.
For all $n \ge 7$, every feasible requirement admits at least two distinct extensions.

---

## 3. Mathematical Optimization Formulation

Let $z_x \in \{0, 1\}$ indicate whether legal configuration $x \in \mathcal{L}(C_n)$ is included in the test suite.
The integer programming (IP) formulation is:
$$\min \sum_{x \in \mathcal{L}(C_n)} z_x \quad \text{s.t.} \quad \sum_{x: (x_i, x_j)=(a, b)} z_x \ge 2 \quad (\forall (i, j, a, b) \in \mathcal{R}), \quad z_x \in \{0, 1\}$$
The optimal integer value is denoted $N(n)$.

The linear programming (LP) relaxation relaxes $z_x \in \{0, 1\}$ to $0 \le y_x \le 1$:
$$LP(n) = \min \sum_{x \in \mathcal{L}(C_n)} y_x \quad \text{s.t.} \quad \sum_{x: (x_i, x_j)=(a, b)} y_x \ge 2 \quad (\forall (i, j, a, b) \in \mathcal{R}), \quad 0 \le y_x \le 1$$

The **additive integrality gap** is:
$$G(n) = N(n) - LP(n) \ge 0$$
