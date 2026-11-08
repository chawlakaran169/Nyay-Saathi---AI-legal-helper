"""Labeled evaluation of problem-type detection (first message only).
Outcomes: CORRECT | SAFE (asked to clarify / referred out when it should have answered; no wrong advice) | WRONG (gave advice for the wrong problem, or advice on an out-of-scope problem).
Writes outputs/classifier_eval.json."""
import json, os, sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lawyer.engine import Session

SET = [  # (message, label)  label: deposit | refund | salary | oos
 ("landlord not returning my deposit of 30000", "deposit"),
 ("I vacated my PG last month and the owner is refusing to return my advance", "deposit"),
 ("मकान मालिक ने सिक्योरिटी डिपॉजिट वापस नहीं किया", "deposit"),
 ("mera makan malik security deposit nahi de raha", "deposit"),
 ("my flatmate and I left the flat and the broker says deposit is forfeited", "deposit"),
 ("owner deducted 20000 from my rent deposit for no reason", "deposit"),
 ("I paid 2 months rent as caution money, house owner not giving back", "deposit"),
 ("kiraya agreement khatam hua, malik paisa wapas nahi kar raha", "deposit"),
 ("tenant here, landlord says he will refund deposit after painting, 4 months passed", "deposit"),
 ("PG wale ne advance wapas nahi kiya", "deposit"),
 ("hostel warden is not returning my caution deposit", "deposit"),
 ("the shop owner I rented from won't return my security", "deposit"),
 ("Flipkart did not refund my money for the defective phone", "refund"),
 ("I cancelled my flight ticket and the airline has not refunded", "refund"),
 ("coaching institute is not refunding my fees after I left", "refund"),
 ("रिफंड नहीं मिला, ऑर्डर कैंसिल किया था", "refund"),
 ("paisa wapas nahi mil raha, seller ne kharab saman bheja", "refund"),
 ("bought a washing machine that stopped working in a week, company refuses to replace", "refund"),
 ("online course seller is not giving my money back", "refund"),
 ("Swiggy charged me twice and refused to refund", "refund"),
 ("hotel booking cancelled by them but no refund", "refund"),
 ("my gym membership fee refund is pending", "refund"),
 ("ordered a laptop with a broken screen from Amazon, they won't give refund", "refund"),
 ("company has not paid my salary for 3 months", "salary"),
 ("my employer is not giving my full and final settlement after I resigned", "salary"),
 ("तनख्वाह नहीं मिली दो महीने से", "salary"),
 ("salary nahi mil rahi, HR reply nahi kar raha", "salary"),
 ("I was terminated and they are withholding my last month pay", "salary"),
 ("contractor hasn't paid my wages for the work I did", "salary"),
 ("boss deducted half my salary without telling me", "salary"),
 ("offer letter said 40k but they paid 30k", "salary"),
 ("my internship stipend was not paid", "salary"),
 ("company is not releasing my experience letter and last salary", "salary"),
 ("I want a divorce", "oos"),
 ("my neighbour is encroaching my land", "oos"),
 ("police filed FIR against me", "oos"),
 ("how to register a trademark for my brand", "oos"),
 ("someone hacked my instagram and is blackmailing me", "oos"),
 ("my father died, how to get the will executed", "oos"),
 ("I got into a road accident, who pays", "oos"),
 ("insurance company rejected my health claim wrongly", "oos"),
 ("income tax notice for my 2022 return", "oos"),
]


HOLDOUT = [  # written AFTER tuning on SET; never used to change the rules
 ("I left my rented room in Bangalore in July and the owner is sitting on my 45000", "deposit"),
 ("ghar khali kar diya par malik ne ek paisa wapas nahi diya", "deposit"),
 ("मैंने फ्लैट छोड़ दिया लेकिन मकान मालिक डिपॉजिट के पैसे नहीं दे रहा", "deposit"),
 ("my lease ended, they say deposit adjusted against some repairs but never showed bills", "deposit"),
 ("the guesthouse I stayed in for 6 months refuses to return my refundable security amount", "deposit"),
 ("I returned a damaged speaker within 7 days but the website never credited my money", "refund"),
 ("travel agency took 80000 for a Goa package and then cancelled, no money back", "refund"),
 ("मैंने मोबाइल खरीदा था जो खराब निकला, दुकानदार पैसे वापस नहीं कर रहा", "refund"),
 ("online tutoring app deducted money twice from my card and support is ignoring me", "refund"),
 ("sofa delivered with a broken leg and the furniture store says no returns", "refund"),
 ("bhai order cancel kiya tha 15 din ho gaye refund ka koi pata nahi", "refund"),
 ("my last 2 months pay is stuck after I quit the startup", "salary"),
 ("employer says they will pay my dues next month, been saying that since March", "salary"),
 ("मेरी पिछले तीन महीने की सैलरी कंपनी ने रोक रखी है", "salary"),
 ("they cut my pay by 10000 every month and won't explain", "salary"),
 ("I am a freelancer and the client hasn't paid my invoice of 25000", "salary"),
 ("HR is delaying my full and final since I resigned in September", "salary"),
 ("my wife and I are fighting about who gets the car after separation", "oos"),
 ("a man cheated me on a bike sale and I want him arrested", "oos"),
 ("my business partner forged my signature, what to do", "oos"),
 ("builder has not given possession of my flat for 3 years", "oos"),
 ("my bank is harassing me for EMI recovery", "oos"),
 ("how do I file a patent for my invention", "oos"),
 ("school is not giving my child's transfer certificate", "oos"),
]


