# Raw outputs
- `transcripts/*.md` — 26 scripted conversations, with user turns, assistant replies, and pass/fail results
- `results.json` — machine-readable case results, 49 extra checks, and hallucination-guard attacks
- `probes.md` — exploratory probes, including cases that still need improvement
- `reports/*.md` — one-shot reports for five sample stories
- `dashboard.html` — quality dashboard
- `classifier_eval.json` — labeled problem-type evaluation (development and held-out sets)
- `parity.json` — English/Hindi parity on paired stories and speed benchmark

Regenerate on Windows from the project folder with `python tests\run_tests.py` and `python tests\probes.py` (offline; no API key required).
