"""Evidence checklist: what proof each kind of case usually needs, ticked against what the user said they have."""

# (tag(s) that count as 'have it', english, hindi)
ITEMS = {
"deposit": [
 (("agreement",), "Rental agreement (or any written rent terms)", "किराया एग्रीमेंट (या लिखित शर्तें)"),
 (("bank/UPI record", "receipt/invoice"), "Proof you paid the deposit: bank/UPI record or receipt", "डिपॉजिट देने का सबूत: बैंक/UPI रिकॉर्ड या रसीद"),
 (("photos/videos",), "Photos/videos of the home when you left", "घर छोड़ते समय की फ़ोटो/वीडियो"),
 (("chats/emails",), "Your notice to vacate and the landlord's replies or excuses (chats/emails)", "घर खाली करने का आपका नोटिस और मकान मालिक के जवाब/बहाने (चैट/ईमेल)"),
 ((), "Proof you returned the keys / handed over possession", "चाबी लौटाने / कब्ज़ा सौंपने का सबूत"),
 ((), "Final electricity/water/maintenance bills showing no dues", "बिजली/पानी/मेंटेनेंस के अंतिम बिल (कोई बकाया नहीं)"),
 ((), "Your written demand, with proof it was sent (screenshot, speed-post receipt)", "आपकी लिखित माँग और भेजने का सबूत (स्क्रीनशॉट, स्पीड-पोस्ट रसीद)"),
],
"refund": [
 (("receipt/invoice",), "Invoice / order confirmation", "इनवॉइस / ऑर्डर कन्फ़र्मेशन"),
 (("bank/UPI record",), "Proof of payment (bank/UPI/card statement)", "भुगतान का सबूत (बैंक/UPI/कार्ड स्टेटमेंट)"),
 (("photos/videos",), "Photos/video of the defect or what you actually received", "खराबी या जो वास्तव में मिला उसकी फ़ोटो/वीडियो"),
 (("chats/emails",), "Complaints, ticket numbers and replies from the seller/company", "विक्रेता/कंपनी को शिकायतें, टिकट नंबर और उनके जवाब"),
 ((), "Screenshot of the ad, offer or refund policy you relied on", "जिस विज्ञापन, ऑफ़र या रिफंड पॉलिसी पर भरोसा किया उसका स्क्रीनशॉट"),
 ((), "Delivery / return-pickup proof", "डिलीवरी / रिटर्न-पिकअप का सबूत"),
 ((), "Your written demand, with proof it was sent", "आपकी लिखित माँग और भेजने का सबूत"),
],
"salary": [
 (("agreement",), "Offer / appointment letter showing salary and terms", "ऑफ़र / नियुक्ति पत्र जिसमें वेतन और शर्तें हों"),
 (("payslips",), "Payslips (especially the last paid month)", "पेस्लिप (खासकर आखिरी भुगतान वाला महीना)"),
 (("bank/UPI record",), "Bank statements showing salary credits and where they stopped", "बैंक स्टेटमेंट जिसमें सैलरी आई और कहाँ रुकी"),
 (("chats/emails",), "Emails/chats with HR or your manager about the delay or promised dates", "देरी या वादा की गई तारीखों पर HR/मैनेजर से ईमेल/चैट"),
 ((), "Proof you worked: ID card, attendance, work emails", "काम करने का सबूत: आईडी कार्ड, हाज़िरी, ऑफ़िस ईमेल"),
 ((), "Resignation or termination email and your last working day", "इस्तीफ़ा या बर्खास्तगी का ईमेल और आखिरी कार्य-दिवस"),
 ((), "PF / Form 16 details, if you have them", "PF / फ़ॉर्म 16 की जानकारी, यदि हो"),
 ((), "Your written demand, with proof it was sent", "आपकी लिखित माँग और भेजने का सबूत"),
],
}


def build(topic, lang, have):
    hi = lang == "hi"
    lines = []
    for tags, en, hin in ITEMS[topic]:
        ok = bool(tags) and any(t in have for t in tags)
        lines.append(f"- {'✅' if ok else '⬜'} {hin if hi else en}")
    return "\n".join(lines)
