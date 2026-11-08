"""Unscripted probes used to hunt for failures. Output is saved unedited to outputs/probes.md."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lawyer.engine import Session

PROBES = [
 ("Mixed amounts (found a bug in v1, now fixed)", "I paid 2 lakh, they returned 50k, now they owe me 1.5 lakh deposit, landlord says wait"),
 ("Threat + deposit: emergency screen fires and the deposit problem is dropped (over-caution, kept on purpose)", "My landlord threatened to throw my stuff out unless I pay extra, and he keeps my deposit of 30000"),
 ("Out-of-scope word 'harassment' makes it refuse the in-scope salary claim too (over-refusal, known failure)", "My boss hasn't paid me since January 2026 but I also want to know if I can sue for harassment"),
 ("PG 'advance' recognised as deposit; bare number without Rs not read as amount", "PG owner is not returning my advance of 12000, I left in June 2026"),
 ("Small consumer claim", "Zomato did not refund Rs 300 for my cancelled order yesterday"),
 ("Tamil input with no LLM connected: must say so honestly", "என் வீட்டு உரிமையாளர் டெபாசிட் தரவில்லை"),
 ("Hinglish: understood, but reply is English (known limitation)", "bhai mera kiraya deposit wapas nahi mil raha, 25000 hai, 4 mahine pehle ghar chhoda"),
]
out = ["# Unscripted probes (raw)\n"]
for title, msg in PROBES:
    s = Session(); s.llm = None
    r = s.say(msg)
    out += [f"## {title}", f"**USER:** {msg}", "", f"_detected: topic={s.topic}, facts={ {k: v for k, v in s.facts.items() if v not in (None, [], False)} }, lang={s.meta['lang']}_", "", "**ASSISTANT (first reply):**", "", r, "", "---", ""]
open(os.path.join(os.path.dirname(__file__), "..", "outputs", "probes.md"), "w", encoding="utf-8").write("\n".join(out))
print("wrote outputs/probes.md")
