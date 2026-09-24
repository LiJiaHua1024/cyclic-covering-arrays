#!/usr/bin/env python3
"""Unified master runner for all registered mechanical certificates in the cyclic covering array project.

Executes all 8 independent standard-library verification scripts:
1. verify_markov_chain.py: Rational arithmetic 2-step gap Markov recurrence (lambda=2).
2. verify_c13.py: C13 exact LP=12, N=13 algebraic infeasibility certificate.
3. verify_c14.py: C14 exact LP=12, N=13 modulo-7 congruence obstruction.
4. verify_c15.py: C15 GF(2) rank obstruction across all 4823 edge sets.
5. verify_c17.py: C17 bit-parallel 54,310-node DFS 12-row exclusion.
6. verify_c19.py: C19 bit-parallel 726,693-node DFS 12-row exclusion & 13-row witness.
7. verify_even_cycles_and_c21.py: C16-C22 13-row & C23 14-row integer witnesses, C21 2-row repair check, C20-C23 LP=12 rational certificates.
8. verify_general_lambda.py: Finite exact verification tool checking 3900 scaled rational inequalities (n in 11..30, lambda in 1..5).
"""


import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

def run_script(script_name: str) -> bool:
    print(f"\n==================================================")
    print(f"Running verifier: {script_name}")
    print(f"==================================================")
    script_path = HERE / script_name
    result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip(), file=sys.stderr)
    if result.returncode != 0:
        print(f"[-] FAILED: {script_name}")
        return False
    print(f"[+] PASSED: {script_name}")
    return True

def main():
    scripts = [
        "verify_markov_chain.py",
        "verify_c13.py",
        "verify_c14.py",
        "verify_c15.py",
        "verify_c17.py",
        "verify_c19.py",
        "verify_even_cycles_and_c21.py",
        "verify_general_lambda.py",
    ]
    all_ok = True
    for s in scripts:
        if not run_script(s):
            all_ok = False
            break

    print("\n" + "="*50)
    if all_ok:
        print("[✓] ALL 8 REGISTERED MECHANICAL CERTIFICATES VERIFIED SUCCESSFULLY (PASS)")
        print("="*50)

        return 0
    else:
        print("[✗] SOME VERIFICATIONS FAILED")
        print("="*50)
        return 1

if __name__ == '__main__':
    sys.exit(main())
