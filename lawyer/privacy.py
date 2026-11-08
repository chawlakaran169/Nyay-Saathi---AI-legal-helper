"""Privacy guard: detect and mask personal identifiers. The assistant never needs them to give guidance.
Used to (1) warn the user, (2) keep identifiers out of any saved log, (3) keep them out of exports."""
import re, json, os, datetime

PATTERNS = {
    "Aadhaar number": re.compile(r"(?<!\d)[2-9]\d{3}[\s-]?\d{4}[\s-]?\d{4}(?!\d)"),
    "PAN": re.compile(r"\b[A-Za-z]{5}\d{4}[A-Za-z]\b"),
    "phone number": re.compile(r"(?<!\d)(?:\+?91[\s-]?|0)?[6-9]\d{9}(?!\d)"),
    "email address": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "card / account number": re.compile(r"(?<!\d)(?:\d[\s-]?){13,18}(?!\d)"),
}


def find(text):
    """Kinds of identifiers present (a 12-digit Aadhaar is not also reported as a card number)."""
    found = []
    masked = text
    for kind, rx in PATTERNS.items():
        if rx.search(masked):
            found.append(kind)
            masked = rx.sub(" ", masked)
    return found


def redact(text):
    out = text
    for kind, rx in PATTERNS.items():
        out = rx.sub(lambda m, k=kind: f"[{k.upper()} REMOVED]", out)
    return out


WARN = {
 "en": "🔒 I noticed you shared a {kinds}. **I never need personal IDs, bank or card details to help you**, so please don't share them here. I have not stored it, and I've masked it in anything saved or exported. You will write your own details into the notice yourself.",
 "hi": "🔒 मैंने देखा कि आपने {kinds} साझा किया है। **आपकी मदद के लिए मुझे कभी व्यक्तिगत पहचान, बैंक या कार्ड की जानकारी नहीं चाहिए**, इसलिए कृपया यहाँ साझा न करें। मैंने इसे सहेजा नहीं है, और सहेजी या एक्सपोर्ट की गई किसी भी चीज़ में इसे छिपा दिया है। नोटिस में अपनी जानकारी आप खुद भरेंगे।",
}
KIND_HI = {"Aadhaar number": "आधार नंबर", "PAN": "PAN", "phone number": "फ़ोन नंबर", "email address": "ईमेल पता", "card / account number": "कार्ड / खाता नंबर"}


def warning(kinds, lang):
    if lang == "Punjabi":
        return "🔒 ਤੁਹਾਡਾ ਨਿੱਜੀ ਵੇਰਵਾ ਪਛਾਣਿਆ ਗਿਆ ਹੈ। ਮਦਦ ਲਈ ਸਾਨੂੰ ਤੁਹਾਡਾ ਨਿੱਜੀ ਨੰਬਰ ਨਹੀਂ ਚਾਹੀਦਾ; ਇਸਨੂੰ ਜਵਾਬ ਅਤੇ ਸੁਰੱਖਿਅਤ ਕੀਤੀ ਸਮੱਗਰੀ ਵਿੱਚੋਂ ਹਟਾਇਆ ਗਿਆ ਹੈ।"
    names = ", ".join(KIND_HI.get(k, k) for k in kinds) if lang == "hi" else ", ".join(kinds)
    return WARN["hi" if lang == "hi" else "en"].format(kinds=names)


def log_failure(msg, outcome, lang):
    """Opt-in (LAWYER_LOG=/path/to/file.jsonl). Stores ONLY redacted text of messages the tool could not help with,
    so the team can see which problem types people actually bring. Nothing is logged by default."""
    path = os.environ.get("LAWYER_LOG")
    if not path:
        return
    rec = {"ts": datetime.datetime.now().isoformat(timespec="seconds"), "outcome": outcome, "lang": lang, "text": redact(msg)[:500]}
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
