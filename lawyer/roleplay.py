"""Practice mode: the assistant plays the other side; rule-based coaching, no legal claims invented."""
import re

STEPS = {
"deposit": {"en": [
 ("I deducted for damage and repainting. There is nothing left to return.", r"itemi|bill|photo|proof|receipt|wear|list|breakdown|invoice", "Good: you asked for evidence of the deductions.", "Ask for an itemised list with bills or photos. Normal wear and tear is not the same as damage. Mention your move-out photos if you have them."),
 ("You left without proper notice, so the deposit is forfeited.", r"agreement|clause|notice|message|email|whatsapp|period", "Good: you tied your answer to the agreement or your notice.", "Quote the notice clause from the agreement exactly. If you gave notice by message or email, point to that message."),
 ("I will pay later. I don't have the money right now.", r"date|deadline|days|by |writing|written|schedule", "Good: you asked for a date or something in writing.", "Don't accept a vague promise. Ask for a specific date in writing, and say a formal notice follows if it passes."),
 ("Go to court then. Nothing will happen to me.", r"notice|legal|court|lawyer|forum|authority|tribunal|complaint", "Good: you stated a concrete next step calmly.", "Stay calm and state your next step: a legal notice with a 15-day deadline, then legal action. Don't argue or threaten."),
], "hi": [
 ("मैंने नुकसान और पेंटिंग के लिए पैसे काट लिए। लौटाने को कुछ नहीं बचा।", r"ब्यौरा|बिल|फोटो|फ़ोटो|सबूत|रसीद|सूची|घिसावट", "अच्छा: आपने कटौतियों का सबूत माँगा।", "बिल या फ़ोटो के साथ कटौतियों की सूची माँगें। सामान्य घिसावट नुकसान नहीं है। घर खाली करते समय की फ़ोटो हों तो बताएँ।"),
 ("आपने ठीक से नोटिस दिए बिना घर छोड़ा, इसलिए डिपॉजिट जब्त है।", r"एग्रीमेंट|क्लॉज|नोटिस|मैसेज|ईमेल|व्हाट्सएप|अवधि", "अच्छा: आपने जवाब को एग्रीमेंट या अपने नोटिस से जोड़ा।", "एग्रीमेंट की नोटिस वाली शर्त ज्यों की त्यों बताएँ। अगर मैसेज या ईमेल से नोटिस दिया था तो वह दिखाएँ।"),
 ("मैं बाद में दे दूँगा। अभी पैसे नहीं हैं।", r"तारीख|दिन|लिखित|लिखकर|समय", "अच्छा: आपने तारीख या लिखित वादा माँगा।", "अस्पष्ट वादा न मानें। लिखित में पक्की तारीख माँगें और कहें कि तारीख निकली तो औपचारिक नोटिस जाएगा।"),
 ("कोर्ट जाओ फिर। मेरा कुछ नहीं बिगड़ेगा।", r"नोटिस|कानूनी|कोर्ट|अदालत|वकील|शिकायत", "अच्छा: आपने शांति से अगला कदम बताया।", "शांत रहें और अगला कदम बताएँ: 15 दिन की समय-सीमा वाला कानूनी नोटिस, फिर कानूनी कार्यवाही। बहस या धमकी न दें।"),
]},
"refund": {"en": [
 ("Refunds are not possible. Our policy says purchases are non-refundable.", r"defect|not as|promis|advertis|order|invoice|wrong|damaged|consumer|service", "Good: you stated what was wrong or promised.", "A 'no refund' line may not protect them if the product was defective or the service deficient. State clearly what was promised and what you got."),
 ("Please email support; we have raised a ticket.", r"ticket|number|email|writing|written|deadline|date|days", "Good: you pushed for a record and a date.", "Get the ticket number in writing and ask for a resolution date. Keep every reply."),
 ("Your refund will come in 30 to 45 working days.", r"date|deadline|days|helpline|1915|complaint|consumer|writing", "Good: you pressed on timing or escalation.", "Ask for a written commitment with a date. Mention the National Consumer Helpline (1915) if there is no firm date."),
 ("You can't do anything. Go ahead and complain.", r"consumer|complaint|commission|helpline|1915|notice|legal", "Good: you named the forum or your next step.", "Calmly name your next step: the National Consumer Helpline, a legal notice, then a consumer complaint."),
], "hi": [
 ("रिफंड संभव नहीं है। हमारी पॉलिसी में खरीद वापसी-योग्य नहीं है।", r"खराब|वादा|विज्ञापन|ऑर्डर|इनवॉइस|उपभोक्ता|सेवा|गलत", "अच्छा: आपने बताया कि क्या गलत था या क्या वादा हुआ था।", "'रिफंड नहीं' वाली लाइन उन्हें नहीं बचा सकती अगर सामान खराब या सेवा में कमी थी। साफ़ बताएँ कि क्या वादा था और क्या मिला।"),
 ("कृपया सपोर्ट को ईमेल करें, हमने टिकट बना दिया है।", r"टिकट|नंबर|ईमेल|लिखित|तारीख|दिन", "अच्छा: आपने रिकॉर्ड और तारीख पर ज़ोर दिया।", "टिकट नंबर लिखित में लें और समाधान की तारीख माँगें। हर जवाब सँभालकर रखें।"),
 ("आपका रिफंड 30 से 45 कार्य-दिवस में आएगा।", r"तारीख|दिन|हेल्पलाइन|1915|शिकायत|उपभोक्ता|लिखित", "अच्छा: आपने समय या आगे की कार्रवाई पर ज़ोर दिया।", "तारीख के साथ लिखित वादा माँगें। पक्की तारीख न मिले तो राष्ट्रीय उपभोक्ता हेल्पलाइन (1915) का ज़िक्र करें।"),
 ("आप कुछ नहीं कर सकते। जाइए शिकायत कर दीजिए।", r"उपभोक्ता|शिकायत|आयोग|हेल्पलाइन|1915|नोटिस|कानूनी", "अच्छा: आपने मंच या अगला कदम बताया।", "शांति से अगला कदम बताएँ: राष्ट्रीय उपभोक्ता हेल्पलाइन, कानूनी नोटिस, फिर उपभोक्ता शिकायत।"),
]},
"salary": {"en": [
 ("The company is facing a cash crunch. Salary will come soon.", r"date|when|written|writing|deadline|exact|days|by ", "Good: you asked for a date or written commitment.", "'Soon' is not an answer. Ask for an exact date in writing for the pending salary."),
 ("You didn't serve your notice period, so we are withholding your final settlement.", r"appointment|offer|agreement|clause|policy|payslip|earned|already|worked|salary for", "Good: you separated earned salary from settlement deductions.", "Salary you already earned is different from final-settlement deductions. Ask which clause of your appointment letter they rely on, in writing."),
 ("We have no record that we owe you anything.", r"payslip|bank|statement|attendance|email|offer|record|proof|slip", "Good: you pointed to your records.", "Point to payslips, bank statements, attendance records and emails. Say you have kept copies."),
 ("Do what you want. We have lawyers.", r"labou?r|commissioner|notice|legal|complaint|department|lawyer", "Good: you named a concrete forum.", "Stay calm and name your next step: a written legal notice, then a complaint to the Labour Commissioner."),
], "hi": [
 ("कंपनी में पैसों की तंगी है। तनख्वाह जल्दी आ जाएगी।", r"तारीख|कब|लिखित|लिखकर|दिन|समय", "अच्छा: आपने तारीख या लिखित वादा माँगा।", "'जल्दी' कोई जवाब नहीं है। बकाया तनख्वाह की सटीक तारीख लिखित में माँगें।"),
 ("आपने नोटिस पीरियड पूरा नहीं किया, इसलिए फुल-एंड-फ़ाइनल रोक रहे हैं।", r"नियुक्ति|ऑफर|एग्रीमेंट|क्लॉज|पॉलिसी|पेस्लिप|कमाई|काम किया", "अच्छा: आपने कमाई हुई तनख्वाह और सेटलमेंट की कटौती को अलग रखा।", "जो तनख्वाह आप कमा चुके हैं वह फुल-एंड-फ़ाइनल की कटौतियों से अलग है। लिखित में पूछें कि वे नियुक्ति पत्र की किस शर्त पर निर्भर हैं।"),
 ("हमारे रिकॉर्ड में आपका कुछ बकाया नहीं है।", r"पेस्लिप|बैंक|स्टेटमेंट|हाज़िरी|ईमेल|ऑफर|रिकॉर्ड|सबूत", "अच्छा: आपने अपने रिकॉर्ड का हवाला दिया।", "पेस्लिप, बैंक स्टेटमेंट, हाज़िरी और ईमेल का ज़िक्र करें। कहें कि आपके पास प्रतियाँ हैं।"),
 ("जो करना है कर लो। हमारे पास वकील हैं।", r"श्रम|आयुक्त|नोटिस|कानूनी|शिकायत|विभाग|वकील", "अच्छा: आपने ठोस मंच बताया।", "शांत रहें और अगला कदम बताएँ: लिखित कानूनी नोटिस, फिर श्रम आयुक्त को शिकायत।"),
]},
}

