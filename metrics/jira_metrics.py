"""Turn a Jira CSV export into tidy tables for Power BI.

    python metrics/jira_metrics.py <jira_export.csv> metrics/sprints.csv [--out metrics/out]

Inputs
  jira_export.csv  Jira → Filters → "labels = wincs-faq" → Export → CSV (all fields).
  sprints.csv      columns: sprint,start,end   (dates YYYY-MM-DD, end inclusive)

Outputs (in --out)
  issues.csv     one row per issue: points, sprints, start/resolved dates, cycle & lead time (days)
  velocity.csv   per sprint: committed points, completed points, stories done
  burndown.csv   per sprint per day: remaining points and the ideal line

Definitions
  committed  = points of all issues that were in the sprint (Jira's Sprint field)
  completed  = points of those issues resolved between the sprint's start and end dates
  cycle time = Start date (set by the "In Progress" automation) → Resolved, in days
  lead time  = Created → Resolved, in days
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
from pathlib import Path

DATE_FORMATS = ["%d/%b/%y %I:%M %p", "%d/%b/%y", "%Y-%m-%d %H:%M", "%Y-%m-%d", "%d/%m/%Y %H:%M", "%d/%m/%Y"]
POINT_COLS = ["Custom field (Story Points)", "Custom field (Story point estimate)", "Story Points", "Story point estimate"]
START_COLS = ["Custom field (Start date)", "Start date"]


def parse_date(s: str) -> dt.date | None:
    s = (s or "").strip()
    for f in DATE_FORMATS:
        try:
            return dt.datetime.strptime(s, f).date()
        except ValueError:
            pass
    return None


def read_export(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    header, data = rows[0], rows[1:]
    issues = []
    for r in data:
        get = lambda name: next((r[i] for i, h in enumerate(header) if h == name and i < len(r) and r[i]), "")
        pts = next((get(c) for c in POINT_COLS if get(c)), "")
        start = next((get(c) for c in START_COLS if get(c)), "")
        sprints = [r[i] for i, h in enumerate(header) if h == "Sprint" and i < len(r) and r[i]]  # repeated column
        issues.append(
            {
                "key": get("Issue key"),
                "type": get("Issue Type"),
                "summary": get("Summary"),
                "status": get("Status"),
                "points": float(pts) if pts else 0.0,
                "sprints": sprints,
                "created": parse_date(get("Created")),
                "started": parse_date(start),
                "resolved": parse_date(get("Resolved")),
            }
        )
    return [i for i in issues if i["type"] != "Epic"]


def read_sprints(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return [
            {"sprint": r["sprint"], "start": dt.date.fromisoformat(r["start"]), "end": dt.date.fromisoformat(r["end"])}
            for r in csv.DictReader(f)
        ]


def days(a, b):
    return (b - a).days if a and b else ""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("export", type=Path)
    p.add_argument("sprints", type=Path)
    p.add_argument("--out", type=Path, default=Path(__file__).parent / "out")
    a = p.parse_args()
    issues, sprints = read_export(a.export), read_sprints(a.sprints)
    a.out.mkdir(parents=True, exist_ok=True)

    with (a.out / "issues.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["key", "type", "summary", "status", "points", "last_sprint", "sprint_count",
                    "created", "started", "resolved", "cycle_days", "lead_days"])
        for i in issues:
            w.writerow([i["key"], i["type"], i["summary"], i["status"], i["points"],
                        i["sprints"][-1] if i["sprints"] else "", len(i["sprints"]),
                        i["created"] or "", i["started"] or "", i["resolved"] or "",
                        days(i["started"], i["resolved"]), days(i["created"], i["resolved"])])

    with (a.out / "velocity.csv").open("w", newline="") as fv, (a.out / "burndown.csv").open("w", newline="") as fb:
        wv, wb = csv.writer(fv), csv.writer(fb)
        wv.writerow(["sprint", "sprint_order", "start", "end", "committed_points", "completed_points", "items_done", "bugs_done"])
        wb.writerow(["sprint", "date", "day", "remaining_points", "ideal_points"])
        for order, s in enumerate(sprints, 1):
            ins = [i for i in issues if s["sprint"] in i["sprints"]]
            done = [i for i in ins if i["resolved"] and s["start"] <= i["resolved"] <= s["end"]]
            committed = sum(i["points"] for i in ins)
            wv.writerow([s["sprint"], order, s["start"], s["end"], committed, sum(i["points"] for i in done),
                         len(done), sum(1 for i in done if i["type"] == "Bug")])
            n = (s["end"] - s["start"]).days
            for d in range(n + 1):
                day = s["start"] + dt.timedelta(days=d)
                remaining = sum(i["points"] for i in ins if not (i["resolved"] and s["start"] <= i["resolved"] <= day))
                wb.writerow([s["sprint"], day, d, remaining, round(committed * (1 - d / n), 2) if n else 0])
    print(f"{len(issues)} issues, {len(sprints)} sprints -> {a.out}")


if __name__ == "__main__":
    main()
