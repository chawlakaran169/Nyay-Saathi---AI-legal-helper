"""Understand a legal notice the USER RECEIVED. Rule-based reading + a reply template with brackets."""
import re, datetime
from . import extract as X

TRIGGER = re.compile(
    r"(received|got|have|was (sent|served)|sent me|served (me )?with)\b.{0,40}\bnotice|notice (from|by|against)|"
    r"\b(reply|respond|answer)\b.{0,25}\bnotice|मुझे.{0,25}नोटिस|नोटिस (मिला|आया|भेजा)|नोटिस का जवाब", re.I)
COURT = re.compile(r"summons?|court|hearing|suit|proceedings|सम्मन|समन|अदालत|कोर्ट|सुनवाई|मुकदमा", re.I)
CHEQUE = re.compile(r"cheque|check bounce|dishonou?r|section 138|चेक|बाउंस", re.I)
CRIM = re.compile(r"\bfir\b|police|criminal|cheating|fraud|420|पुलिस|आपराधिक|धोखाधड़ी|एफआईआर", re.I)
BANK = re.compile(r"\bbank\b|\bloan\b|\bemi\b|credit card|sarfaesi|nbfc|बैंक|लोन|ईएमआई", re.I)
SENDER = [("lawyer", re.compile(r"advocate|lawyer|counsel|through my client|under instructions|वकील|एडवोकेट", re.I)),
          ("bank", BANK),
          ("landlord", re.compile(r"landlord|tenan|rent|premises|flat|मकान मालिक|किराया|किरायेदार", re.I)),
          ("employer", re.compile(r"employer|employee|company|salary|notice period|resign|नियोक्ता|कंपनी|सैलरी|तनख्वाह", re.I))]

REPLY = {
"en": """**DRAFT REPLY TO LEGAL NOTICE**

Date: {today}
To: [SENDER / THEIR ADVOCATE, ADDRESS]
From: [YOUR FULL NAME AND ADDRESS]
Reference: Your notice dated [DATE OF NOTICE], received by me on [DATE YOU RECEIVED IT]

Sir/Madam,

1. I acknowledge receipt of your notice dated [DATE OF NOTICE] on [DATE YOU RECEIVED IT] and I have read it.
2. [CHOOSE ONE AND DELETE THE OTHERS: (a) I dispute the claim in full. (b) I dispute part of the claim, namely [PART]. (c) I accept {amount} is due and request time to pay on [PLAN].]
3. Please send me copies of the documents and calculation on which the claim {amount_phrase}is based, such as [AGREEMENT / RECEIPTS / STATEMENT OF ACCOUNT].
4. My version of the facts: [2 TO 4 SHORT, FACTUAL SENTENCES WITH DATES. ATTACH PROOF.]
5. [ONLY IF TRUE: I am willing to discuss and settle this matter.] I request you to take no further step until you have responded to this reply.

Enclosures: [LIST COPIES OF YOUR DOCUMENTS]

Yours faithfully,
[NAME]   [SIGNATURE]   [PHONE / EMAIL]""",
"hi": """**कानूनी नोटिस का जवाब (ड्राफ्ट)**

तारीख: {today}
प्रति: [भेजने वाला / उनके एडवोकेट, पता]
प्रेषक: [आपका पूरा नाम और पता]
संदर्भ: आपका [नोटिस की तारीख] का नोटिस, जो मुझे [मिलने की तारीख] को मिला

महोदय/महोदया,

1. मैं आपके [नोटिस की तारीख] के नोटिस की प्राप्ति [मिलने की तारीख] को स्वीकार करता/करती हूँ और मैंने उसे पढ़ा है।
2. [एक चुनें और बाकी हटाएँ: (क) मैं दावे को पूरी तरह अस्वीकार करता/करती हूँ। (ख) मैं दावे के एक हिस्से, यानी [हिस्सा], को अस्वीकार करता/करती हूँ। (ग) मैं मानता/मानती हूँ कि {amount} देय है और [योजना] पर भुगतान के लिए समय माँगता/माँगती हूँ।]
3. कृपया वे दस्तावेज़ और गणना की प्रतियाँ भेजें जिन पर दावा {amount_phrase}आधारित है, जैसे [एग्रीमेंट / रसीदें / खाता-विवरण]।
4. तथ्यों पर मेरा पक्ष: [2 से 4 छोटे, तथ्यात्मक वाक्य, तारीख़ों सहित। सबूत संलग्न करें।]
5. [केवल यदि सच हो: मैं बातचीत से मामला सुलझाने को तैयार हूँ।] मैं अनुरोध करता/करती हूँ कि इस जवाब का उत्तर देने तक आप कोई आगे की कार्रवाई न करें।

संलग्न: [अपने दस्तावेज़ों की प्रतियाँ सूचीबद्ध करें]

भवदीय,
[नाम]   [हस्ताक्षर]   [फ़ोन / ईमेल]""",
}


def parse(text):
    d = re.search(r"(\d{1,3})\s*(?:\([^)]*\)\s*)?(?:days?|दिन)", text, re.I)
    sender = next((k for k, rx in SENDER if rx.search(text)), "unknown")
    return {
        "amounts": X.parse_amounts(text),
        "days": int(d.group(1)) if d else None,
        "sender": sender,
        "court": bool(COURT.search(text)), "cheque": bool(CHEQUE.search(text)),
        "criminal": bool(CRIM.search(text)), "bank": bool(BANK.search(text)),
    }


def reply_draft(lang, info):
    am = X.inr(info["amounts"][0]) if len(info["amounts"]) == 1 else ("[AMOUNT]" if lang != "hi" else "[राशि]")
    phrase = (f"of {am} " if lang != "hi" else f"{am} की ") if len(info["amounts"]) == 1 else ""
    return REPLY["hi" if lang == "hi" else "en"].format(today=datetime.date.today().strftime("%d %B %Y"), amount=am, amount_phrase=phrase)
