# Risk register

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Public website info changes or is incomplete (e.g. no cost or mentoring info) | Medium | Medium | Re-check sources each sprint; the bot must answer "I don't have that information" for gaps | PO |
| Seen as an official WinCS tool | Low | Medium | "Unofficial" disclaimer in the app, README and demo | PO |
| Volunteers miss meetings | High | Medium | Async stand-ups; short, fixed meeting slots; record decisions in Confluence | SM |
| Bot gives wrong or unsafe information | Medium | High | Grounding prompt, 30-case test plan, harmful-input screening, sources shown | Dev |
| API costs | Low | Low | Effort `low`, short answers, spending limit set in the Anthropic Console | Dev |
| Fewer than 5 testers for SUS | Medium | Medium | Recruit 7 to allow for no-shows; use friends on other courses | PO |
