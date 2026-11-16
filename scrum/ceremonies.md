# Scrum ceremonies kit (Miro + Jira)

Team: you (Product Owner + Scrum Master + Developer) and 2–3 WinCS members (stakeholders / testers / co-developers).
Be honest about the roles on your CV: "acted as Scrum Master and Product Owner for a 3–4 person team".

Sprint length: 2 weeks. Three sprints. Suggested goals:

| Sprint | Goal | Suggested stories (label in Jira) |
|---|---|---|
| 1 | "A member can ask a question and get a sourced answer from the real FAQ." | `suggested-sprint-1` (~23 pts) |
| 2 | "The assistant is tested, safe, and we have a baseline SUS score." | `suggested-sprint-2` (~20 pts) |
| 3 | "Usability is improved and measured again; bugs fixed; demo ready." | `suggested-sprint-3` + bugs from sprint 2 |

The labels are only suggestions. Decide what goes in each sprint during sprint planning, with the team.

---

## Miro board layout (one board, one frame per ceremony)

Create a free Miro board called **WinCS FAQ Assistant – Scrum**. Add these frames left to right:

1. **Team & working agreement**: names, roles, meeting times, Definition of Done (copy from `docs/confluence/04-definition-of-done.md`).
2. **Sprint 1 Planning**, **Sprint 1 Review**, **Sprint 1 Retro**, and the same for sprints 2 and 3.
3. **Parking lot**: ideas that are not for now.

Take a screenshot of each frame after the meeting and add it to the sprint report page in Confluence.

---

## Sprint planning (60 min, day 1 of each sprint)

Before: groom the backlog in Jira (top items have acceptance criteria and estimates).

| Time | Activity | Miro |
|---|---|---|
| 5 min | Review last sprint's velocity (sprint 1: guess capacity from hours available) | Sticky: "Capacity: __ hrs / __ pts" |
| 10 min | Product Owner proposes the sprint goal | Big sticky at top of frame |
| 25 min | Walk the top backlog items; estimate any unestimated ones with Planning Poker (1, 2, 3, 5, 8) | One sticky per story; dot-vote the points |
| 15 min | Pull stories until capacity is reached; split anything that is 8+ | Two columns: "In sprint" / "Not this time" |
| 5 min | Confirm goal, start the sprint in Jira | ✅ |

Planning Poker in Miro: each person writes their estimate on a hidden sticky, everyone reveals at once, and the highest and lowest explain their reasons before a re-vote.

## Daily stand-up (async, 5 min)

With a volunteer team, use a WhatsApp or Discord thread instead of a meeting. Each person posts three things every day (or every two days):
**Done since last time · Doing next · Blockers**. Update the Jira board straight afterwards, because the metrics depend on it.

## Sprint review (30–45 min, last day of the sprint)

| Time | Activity |
|---|---|
| 5 min | Sprint goal: met or not? Points committed vs completed |
| 20 min | Live demo of each completed story against its acceptance criteria |
| 10 min | Stakeholder feedback → new stickies → new Jira stories or bugs |
| 5 min | Show updated metrics (velocity and burndown from Power BI) |

Only stories that meet the Definition of Done count as completed. Unfinished work goes back to the backlog and does not count as partly done.

## Retrospective (45 min, straight after the review)

Use a different format each sprint so that it stays fresh:

- **Sprint 1: Start / Stop / Continue.** Three columns.
- **Sprint 2: 4Ls.** Liked, Learned, Lacked, Longed for.
- **Sprint 3: Sailboat.** Wind (what helped), Anchors (what slowed us), Rocks (risks), Island (goal).

| Time | Activity |
|---|---|
| 5 min | Check-in: one word for how the sprint felt |
| 10 min | Silent writing: everyone adds stickies |
| 10 min | Group similar stickies; dot-vote (3 dots each) |
| 15 min | Discuss the top 2–3; agree **max 2 action items**, each with an owner |
| 5 min | Review last retro's actions: done or not? |

Put each action item in Jira as a task (label `retro-action`) so that it is visible next sprint.

## Bug workflow

1. Running `python evals/run_evals.py` or user testing finds a failure.
2. Create a Jira **Bug**: summary = what's wrong, description = test case ID, input, actual output, expected output, severity.
3. Bugs found in sprint N are triaged in sprint N+1 planning. Fix them, then re-run that test case (`--only TC13`) and paste the result in the bug before closing it.
4. Count them for the CV: bugs found, bugs fixed, and test pass rate before and after.

## Jira setup checklist

- [ ] Create a free Jira Software site → **Scrum** project template (company-managed if you can, because it makes importing easier).
- [ ] Settings → Issues → make sure **Story Points** is on the Story screen.
- [ ] Import `scrum/jira_backlog_import.csv` (System → External system import → CSV). Map: Issue Id → *Issue Id*, Parent Id → *Parent*, Story Points → *Story Points* (team-managed: *Story point estimate*), Labels → *Labels*.
- [ ] Board columns: **To Do → In Progress → In Review → Done**.
- [ ] Automation rule, needed for cycle time: *When issue transitioned to In Progress → Edit issue field "Start date" = `{{now}}`* (only if Start date is empty).
- [ ] Create Sprint 1 in the backlog view and drag in the stories you agree on in planning.
