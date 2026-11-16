"""Score SUS responses and compare rounds.

    python usability/sus_score.py usability/sus_responses.csv

CSV columns: participant,round,q1..q10 (each 1-5).
SUS per person = ((sum of (odd item - 1)) + (sum of (5 - even item))) * 2.5   -> 0..100
Benchmark: 68 is average. Adjective scale (Bangor et al., 2009): ~51 OK, ~71 Good, ~85 Excellent.
"""
import csv
import statistics as st
import sys
from collections import defaultdict


def sus(answers: list[int]) -> float:
    if len(answers) != 10 or not all(1 <= a <= 5 for a in answers):
        raise ValueError(f"need 10 answers between 1 and 5, got {answers}")
    odd = sum(a - 1 for a in answers[0::2])
    even = sum(5 - a for a in answers[1::2])
    return (odd + even) * 2.5


def grade(score: float) -> str:
    return "Excellent" if score >= 85 else "Good" if score >= 71 else "OK" if score >= 51 else "Poor"


def main(path: str) -> None:
    rounds = defaultdict(list)
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            s = sus([int(r[f"q{i}"]) for i in range(1, 11)])
            rounds[r["round"]].append(s)
            print(f"round {r['round']}  {r['participant']:<10} {s:5.1f}")
    print()
    means = {}
    for rnd, scores in sorted(rounds.items()):
        means[rnd] = st.mean(scores)
        sd = st.stdev(scores) if len(scores) > 1 else 0
        print(f"Round {rnd}: n={len(scores)}  mean={means[rnd]:.1f}  sd={sd:.1f}  ({grade(means[rnd])})")
    if len(means) >= 2:
        first, last = list(means)[0], list(means)[-1]
        print(f"Change round {first} -> {last}: {means[last] - means[first]:+.1f} points")
        print("Note: with n=5 per round, report this as an indicative change, not a statistically significant one.")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "usability/sus_responses.csv")
