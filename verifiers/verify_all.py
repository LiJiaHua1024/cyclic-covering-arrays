#!/usr/bin/env python3
"""Unified master verifier for all results in the cyclic covering array project.

Runs:
1. verify_markov_chain.py: Proves lim_{n->inf} LP(n) = 12 via exact 2-step gap Markov chain.
2. verify_c13.py: Exact LP=12, N=13 integrality gap on C13 without row repeats.
3. verify_c14.py: Exact LP=12, N=13 certificate on C14 with distinct rows.
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
    ]
    all_ok = True
    for s in scripts:
        if not run_script(s):
            all_ok = False
            break

    print("\n" + "="*50)
    if all_ok:
        print("[✓] ALL MECHANICAL CERTIFICATES VERIFIED SUCCESSFULLY (PASS)")
        print("="*50)
        return 0
    else:
        print("[✗] SOME VERIFICATIONS FAILED")
        print("="*50)
        return 1

if __name__ == '__main__':
    sys.exit(main())
