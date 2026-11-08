"""Anti-hallucination guard.

Every outgoing message is checked. Anything that names an Act, a Section, a case
or a court-report citation that is NOT in the closed knowledge base is a violation.
This is deliberately coarse: a false alarm costs a fallback message, a miss costs trust.
"""
import re
from . import kb

ACT_RE = re.compile(
    r"((?:[A-Z][A-Za-z()&'\-]*,?\s+(?:of\s+)?){0,12}?(?:Act|Code|Sanhita|Adhiniyam|Rules)),?\s+(\d{4})")
SEC_RE = re.compile(r"(?:[Ss]ections?|धारा|Sec\.)\s+(\d+[A-Za-z]?)")
CASE_RE = re.compile(r"\b[A-Z][\w.]+\s+(?:v\.?|vs\.?|versus)\s+[A-Z]|\bAIR\s+\d{4}|\bSCC\b|\(\d{4}\)\s*\d+\s*SCC|\bWrit Petition\b", re.I)
NUM_RE = re.compile(r"\d[\d,]*")

FALLBACK = {
    "en": ("I can't safely state that without risking a wrong or invented legal reference. "
           "Please check this point with a lawyer, or call free legal aid (NALSA) on 15100."),
    "hi": ("मैं इस बात को बिना गलत या गढ़े हुए कानूनी संदर्भ के जोखिम के नहीं बता सकता। "
           "कृपया इसे किसी वकील से जाँच लें, या मुफ़्त कानूनी सहायता (NALSA) 15100 पर कॉल करें।"),
}


def _norm(s):
    s = re.sub(r"^\s*(the|under|of)\s+", "", s.strip(), flags=re.I)
    return re.sub(r"\s+", " ", s).lower()


def violations(text):
    """Return a list of human-readable violations ([] means clean)."""
    acts = kb.allowed_acts()
    secs = kb.allowed_sections()
    bad = []
    stripped = text
    for a in sorted(acts, key=len, reverse=True):  # remove KNOWN laws first; whatever law-like text remains is unknown
        stripped = re.sub(re.escape(a), " <KNOWN> ", stripped, flags=re.I)
    for m in ACT_RE.finditer(stripped):
        full = _norm(f"{m.group(1)}, {m.group(2)}")
        if not any(full.endswith(a) for a in acts):
            bad.append(f"unknown law: {m.group(1)}, {m.group(2)}")
    for m in SEC_RE.finditer(text):
        n = m.group(1).lower()
        window = text[max(0, m.start() - 90): m.end() + 110].lower()
        ok = any(sn == n and act in window for sn, act in secs)
        if not ok:
            bad.append(f"unverified section: {m.group(0)}")
    for m in CASE_RE.finditer(text):
        bad.append(f"case-style citation: {m.group(0)}")
    return bad


def numbers(text):
    return {n.replace(",", "") for n in NUM_RE.findall(text)}


def accept_rewrite(original, rewritten):
    """For LLM rewrites: no new legal references and no new numbers."""
    v = violations(rewritten)
    new_nums = numbers(rewritten) - numbers(original)
    if new_nums:
        v.append("new numbers introduced: " + ",".join(sorted(new_nums)))
    missing_nums = numbers(original) - numbers(rewritten)
    if missing_nums:
        v.append("numbers omitted: " + ",".join(sorted(missing_nums)))
    return v


def enforce(text, lang="en"):
    """Final gate on any outgoing message. Returns (text, violations)."""
    v = violations(text)
    if v:
        return FALLBACK.get(lang, FALLBACK["en"]), v
    return text, []
