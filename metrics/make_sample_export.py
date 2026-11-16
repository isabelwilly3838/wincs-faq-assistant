"""Create a FAKE Jira export so you can build the Power BI report before real data exists.
The output is clearly labelled SAMPLE. Never put these numbers on your CV.

    python metrics/make_sample_export.py   ->  metrics/sample/SAMPLE_jira_export.csv + SAMPLE_sprints.csv
"""
import csv
import datetime as dt
import random
from pathlib import Path

random.seed(7)
OUT = Path(__file__).parent / "sample"
OUT.mkdir(exist_ok=True)
start = dt.date(2026, 1, 12)
sprints = [(f"WFA Sprint {n}", start + dt.timedelta(days=14 * (n - 1)), start + dt.timedelta(days=14 * n - 1)) for n in (1, 2, 3)]
with (OUT / "SAMPLE_sprints.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["sprint", "start", "end"])
    for s, a, b in sprints:
        w.writerow([s, a, b])

fmt = lambda d: d.strftime("%d/%b/%y 10:00 AM")
rows, k = [], 1
for idx, (name, a, b) in enumerate(sprints):
    for _ in range(8):
        pts = random.choice([1, 2, 2, 3, 3, 5])
        typ = "Bug" if idx > 0 and random.random() < 0.3 else "Story"
        started = a + dt.timedelta(days=random.randint(0, 9))
        resolved = started + dt.timedelta(days=random.randint(1, 4))
        carried = resolved > b and idx < 2
        sp = [name] + ([sprints[idx + 1][0]] if carried else [])
        if resolved > b and idx == 2:
            resolved = None
        rows.append([f"WFA-{k}", typ, f"SAMPLE item {k}", "Done" if resolved else "In Progress", pts,
                     fmt(a - dt.timedelta(days=3)), fmt(started), fmt(resolved) if resolved else ""] + sp)
        k += 1
with (OUT / "SAMPLE_jira_export.csv").open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Issue key", "Issue Type", "Summary", "Status", "Custom field (Story Points)", "Created",
                "Custom field (Start date)", "Resolved", "Sprint", "Sprint"])
    for r in rows:
        w.writerow(r + [""] * (10 - len(r)))
print("wrote", OUT)
