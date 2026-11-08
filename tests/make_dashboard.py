"""Builds outputs/dashboard.html from outputs/results.json (self-contained page)."""
import json, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "outputs")

KNOWN_FAILURES = [
 ("Keyword rules generalise only partly (measured)", "98% on the set they were tuned on, 71-80% on fresh sets, with 0-4% wrong advice. Messages it cannot place get a clarifying question, not a guess; many out-of-scope topics are 'asked' rather than clearly 'referred'."),
 ("Over-caution on threats", "'threatened' triggers the emergency screen and drops an in-scope deposit problem."),
 ("Over-refusal on one word", "'harassment' makes it refuse the whole message, including an in-scope salary claim."),
 ("Hinglish answered in English", "Understood, but the reply language is English. Other Indian languages need an LLM."),
 ("Date and amount reading is heuristic", "Picks dates next to cue words and asks when several amounts appear, but odd phrasing can still mislead it. Everything is shown back to the user, who can correct it in one message."),
 ("Not verified by a lawyer", "Selected legal claims were checked against India Code, Gazette notifications and official Department of Consumer Affairs / Labour sources; the knowledge base has not been reviewed by a lawyer. Consumer Commission depends on consideration paid, and state/transition rules may apply. Live-LLM path and browser mic are untested."),
]


