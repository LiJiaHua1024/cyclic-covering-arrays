#!/usr/bin/env python3
"""
Verifier for Even Cycles (C16, C18), the Continuous Plateau [13, 19],
and Cycle C21 (14-row upper bound & 1/2-row repair obstruction on the near-miss).
"""
import os
from itertools import combinations, product
from time import perf_counter

SUITES = {
    16: [
        37458, 43306, 43668, 42314, 18773, 21162, 19114,
        42130, 10825, 21673, 38180, 8869, 21845,
    ],
    18: [
        76362, 86674, 43689, 174418, 152746, 87369, 76453,
        150100, 168612, 38229, 173354, 84261, 74901,
    ],
    20: [
        149845, 169129, 300370, 305829, 337225, 346410, 348821,
        600658, 611474, 611620, 676426, 697684, 699050,
    ],
}

NEAR_21 = [
    338517, 599338, 608914, 693589, 1223338, 1348170, 676517,
    1201490, 349353, 698697, 1352852, 1397066, 1394980,
]
SUITES[21] = [
    299605, 338213, 599189, 600658, 608841, 676517, 693546,
    697673, 1198418, 1223316, 1354410, 1397930, 1398100,
]
SUITES[22] = [
    599205, 692821, 1198741, 1221970, 1354021, 1354057, 1397418,
    1398089, 2397332, 2435666, 2705748, 2774314, 2796202,
]



def bit(mask, i, n):
    return (mask >> (i % n)) & 1


