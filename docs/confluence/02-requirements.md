# Requirements and personas

## Personas
**Priya, first-year CS student.** She is curious about WinCS but shy about messaging the committee. She wants quick answers on her phone.
**Sam, second-year non-CS student.** Sam isn't sure they're "allowed" to join. Sam needs reassurance and clear facts.
**Committee member.** Wants fewer repeated questions, and confidence that the bot never gives wrong information.

## User stories
All stories and acceptance criteria live in Jira (epic → story). Embed the Jira backlog here with the Jira macro: `/jira` → filter `labels = wincs-faq`.

## Non-functional requirements
- Answers come only from the FAQ, and a source is shown for every answer.
- Response time under 10 seconds for a typical question.
- No personal data is stored. The feedback log keeps only the question, the answer and the rating.
- Works on a mobile browser.
- The API key is never committed to the repo.
