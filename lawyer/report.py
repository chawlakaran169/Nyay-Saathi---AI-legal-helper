"""One-shot mode: read a whole story (text) and produce a full case report with no back-and-forth.
Facts the text doesn't contain stay unknown / in [BRACKETS]; the report lists what is missing."""
import re
from . import extract as X, received, notice, guard
from .engine import Session
from .text import t, S, TOPIC_NAME

DEMANDED = re.compile(r"\b(asked|requested|messaged|emailed|e-mailed|reminded|wrote to|sent (a |an )?(message|mail|email|whatsapp)|called|demanded)\b|मैसेज|ईमेल किया|माँगा|मांगा|कहा था", re.I)


def build_report(text, name="story"):
    s = Session(); s.llm = None
    d = X.detect_lang(text)
    s.lang = "hi" if d == "hi" else "en"
    L = s.lang
    head = [f"# Case report: {name}", f"_Input language detected: {d}. Generated offline; no AI model used._", ""]
    if X.is_emergency(text):
        return "\n".join(head) + t("emergency", L), s
    if received.TRIGGER.search(text):
        return "\n".join(head) + s._received(text), s
    topic, scores = X.classify(text)
    best = max(scores.values()) if scores else 0
    if X.is_out_of_scope(text) and (topic in (None, "ambiguous") or best <= 1):
        return "\n".join(head) + t("out_of_scope", L), s
    if topic in (None, "ambiguous"):
        return "\n".join(head) + "Could not tell which problem this is (deposit / refund / salary). " + t("ask_topic", L), s
    s.topic = topic
    f = s.facts
    amts = X.parse_amounts(text)
    if len(amts) == 1:
        f["amount"] = amts[0]
    f["elapsed"] = X.parse_when(text)
    found, none = X.parse_proof(text)
    f["proof"] = found
    f["noproof"] = none
    f["demanded"] = True if DEMANDED.search(text) else None
    if X.GUARANTEE.search(text):
        s.wants_guarantee = True
    if re.search(r"fraud|cheat|cheque|police|fir\b|धोखा|चेक|पुलिस", text, re.I):
        s.crim = True
    missing = []
    if f["amount"] is None:
        missing.append("amount owed (several amounts were found: " + ", ".join(X.inr(a) for a in amts) + ")" if len(amts) > 1 else "amount owed")
    conflict = X.when_conflict(text)
    if f["elapsed"] is None: missing.append("when it happened / how long ago")
    elif conflict: missing.append("dates in the text disagree (about " + ", ".join(str(m) for m in conflict) + " months ago); I used the most recent: please confirm")
    if not f["proof"] and not f["noproof"]: missing.append("what proof you have")
    if f["demanded"] is None: missing.append("whether you already asked in writing")
    s.mode = "advice"
    body = [f"## {t('story_missing', L)}", ("\n".join("- " + m for m in missing) if missing else "- (nothing important missing)"), "",
            s._advice(), "", s._checklist(), "", "### " + ("Draft legal notice" if L != "hi" else "कानूनी नोटिस का ड्राफ्ट"), notice.build(topic, L, f)]
    return "\n".join(head) + "\n\n".join(body), s
