# Decision log

| # | Date | Decision | Options considered | Why |
|---|---|---|---|---|
| 1 | | Use Streamlit for the UI | Streamlit, Flask + HTML, Discord bot | Fastest to build, works on mobile, free hosting |
| 2 | | BM25 keyword retrieval | Embeddings + vector DB, sending the whole FAQ | Small FAQ, explainable, no extra service, easy to unit-test |
| 3 | | Fixed "I don't have that information" sentence | Free-form refusals | Makes hallucination tests automatable |
| 4 | | Screen harmful input before the model | Rely only on model safety | Predictable, testable, cheaper; model safety stays as a second layer |
| 5 | | | | |