HOLDOUT2 = [  # FROZEN before the classifier upgrade; used once to measure it. Written to be varied and a little awkward.
 ("my landlord in Pune is sitting on 55000 of mine since I moved out in September", "deposit"),
 ("flat chhodh diya but owner deposit ka paisa lautane se mana kar raha hai", "deposit"),
 ("किराए का कमरा खाली किए 5 महीने हो गए, मालिक सिक्योरिटी नहीं लौटा रहा", "deposit"),
 ("the PG I stayed at says my caution money is gone because of 'maintenance' with no receipt", "deposit"),
 ("my tenancy ended in June and the landlord keeps making excuses about returning the security amount", "deposit"),
 ("I gave 1 lakh advance to the house owner and he refuses to give it back after I cancelled the lease", "deposit"),
 ("owner ne rent agreement ke baad jo deposit liya tha wo wapas nahi kar raha", "deposit"),
 ("the e-commerce site cancelled my order but only refunded half the amount", "refund"),
 ("I paid 12000 for a yoga retreat that was cancelled, the organiser won't give money back", "refund"),
 ("ऑनलाइन ख़रीदी घड़ी नकली निकली, कंपनी रिफंड देने से मना कर रही है", "refund"),
 ("phone screen cracked on day two, service centre says no replacement or return", "refund"),
 ("bank se nahi, dukan se liya tha fridge, kharab hai, dukandar paise nahi lauta raha", "refund"),
 ("airline cancelled my flight and has not returned my ticket money in 3 months", "refund"),
 ("the coaching centre closed down after I paid the full year fee", "refund"),
 ("my former manager says my last salary will be released 'after clearance' but 2 months have passed", "salary"),
 ("employer is not paying my wages and says business is slow", "salary"),
 ("मुझे इस महीने की तनख्वाह नहीं मिली और कंपनी जवाब नहीं दे रही", "salary"),
 ("they deducted notice period pay from my final settlement even though I served it", "salary"),
 ("my bonus and last month salary are pending since I left the job in August", "salary"),
 ("salary slip aa gayi par paisa account mein nahi aaya, 3 mahine se", "salary"),
 ("I am a delivery partner and the company hasn't paid my weekly earnings", "salary"),
 ("my sister is being harassed for dowry what do we do", "oos"),
 ("I want to challenge a traffic challan", "oos"),
 ("someone is occupying my father's house and refuses to leave", "oos"),
 ("my startup co-founder is leaving, how to split equity", "oos"),
 ("I need a lawyer for my bail", "oos"),
 ("how to get a copyright for my song", "oos"),
 ("my car insurer refuses to pay for accident damage", "oos"),
 ("आधार कार्ड में नाम सुधारना है", "oos"),
 ("mera padosi roz noise karta hai, kya kar sakta hu", "oos"),
]


def predict(msg):
    s = Session(); s.llm = None
    r = s.say(msg)
    if s.topic: return s.topic
    if "not equipped" in r: return "refer"
    if "urgent or unsafe" in r: return "emergency"
    return "ask"


def score(data):
    rows, c = [], {"CORRECT": 0, "SAFE": 0, "WRONG": 0}
    for msg, label in data:
        p = predict(msg)
        if label == "oos":
            out = "SAFE" if p in ("refer", "ask", "emergency") else "WRONG"
            out = "CORRECT" if p == "refer" else out
        else:
            out = "CORRECT" if p == label else "SAFE" if p in ("ask", "refer") else "WRONG"
        c[out] += 1
        rows.append({"message": msg, "label": label, "predicted": p, "outcome": out})
    n = len(data)
    return {"n": n, "correct": c["CORRECT"], "safe_abstain": c["SAFE"], "wrong": c["WRONG"],
           "strict_accuracy": round(c["CORRECT"] / n, 3), "wrong_rate": round(c["WRONG"] / n, 3), "rows": rows}


FIRST_RUN = {"n": 42, "correct": 35, "safe_abstain": 5, "wrong": 2, "strict_accuracy": 0.833, "wrong_rate": 0.048,
             "note": "first run on the dev set, before any vocabulary fix (recorded as it happened)"}


BASELINE2 = {"n": 30, "correct": 22, "safe_abstain": 8, "wrong": 0, "strict_accuracy": 0.733, "wrong_rate": 0.0,
             "note": "old keyword rules, measured on the frozen set before the classifier upgrade"}


def run():
    res = {"dev_first_run": FIRST_RUN, "dev_after_tuning": score(SET), "holdout": score(HOLDOUT), "holdout2": score(HOLDOUT2),
           "holdout2_baseline": BASELINE2,
           "note": "dev_after_tuning is optimistic (rules were tuned on it); holdout was written after tuning and never used to change rules."}
    json.dump(res, open(os.path.join(os.path.dirname(__file__), "..", "outputs", "classifier_eval.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return res


if __name__ == "__main__":
    r = run()
    for k in ("dev_after_tuning", "holdout", "holdout2"):
        d = r[k]
        print(f"{k}: n={d['n']} correct={d['correct']} safe-abstain={d['safe_abstain']} WRONG={d['wrong']}  strict {d['strict_accuracy']:.0%}, wrong-advice {d['wrong_rate']:.0%}")
        for x in d["rows"]:
            if x["outcome"] != "CORRECT":
                print(f"   {x['outcome']:5} label={x['label']:8} pred={x['predicted']:8} | {x['message']}")
