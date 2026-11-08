"""Rule-based language detection, topic classification and fact extraction.
Deterministic on purpose: facts that feed deadlines and forum choice are code, not LLM."""
import re, datetime

DEV = re.compile(r"[ऀ-ॿ]")
LATIN = re.compile(r"[A-Za-z]")
SCRIPTS = {  # non-supported scripts -> language name (needs LLM to translate)
    "Tamil": (0x0B80, 0x0BFF), "Telugu": (0x0C00, 0x0C7F), "Bengali": (0x0980, 0x09FF),
    "Gujarati": (0x0A80, 0x0AFF), "Kannada": (0x0C80, 0x0CFF), "Malayalam": (0x0D00, 0x0D7F),
    "Punjabi": (0x0A00, 0x0A7F),
}
HINGLISH = {"mera", "meri", "mere", "nahi", "nahin", "wapas", "paisa", "paise", "malik", "kiraya", "kiraye",
            "mahine", "saal", "pehle", "kya", "hai", "hain", "nahi", "diya", "diye", "raha", "rahi", "mujhe",
            "aur", "tankhwah", "salary", "bhai", "madad", "kaise", "kab", "kitna", "haan", "ji", "dena"}


def detect_lang(t):
    dev = len(DEV.findall(t)); lat = len(LATIN.findall(t))
    for name, (a, b) in SCRIPTS.items():
        if sum(a <= ord(c) <= b for c in t) >= 3:
            return name
    if dev and dev >= lat:
        return "hi"
    words = set(re.findall(r"[a-z]+", t.lower()))
    if len(words & HINGLISH) >= 2:
        return "hinglish"
    return "en"


LEX = {
    "deposit": {"strong": ["landlord", "tenant", "security deposit", "caution money", "rental", "house owner", "malik", "makan",
                           "kiraya", "kiraye", "kiraydar", "मकान मालिक", "किराया", "किरायेदार", "सिक्योरिटी डिपॉजिट", "डिपॉज़िट", "डिपॉजिट"],
                "weak": ["deposit", "rent", "flat", "pg ", "room", "vacate", "vacated", "advance", "lease", "hostel", "warden", "caution", "फ्लैट", "कमरा"]},
    "refund": {"strong": ["refund", "defective", "seller", "amazon", "flipkart", "myntra", "swiggy", "zomato", "consumer",
                          "रिफंड", "पैसे वापस", "paisa wapas", "paise wapas", "सामान", "ऑर्डर"],
               "weak": ["order", "product", "delivered", "course", "coaching", "fees", "cancel", "booking", "ticket", "airline",
                        "warranty", "refund", "return", "replace", "replacement", "stopped working", "not working", "wapas", "खराब", "कंपनी"]},
    "salary": {"strong": ["salary", "wages", "payslip", "employer", "hr ", "resign", "full and final", "tankhwah", "तनख्वाह",
                          "सैलरी", "वेतन", "तनख़्वाह", "नियोक्ता", "stipend", "स्टाइपेंड"],
               "weak": ["boss", "job", "office", "notice period", "terminated", "fired", "offer letter", "stipend", "नौकरी"]},
}
OUT_OF_SCOPE = ["divorce", "custody", "dowry", "alimony", "maintenance", "will ", "inheritance", "bail", "fir ", "accident",
                "defamation", "ragging", "builder", "rera", "possession of flat", "trademark", "patent", "income tax", "gst", "cyber", "hack", "blackmail", "encroach", "insurance", "harass", "loan recovery", "adoption",
                "तलाक", "दहेज", "वसीयत", "जमानत", "एफआईआर", "मानहानि", "talaq"]
EMERGENCY = ["arrested", "arrest", "police is coming", "threatened", "threatening me", "beat", "hit me", "violence", "suicide",
             "kill", "गिरफ्तार", "मारपीट", "धमकी", "जान से", "मार डाल"]
