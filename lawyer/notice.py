"""Legal-notice drafting. Pure templates: it never invents a fact. Unknown facts become [BRACKETS]."""
import datetime
from .extract import inr
from .text import proof_names

T = {
"deposit": {"en": """**LEGAL NOTICE (DRAFT)**

Date: {today}
From: [YOUR FULL NAME AND ADDRESS]
To: [LANDLORD'S FULL NAME AND ADDRESS]
Sent by: Speed Post and Email

**Subject: Demand for refund of security deposit of {amount}**

Sir/Madam,

1. I was your tenant at [ADDRESS OF THE PREMISES] under a rental arrangement dated [DATE OF AGREEMENT].
2. I paid you a refundable security deposit of {amount} on [DATE] by [MODE OF PAYMENT, e.g. bank transfer / UPI / cash with receipt].
3. I vacated the premises and handed over possession {when_clause}.
4. {demand_clause}You have not returned the deposit and have not given me any itemised reason for withholding it.
5. I therefore call upon you to pay me {amount} within **15 days** of receiving this notice. If you fail to do so, I will be compelled to take appropriate legal proceedings to recover the amount, entirely at your cost and risk.

Enclosures: {enclosures}

Yours faithfully,
[NAME]   [SIGNATURE]   [PHONE / EMAIL]""",
"hi": """**कानूनी नोटिस (ड्राफ्ट)**

तारीख: {today}
प्रेषक: [आपका पूरा नाम और पता]
प्रति: [मकान मालिक का पूरा नाम और पता]
भेजने का माध्यम: स्पीड पोस्ट और ईमेल

**विषय: {amount} की सिक्योरिटी डिपॉजिट की वापसी हेतु माँग**

महोदय/महोदया,

1. मैं [परिसर का पता] में [एग्रीमेंट की तारीख] के किराया-अनुबंध के तहत आपका किरायेदार था/थी।
2. मैंने आपको [तारीख] को [भुगतान का तरीका, जैसे बैंक ट्रांसफ़र / UPI / रसीद सहित नकद] से {amount} की वापसी-योग्य सिक्योरिटी डिपॉजिट दी थी।
3. मैंने परिसर खाली कर कब्ज़ा {when_clause} लौटा दिया।
4. {demand_clause}आपने डिपॉजिट वापस नहीं किया और रोकने का कोई ब्यौरेवार कारण भी नहीं बताया।
5. इसलिए मैं आपसे माँग करता/करती हूँ कि इस नोटिस के मिलने के **15 दिनों** के भीतर मुझे {amount} का भुगतान करें। ऐसा न करने पर मैं राशि की वसूली के लिए उचित कानूनी कार्यवाही करने को बाध्य हूँगा/हूँगी, जिसका पूरा खर्च और जोखिम आप पर होगा।

संलग्न: {enclosures}

भवदीय,
[नाम]   [हस्ताक्षर]   [फ़ोन / ईमेल]"""},
"refund": {"en": """**LEGAL NOTICE (DRAFT)**

Date: {today}
From: [YOUR FULL NAME AND ADDRESS]
To: [COMPANY / SELLER NAME, REGISTERED ADDRESS, GRIEVANCE OFFICER EMAIL]
Sent by: Speed Post and Email

**Subject: Demand for refund of {amount}**

Sir/Madam,

1. On [DATE] I paid {amount} to you for [PRODUCT / SERVICE] (order / invoice no. [NUMBER]) by [MODE OF PAYMENT].
2. [DESCRIBE THE PROBLEM IN ONE OR TWO FACTUAL SENTENCES: e.g. product defective / service not provided / refund promised but not received]. This happened {when_clause}.
3. {demand_clause}I have not received a refund or a satisfactory resolution.
4. I therefore call upon you to refund {amount} within **15 days** of receiving this notice. If you fail to do so, I will file a complaint before the appropriate Consumer Commission under the Consumer Protection Act, 2019 seeking refund, compensation and costs.

Enclosures: {enclosures}

Yours faithfully,
[NAME]   [SIGNATURE]   [PHONE / EMAIL]""",
"hi": """**कानूनी नोटिस (ड्राफ्ट)**

तारीख: {today}
प्रेषक: [आपका पूरा नाम और पता]
प्रति: [कंपनी / विक्रेता का नाम, पंजीकृत पता, शिकायत अधिकारी का ईमेल]
भेजने का माध्यम: स्पीड पोस्ट और ईमेल

**विषय: {amount} की वापसी (रिफंड) हेतु माँग**

महोदय/महोदया,

1. [तारीख] को मैंने [सामान / सेवा] (ऑर्डर / इनवॉइस नं. [नंबर]) के लिए [भुगतान का तरीका] से आपको {amount} का भुगतान किया।
2. [समस्या को एक-दो तथ्यात्मक वाक्यों में लिखें: जैसे सामान खराब / सेवा नहीं मिली / वादा किया रिफंड नहीं मिला]। यह {when_clause} हुआ।
3. {demand_clause}मुझे न रिफंड मिला है और न संतोषजनक समाधान।
4. इसलिए मैं माँग करता/करती हूँ कि इस नोटिस के मिलने के **15 दिनों** के भीतर {amount} वापस करें। ऐसा न करने पर मैं Consumer Protection Act, 2019 के तहत उपयुक्त उपभोक्ता आयोग में रिफंड, मुआवज़े और खर्च की माँग के साथ शिकायत दायर करूँगा/करूँगी।

संलग्न: {enclosures}

भवदीय,
[नाम]   [हस्ताक्षर]   [फ़ोन / ईमेल]"""},
"salary": {"en": """**LEGAL NOTICE (DRAFT)**

Date: {today}
From: [YOUR FULL NAME, EMPLOYEE ID, ADDRESS]
To: [EMPLOYER / COMPANY NAME, REGISTERED ADDRESS, HR HEAD EMAIL]
Sent by: Speed Post and Email

**Subject: Demand for payment of pending salary of {amount}**

Sir/Madam,

1. I am/was employed with you as [DESIGNATION] since [DATE OF JOINING] [until DATE OF LEAVING, if applicable], at a monthly salary of [AMOUNT].
2. My salary for [MONTHS] remains unpaid, totalling {amount}. The non-payment has continued {when_clause}.
3. {demand_clause}Despite this, the amount has not been paid.
4. I therefore call upon you to pay {amount}, together with any full-and-final settlement dues, within **15 days** of receiving this notice. If you fail to do so, I will approach the Labour Commissioner / the appropriate legal forum for recovery, at your cost and risk.

Enclosures: {enclosures}

Yours faithfully,
[NAME]   [SIGNATURE]   [PHONE / EMAIL]""",
"hi": """**कानूनी नोटिस (ड्राफ्ट)**

तारीख: {today}
प्रेषक: [आपका पूरा नाम, कर्मचारी आईडी, पता]
प्रति: [नियोक्ता / कंपनी का नाम, पंजीकृत पता, HR प्रमुख का ईमेल]
भेजने का माध्यम: स्पीड पोस्ट और ईमेल

**विषय: {amount} की बकाया तनख्वाह के भुगतान हेतु माँग**

महोदय/महोदया,

1. मैं [पद] के रूप में [नौकरी शुरू होने की तारीख] से [छोड़ने की तारीख, यदि लागू] आपके यहाँ कार्यरत हूँ/था/थी, मासिक वेतन [राशि]।
2. [महीनों] की मेरी तनख्वाह बकाया है, कुल {amount}। यह भुगतान न होना {when_clause} से जारी है।
3. {demand_clause}इसके बावजूद राशि का भुगतान नहीं हुआ।
4. इसलिए मैं माँग करता/करती हूँ कि इस नोटिस के मिलने के **15 दिनों** के भीतर {amount} तथा फुल-एंड-फ़ाइनल की देय राशि का भुगतान करें। ऐसा न करने पर मैं वसूली के लिए श्रम आयुक्त / उपयुक्त कानूनी मंच के पास जाऊँगा/जाऊँगी, जिसका खर्च और जोखिम आप पर होगा।

संलग्न: {enclosures}

भवदीय,
[नाम]   [हस्ताक्षर]   [फ़ोन / ईमेल]"""},
}


