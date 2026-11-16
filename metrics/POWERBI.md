# Power BI agile-metrics dashboard

## 1. Get the data
1. In Jira: **Filters → Advanced search** → `project = WFA AND labels = wincs-faq ORDER BY created` → **Export → CSV (all fields)**.
2. Create `metrics/sprints.csv` with your real sprint dates:
   ```
   sprint,start,end
   WFA Sprint 1,2026-12-01,2026-12-14
   ```
   The sprint names must match Jira exactly.
3. Run `python metrics/jira_metrics.py path/to/Jira.csv metrics/sprints.csv`. This writes `metrics/out/issues.csv`, `velocity.csv` and `burndown.csv`.

To practise before you have real data: `python metrics/make_sample_export.py`, then run the script on `metrics/sample/SAMPLE_*.csv`. Delete the sample numbers before you show the report to anyone.

## 2. Load into Power BI Desktop
**Get data → Text/CSV** for each of the three files. In Power Query, set the date columns to *Date* and points to *Decimal*.
Relationships: `velocity[sprint]` 1→* `burndown[sprint]`. For cycle time, `issues.csv` stands alone.

## 3. Measures (DAX)
```DAX
Completed Points = SUM ( velocity[completed_points] )
Committed Points = SUM ( velocity[committed_points] )
Say/Do Ratio     = DIVIDE ( [Completed Points], [Committed Points] )
Avg Velocity     = AVERAGEX ( VALUES ( velocity[sprint] ), [Completed Points] )
Avg Cycle Time (days) =
    AVERAGEX ( FILTER ( issues, NOT ISBLANK ( issues[cycle_days] ) ), issues[cycle_days] )
Median Cycle Time (days) =
    MEDIANX ( FILTER ( issues, NOT ISBLANK ( issues[cycle_days] ) ), issues[cycle_days] )
Bugs Fixed = CALCULATE ( COUNTROWS ( issues ), issues[type] = "Bug", NOT ISBLANK ( issues[resolved] ) )
```

## 4. Visuals (one page)
| Visual | Fields |
|---|---|
| **Velocity**: clustered column | Axis `velocity[sprint]` (sort by `sprint_order`); values Committed Points and Completed Points; add an Avg Velocity constant line |
| **Burndown**: line chart | Axis `burndown[day]`; values `remaining_points` (solid) and `ideal_points` (dashed); slicer on `sprint` |
| **Cycle time**: column (histogram) or scatter | `issues[cycle_days]` binned by 1 day; or scatter of resolved date vs cycle days |
| **KPI cards** | Avg Velocity · Say/Do Ratio · Median Cycle Time · Bugs Fixed |

Tip: export the page as a PNG for the Confluence sprint reports and the README.
