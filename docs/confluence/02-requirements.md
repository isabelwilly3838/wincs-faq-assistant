# Requirements and personas

## Personas
**Priya, first-year CS student.** She is curious about WinCS at TUM but shy about messaging the team. She wants quick answers on her phone.
**Sam, second-year non-CS student.** Sam isn't sure they're "allowed" to join. Sam needs reassurance and clear facts.
**Prospective company partner.** Wants to quickly find how to sponsor an event or post roles to the Talent Pool.

## User stories
All stories and acceptance criteria live in Jira (epic → story). Embed the Jira backlog here with the Jira macro: `/jira` → filter `labels = wincs-faq`.

## Non-functional requirements
- Answers come only from the FAQ, and a source is shown for every answer.
- Response time under 10 seconds for a typical question.
- No personal data is stored. The feedback log keeps only the question, the answer and the rating.
- Works on a mobile browser.
- The API key is never committed to the repo.
