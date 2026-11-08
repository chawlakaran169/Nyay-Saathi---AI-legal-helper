# Raw outputs (unedited, produced by running the tool)
- `transcripts/*.md`  26 scripted conversations (my test cases): user turns + assistant replies + PASS/FAIL line
- `results.json`      machine-readable results of all cases + the guard attack table
- `probes.md`         unscripted probes used to find failures (including ones that still fail)
Regenerate: `python3 tests/run_tests.py && python3 tests/probes.py`  (offline, no API key; LLM mode off)
- `reports/*.md`      one-shot reports on 5 new sample stories (`python3 run_story.py samples/`)
- `dashboard.html`    quality dashboard (open in a browser)
- `classifier_eval.json`  labeled problem-type evaluation: dev first run, dev after tuning, held-out
- `parity.json`  English vs Hindi parity on 8 paired stories + speed benchmark