CASELAW = re.compile(r"case law|case-law|judg(e)?ment|precedent|supreme court|high court|landmark|which case|कौन सा केस|फैसल|मिसाल", re.I)
INJECTION = re.compile(r"ignore (all |your |the )?(previous|above|prior) |system prompt|you are now|pretend (to be|you are)|jailbreak|forget your rules", re.I)
GUARANTEE = re.compile(r"will i win|guarantee|sure ?shot|100 ?%|pakka jeet|जीत जाऊँगा|जीतूंगा|जीत पक्की", re.I)
DRAFT = re.compile(r"\b(draft|notice|letter)\b|नोटिस|ड्राफ्ट|पत्र", re.I)
PRACTISE = re.compile(r"practi[sc]e|role ?-?play|argue|play the|mock|rehears|अभ्यास|प्रैक्टिस", re.I)
STOP = re.compile(r"^\s*(stop|exit|end|quit|done|बंद|रुको)\b", re.I)
RESTART = re.compile(r"\b(restart|new (case|problem)|start over)\b|नई समस्या", re.I)
GREETING = re.compile(r"^\s*(hi|hello|hey|namaste|namaskar|help|नमस्ते|हेलो|हैलो|मदद)\W*$", re.I)


PHRASES = {  # (regex, weight): phrase patterns capture who-does-what, which single keywords cannot
 "deposit": [
  (r"(owner|landlord|malik|मकान मालिक|मालिक).{0,80}(return|refund|wapas|vapas|वापस|लौट|lauta|give (it )?back|sitting on|keep|withh?eld)", 3),
  (r"(security|caution|advance|deposit).{0,40}(return|refund|back|wapas|वापस|forfeit|lauta|लौट)", 3),
  (r"(moved out|vacat|left (the|my) (flat|room|house|pg|rented)|khali|खाली|tenancy ended|lease ended|chhod)", 2),
 ],
 "refund": [
  (r"(seller|store|shop|website|site|app|platform|company|organi[sz]er|centre|center|airline|agency|dukan|dukandar|दुकान|कंपनी).{0,80}(refund|return|replace|money back|paisa wapas|paise|पैसे वापस|रिफंड)", 3),
  (r"(cancel+ed|cancelled).{0,60}(refund|money|order|booking|ticket|flight)", 2),
  (r"(defective|broken|damaged|not working|stopped working|fake|nakli|kharab|खराब|नकली|cracked)", 2),
 ],
 "salary": [
  (r"(salary|wages?|\bpay\b|dues|stipend|earnings|payment|invoice|bonus).{0,60}(not (been )?(paid|received|credited|released)|unpaid|pending|stuck|withh?eld|delay|nahi|नहीं|रोक|cut|deduct)", 3),
  (r"(not (been )?paid|haven'?t paid|hasn'?t paid|won'?t pay|not paying).{0,40}(salary|wages?|pay|dues|invoice|stipend|earnings)|(सैलरी|तनख्वाह|तनख़्वाह|वेतन).{0,40}(नहीं|रोक)", 3),
  (r"(full and final|\bfnf\b|notice period|last working day|resign|\bquit\b|terminat|last salary)", 2),
 ],
}
PHRASES = {k: [(re.compile(rx, re.I), w) for rx, w in v] for k, v in PHRASES.items()}
MARGIN = 2  # if the runner-up is within this many points of the leader, ask instead of guessing


_WORD = {}


def has_word(tl, w):
    """Keyword match that cannot fire inside another word ('lease' must not match 'please'), while stems still match
    to the right ('refund' matches 'refunded'). Non-Latin keywords use plain substring match."""
    if not w.isascii():
        return w in tl
    rx = _WORD.get(w)
    if rx is None:
        rx = _WORD[w] = re.compile(r"(?<![a-z])" + re.escape(w))
    return bool(rx.search(tl))


def classify(text):
    tl = " " + text.lower() + " "
    scores = {}
    for t, lex in LEX.items():
        s = 2 * sum(has_word(tl, w) for w in lex["strong"]) + sum(has_word(tl, w) for w in lex["weak"])
        s += sum(w for rx, w in PHRASES[t] if rx.search(text))
        scores[t] = s
    ranked = sorted(scores.values(), reverse=True)
    best, second = ranked[0], ranked[1]
    if best == 0:
        return None, scores
    top = [t for t, s in scores.items() if s == best][0]
    if second > 0 and (best == second or (second >= MARGIN and best - second < MARGIN)):
        return "ambiguous", scores  # a tie, or two real contenders: ask instead of guessing
    return top, scores


def is_out_of_scope(text):
    tl = " " + text.lower() + " "
    return any(has_word(tl, w) for w in OUT_OF_SCOPE)


