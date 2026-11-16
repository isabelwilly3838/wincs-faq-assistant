"""Run the 30-case AI test plan against the live model.

    python evals/run_evals.py            # writes evals/results/run-<timestamp>.csv
    python evals/run_evals.py --only TC13 TC14

Automatic checks: status matches, every must_include term present ('|' separates terms; all are
required), and no must_not_include term present. A human should still read each answer:
fill in the 'manual_verdict' column (pass/fail) in the results CSV before reporting numbers.
Each run costs a little API usage (30 short requests).
"""
import argparse
import csv
import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from assistant.core import ask, load_kb  # noqa: E402

CASES = ROOT / "evals" / "test_cases.csv"
OUT = ROOT / "evals" / "results"


def check(case, a):
    problems = []
    if a.status != case["expected_status"]:
        problems.append(f"status {a.status} != {case['expected_status']}")
    low = a.text.lower()
    if case["must_include"]:
        alts = [t.strip().lower() for t in case["must_include"].split("|")]
        missing = [t for t in alts if t and t not in low]
        if missing:
            problems.append("missing: " + ", ".join(missing))
    if case["must_not_include"]:
        bad = [t for t in case["must_not_include"].split("|") if t.strip() and t.strip().lower() in low]
        if bad:
            problems.append("contains: " + ", ".join(bad))
    return problems


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--only", nargs="*")
    args = p.parse_args()
    chunks = load_kb()
    cases = list(csv.DictReader(CASES.open(encoding="utf-8")))
    if args.only:
        cases = [c for c in cases if c["id"] in args.only]
    OUT.mkdir(exist_ok=True)
    out = OUT / f"run-{dt.datetime.now():%Y%m%d-%H%M%S}.csv"
    passed = 0
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "category", "input", "status", "auto_result", "problems", "answer", "manual_verdict"])
        for c in cases:
            text = "" if c["input"] == "(empty message)" else c["input"]
            a = ask(text, chunks=chunks)
            problems = check(c, a)
            ok = not problems
            passed += ok
            print(f"{c['id']:5} {c['category']:13} {'PASS' if ok else 'FAIL'}  {'; '.join(problems)}")
            w.writerow([c["id"], c["category"], c["input"], a.status, "pass" if ok else "fail", "; ".join(problems), a.text, ""])
    print(f"\n{passed}/{len(cases)} passed automatic checks -> {out.relative_to(ROOT)}")
    print("Read each answer and fill 'manual_verdict'. Log every real failure as a Bug in Jira.")


if __name__ == "__main__":
    main()
