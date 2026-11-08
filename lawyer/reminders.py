"""Reminder calendar (.ics). Deterministic dates computed from the user's own facts; every event says it is approximate."""
import datetime, uuid


def _add_months(d, m):
    y, mo = divmod(d.month - 1 + m, 12)
    return datetime.date(d.year + y, mo + 1, min(d.day, 28))


def events(topic, facts, lang="en", today=None, notice_days=None):
    today = today or datetime.date.today()
    hi = lang == "hi"
    E = []

    def ev(days, en, hin, note_en="", note_hi=""):
        E.append((today + datetime.timedelta(days=days), hin if hi else en, note_hi if hi else note_en))

    ev(3, "Gather your documents and proofs", "अपने दस्तावेज़ और सबूत इकट्ठे करें",
       "Use the evidence checklist. Back up chats and statements.", "सबूतों की सूची देखें। चैट और स्टेटमेंट का बैकअप लें।")
    ev(7, "Send your written demand / legal notice", "अपनी लिखित माँग / कानूनी नोटिस भेजें",
       "Speed post + email. Note the date you send it; the 15-day deadline counts from receipt.", "स्पीड पोस्ट + ईमेल। भेजने की तारीख लिखें; 15 दिन की गिनती प्राप्ति से शुरू होती है।")
    ev(22, "Notice deadline likely over: decide the next step", "नोटिस की समय-सीमा संभवतः खत्म: अगला कदम तय करें",
       "Assumes you sent the notice on day 7 and the deadline is 15 days. Edit if different. See a lawyer before filing.",
       "मानकर चला गया है कि नोटिस 7वें दिन भेजा और समय-सीमा 15 दिन है। अलग हो तो बदलें। दायर करने से पहले वकील से मिलें।")
    m = facts.get("elapsed")
    if topic in ("deposit", "refund") and m is not None:
        period = 36 if topic == "deposit" else 24
        left = period - m
        if left <= 0:
            ev(2, "URGENT: time limit may already have passed: see a lawyer", "ज़रूरी: समय-सीमा शायद बीत चुकी है: वकील से मिलें",
               f"Approx. limit is {period // 12} years from when the right arose. A court may still excuse delay: only a lawyer can say.",
               f"अनुमानित सीमा {period // 12} साल है। अदालत देरी माफ़ कर सकती है: यह केवल वकील बता सकता है।")
        else:
            lim = _add_months(today, left)
            warn = max(lim - datetime.timedelta(days=90), today + datetime.timedelta(days=1))
            E.append((warn, "Time-limit review: see a lawyer before the limit" if not hi else "समय-सीमा की समीक्षा: सीमा से पहले वकील से मिलें",
                      (f"Approximate limit date: {lim.isoformat()} (about {period // 12} years from the event). Estimated from your 'how long ago' answer." if not hi
                       else f"अनुमानित सीमा तिथि: {lim.isoformat()} (घटना से लगभग {period // 12} साल)। आपके 'कितना समय पहले' उत्तर से अनुमानित।")))
    elif topic == "salary":
        ev(30, "Labour forums can have short limits: if unpaid, escalate now", "श्रम मंचों की समय-सीमा कम हो सकती है: बकाया हो तो अभी आगे बढ़ें",
           "Complaint to the Labour Commissioner / Labour Department.", "श्रम आयुक्त / श्रम विभाग में शिकायत।")
    if notice_days:
        ev(max(notice_days - 3, 1), f"Send your reply to the notice (deadline is {notice_days} days from the day YOU received it)",
           f"नोटिस का जवाब भेजें (समय-सीमा आपको मिलने से {notice_days} दिन)",
           "Assumes you received it today. Edit the date to match the real receipt date.", "मानकर चला गया है कि आपको आज मिला। असली तारीख के अनुसार बदलें।")
    return sorted(E, key=lambda x: x[0])


def _esc(t):
    return t.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def ics(evs):
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    L = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Nyay Saathi//Reminders//EN", "CALSCALE:GREGORIAN"]
    for d, title, note in evs:
        L += ["BEGIN:VEVENT", f"UID:{uuid.uuid4()}@nyay-saathi", f"DTSTAMP:{stamp}", f"DTSTART;VALUE=DATE:{d.strftime('%Y%m%d')}",
              f"DTEND;VALUE=DATE:{(d + datetime.timedelta(days=1)).strftime('%Y%m%d')}", f"SUMMARY:{_esc(title)}",
              f"DESCRIPTION:{_esc(note + ' (Approximate dates, general information, not legal advice.)')}",
              "BEGIN:VALARM", "ACTION:DISPLAY", "DESCRIPTION:Reminder", "TRIGGER:-P1D", "END:VALARM", "END:VEVENT"]
    L.append("END:VCALENDAR")
    return "\r\n".join(L) + "\r\n"


def as_text(evs, lang="en"):
    head = "### Your reminder dates (approximate)" if lang != "hi" else "### आपकी रिमाइंडर तारीख़ें (अनुमानित)"
    return head + "\n\n" + "\n".join(f"- **{d.strftime('%d %b %Y')}**: {t}" for d, t, _ in evs)
