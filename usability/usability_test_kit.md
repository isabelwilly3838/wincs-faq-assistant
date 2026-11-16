# Usability test kit (5 users × 2 rounds)

Run round 1 at the end of Sprint 2 and round 2 at the end of Sprint 3. Use **different** people in round 2 if you can; if you reuse people, say so in your write-up.

## Session script (~15 min per person)
1. **Consent (1 min):** "We're testing the tool, not you. Nothing personal is recorded. You can stop at any time."
2. **Tasks (8 min).** Read each one aloud. Don't help. Note time taken, errors and comments.
   | # | Task | Success = |
   |---|---|---|
   | T1 | Find out how much it costs to join WinCS. | Gets "free" |
   | T2 | Find out when and where the weekly meeting is. | Day, time and room |
   | T3 | Find out how to get a mentor. | Knows when and how to apply |
   | T4 | Ask something you think the bot *won't* know. | Understands the "I don't know" reply and the contact |
   | T5 | Check where the answer to T2 came from. | Opens Sources |
3. **SUS questionnaire (3 min):** a Google/Microsoft Form with the 10 items below, each on a 1–5 scale.
4. **Debrief (3 min):** "What was most confusing? What one thing would you change?"

## Observation log (copy into a spreadsheet)
`participant, round, task, success(y/n), seconds, errors, quote`

## SUS questionnaire (standard wording; 1 = strongly disagree … 5 = strongly agree)
1. I think that I would like to use this system frequently.
2. I found the system unnecessarily complex.
3. I thought the system was easy to use.
4. I think that I would need the support of a technical person to be able to use this system.
5. I found the various functions in this system were well integrated.
6. I thought there was too much inconsistency in this system.
7. I would imagine that most people would learn to use this system very quickly.
8. I found the system very cumbersome to use.
9. I felt very confident using the system.
10. I needed to learn a lot of things before I could get going with this system.

Export the responses to CSV with columns `participant,round,q1,…,q10`, and score them with:
```
python usability/sus_score.py usability/sus_responses.csv
```
