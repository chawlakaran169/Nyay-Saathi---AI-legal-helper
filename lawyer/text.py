"""All user-facing strings, English + Hindi. Legal content lives in kb/sources.json, not here."""

TOPIC_NAME = {
    "deposit": {"en": "Security deposit not returned (tenant / landlord)", "hi": "सिक्योरिटी डिपॉजिट वापस नहीं मिला (किरायेदार / मकान मालिक)"},
    "refund": {"en": "Refund / defective product or service (consumer)", "hi": "रिफंड / खराब सामान या सेवा (उपभोक्ता)"},
    "salary": {"en": "Unpaid salary / wages (employee / employer)", "hi": "बकाया तनख्वाह / मज़दूरी (कर्मचारी / नियोक्ता)"},
}
OTHER_SIDE = {
    "deposit": {"en": "the landlord", "hi": "मकान मालिक"},
    "refund": {"en": "the seller / company", "hi": "विक्रेता / कंपनी"},
    "salary": {"en": "the employer", "hi": "नियोक्ता"},
}

S = {
"intro": {
"en": ("Namaste. I'm an AI legal helper for everyday problems in India. I'm **not a lawyer** and I can make mistakes.\n\n"
       "I can help with: **(1)** a security deposit a landlord won't return, **(2)** a refund or defective product/service, "
       "**(3)** unpaid salary. I can explain where you stand, build your case, draft a legal notice, and let you practise "
       "the argument.\n\nTell me what happened, in English or Hindi (text or voice)."),
"hi": ("नमस्ते। मैं भारत में रोज़मर्रा की कानूनी समस्याओं के लिए एक AI सहायक हूँ। मैं **वकील नहीं हूँ** और मुझसे गलती हो सकती है।\n\n"
       "मैं इनमें मदद कर सकता हूँ: **(1)** मकान मालिक डिपॉजिट वापस नहीं कर रहा, **(2)** रिफंड या खराब सामान/सेवा, **(3)** बकाया तनख्वाह। "
       "मैं बता सकता हूँ कि आप कहाँ खड़े हैं, आपका केस तैयार कर सकता हूँ, कानूनी नोटिस का ड्राफ्ट बना सकता हूँ और बहस का अभ्यास करा सकता हूँ।\n\n"
       "बताइए क्या हुआ, हिंदी या अंग्रेज़ी में (लिखकर या बोलकर)।")},
"ask_topic": {
"en": "I want to be sure I understand. Is your problem about: **1) a deposit** from a landlord, **2) a refund** from a seller/company, or **3) unpaid salary**? Reply with 1, 2 or 3 (or describe it again). If it is something else (family, criminal, property, tax, traffic, IP...), I can't help with that: please see a lawyer, or call free legal aid (NALSA) on **15100**.",
"hi": "मैं सही समझना चाहता हूँ। आपकी समस्या किस बारे में है: **1) मकान मालिक से डिपॉजिट**, **2) विक्रेता/कंपनी से रिफंड**, या **3) बकाया तनख्वाह**? 1, 2 या 3 लिखें (या फिर से बताएँ)। अगर यह कुछ और है (पारिवारिक, आपराधिक, संपत्ति, टैक्स, ट्रैफ़िक, IP...), तो मैं उसमें मदद नहीं कर सकता: कृपया वकील से मिलें या मुफ़्त कानूनी सहायता (NALSA) **15100** पर कॉल करें।"},
"out_of_scope": {
"en": ("This looks like a matter I'm **not equipped to handle** (for example family, criminal, property-title, tax or cyber matters). "
       "Giving you guesses here could hurt you. Please speak to a lawyer. If money is a worry, free legal aid is available: call NALSA on **15100** "
       "or visit your District Legal Services Authority.\n\nIf you also have a deposit, refund or salary problem, tell me about that and I'll help."),
"hi": ("यह ऐसा मामला लगता है जिसे सँभालने के लिए मैं **सक्षम नहीं** हूँ (जैसे पारिवारिक, आपराधिक, संपत्ति-स्वामित्व, टैक्स या साइबर मामले)। यहाँ अंदाज़े देना आपको नुकसान पहुँचा सकता है। कृपया किसी वकील से मिलें। "
       "पैसे की चिंता हो तो मुफ़्त कानूनी सहायता उपलब्ध है: NALSA को **15100** पर कॉल करें या अपने ज़िला विधिक सेवा प्राधिकरण जाएँ।\n\nअगर आपकी डिपॉजिट, रिफंड या तनख्वाह की भी समस्या है तो वह बताइए, मैं मदद करूँगा।")},
"emergency": {
"en": ("This sounds **urgent or unsafe**. Please don't rely on a chatbot.\n- Danger right now: call **112**.\n- Arrested, or police action against you: contact a lawyer immediately; "
       "free legal aid via NALSA **15100**.\n- Do not sign anything you don't understand.\n\nWhen you are safe, I can help with deposit, refund or salary problems."),
"hi": ("यह **तुरंत ध्यान देने वाला या असुरक्षित** मामला लगता है। कृपया सिर्फ़ चैटबॉट पर भरोसा न करें।\n- अभी खतरा हो तो **112** पर कॉल करें।\n- गिरफ्तारी या पुलिस कार्रवाई हो तो तुरंत वकील से संपर्क करें; मुफ़्त सहायता NALSA **15100**।\n- जो समझ न आए उस पर हस्ताक्षर न करें।\n\nसुरक्षित होने पर मैं डिपॉजिट, रिफंड या तनख्वाह की समस्या में मदद कर सकता हूँ।")},
"caselaw": {
"en": ("I don't quote court cases or judgments: AI tools often invent them, and a wrong citation can damage your case. "
       "What I can give you are the laws in my verified list (below). For case law, ask a lawyer or search the Supreme Court / High Court websites yourself."),
"hi": ("मैं अदालती मामलों या फैसलों के हवाले नहीं देता: AI अक्सर इन्हें गढ़ देता है और गलत हवाला आपके केस को नुकसान पहुँचा सकता है। "
       "मैं केवल अपनी सत्यापित सूची के कानून बता सकता हूँ (नीचे)। फैसलों के लिए वकील से पूछें या सुप्रीम कोर्ट / हाई कोर्ट की वेबसाइट देखें।")},
"injection": {
"en": "I can't change my rules or pretend to be something else. I'm here to help with deposit, refund and salary problems, and I only state laws from my verified list. What happened in your case?",
"hi": "मैं अपने नियम नहीं बदल सकता और न ही कुछ और बनने का दिखावा कर सकता हूँ। मैं डिपॉजिट, रिफंड और तनख्वाह की समस्याओं में मदद के लिए हूँ और केवल अपनी सत्यापित सूची के कानून बताता हूँ। आपके मामले में क्या हुआ?"},
"guarantee": {
"en": "**No one can promise you will win, and I can't either.** Outcomes depend on proof, the other side's response and the forum.",
"hi": "**जीत की गारंटी कोई नहीं दे सकता, मैं भी नहीं।** नतीजा सबूतों, दूसरे पक्ष के जवाब और मंच पर निर्भर करता है।"},
"q": {
"when": {
 "deposit": {"en": "When did you vacate (or when should the deposit have come back)? e.g. 'March 2025' or '3 months ago'.", "hi": "आपने घर कब खाली किया (या डिपॉजिट कब लौटना था)? जैसे 'मार्च 2025' या '3 महीने पहले'।"},
 "refund": {"en": "When did you pay, or when did the problem start? e.g. 'January 2026' or '2 months ago'.", "hi": "आपने पैसे कब दिए, या समस्या कब शुरू हुई? जैसे 'जनवरी 2026' या '2 महीने पहले'।"},
 "salary": {"en": "Since when has your salary been unpaid? e.g. 'since June 2026' or '3 months'.", "hi": "आपकी तनख्वाह कब से बकाया है? जैसे 'जून 2026 से' या '3 महीने'।"}},
"amount": {
 "deposit": {"en": "How much deposit is the landlord holding (in ₹)?", "hi": "मकान मालिक के पास कितना डिपॉजिट है (₹ में)?"},
 "refund": {"en": "How much did you pay (in ₹)?", "hi": "आपने कितना पैसा दिया (₹ में)?"},
 "salary": {"en": "How much salary is pending in total (in ₹)?", "hi": "कुल कितनी तनख्वाह बकाया है (₹ में)?"}},
"proof": {"all": {"en": "What proof do you have? (agreement, receipts, bank/UPI transfers, WhatsApp/email chats, photos, payslips...). If none, say 'none'.",
                  "hi": "आपके पास क्या सबूत है? (एग्रीमेंट, रसीदें, बैंक/UPI ट्रांसफ़र, WhatsApp/ईमेल चैट, फ़ोटो, पेस्लिप...). कुछ नहीं हो तो 'कुछ नहीं' लिखें।"}},
"demanded": {"all": {"en": "Have you already asked them in writing (message or email) to pay? Yes or no?",
                     "hi": "क्या आप उन्हें लिखित में (मैसेज या ईमेल) पैसे देने को कह चुके हैं? हाँ या नहीं?"}},
},
"h_situ": {"en": "### 1. Your situation (as I understood it)", "hi": "### 1. आपकी स्थिति (जैसा मैंने समझा)"},
"h_stand": {"en": "### 2. Where you stand", "hi": "### 2. आप कहाँ खड़े हैं"},
"h_opts": {"en": "### 3. Your options, in order", "hi": "### 3. आपके विकल्प, क्रम से"},
"h_week": {"en": "### 4. What to do this week", "hi": "### 4. इस हफ़्ते क्या करें"},
"h_src": {"en": "### Sources used (verify before relying)", "hi": "### प्रयुक्त स्रोत (भरोसा करने से पहले जाँचें)"},
"f_issue": {"en": "Issue", "hi": "समस्या"}, "f_amount": {"en": "Amount", "hi": "राशि"},
"f_when": {"en": "How long ago", "hi": "कितना समय पहले"}, "f_proof": {"en": "Proof you have", "hi": "आपके सबूत"},
"f_written": {"en": "Asked in writing already", "hi": "लिखित में माँग चुके"},
"yes": {"en": "Yes", "hi": "हाँ"}, "no": {"en": "No", "hi": "नहीं"}, "unknown": {"en": "not stated", "hi": "बताया नहीं"},
"none_proof": {"en": "none yet", "hi": "अभी कुछ नहीं"},
"months": {"en": "about {n} month(s)", "hi": "लगभग {n} महीने"},
"lim_ok": {"en": "**Time limit:** about {p} applies (see sources). You appear to be inside it, but don't wait.",
           "hi": "**समय-सीमा:** लगभग {p} लागू होती है (स्रोत देखें)। आप सीमा के भीतर लगते हैं, पर देर न करें।"},
"lim_near": {"en": "**Time limit warning:** about {p} applies and you may be close to it. See a lawyer **this week**.",
             "hi": "**समय-सीमा चेतावनी:** लगभग {p} लागू होती है और आप उसके करीब हो सकते हैं। **इसी हफ़्ते** वकील से मिलें।"},
"lim_exp": {"en": "**Time limit warning:** about {p} applies and it may **already have passed**. Courts can still sometimes excuse delay, but you need a lawyer's view before anything else.",
            "hi": "**समय-सीमा चेतावनी:** लगभग {p} लागू होती है और वह **पहले ही बीत चुकी हो सकती है**। अदालतें कभी-कभी देरी माफ़ कर देती हैं, पर पहले वकील की राय ज़रूरी है।"},
"lim_unknown": {"en": "**Time limit:** labour forums can have short limits; act quickly.", "hi": "**समय-सीमा:** श्रम मंचों पर समय-सीमा कम हो सकती है; जल्दी कार्रवाई करें।"},
"p3y": {"en": "3 years", "hi": "3 साल"}, "p2y": {"en": "2 years", "hi": "2 साल"},
"forum_limits": {"en": "Consumer Commission limits use the value **paid as consideration**, not necessarily the unpaid refund: **District Consumer Commission** up to ₹50 lakh; **State Consumer Commission** above ₹50 lakh up to ₹2 crore; **National Consumer Commission** above ₹2 crore. I have not collected the amount you paid separately, so confirm the right Commission before filing.", "hi": "उपभोक्ता आयोग की सीमा आपके **भुगतान किए गए प्रतिफल के मूल्य** पर निर्भर करती है, जो बकाया रिफंड से अलग हो सकता है: **जिला उपभोक्ता आयोग** ₹50 लाख तक; **राज्य उपभोक्ता आयोग** ₹50 लाख से अधिक और ₹2 करोड़ तक; **राष्ट्रीय उपभोक्ता आयोग** ₹2 करोड़ से अधिक। भुगतान की गई राशि अलग से नहीं पूछी गई है, इसलिए शिकायत से पहले सही आयोग की पुष्टि करें।"},
"opts": {
 "deposit": {"en": ["Ask in writing again, politely, requesting itemised deductions and a date.",
                    "Send a legal notice with a 15-day deadline (say **draft notice** and I'll prepare it).",
                    "Civil recovery suit / state rent authority, with a lawyer (free legal aid may apply)."],
             "hi": ["विनम्रता से फिर लिखित में माँगें, कटौतियों का ब्यौरा और तारीख़ माँगते हुए।",
                    "15 दिन की समय-सीमा वाला कानूनी नोटिस भेजें (**draft notice** लिखें, मैं तैयार कर दूँगा)।",
                    "वकील के साथ दीवानी वसूली मुकदमा / राज्य का रेंट प्राधिकरण (मुफ़्त कानूनी सहायता लागू हो सकती है)।"]},
 "refund": {"en": ["Complain in writing to the company's grievance officer with a deadline.",
                   "Raise it on the National Consumer Helpline (1915 / NCH app).",
                   "If unresolved, file a consumer complaint online through e-Jagriti. A notice first is helpful, not compulsory."],
            "hi": ["कंपनी के शिकायत अधिकारी को समय-सीमा के साथ लिखित शिकायत करें।",
                   "राष्ट्रीय उपभोक्ता हेल्पलाइन (1915 / NCH ऐप) पर शिकायत दर्ज करें।",
                   "हल न हो तो e-Jagriti पर ऑनलाइन उपभोक्ता शिकायत दायर करें। पहले नोटिस उपयोगी है, अनिवार्य नहीं।"]},
 "salary": {"en": ["Send a written demand to HR/employer for pending salary and full-and-final settlement.",
                   "Complain to your state Labour Commissioner / Labour Department.",
                   "If you are a 'worker', you may be able to apply to recover the money due from the employer under the Industrial Relations Code; ask the Labour Department, a lawyer or free legal aid."],
            "hi": ["HR/नियोक्ता को बकाया तनख्वाह और फुल-एंड-फ़ाइनल के लिए लिखित माँग भेजें।",
                   "अपने राज्य के श्रम आयुक्त / श्रम विभाग में शिकायत करें।",
                   "अगर आप 'कामगार (worker)' हैं तो Industrial Relations Code के तहत नियोक्ता से बकाया धन की वसूली का आवेदन संभव हो सकता है; श्रम विभाग, वकील या मुफ़्त कानूनी सहायता से पूछें।"]}},
"week_common": {"en": ["Put all your documents and screenshots in one folder and back them up.",
                       "Write a one-page timeline: date, what happened, who said what.",
                       "Do not agree to anything verbally; keep communication in writing."],
                "hi": ["सभी दस्तावेज़ और स्क्रीनशॉट एक फ़ोल्डर में रखें और बैकअप लें।",
                       "एक पन्ने की टाइमलाइन लिखें: तारीख़, क्या हुआ, किसने क्या कहा।",
                       "मौखिक रूप से कुछ भी न मानें; बातचीत लिखित में रखें।"]},
"week_noproof": {"en": "You listed little or no proof: look for bank/UPI statements, old chats, emails and the names of anyone who witnessed it. Bank statements are the strongest simple proof of payment.",
                 "hi": "आपने कम या कोई सबूत नहीं बताया: बैंक/UPI स्टेटमेंट, पुरानी चैट, ईमेल और गवाहों के नाम खोजें। भुगतान का सबसे आसान मज़बूत सबूत बैंक स्टेटमेंट है।"},
"week_nowritten": {"en": "You haven't asked in writing yet: send a short written demand first. It is your cheapest and most useful step.",
                   "hi": "आपने अभी लिखित में नहीं माँगा: पहले छोटी लिखित माँग भेजें। यह आपका सबसे सस्ता और उपयोगी कदम है।"},
"see_lawyer": {"en": "**See a real lawyer before filing anything.** Especially because: {why}.",
               "hi": "**कुछ भी दायर करने से पहले असली वकील से मिलें।** खासकर क्योंकि: {why}।"},
"why_big": {"en": "the amount is large", "hi": "राशि बड़ी है"},
"why_time": {"en": "the time limit may be near or over", "hi": "समय-सीमा पास या खत्म हो सकती है"},
"why_proof": {"en": "you have little proof", "hi": "आपके पास सबूत कम हैं"},
"why_std": {"en": "every case has details I can't see", "hi": "हर केस की ऐसी बारीकियाँ होती हैं जो मैं नहीं देख सकता"},
"next_menu": {"en": "\n\nNext: say **draft notice** for a ready-to-edit legal notice, or **practise** to rehearse the argument with me playing the other side.",
              "hi": "\n\nआगे: तैयार नोटिस ड्राफ्ट के लिए **draft notice** लिखें, या **practise** लिखें, मैं दूसरे पक्ष की भूमिका निभाकर बहस का अभ्यास कराऊँगा।"},
"disclaimer": {"en": "\n\n_General information, not legal advice. Laws change; verify using the links above._",
               "hi": "\n\n_यह सामान्य जानकारी है, कानूनी सलाह नहीं। कानून बदलते हैं; ऊपर दिए लिंक से जाँचें।_"},
"need_case": {"en": "Let's first understand your problem. Tell me what happened.", "hi": "पहले आपकी समस्या समझ लेते हैं। बताइए क्या हुआ।"},
"reset": {"en": "Okay, starting fresh. Tell me about your problem.", "hi": "ठीक है, नए सिरे से शुरू करते हैं। अपनी समस्या बताइए।"},
"notice_head": {"en": "Here is a **draft** legal notice. Fill the [BRACKETS], check every fact, and ideally have a lawyer review it before sending by speed post and email.\n\n---\n",
                "hi": "यह कानूनी नोटिस का **ड्राफ्ट** है। [ब्रैकेट] भरें, हर तथ्य जाँचें और भेजने से पहले (स्पीड पोस्ट और ईमेल से) बेहतर है कि वकील से दिखवा लें।\n\n---\n"},
"notice_tail": {"en": "\n---\nTip: say **practise** to rehearse how the other side may respond.", "hi": "\n---\nसुझाव: दूसरे पक्ष के जवाब का अभ्यास करने के लिए **practise** लिखें।"},
"rp_start": {"en": "**Practice mode.** I will play {side}. I'll be difficult, as real people often are. Reply as you would in real life; after each reply I'll give you a tip. Say **stop** any time.\n\n",
             "hi": "**अभ्यास मोड।** मैं {side} की भूमिका निभाऊँगा। मैं कठिन रहूँगा, जैसा असल में अक्सर होता है। असल जैसा जवाब दें; हर जवाब के बाद मैं एक सुझाव दूँगा। कभी भी **stop** लिखें।\n\n"},
"rp_tip": {"en": "\n\n> **Coach tip:** {tip}\n\n", "hi": "\n\n> **कोच का सुझाव:** {tip}\n\n"},
"rp_end": {"en": "**Practice finished.** Your checklist from this round:\n{lines}\n\nSay **draft notice** to put the strongest points on paper.",
           "hi": "**अभ्यास पूरा।** इस राउंड की आपकी चेकलिस्ट:\n{lines}\n\nसबसे मज़बूत बातें कागज़ पर उतारने के लिए **draft notice** लिखें।"},
"rp_not_started": {"en": "Say **practise** after we've discussed your case, and I'll play the other side.", "hi": "पहले आपके केस पर बात कर लें, फिर **practise** लिखें, मैं दूसरे पक्ष की भूमिका निभाऊँगा।"},
}


