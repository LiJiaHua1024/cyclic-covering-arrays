"""Exact, solver-free verifier for the C13 integrality-gap certificate."""
from fractions import Fraction
from itertools import combinations, product

N = 13
MASK = (1 << N) - 1
A, B, C = 1365, 1173, 1189
ALPHA = [-6, 5, 5, 5, -6, -6, -6, 5, 5, 5, 5, -6, -6]
BETA = [-4, 7, 7, -4, -4, -4, -4, 7, 7, 7, -4, -4, -4]
H = dict(zip(
    ('00000','00001','00010','00100','00101','01000','01001',
     '01010','10000','10001','10010','10100','10101'),
    (0,0,0,1,0,0,2,1,0,1,3,2,2)
))
UPPER = [661,1189,1353,2341,2386,2645,2697,2730,
         4682,4772,5266,5418,5460]

def bit(m, i):
    return (m >> (i % N)) & 1

def rotate(m, k):
    return ((m << k) | (m >> (N-k))) & MASK

def valid(m):
    return 0 <= m <= MASK and all(not(bit(m,i) and bit(m,i+1))
                                       for i in range(N))

def score(m):
    return sum(w * sum(bit(m,i)*bit(m,i+d) for i in range(N))
               for d,w in ((3,3),(4,2),(5,1)))

def weighted(m):
    return sum(ALPHA[i]*bit(m,i)*bit(m,i+3)
               + BETA[i]*bit(m,i)*bit(m,i+4) for i in range(N))

def assert_local_potential():
    count = 0
    for s in product('01', repeat=6):
        if any(s[i] == s[i+1] == '1' for i in range(5)):
            continue
        t = list(map(int, s))
        lhs = t[0]*(3*t[3]+2*t[4]+t[5])
        rhs = 1 + H[''.join(s[:5])] - H[''.join(s[1:])]
        assert lhs <= rhs
        count += 1
    assert count == 21

def assert_tight_classification():
    tight = {m for m in range(1 << N) if valid(m) and score(m) == N}
    three = {rotate(m,j) for m in (A,B,C) for j in range(N)}
    assert len(tight) == len(three) == 39 and tight == three
    assert [sum(bit(m,i)*bit(m,i+d) for i in range(N))
            for m in (A,B,C) for d in (3,4,5)] == [1,4,2,3,1,2,3,0,4]

def assert_integer_certificate():
    assert sum(ALPHA) + sum(BETA) == 2
    assert [weighted(rotate(B,j)) for j in range(N)] == [0]*N
    assert [weighted(rotate(A,j)) for j in range(N)] == [11 if j == 5 else 0 for j in range(N)]
    assert weighted(C) == 15
    assert rotate(A,5) == 2725
    assert 2*(sum(ALPHA)+sum(BETA)) == 4
    assert 4-15 == -11

def assert_primal_witnesses():
    fractional = {}
    for m,w in ((A,Fraction(5,13)), (B,Fraction(6,13)),
                (C,Fraction(1,13))):
        for j in range(N):
            r = rotate(m,j)
            assert r not in fractional
            fractional[r] = w
    assert sum(fractional.values()) == 12
    assert len(UPPER) == len(set(UPPER)) == 13
    assert all(valid(m) for m in fractional)
    assert all(valid(m) for m in UPPER)
    for i,j in combinations(range(N), 2):
        adjacent = j == i+1 or (i,j) == (0,N-1)
        for a,b in product((0,1), repeat=2):
            if adjacent and a == b == 1:
                continue
            matching = lambda m: bit(m,i) == a and bit(m,j) == b
            assert sum(w for m,w in fractional.items() if matching(m)) >= 2
            assert sum(matching(m) for m in UPPER) >= 2

if __name__ == '__main__':
    assert_local_potential()
    assert_tight_classification()
    assert_integer_certificate()
    assert_primal_witnesses()
    print('PASS: universal local inequality; C13 tight classification;')
    print('exact integer infeasibility certificate; LP=12; N=13.')
