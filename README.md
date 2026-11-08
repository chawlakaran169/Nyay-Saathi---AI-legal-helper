# Nyay Saathi: AI legal helper for everyday problems in India (Kuku Problem 2)

Talks to an ordinary person (text, English/Hindi voice, and optional LLM translation for supported regional-language scripts), builds their case, explains where they stand,
drafts a legal notice, lists the proof they still need, lets them practise the argument and download their case file.
Also explains a legal notice they **received** and drafts a reply. Covers **three** problems in depth:
security deposit not returned, consumer refund, unpaid salary. Everything else is referred to a real lawyer / free legal aid.

## Run it (Python 3.9+, no installs, no API key, no cost)
```bash
python3 server.py          # open http://localhost:8000  (mic + read-aloud work in Chrome/Edge)
python3 cli.py             # or chat in the terminal
python3 tests/run_tests.py # 26 scripted cases + 45 extra checks + guard attacks + classifier eval + EN/HI parity + speed -> outputs/ (+ outputs/dashboard.html)
python3 tests/eval_classifier.py # labeled problem-type evaluation (dev + held-out) -> outputs/classifier_eval.json
python3 run_story.py samples/   # NEW INPUT: any story .txt (or folder) -> full report in outputs/reports/
python3 tests/probes.py    # unscripted probes -> outputs/probes.md
```

## Features
- Chat in English/Hindi; optional LLM translation for supported regional-language scripts. Browser voice language choices include English, Hindi, Tamil, Telugu, Bengali, Gujarati, Kannada, Malayalam and Punjabi (recognition depends on browser/device support); asks <=4 questions, then explains where you stand, options, time limit, this week's steps, sources
- **Draft legal notice** (EN/HI) with [BRACKETS] for facts the user did not give
- **Received a notice?** paste it: sender, amount, deadline, threats, urgent flags, draft reply
- **Evidence checklist** (say `checklist`): ticks the proof you have, shows what is missing
- **Practice mode** (say `practise`): the assistant plays the other side and coaches
- **Download / print** summary, notice, checklist, reply (links under the chat)
- **Reminder calendar** (say `reminders`, or the .ics link): send-notice, escalate and time-limit-review dates, all marked approximate
- **Privacy guard**: Aadhaar / PAN / phone / email / card numbers are detected, masked before anything is processed, stored or exported, and the user is warned. Opt-in redacted failure log: `LAWYER_LOG=fails.jsonl`
- **One-shot report** for any story file; **quality dashboard** at `/dashboard`
- **Corrections**: "sorry, the amount is 65000" / "wrong, it's a deposit problem" update the case instead of being ignored
- **Optional LLM fallback** for problem type when rules can't tell (one-word whitelisted output; requires a provider key)

## How it avoids inventing law
1. **Closed knowledge base** (`kb/sources.json`): the only place legal statements live. 16 entries, each with a source, a confidence flag, a verify link and a **verification record** (checked 2026-11-08 against India Code, Gazette notifications and official department sources where available; some practice guidance uses secondary explainers). Not a lawyer's review.
2. **The model never writes legal content.** Deadlines and notices are code and templates. Consumer Commission limits are explained from the value paid as consideration; the app does not infer this from an unpaid refund.
3. **Output guard** (`lawyer/guard.py`): every outgoing message is scanned; any Act, Section, case citation or new number that is not in the knowledge base is blocked and replaced with "check with a lawyer".
4. **Refuses** case-law requests, guarantees, prompt-injection, out-of-scope areas (family, criminal, property, tax, cyber) and emergencies.
5. **Always** shows sources + "see a real lawyer" triggers (big amount, time limit near, little proof).

## Enable Gemini (optional; default app remains offline)
Create a Gemini API key in [Google AI Studio](https://aistudio.google.com/apikey). Keep it private; do not add it to source files, screenshots, or the submission ZIP. On Windows PowerShell, from this project directory, enter:
```powershell
$env:LAWYER_LLM = "gemini"
$env:PORT = "8001"
$secureKey = Read-Host "Gemini API key" -AsSecureString
$keyPtr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureKey)
try {
    $env:GEMINI_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($keyPtr)
    python server.py
} finally {
    Remove-Item Env:GEMINI_API_KEY -ErrorAction SilentlyContinue
    Remove-Item Env:LAWYER_LLM -ErrorAction SilentlyContinue
    Remove-Item Env:PORT -ErrorAction SilentlyContinue
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($keyPtr)
}
```
Stop the app with Ctrl+C. Port 8001 avoids accidentally connecting to an older server already using port 8000. Open http://localhost:8001 and check http://localhost:8001/api/health; the response should include `"build":"localized-exports-v3"` and `"llm":"gemini"`. The key is prompted without echo and is not saved in the project; the app needs it in its process environment while running. The default model is `gemini-3.6-flash`; override with `$env:LAWYER_MODEL` if needed. The key must have access to the Gemini API, and provider quotas, eligibility, and billing depend on the account and Google's current terms.

When enabled, supported non-English scripts may be sent to Google for translation, and grounded answers, notices, summaries, checklists, and calendar event text are rewritten in the language of the latest message. The interface and print/download controls switch to Punjabi or Hindi as appropriate. Redact personal information before sending; the app masks identifiers it recognizes, but no automated detector catches every sensitive detail. English legal content generation remains local. The LLM is not a lawyer and does not decide the legal advice.

## Other optional LLM providers
```bash
export LAWYER_LLM=gemini  GEMINI_API_KEY=...        # or: openai (OPENAI_API_KEY, OPENAI_BASE_URL) / anthropic (ANTHROPIC_API_KEY)
export LAWYER_MODEL=<model name>                      # optional
python3 server.py
```
The LLM does only limited language tasks and topic fallback. Rewritten output must pass the guard (no new law, section, case or number) or the grounded text is used instead. The owner manually confirmed Punjabi translation and a response on their local Gemini setup. The live topic-classifier fallback has not been separately tested; automated tests use fake providers and do not require a key.

## Layout
`kb/` knowledge base · `lawyer/` engine, guard, notice, roleplay, LLM adapter · `web/` chat UI · `tests/` cases + probes · `outputs/` raw results · `doc/` solution doc + video script

## Measured quality (see outputs/dashboard.html)
- 26 scripted conversations and 45 extra checks pass; 7/7 hallucination attacks blocked
- Problem-type detection: first run 83% (2 wrong); 98% after tuning on that set (optimistic). **Frozen set of 30 fresh messages: old rules 73% -> upgraded rules 80%, 0 wrong.** Earlier held-out set: 58% -> 71%, wrong advice 8% -> 4%. Rules still generalise only partly; unplaceable messages get a question, not a guess.
- EN vs Hindi parity: 100% of 72 fields over 8 paired stories (first run 90%). Recent offline runs measured p95 between 1.6 and 2.7 ms per message.
- Knowledge base checked 2026-11-08 against official sources where available (not a lawyer's review): two repealed-law references were found and corrected; e-Jagriti and the official filing/fee rules are now cited.