def t(key, lang, **kw):
    node = S[key]
    s = node.get(lang) or node["en"]
    return s.format(**kw) if kw else s


S.update({
"intro": {
"en": ("Namaste. I'm an AI legal helper for everyday problems in India. I'm **not a lawyer** and I can make mistakes.\n\n"
       "I can help with: **(1)** a security deposit a landlord won't return, **(2)** a refund or defective product/service, "
       "**(3)** unpaid salary, **(4)** a legal notice you **received** and don't understand. I can explain where you stand, build your case, "
       "list the proof you need, draft a notice or a reply, let you practise the argument, and give you a file to download.\n\n"
       "Tell me what happened, in English or Hindi (text or voice)."),
"hi": ("नमस्ते। मैं भारत में रोज़मर्रा की कानूनी समस्याओं के लिए एक AI सहायक हूँ। मैं **वकील नहीं हूँ** और मुझसे गलती हो सकती है।\n\n"
       "मैं इनमें मदद कर सकता हूँ: **(1)** मकान मालिक डिपॉजिट वापस नहीं कर रहा, **(2)** रिफंड या खराब सामान/सेवा, **(3)** बकाया तनख्वाह, "
       "**(4)** आपको **मिला** कानूनी नोटिस जो समझ नहीं आ रहा। मैं बता सकता हूँ कि आप कहाँ खड़े हैं, केस तैयार कर सकता हूँ, ज़रूरी सबूतों की सूची दे सकता हूँ, "
       "नोटिस या जवाब का ड्राफ्ट बना सकता हूँ, बहस का अभ्यास करा सकता हूँ और डाउनलोड के लिए फ़ाइल दे सकता हूँ।\n\n"
       "बताइए क्या हुआ, हिंदी या अंग्रेज़ी में (लिखकर या बोलकर)।")},
"next_menu": {
"en": "\n\nNext: say **draft notice** for a ready-to-edit legal notice, **checklist** for the proof you still need, or **practise** to rehearse the argument with me playing the other side. You can also download your case summary below the chat.",
"hi": "\n\nआगे: तैयार नोटिस ड्राफ्ट के लिए **draft notice**, ज़रूरी सबूतों की सूची के लिए **checklist**, या **practise** लिखें, मैं दूसरे पक्ष की भूमिका निभाकर बहस का अभ्यास कराऊँगा। चैट के नीचे से आप अपना केस-सारांश डाउनलोड भी कर सकते हैं।"},
"ev_head": {"en": "### Evidence checklist: what to have ready", "hi": "### सबूतों की सूची: क्या तैयार रखें"},
"ev_foot": {"en": "✅ = you told me you have it. ⬜ = not mentioned: look for it now. Keep originals and make copies; for chats and emails keep the original phone and take backups.",
            "hi": "✅ = आपने बताया कि आपके पास है। ⬜ = नहीं बताया: अभी खोजें। मूल दस्तावेज़ रखें और प्रतियाँ बनाएँ; चैट और ईमेल के लिए असली फ़ोन रखें और बैकअप लें।"},
"rcv_ask": {"en": "I can help you understand it. Please **paste the text** of the notice, or tell me: who sent it, what they want, how much money, by when, and whether it mentions a court, police, a cheque or a bank loan.",
            "hi": "मैं इसे समझाने में मदद कर सकता हूँ। कृपया नोटिस का **पाठ पेस्ट करें**, या बताएँ: किसने भेजा, क्या माँगा, कितना पैसा, कब तक, और क्या उसमें अदालत, पुलिस, चेक या बैंक लोन का ज़िक्र है।"},
"rcv_h1": {"en": "### What a legal notice is", "hi": "### कानूनी नोटिस क्या होता है"},
"rcv_h2": {"en": "### What this notice seems to say (my reading, check it)", "hi": "### यह नोटिस क्या कहता लगता है (मेरी समझ, जाँच लें)"},
"rcv_h3": {"en": "### What to do, in order", "hi": "### क्या करें, क्रम से"},
"rcv_h4": {"en": "### Draft reply (edit before sending)", "hi": "### जवाब का ड्राफ्ट (भेजने से पहले बदलें)"},
"rcv_h5": {"en": "### ⚠️ Urgent flags", "hi": "### ⚠️ तुरंत ध्यान दें"},
"rcv_from": {"en": "Sent by", "hi": "भेजने वाला"}, "rcv_amt": {"en": "Amount claimed", "hi": "माँगी गई राशि"},
"rcv_dl": {"en": "Deadline", "hi": "समय-सीमा"}, "rcv_thr": {"en": "Action threatened", "hi": "धमकाई गई कार्रवाई"},
"rcv_dl_v": {"en": "{n} days (count from the date YOU received it; write that date down)", "hi": "{n} दिन (उस तारीख से गिनें जब **आपको** मिला; वह तारीख लिख लें)"},
"rcv_unk": {"en": "not clear from what you gave me", "hi": "आपके दिए विवरण से साफ़ नहीं"},
"rcv_steps": {"en": ["Don't panic and don't ignore it: it is a warning, not a court order.",
                     "Write down the date and how you received it. Keep the envelope or email.",
                     "Read exactly what is claimed. List what is true, untrue or unclear.",
                     "Reply in writing before the deadline (draft below). Don't admit liability or promise payment yet.",
                     "Collect your documents (say **checklist** after telling me your case).",
                     "Show the notice and your reply to a lawyer; free legal aid may be available."],
              "hi": ["घबराएँ नहीं और अनदेखा भी न करें: यह चेतावनी है, अदालत का आदेश नहीं।",
                     "तारीख और मिलने का तरीका लिख लें। लिफ़ाफ़ा या ईमेल सँभालकर रखें।",
                     "ठीक से पढ़ें कि क्या दावा है। लिखें क्या सच है, क्या गलत, क्या अस्पष्ट।",
                     "समय-सीमा से पहले लिखित जवाब भेजें (नीचे ड्राफ्ट)। अभी दोष न मानें और भुगतान का वादा न करें।",
                     "अपने दस्तावेज़ इकट्ठे करें (अपना केस बताकर **checklist** लिखें)।",
                     "नोटिस और अपना जवाब वकील को दिखाएँ; मुफ़्त कानूनी सहायता मिल सकती है।"]},
"rcv_f_court": {"en": "It mentions a court, summons or a hearing: see a lawyer **immediately**; a court date has its own deadline.", "hi": "इसमें अदालत, सम्मन या सुनवाई का ज़िक्र है: **तुरंत** वकील से मिलें; अदालत की तारीख की अपनी समय-सीमा होती है।"},
"rcv_f_cheque": {"en": "It mentions a bounced cheque: this has strict timelines. See a lawyer **today**.", "hi": "इसमें बाउंस चेक का ज़िक्र है: इसमें सख़्त समय-सीमाएँ होती हैं। **आज ही** वकील से मिलें।"},
"rcv_f_crim": {"en": "It threatens police or criminal action: don't ignore it and don't reply emotionally. See a lawyer before replying.", "hi": "इसमें पुलिस या आपराधिक कार्रवाई की धमकी है: अनदेखा न करें और भावनाओं में जवाब न दें। जवाब से पहले वकील से मिलें।"},
"rcv_f_bank": {"en": "Loans and banks have special recovery rules that I do not cover. Do not ignore this; see a lawyer promptly.", "hi": "लोन और बैंक की वसूली के विशेष नियम होते हैं जो मैं कवर नहीं करता। इसे अनदेखा न करें; जल्दी वकील से मिलें।"},
"rcv_f_big": {"en": "The amount is large: get a lawyer before you reply.", "hi": "राशि बड़ी है: जवाब देने से पहले वकील से मिलें।"},
"rcv_sender": {"lawyer": {"en": "a lawyer / advocate", "hi": "वकील / एडवोकेट"}, "landlord": {"en": "a landlord", "hi": "मकान मालिक"},
               "employer": {"en": "an employer / company", "hi": "नियोक्ता / कंपनी"}, "bank": {"en": "a bank / lender", "hi": "बैंक / ऋणदाता"},
               "unknown": {"en": "not clear", "hi": "साफ़ नहीं"}},
"rcv_thr_v": {"court": {"en": "court case", "hi": "अदालती मामला"}, "criminal": {"en": "police / criminal case", "hi": "पुलिस / आपराधिक मामला"},
              "cheque": {"en": "cheque bounce case", "hi": "चेक बाउंस मामला"}},
"export_head": {"en": "Nyay Saathi: case file", "hi": "न्याय साथी: केस फ़ाइल"},
"export_none": {"en": "Nothing to export yet. Tell me about your problem first.", "hi": "अभी एक्सपोर्ट करने के लिए कुछ नहीं है। पहले अपनी समस्या बताइए।"},
"story_missing": {"en": "Information I could not find in the text (the chat tool would ask for these)", "hi": "जो जानकारी पाठ में नहीं मिली (चैट टूल ये पूछता)"},
})


PROOF_HI = {"agreement": "एग्रीमेंट / पत्र", "receipt/invoice": "रसीद / इनवॉइस", "bank/UPI record": "बैंक / UPI रिकॉर्ड",
            "chats/emails": "चैट / ईमेल", "photos/videos": "फ़ोटो / वीडियो", "payslips": "पेस्लिप"}


def proof_names(tags, lang):
    return [PROOF_HI.get(x, x) if lang == "hi" else x for x in tags]