CHECKS = [
 ("Referred to proof / documents", "सबूत / दस्तावेज़ों का ज़िक्र", r"proof|document|receipt|bill|payslip|statement|agreement|screenshot|photo|सबूत|दस्तावेज़|रसीद|बिल|पेस्लिप|एग्रीमेंट|फोटो|फ़ोटो"),
 ("Asked for a date or deadline", "तारीख या समय-सीमा माँगी", r"date|deadline|days|by |तारीख|दिन|समय-सीमा"),
 ("Kept things in writing", "बातचीत लिखित में रखी", r"writing|written|email|message|notice|लिखित|लिखकर|ईमेल|मैसेज|नोटिस"),
 ("Named a concrete next step", "ठोस अगला कदम बताया", r"notice|complaint|court|commission|commissioner|helpline|lawyer|नोटिस|शिकायत|अदालत|कोर्ट|आयोग|आयुक्त|हेल्पलाइन|वकील"),
]
ABUSE = re.compile(r"idiot|stupid|bastard|saala|chor|चोर|बेवकूफ|गाली", re.I)


def steps(topic, lang):
    return STEPS[topic]["hi" if lang == "hi" else "en"]


def evaluate(step, user_text, lang):
    _, rx, good, miss = step
    tip = good if re.search(rx, user_text, re.I) else miss
    if ABUSE.search(user_text):
        tip += (" Also avoid insults or accusations you can't prove; they weaken your position." if lang != "hi"
                else " साथ ही गाली-गलौज या ऐसे आरोपों से बचें जिन्हें आप साबित नहीं कर सकते; इससे आपकी स्थिति कमज़ोर होती है।")
    return tip


def checklist(all_user_text, lang):
    lines = []
    for en, hi, rx in CHECKS:
        ok = bool(re.search(rx, all_user_text, re.I))
        lines.append(f"- {'✅' if ok else '⬜'} {hi if lang == 'hi' else en}")
    return "\n".join(lines)