def build():
    r = json.load(open(os.path.join(OUT, "results.json"), encoding="utf-8"))
    cases, guard, extra = r["cases"], r["guard_attacks"], r.get("extra", [])
    passed = sum(c["pass"] for c in cases)
    blocked = sum(g["blocked"] for g in guard if "HONEST" not in g["attack"])
    attacks = len(guard) - 1
    e_pass = sum(e["pass"] for e in extra)
    ce = json.load(open(os.path.join(OUT, "classifier_eval.json"), encoding="utf-8")) if os.path.exists(os.path.join(OUT, "classifier_eval.json")) else None
    pr = json.load(open(os.path.join(OUT, "parity.json"), encoding="utf-8")) if os.path.exists(os.path.join(OUT, "parity.json")) else None
    kb = json.load(open(os.path.join(HERE, "..", "kb", "sources.json"), encoding="utf-8"))["entries"]
    conf = {}
    for e in kb: conf[e["confidence"]] = conf.get(e["confidence"], 0) + 1
    rows = "".join(f"<tr><td>{html.escape(c['id'])}</td><td>{html.escape(c['title'])}</td><td class='{'ok' if c['pass'] else 'bad'}'>{'PASS' if c['pass'] else 'FAIL'}</td></tr>" for c in cases)
    grows = "".join(f"<tr><td>{html.escape(g['attack'])}</td><td class='{'ok' if (g['blocked'] != ('HONEST' in g['attack'])) else 'bad'}'>{'accepted' if 'HONEST' in g['attack'] and not g['blocked'] else 'BLOCKED' if g['blocked'] else 'MISSED'}</td></tr>" for g in guard)
    erows = "".join(f"<tr><td>{html.escape(e['name'])}</td><td class='{'ok' if e['pass'] else 'bad'}'>{'PASS' if e['pass'] else 'FAIL'}</td><td>{html.escape(e['why'])}</td></tr>" for e in extra)
    frows = "".join(f"<li><b>{html.escape(a)}:</b> {html.escape(b)}</li>" for a, b in KNOWN_FAILURES)
    cls = ""
    if ce:
        def line(name, d, note): return f"<tr><td>{name}</td><td>{d['n']}</td><td>{d['correct']} ({d['strict_accuracy']:.0%})</td><td>{d['safe_abstain']}</td><td class='{'bad' if d['wrong'] else 'ok'}'>{d['wrong']} ({d['wrong_rate']:.0%})</td><td>{note}</td></tr>"
        cls = ("<h2>Problem-type detection: labeled evaluation</h2><table><tr><th>Set</th><th>n</th><th>Correct</th><th>Safe (asked / referred)</th><th>Wrong advice</th><th>Note</th></tr>"
               + line("Dev, first run", ce["dev_first_run"], "before any fix")
               + line("Dev, after tuning", ce["dev_after_tuning"], "optimistic: rules tuned on it")
               + line("Held-out 1", ce["holdout"], "written after the first tuning round, then used to improve the rules (so now also dev)")
               + line("Held-out 2: OLD rules", ce["holdout2_baseline"], "frozen set, measured BEFORE the classifier upgrade")
               + line("Held-out 2: NEW rules", ce["holdout2"], "same frozen set, measured once after the upgrade (phrase patterns, margin rule, word-boundary fix)") + "</table>"
               + "<div class=sub>Wrong advice is the dangerous outcome; asking or referring is safe. Rules are brittle on new phrasing; an optional LLM fallback exists but is untested live.</div>")
    vrows = "".join(f"<tr><td>{html.escape(e['id'])}</td><td>{html.escape(e['source'])}</td><td class='{'bad' if e['verification']['status']=='corrected' else 'ok' if e['verification']['status'].startswith('confirmed') else ''}'>{html.escape(e['verification']['status'])}</td><td>{html.escape(e['verification']['evidence'])}</td></tr>" for e in kb if "verification" in e)
    prows = "".join(f"<tr><td>{html.escape(x['pair'])}</td><td class='{'ok' if x['match']==x['fields'] else 'bad'}'>{x['match']}/{x['fields']}</td></tr>" for x in (pr['rows'] if pr else []))
    page = f"""<!doctype html><html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Nyay Saathi quality dashboard</title><style>
:root{{--bg:#f6f4ef;--card:#fff;--ink:#1d2433;--mut:#667;--ok:#1f7a4d;--bad:#b3261e;--line:#ddd8cc;--acc:#1f5f4a}}
@media(prefers-color-scheme:dark){{:root{{--bg:#14171c;--card:#1c2027;--ink:#e8e6e1;--mut:#9aa;--ok:#58c08f;--bad:#f08a82;--line:#2c323b;--acc:#58b898}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}}main{{max-width:900px;margin:0 auto;padding:16px}}
h1{{font-size:20px;margin:6px 0}}h2{{font-size:16px;margin:22px 0 6px;color:var(--acc)}}.sub{{color:var(--mut);font-size:13px}}
.tiles{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:12px 0}}.t{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 14px}}
.t b{{font-size:24px;display:block}}table{{border-collapse:collapse;width:100%;background:var(--card);font-size:14px}}td,th{{border:1px solid var(--line);padding:5px 8px;text-align:left;vertical-align:top}}
.ok{{color:var(--ok);font-weight:600}}.bad{{color:var(--bad);font-weight:700}}.note{{background:var(--card);border-left:4px solid #d9a23b;padding:8px 12px;border-radius:6px}}li{{margin:4px 0}}
</style></head><body><main>
<h1>Nyay Saathi: quality dashboard</h1><div class=sub>Run at {html.escape(r['run_at'])}. Offline mode, no AI model. Every number below comes from <code>outputs/results.json</code>.</div>
<div class=tiles><div class=t><b>{passed}/{len(cases)}</b>scripted conversations pass</div><div class=t><b>{blocked}/{attacks}</b>hallucination attacks blocked</div>
<div class=t><b>{e_pass}/{len(extra)}</b>extra checks (export, one-shot reports)</div><div class=t><b>{f"{pr['parity']:.0%}" if pr else "-"}</b>EN vs Hindi parity<br><span class=sub>{pr['fields_compared'] if pr else 0} fields over {pr['pairs'] if pr else 0} paired stories</span></div><div class=t><b>{pr['perf']['p95_ms'] if pr else "-"} ms</b>p95 per message<br><span class=sub>offline, ~{pr['perf']['msgs_per_sec_single_core'] if pr else 0} msgs/s per core</span></div><div class=t><b>{len(kb)}</b>knowledge-base entries<br><span class=sub>{', '.join(f'{v} {k}' for k, v in conf.items())} confidence</span></div></div>
<h2>Known failures (honest list)</h2><div class=note><ul>{frows}</ul></div>
{cls}<h2>Knowledge-base verification (web check, 2026-11-08)</h2><div class=sub>Public secondary sources only (news, law-firm and government explainers). Not a lawyer's review, not the Gazette.</div><table><tr><th>ID</th><th>Source</th><th>Status</th><th>Evidence / what changed</th></tr>{vrows}</table>
<h2>Language parity (same story, English vs Hindi)</h2><div class=sub>{html.escape(pr['first_run']['note']) if pr else ''}</div>
<table><tr><th>Story</th><th>Fields matching</th></tr>{prows}</table>
<h2>Hallucination guard attacks</h2><table><tr><th>Attack</th><th>Result</th></tr>{grows}</table>
<h2>Scripted conversations</h2><table><tr><th>ID</th><th>What it tests</th><th>Result</th></tr>{rows}</table>
<h2>Extra checks</h2><table><tr><th>Check</th><th>Result</th><th>Detail</th></tr>{erows}</table>
</main></body></html>"""
    open(os.path.join(OUT, "dashboard.html"), "w", encoding="utf-8").write(page)


if __name__ == "__main__":
    build(); print("wrote outputs/dashboard.html")
