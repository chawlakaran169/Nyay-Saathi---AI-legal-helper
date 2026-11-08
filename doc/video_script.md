# 3-minute walkthrough: script + shot list (record in your own voice)

Tip: run `python3 server.py`, open http://localhost:8000, start screen recording (QuickTime: File > New Screen Recording).
Speak in your own words; this is only a guide. Keep it under 3:00.

| Time | Show on screen | Say (gist) |
|---|---|---|
| 0:00-0:20 | Title / the chat page | "I picked Problem 2. People skip legal help for small money problems. I built Nyay Saathi for three: deposit, refund, unpaid salary. Everything else it refers to a real lawyer." |
| 0:20-1:10 | Click the **deposit chip**. Answer its questions (proof: "agreement and bank transfer", written: "no") | "It asks only what matters: when, how much, proof, did you ask in writing. Then: where you stand, options in order, time limit, what to do this week, sources with links." Point at the **Sources** list and "See a real lawyer". |
| 1:10-1:40 | Type **draft notice** | "A ready-to-edit notice. It only fills facts I gave; the rest stay in [BRACKETS]. It never invents facts." |
| 1:40-2:10 | Click the **Hindi chip** (or press the mic and speak Hindi). Show the Hindi answer. | "Same flow in Hindi, text or voice." |
| 2:10-2:25 | Click the **Received a notice** chip | "If you *received* a notice: it reads who sent it, the amount, the deadline, flags court/police/cheque as urgent, and drafts a reply." Also type **checklist** (ticks the proof you have). |
| 2:25-2:35 | Type **reminders** (dates + .ics link); paste a fake phone number once to show the privacy mask; then type **practise**, answer one objection, show the coach tip | "It plays the landlord and coaches me after each reply." |
| 2:35-2:55 | Open http://localhost:8000/dashboard (or run `python3 run_story.py samples/`) | "How I avoid invented law: a closed knowledge base, and a guard that blocks any Act, section, case or number that isn't in it. I attacked it with a fake hallucinating model; all blocked. And `run_story.py` runs it on any new story." |
| 2:55-3:00 | Dashboard: classifier table (98% tuned vs 58% held-out) and the knowledge-base verification table | "Where it fails: on new phrasing the classifier drops from 98% to 58%, and I found two outdated laws in my own first draft. All in my doc." |

Before recording, try the mic once (Chrome/Edge only). If it fails, skip the voice part and say so; it's honest.
