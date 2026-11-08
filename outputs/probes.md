# Unscripted probes (raw)

## Mixed amounts (found a bug in v1, now fixed)
**USER:** I paid 2 lakh, they returned 50k, now they owe me 1.5 lakh deposit, landlord says wait

_detected: topic=deposit, facts={}, lang=en_

**ASSISTANT (first reply):**

**Issue:** Security deposit not returned (tenant / landlord)

A few quick questions so my guidance fits your case (at most 4). _Wrong problem? Say e.g. "wrong, it's a salary problem"._

When did you vacate (or when should the deposit have come back)? e.g. 'March 2025' or '3 months ago'.

---

## Threat + deposit: emergency screen fires and the deposit problem is dropped (over-caution, kept on purpose)
**USER:** My landlord threatened to throw my stuff out unless I pay extra, and he keeps my deposit of 30000

_detected: topic=None, facts={}, lang=en_

**ASSISTANT (first reply):**

This sounds **urgent or unsafe**. Please don't rely on a chatbot.
- Danger right now: call **112**.
- Arrested, or police action against you: contact a lawyer immediately; free legal aid via NALSA **15100**.
- Do not sign anything you don't understand.

When you are safe, I can help with deposit, refund or salary problems.

---

## Out-of-scope word 'harassment' makes it refuse the in-scope salary claim too (over-refusal, known failure)
**USER:** My boss hasn't paid me since January 2026 but I also want to know if I can sue for harassment

_detected: topic=None, facts={}, lang=en_

**ASSISTANT (first reply):**

This looks like a matter I'm **not equipped to handle** (for example family, criminal, property-title, tax or cyber matters). Giving you guesses here could hurt you. Please speak to a lawyer. If money is a worry, free legal aid is available: call NALSA on **15100** or visit your District Legal Services Authority.

If you also have a deposit, refund or salary problem, tell me about that and I'll help.

---

## PG 'advance' recognised as deposit; bare number without Rs not read as amount
**USER:** PG owner is not returning my advance of 12000, I left in June 2026

_detected: topic=deposit, facts={'elapsed': 5}, lang=en_

**ASSISTANT (first reply):**

**Issue:** Security deposit not returned (tenant / landlord)

A few quick questions so my guidance fits your case (at most 4). _Wrong problem? Say e.g. "wrong, it's a salary problem"._

How much deposit is the landlord holding (in ₹)?

---

## Small consumer claim
**USER:** Zomato did not refund Rs 300 for my cancelled order yesterday

_detected: topic=refund, facts={'amount': 300}, lang=en_

**ASSISTANT (first reply):**

**Issue:** Refund / defective product or service (consumer)

A few quick questions so my guidance fits your case (at most 4). _Wrong problem? Say e.g. "wrong, it's a salary problem"._

When did you pay, or when did the problem start? e.g. 'January 2026' or '2 months ago'.

---

## Tamil input with no LLM connected: must say so honestly
**USER:** என் வீட்டு உரிமையாளர் டெபாசிட் தரவில்லை

_detected: topic=None, facts={}, lang=None_

**ASSISTANT (first reply):**

This server can handle English and Hindi offline. Punjabi translation needs Gemini enabled. Restart from the project README's Gemini steps, then check /api/health shows "llm":"gemini".

---

## Hinglish: understood, but reply is English (known limitation)
**USER:** bhai mera kiraya deposit wapas nahi mil raha, 25000 hai, 4 mahine pehle ghar chhoda

_detected: topic=deposit, facts={'elapsed': 4}, lang=hinglish_

**ASSISTANT (first reply):**

**Issue:** Security deposit not returned (tenant / landlord)

A few quick questions so my guidance fits your case (at most 4). _Wrong problem? Say e.g. "wrong, it's a salary problem"._

How much deposit is the landlord holding (in ₹)?

---