def is_emergency(text):
    tl = " " + text.lower() + " "
    return any(has_word(tl, w) for w in EMERGENCY)


# ---------- facts ----------
MULT = {"lakh": 100000, "lac": 100000, "lakhs": 100000, "लाख": 100000, "crore": 10000000, "करोड़": 10000000, "cr": 10000000,
        "k": 1000, "thousand": 1000, "हज़ार": 1000, "हजार": 1000, "hazar": 1000}
AMT_RE = re.compile(r"(?:₹|rs\.?|inr|rupees?)\s*(\d[\d,]*(?:\.\d+)?)\s*(lakhs?|lac|crore|cr|k|thousand|हज़ार|हजार|लाख|करोड़|hazar)?"
                    r"|(\d[\d,]*(?:\.\d+)?)\s*(lakhs?|lac|crore|cr|k|thousand|हज़ार|हजार|लाख|करोड़|hazar)\b"
                    r"|(\d[\d,]*)\s*(?:rupees?|rs\b|रुपये|रुपए|रु)", re.I)


def parse_amount(text, bare_ok=False):
    m = AMT_RE.search(text)
    if m:
        num = m.group(1) or m.group(3) or m.group(5)
        unit = (m.group(2) or m.group(4) or "").lower()
        try:
            v = float(num.replace(",", ""))
        except ValueError:
            return None
        return int(v * MULT.get(unit, 1))
    if bare_ok:
        m = re.search(r"\b(\d[\d,]{2,})\b", text)
        if m:
            v = int(m.group(1).replace(",", ""))
            if not 1990 <= v <= 2100:
                return v
    return None


def parse_amounts(text):
    """All distinct rupee amounts mentioned, in order."""
    out = []
    for m in AMT_RE.finditer(text):
        num = m.group(1) or m.group(3) or m.group(5)
        unit = (m.group(2) or m.group(4) or "").lower()
        try:
            v = int(float(num.replace(",", "")) * MULT.get(unit, 1))
        except ValueError:
            continue
        if v not in out:
            out.append(v)
    return out


MONTHS = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
WORDNUM = {"a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
           "nine": 9, "ten": 10, "दो": 2, "तीन": 3, "चार": 4, "पाँच": 5, "पांच": 5, "छह": 6, "सात": 7, "आठ": 8, "नौ": 9, "दस": 10, "एक": 1, "eleven": 11, "twelve": 12, "ek": 1, "do": 2, "teen": 3, "char": 4, "paanch": 5, "chhe": 6}
REL_RE = re.compile(r"(?<![A-Za-z])(\d+|a|an|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|ek|do|teen|char|paanch|chhe|दो|तीन|चार|पाँच|पांच|छह|सात|आठ|नौ|दस|एक)\s*"
                    r"(year|yr|saal|sal|साल|वर्ष|month|mahine|mahina|महीने|महीना|माह|week|hafte|हफ्ते)s?(?![A-Za-z])", re.I)
HI_MONTHS = {"जनवरी": 1, "फरवरी": 2, "फ़रवरी": 2, "मार्च": 3, "अप्रैल": 4, "मई": 5, "जून": 6, "जुलाई": 7, "अगस्त": 8,
             "सितंबर": 9, "सितम्बर": 9, "अक्टूबर": 10, "अक्तूबर": 10, "नवंबर": 11, "नवम्बर": 11, "दिसंबर": 12, "दिसम्बर": 12}