def build(topic, lang, facts):
    en = lang != "hi"
    amount = inr(facts["amount"]) if facts.get("amount") else ("[AMOUNT]" if en else "[राशि]")
    m = facts.get("elapsed")
    if m is None:
        when = "[approximate date]" if en else "[अनुमानित तारीख]"
    else:
        when = f"about {m} month(s) ago" if en else f"लगभग {m} महीने पहले"
    if facts.get("demanded") is True:
        demand = ("I have already asked you in writing on [DATE(S)] to pay. " if en else "मैं [तारीख(ें)] को आपसे लिखित में भुगतान माँग चुका/चुकी हूँ। ")
    else:
        demand = ("I have requested payment several times. " if en else "मैंने कई बार भुगतान का अनुरोध किया है। ")
        demand = "[CONFIRM BEFORE SENDING: " + demand.strip() + "] " if en else "[भेजने से पहले पुष्टि करें: " + demand.strip() + "] "
    enc = proof_names(facts.get("proof") or [], lang)
    enclosures = ", ".join(enc) if enc else ("[list copies of your documents]" if en else "[अपने दस्तावेज़ों की प्रतियाँ सूचीबद्ध करें]")
    tpl = T[topic]["hi" if lang == "hi" else "en"]
    return tpl.format(today=datetime.date.today().strftime("%d %B %Y"), amount=amount, when_clause=when,
                      demand_clause=demand, enclosures=enclosures)
