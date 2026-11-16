# WinCS FAQ Assistant

An AI chat assistant that answers questions about WinCS **only from the society's FAQ**, shows its sources, says "I don't know" instead of guessing, and handles harmful input safely. It was built with Claude Code and run as a 3-sprint Scrum project.

> ⚠️ `knowledge_base/*.md` currently holds **sample** content. Replace it with real, committee-approved WinCS information before any user testing (that's backlog story 2).

## Run it
Requires Python 3.10+.
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...      # or: ant auth login
streamlit run app.py
```
Terminal-only: `python -m assistant.core "How much does membership cost?"`

## Test it
```bash
pytest                         # 20 offline unit tests, no API key needed
python evals/run_evals.py      # the 30-case AI test plan against the live model
```

## What's in the repo
| Path | What |
|---|---|
| `assistant/core.py` | Input screening → BM25 retrieval → grounded Claude answer → status + sources |
| `app.py` | Streamlit chat UI with sources, example questions and 👍/👎 feedback |
| `knowledge_base/` | The FAQ (one `##` heading = one searchable section) |
| `tests/` | Offline unit tests |
| `evals/` | 30 test cases (correct / hallucination / edge / harmful) and the runner |
| `scrum/` | Jira backlog import CSV (4 epics, 25 stories, 67 pts) and the ceremony kit for Miro |
| `docs/confluence/` | 8 Confluence pages ready to paste in |
| `metrics/` | Jira export → velocity / burndown / cycle-time tables, and the Power BI guide with DAX |
| `usability/` | Usability test script, SUS questionnaire and SUS scorer |
| `training/` | One-page user guide and the 3-minute demo script |
| `cv/` | CV entry and interview-story template (fill in with real numbers only) |

---

## Your 6-week runbook

The code is built. What's left needs **you and real people**, because that's what makes it a genuine Scrum project and gives you honest CV numbers.

### Week 0 (setup, ~1 evening)
- [ ] Push this folder to a new public GitHub repo.
- [ ] Create free **Jira** (Scrum template), **Confluence** and **Miro** accounts, then follow the Jira checklist at the bottom of `scrum/ceremonies.md`.
- [ ] Import `scrum/jira_backlog_import.csv` into Jira.
- [ ] Paste `docs/confluence/*.md` into Confluence pages (the editor converts Markdown when you paste it).
- [ ] Ask 2–3 WinCS members to join. Agree a 1-hour slot every second week, plus async stand-ups.
- [ ] Get an API key at console.anthropic.com and set a monthly spending limit.

### Sprint 1 (weeks 1–2): working MVP with real content
- [ ] Sprint planning on Miro. Pick a sprint goal, then pull stories.
- [ ] Collect the real FAQ from the committee and replace `knowledge_base/` (story 2).
- [ ] Move each story through the Jira board **as you actually work on it**, because the metrics come from those dates.
- [ ] Use Claude Code for changes, which is the "AI-assisted coding" part. Keep notes on what you asked it to do; they make good interview material.
- [ ] Sprint review + Start/Stop/Continue retro. Write the sprint report in Confluence.

### Sprint 2 (weeks 3–4): test, harden, baseline usability
- [ ] Update the test cases to match your real FAQ facts (`must_include` columns).
- [ ] `python evals/run_evals.py`. Read every answer, mark `manual_verdict`, and log each real failure as a Jira **Bug**.
- [ ] Usability round 1: 5 users, the tasks and SUS form from `usability/usability_test_kit.md`, then `python usability/sus_score.py`.
- [ ] Review + 4Ls retro.

### Sprint 3 (weeks 5–6): fix, improve, measure again, ship
- [ ] Fix the bugs from sprint 2 and re-run the evals. Record the new pass rate.
- [ ] Fix the top 3 usability issues, then run usability round 2 and compare the SUS scores.
- [ ] Deploy to Streamlit Community Cloud (put the API key in **Secrets**).
- [ ] Export Jira → `python metrics/jira_metrics.py …` → build the Power BI dashboard (`metrics/POWERBI.md`).
- [ ] Record the demo (`training/demo_video_script.md`) and finish the user guide.
- [ ] Review + Sailboat retro. Fill in `cv/cv_entry_TEMPLATE.md` with **real** numbers.

### Quick wins alongside (a few hours each)
- Atlassian University: free Jira and Confluence fundamentals courses and badges
- Scrum.org: free Open Assessment for Scrum (practise for PSM I later)
- Miro Academy: free course on running retrospectives and workshops

## How it works (short version)
1. `screen_input` blocks empty, over-long, prompt-injection, personal-data and self-harm messages *before* any API call. Self-harm messages get a supportive reply with a helpline; set `WINCS_HELPLINE` for your country.
2. `retrieve` ranks FAQ sections with BM25 and passes the top 4 to the model.
3. Claude (`claude-opus-5-5`, effort `low`) is told to answer only from that context, or to reply with a fixed "I don't have that information…" sentence, which makes hallucination tests easy to automate.
4. If a safety classifier declines, the server-side fallback retries on a suitable model, and a final refusal shows a polite block message.
