# Architecture

```
User (browser)
   │  question
   ▼
Streamlit chat UI (app.py)
   │
   ▼
assistant/core.py
   1. screen_input()  ── blocks empty, too long, prompt injection, harmful, self-harm (no API call)
   2. retrieve()      ── BM25 keyword search over knowledge_base/*.md, top 4 sections
   3. Claude API      ── system prompt: "answer only from <context>, else say I don't know"
   4. classify        ── answered / no_info / blocked / error  (+ sources)
   │
   ▼
Answer + sources shown; 👍/👎 saved to logs/feedback.csv
```

## Key design decisions
See the Decision log page. In short:
- **Retrieval with BM25, not embeddings.** The FAQ is small, BM25 is easy to explain and test, and it needs no extra service.
- **Grounding through the prompt plus a fixed "no info" sentence.** This makes "don't know" answers easy to detect automatically in tests.
- **Input screening before the model.** Obvious abuse is blocked cheaply and predictably, and the model's own safety is a second layer.
- **Model:** Claude (`claude-opus-5-5`, effort `low`), configurable with the `WINCS_MODEL` / `WINCS_EFFORT` environment variables.

## How to run
See the README in the repository.