def inspect(n, rows):
    assert len(rows) == len(set(rows)), f"Repeated rows for C{n}"
    assert all(0 <= mask < (1 << n) for mask in rows)

    for mask in rows:
        assert all(
            not (bit(mask, i, n) and bit(mask, i + 1, n))
            for i in range(n)
        ), f"Adjacent 11 violated for C{n}"

    failures = []
    checked = 0
    for d in range(1, n // 2 + 1):
        for i in range(n):
            j = (i + d) % n
            if n % 2 == 0 and d == n // 2 and i > j:
                continue

            for a, b in product((0, 1), repeat=2):
                if d == 1 and a == b == 1:
                    continue

                count = sum(
                    bit(mask, i, n) == a and bit(mask, j, n) == b
                    for mask in rows
                )
                checked += 1
                if count < 2:
                    failures.append(((i, j, a, b), count))

    assert checked == 2 * n * n - 3 * n
    return failures, checked


def verify_c21_repair_obstruction():
    n = 21
    full = (1 << n) - 1
    def legal(m):
        shifted = ((m << 1) | (m >> (n - 1))) & full
        return not (m & shifted)

    requirements = [
        (i, (i + d) % n, a, b)
        for d in range(1, 11)
        for i in range(n)
        for a, b in product((0, 1), repeat=2)
        if d != 1 or (a, b) != (1, 1)
    ]
    assert len(requirements) == 819

    masks = [m for m in range(1 << n) if legal(m)]
    assert len(masks) == 24476
    idx = {m: j for j, m in enumerate(masks)}

    signature = []
    for m in masks:
        bits = 0
        for p, (i, j, a, b) in enumerate(requirements):
            if ((m >> i) & 1) == a and ((m >> j) & 1) == b:
                bits |= 1 << p
        signature.append(bits)

    original = [signature[idx[m]] for m in NEAR_21]
    counts = [
        sum(bits >> p & 1 for bits in original)
        for p in range(len(requirements))
    ]
    deficiencies = [
        (requirements[p], counts[p])
        for p in range(len(requirements))
        if counts[p] < 2
    ]
    assert deficiencies == [((5, 15, 1, 1), 1)]

    inverse = [0] * len(requirements)
    for j, bits in enumerate(signature):
        candidate_bit = 1 << j
        while bits:
            low = bits & -bits
            inverse[low.bit_length() - 1] |= candidate_bit
            bits -= low

    missing_p = requirements.index((5, 15, 1, 1))
    old_ids = {idx[m] for m in NEAR_21}

    # 1-row replacement check
    one_row_repairs = 0
    for a in range(13):
        rem = [counts[p] - (original[a] >> p & 1) for p in range(len(requirements))]
        if 0 in rem:
            continue
        must_cover = sum(1 << p for p, c in enumerate(rem) if c == 1)
        forbidden = old_ids - {idx[NEAR_21[a]]}
        one_row_repairs += sum(
            j not in forbidden and (sig & must_cover == must_cover)
            for j, sig in enumerate(signature)
        )
    assert one_row_repairs == 0

    # 2-row replacement check
    first_candidates_checked = 0
    two_row_repair = None
    for a, b in combinations(range(13), 2):
        rem = [counts[p] - (original[a] >> p & 1) - (original[b] >> p & 1) for p in range(len(requirements))]
        both_must = sum(1 << p for p, c in enumerate(rem) if c == 0)
        one_must = sum(1 << p for p, c in enumerate(rem) if c == 1)
        forbidden = old_ids - {idx[NEAR_21[a]], idx[NEAR_21[b]]}

        for x, x_bits in enumerate(signature):
            if x in forbidden or not (x_bits >> missing_p & 1):
                continue
            if x_bits & both_must != both_must:
                continue

            first_candidates_checked += 1
            target = both_must | (one_must & ~x_bits)
            possible = (1 << len(masks)) - 1
            while target and possible:
                low = target & -target
                possible &= inverse[low.bit_length() - 1]
                target -= low

            possible &= ~(1 << x)
            for old_j in forbidden:
                possible &= ~(1 << old_j)

            if possible:
                two_row_repair = True
                break
        if two_row_repair:
            break

    assert first_candidates_checked == 40826
    assert two_row_repair is None
    print(f"      C21 near-miss repair check: 0 1-row repairs, 0 2-row repairs across {first_candidates_checked} candidate pairs.")


def main():
    t0 = perf_counter()
    # Verify C16 (13 rows, 464 requirements)
    f16, c16 = inspect(16, SUITES[16])
    assert not f16 and c16 == 464
    print("PASS: C16 verified (13 rows; 464 requirements covered >= 2).")

    # Verify C18 (13 rows, 594 requirements)
    f18, c18 = inspect(18, SUITES[18])
    assert not f18 and c18 == 594
    print("PASS: C18 verified (13 rows; 594 requirements covered >= 2).")

    # Verify C20 (13 rows, 740 requirements)
    f20, c20 = inspect(20, SUITES[20])
    assert not f20 and c20 == 740
    print("PASS: C20 verified (13 rows; 740 requirements covered >= 2).")

    # Verify C21 (13 rows, 819 requirements)
    f21, c21 = inspect(21, SUITES[21])
    assert not f21 and c21 == 819
    print("PASS: C21 verified (13 rows; 819 requirements covered >= 2).")

    # Verify C22 (13 rows, 902 requirements)
    f22, c22 = inspect(22, SUITES[22])
    assert not f22 and c22 == 902
    print("PASS: C22 verified (13 rows; 902 requirements covered >= 2).")

    # Verify C21 repair obstruction
    verify_c21_repair_obstruction()

    # Verify exact rational LP=12 witnesses for C20, C21, C22, C23
    verify_fractional_lp_certificates()

    print(f"All extended cycle and plateau checks passed in {perf_counter() - t0:.2f}s.")


def verify_fractional_lp_certificates():
    from fractions import Fraction
    # C20 LP=12 rational certificate
    N20 = 20
    full20 = (1 << N20) - 1
    reps20 = [149797, 150165, 152741, 152917, 173397]
    weights20 = [Fraction(4, 35), Fraction(4, 35), Fraction(2, 35), Fraction(1, 7), Fraction(6, 35)]
    w20 = {}
    tot20 = Fraction(0)
    for rep, w in zip(reps20, weights20):
        orb = {((rep << k) | (rep >> (N20 - k))) & full20 for k in range(N20)}
        assert len(orb) == 20
        for r in orb:
            w20[r] = w20.get(r, Fraction(0)) + w
            tot20 += w
    assert tot20 == 12

    for d in range(1, N20 // 2 + 1):
        for i in range(N20):
            j = (i + d) % N20
            patterns = ((0, 0), (0, 1), (1, 0)) if d == 1 else ((0, 0), (0, 1), (1, 0), (1, 1))
            for a, b in patterns:
                cov = sum(w for r, w in w20.items() if ((r >> i) & 1) == a and ((r >> j) & 1) == b)
                assert cov >= 2
    print("PASS: C20 exact rational LP=12 witness verified (5 orbits, total weight 12).")

    # C21 LP=12 rational certificate
    N21 = 21
    full21 = (1 << N21) - 1
    reps21 = [299593, 300325, 305813, 349525]
    weights21 = [Fraction(5, 17), Fraction(2, 17), Fraction(6, 17), Fraction(1, 17)]
    w21 = {}
    tot21 = Fraction(0)
    for rep, w in zip(reps21, weights21):
        orb = {((rep << k) | (rep >> (N21 - k))) & full21 for k in range(N21)}
        for r in orb:
            w21[r] = w21.get(r, Fraction(0)) + w
            tot21 += w
    assert tot21 == 12

    for d in range(1, N21 // 2 + 1):
        for i in range(N21):
            j = (i + d) % N21
            patterns = ((0, 0), (0, 1), (1, 0)) if d == 1 else ((0, 0), (0, 1), (1, 0), (1, 1))
            for a, b in patterns:
                cov = sum(w for r, w in w21.items() if ((r >> i) & 1) == a and ((r >> j) & 1) == b)
                assert cov >= 2
    print("PASS: C21 exact rational LP=12 witness verified (4 orbits, total weight 12).")

    # C22 LP=12 rational certificate
    N22 = 22
    full22 = (1 << N22) - 1
    reps22 = [599189, 608597, 610965, 697685, 1398101]
    weights22 = [Fraction(3, 25), Fraction(4, 25), Fraction(2, 25), Fraction(4, 25), Fraction(7, 25)]
    w22 = {}
    tot22 = Fraction(0)
    for rep, w in zip(reps22, weights22):
        orb = {((rep << k) | (rep >> (N22 - k))) & full22 for k in range(N22)}
        for r in orb:
            w22[r] = w22.get(r, Fraction(0)) + w
            tot22 += w
    assert tot22 == 12

    for d in range(1, N22 // 2 + 1):
        for i in range(N22):
            j = (i + d) % N22
            patterns = ((0, 0), (0, 1), (1, 0)) if d == 1 else ((0, 0), (0, 1), (1, 0), (1, 1))
            for a, b in patterns:
                cov = sum(w for r, w in w22.items() if ((r >> i) & 1) == a and ((r >> j) & 1) == b)
                assert cov >= 2
    print("PASS: C22 exact rational LP=12 witness verified (5 orbits, total weight 12).")

    # C23 LP=12 rational certificate
    N23 = 23
    full23 = (1 << N23) - 1
    reps23 = [1198421, 1200725, 1201301, 1354325, 1398101]
    weights23 = [Fraction(19, 253), Fraction(21, 253), Fraction(38, 253), Fraction(31, 253), Fraction(1, 11)]
    w23 = {}
    tot23 = Fraction(0)
    for rep, w in zip(reps23, weights23):
        orb = {((rep << k) | (rep >> (N23 - k))) & full23 for k in range(N23)}
        for r in orb:
            w23[r] = w23.get(r, Fraction(0)) + w
            tot23 += w
    assert tot23 == 12

    for d in range(1, N23 // 2 + 1):
        for i in range(N23):
            j = (i + d) % N23
            patterns = ((0, 0), (0, 1), (1, 0)) if d == 1 else ((0, 0), (0, 1), (1, 0), (1, 1))
            for a, b in patterns:
                cov = sum(w for r, w in w23.items() if ((r >> i) & 1) == a and ((r >> j) & 1) == b)
                assert cov >= 2
    print("PASS: C23 exact rational LP=12 witness verified (5 orbits, total weight 12).")



if __name__ == "__main__":
    main()
