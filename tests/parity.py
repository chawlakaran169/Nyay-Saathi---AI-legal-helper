"""Language parity: the SAME story told in English and in Hindi must give the same case facts, the same legal sources and the same warnings.
Also a speed benchmark. Writes outputs/parity.json."""
import json, os, re, sys, time, statistics
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lawyer.engine import Session

PAIRS = [  # (name, english turns, hindi turns)
 ("deposit, normal", ["My landlord is not returning my security deposit of Rs 50,000. I vacated 3 months ago.", "I have the rental agreement and bank transfer receipt", "yes I messaged him"],
                     ["मेरा मकान मालिक 50000 रुपये की सिक्योरिटी डिपॉजिट वापस नहीं कर रहा। मैंने 3 महीने पहले घर खाली किया।", "मेरे पास रेंट एग्रीमेंट और बैंक ट्रांसफर रसीद है", "हाँ मैंने मैसेज किया था"]),
 ("deposit, time-barred", ["The landlord kept my deposit of Rs 20000. I vacated 4 years ago.", "agreement only", "no"],
                          ["मकान मालिक ने मेरी 20000 रुपये की डिपॉजिट रख ली। मैंने 4 साल पहले घर खाली किया।", "सिर्फ़ एग्रीमेंट है", "नहीं"]),
 ("deposit, large", ["My landlord owes me a deposit of Rs 8 lakh, vacated 6 months ago.", "agreement and bank transfer", "yes I emailed"],
                    ["मकान मालिक पर मेरी 8 लाख रुपये की डिपॉजिट बकाया है, 6 महीने पहले घर खाली किया।", "एग्रीमेंट और बैंक ट्रांसफर है", "हाँ ईमेल किया था"]),
 ("refund, normal", ["The seller refuses to refund Rs 8000 for a defective phone. It happened 1 month ago.", "invoice and email", "yes"],
                    ["विक्रेता खराब फ़ोन के 8000 रुपये का रिफंड नहीं दे रहा। यह 1 महीने पहले हुआ।", "इनवॉइस और ईमेल है", "हाँ"]),
 ("refund, State Commission", ["The company has not given me a refund of Rs 60 lakh, paid 6 months ago.", "invoice and bank transfer", "yes"],
                              ["कंपनी ने मेरा 60 लाख रुपये का रिफंड नहीं दिया, 6 महीने पहले भुगतान किया था।", "इनवॉइस और बैंक ट्रांसफर है", "हाँ"]),
 ("refund, no proof", ["The company is not giving a refund of Rs 3000 for a defective product, 2 months ago.", "nothing", "no"],
                      ["कंपनी खराब सामान के 3000 रुपये का रिफंड नहीं दे रही, 2 महीने पहले की बात है।", "कुछ नहीं", "नहीं"]),
 ("salary, normal", ["My employer has not paid my salary for 3 months, Rs 90000 pending. I have payslips.", "yes I emailed HR"],
                    ["मेरे नियोक्ता ने 3 महीने से तनख्वाह नहीं दी, 90000 रुपये बकाया हैं। मेरे पास पेस्लिप है।", "हाँ मैंने HR को ईमेल किया"]),
 ("salary, large + no written demand", ["My employer owes me salary of Rs 6 lakh since 8 months. I have payslips and bank statement.", "no"],
                                       ["मेरे नियोक्ता पर 6 लाख रुपये की तनख्वाह 8 महीने से बकाया है। मेरे पास पेस्लिप और बैंक स्टेटमेंट है।", "नहीं"]),
]


def run_dialog(turns):
    s = Session(); s.llm = None
    last = ""
    for t in turns:
        last = s.say(t)
    ids = sorted(set(re.findall(r"\[([A-Z]+-\d)\]", last)))
    return {"topic": s.topic, "amount": s.facts["amount"], "elapsed": s.facts["elapsed"], "proof": sorted(s.facts["proof"]),
            "demanded": s.facts["demanded"], "sources": ids,
            "forum": (re.search(r"(District|State|National) Consumer Commission|(जिला|राज्य|राष्ट्रीय) उपभोक्ता आयोग\*\*", last) or [None])[0] and
                     {"District": "district", "जिला": "district", "State": "state", "राज्य": "state", "National": "national", "राष्ट्रीय": "national"}[re.search(r"District|State|National|जिला|राज्य|राष्ट्रीय", re.search(r"(District|State|National) Consumer Commission|(जिला|राज्य|राष्ट्रीय) उपभोक्ता आयोग\*\*", last)[0])[0]],
            "time_warning": "exp" if ("already have passed" in last or "पहले ही बीत चुकी" in last) else "near" if ("close to it" in last or "के करीब" in last) else "ok_or_na",
            "lawyer_big": ("the amount is large" in last) or ("राशि बड़ी है" in last)}


def perf():
    msgs = ["My landlord is not returning my security deposit of Rs 50,000. I vacated 3 months ago.", "मेरे नियोक्ता ने 3 महीने से तनख्वाह नहीं दी, 90000 रुपये बकाया हैं।",
            "agreement and bank transfer", "yes", "draft notice", "checklist", "practise", "I received a legal notice for Rs 80000, pay in 15 days or court"]
    times = []
    for i in range(300):
        s = Session(); s.llm = None
        for m in msgs[:4] if i % 2 == 0 else msgs[1:5]:
            t0 = time.perf_counter(); s.say(m); times.append((time.perf_counter() - t0) * 1000)
    times.sort()
    return {"messages": len(times), "p50_ms": round(statistics.median(times), 2), "p95_ms": round(times[int(len(times) * .95)], 2), "max_ms": round(times[-1], 2),
            "msgs_per_sec_single_core": round(1000 / statistics.mean(times))}


def run():
    rows, total, same = [], 0, 0
    for name, en, hi in PAIRS:
        a, b = run_dialog(en), run_dialog(hi)
        diffs = {k: (a[k], b[k]) for k in a if a[k] != b[k]}
        total += len(a); same += len(a) - len(diffs)
        rows.append({"pair": name, "fields": len(a), "match": len(a) - len(diffs), "differences": diffs})
    res = {"first_run": {"parity": 0.903, "fields_compared": 72, "note": "first run: 5 of the 7 differences were a bug in my forum detector (it matched 'District' in 'District Legal Services Authority'); 2 were real (Hindi 'इनवॉइस' not recognised as an invoice)"}, "pairs": len(PAIRS), "fields_compared": total, "fields_matching": same, "parity": round(same / total, 3), "rows": rows, "perf": perf()}
    json.dump(res, open(os.path.join(os.path.dirname(__file__), "..", "outputs", "parity.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return res


if __name__ == "__main__":
    r = run()
    for x in r["rows"]:
        print(f"{x['pair']:36} {x['match']}/{x['fields']}  {x['differences'] or ''}")
    print(f"\nparity {r['parity']:.0%} over {r['fields_compared']} fields | speed: p50 {r['perf']['p50_ms']} ms, p95 {r['perf']['p95_ms']} ms, ~{r['perf']['msgs_per_sec_single_core']} msgs/s/core")