MY_HI = re.compile("(" + "|".join(HI_MONTHS) + r")\s*,?\s*(20\d\d)")
MY_RE = re.compile(r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?,?\s*(?:of\s+)?(20\d\d)\b", re.I)


CUE = re.compile(r"vacat|started|began|left|moved out|handed|since|ago|has been|have been|not (been )?paid|unpaid|pending|waiting|stopped|refus|खाली|से नहीं|पहले|बकाया|नहीं दी|नहीं दिया|तब से|pehle|khali", re.I)
SKIP_AFTER = re.compile(r"^\W*(notice|rent|deposit|period|lease|tenure)", re.I)


def parse_whens(text, today=None):
    """All date-like candidates as [(elapsed_months, score, position)]. Score 2 if a cue word sits next to it."""
    today = today or datetime.date.today()
    tl = text.lower()
    out = []

    def add(months, m):
        w = tl[max(0, m.start() - 40): m.end() + 6]
        out.append((months, 2 if CUE.search(w) else 1, m.start()))

    for m in MY_RE.finditer(tl):
        d = datetime.date(int(m.group(2)), MONTHS[m.group(1)[:3]], 1)
        add(max(0, (today.year - d.year) * 12 + today.month - d.month), m)
    for m in MY_HI.finditer(text):
        d = datetime.date(int(m.group(2)), HI_MONTHS[m.group(1)], 1)
        out.append((max(0, (today.year - d.year) * 12 + today.month - d.month), 2 if CUE.search(text[max(0, m.start() - 40): m.end() + 12]) else 1, m.start()))
    for m in REL_RE.finditer(tl):
        if SKIP_AFTER.match(tl[m.end(): m.end() + 14]):
            continue  # "one month notice", "two months rent" are not elapsed time
        n = int(m.group(1)) if m.group(1).isdigit() else WORDNUM.get(m.group(1), 1)
        unit = m.group(2)
        if unit.startswith(("year", "yr", "saal", "sal", "साल", "वर्ष")): mo = n * 12
        elif unit.startswith(("week", "hafte", "हफ्ते")): mo = max(1, n // 4)
        else: mo = n
        add(mo, m)
    if not out:
        for m in re.finditer(r"\b(?:in|since|year)\s+(20[12]\d)\b|\b(20[12]\d)\b", tl):
            y = int(m.group(1) or m.group(2))
            add(max(0, (today.year - y) * 12 + 6), m)  # mid-year assumption
    return out


def parse_when(text, today=None):
    """Elapsed months, preferring dates next to cue words ('vacated', 'since', 'ago'); latest mention wins ties."""
    c = parse_whens(text, today)
    if not c:
        return None
    best = max(c, key=lambda x: (x[1], x[2]))
    return best[0]


def when_conflict(text, today=None):
    """Distinct cue-marked dates that disagree by more than 2 months (user should confirm)."""
    c = [m for m, sc, _ in parse_whens(text, today) if sc == 2]
    return sorted(set(c)) if c and max(c) - min(c) > 2 else []


PROOF = {
    "agreement": ["agreement", "contract", "lease", "एग्रीमेंट", "अनुबंध", "offer letter", "appointment letter", "ऑफर लेटर", "ऑफ़र लेटर", "नियुक्ति पत्र"],
    "receipt/invoice": ["receipt", "invoice", "bill", "order confirmation", "रसीद", "बिल", "इनवॉइस", "इनवाइस", "ऑर्डर कन्फ़र्मेशन"],
    "bank/UPI record": ["bank", "upi", "gpay", "phonepe", "paytm", "transfer", "cheque", "statement", "बैंक", "यूपीआई"],
    "chats/emails": ["whatsapp", "chat", "message", "sms", "email", "mail", "screenshot", "व्हाट्सएप", "मैसेज", "ईमेल", "स्क्रीनशॉट"],
    "photos/videos": ["photo", "video", "picture", "फोटो", "वीडियो"],
    "payslips": ["payslip", "pay slip", "salary slip", "पेस्लिप", "सैलरी स्लिप"],
}
NONE_RE = re.compile(r"\b(none|nothing|no proof|no documents?|koi nahi|kuch nahi|nahi hai)\b|कोई नहीं|कुछ नहीं|नहीं है", re.I)
YES_RE = re.compile(r"\b(yes|yeah|yep|haan|han|ha|did|asked|sent|messaged|told)\b|हाँ|हां|जी", re.I)
NO_RE = re.compile(r"\b(no|not yet|nahi|nahin|never|nope)\b|नहीं|नही", re.I)


def parse_proof(text):
    tl = text.lower()
    found = [k for k, ws in PROOF.items() if any(w in tl for w in ws)]
    return found, bool(NONE_RE.search(text)) and not found


def parse_yesno(text):
    y, n = bool(YES_RE.search(text)), bool(NO_RE.search(text))
    if y and not n:
        return True
    if n and not y:
        return False
    return None


def inr(n):
    s = str(int(n))
    if len(s) <= 3:
        return "₹" + s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:]); head = head[:-2]
    if head:
        parts.insert(0, head)
    return "₹" + ",".join(parts + [tail])
