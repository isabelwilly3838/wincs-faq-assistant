# Definition of Ready and Definition of Done

## Definition of Ready (a story can enter a sprint when…)
- It is written as "As a … I want … so that …"
- It has testable acceptance criteria
- It is estimated in story points (1, 2, 3, 5 or 8; split anything bigger)
- Its dependencies are known

## Definition of Done (a story counts as done when…)
- All acceptance criteria are met and demoed in the sprint review
- The code is pushed to GitHub `main`, and `pytest` passes
- If the change affects answers: `python evals/run_evals.py` has been re-run with no new failures
- Docs are updated (README or Confluence) where relevant
- The Jira issue is moved to **Done**, and has a Start date and a Resolved date
