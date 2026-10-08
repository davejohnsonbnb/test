# Airbnb Review Removal — Playbook

_Review Management · researched 2026-10-08 · sources listed at the bottom_

Use this every time we prepare an Airbnb review-removal request (a "review dispute").
Airbnb's own Help Center is the authority; where third-party guides add claims that
Airbnb does not confirm, they are marked **(unofficial)**.

---

## 1. The one rule that matters

Airbnb removes a review **only if it breaks the Reviews Policy**. It will not remove a
review because it is negative, unfair, inaccurate, or the star rating is too low, and it
"generally doesn't mediate disputes about review accuracy". Every request we write must
name **one specific policy ground** and prove it with evidence. Anything else gets
rejected.

---

## 2. How Airbnb reviews work (context for every case)

| Rule | Detail |
|---|---|
| Review window | Host and guest each have **14 days after checkout** to review. |
| Publishing | Reviews stay hidden until **both** submit or the 14 days end (effectively double-blind). |
| Editing | A reviewer can edit **until the review is published**. After that it is locked. |
| Self-removal | A reviewer can **delete their own review within 30 days** of publication. |
| Cancellations | Cancelled **before** check-in day → nobody can review. Some reservations cancelled **on/after** check-in day (from 12:00 AM listing time) → both can review. |
| Ratings | Listing rating = average of all its reviews (shown after 3 reviews). **Removed reviews are excluded** from listing and host ratings. |
| Host response | Host can post one public response; it publishes immediately and must itself follow the Reviews Policy. |
| After removal | The reviewer is emailed, and **cannot write a new review** for that reservation. |

---

## 3. Grounds that CAN get a review removed (official)

These are the categories in Airbnb's Reviews Policy (Help article 2673), with what we need
to prove each one.

### A. Irrelevant review
- **Policy:** Reviews must be about the listing reviewed and reflect **first-hand experience**
  of that reservation. Airbnb treats a review as irrelevant if the guest **never arrived**,
  or **cancelled for reasons unrelated to the listing**. A review of a home that is really
  about a separate service or experience from the same host is also irrelevant.
- **Typical cases:** no-show / never checked in; review is about Airbnb itself, the airline,
  a restaurant, a different booking, or a different property.
- **Evidence:** reservation status, check-in proof (smart-lock / access logs, message thread
  showing no arrival), cancellation record, screenshots showing the review describes
  something else.
- **Strength:** good for clear no-shows. Hosts report denials even with a clear no-show, so
  include hard proof of non-arrival.

### B. Fake review
- **Policy:** must come from (or on behalf of) someone who actually took part in a real
  reservation.
- **Evidence:** booking records showing no real stay; signs the account is linked to a
  competitor.

### C. Bias, deception, extortion, incentives, or pressure
- **Policy:** Users can't "coordinate, manipulate, extort, incentivize, or pressure" others
  to influence reviews. **A negative review can't be threatened to obtain compensation.**
  Reviews can't be traded for discounts, refunds, reciprocal reviews, or promises not to
  take action.
- **Typical case (extortion):** guest writes "refund me or I'll leave 1 star" / "a full
  refund would justify 5 stars", the host refuses, and a bad review follows.
- **What counts:** a direct threat of a negative review, or an offer of a positive one, in
  exchange for money, a refund, a discount, or a favor. A guest saying "I'm reporting this
  to Airbnb" is **not** extortion. It's an official complaint.
- **Evidence:** the threatening message **inside Airbnb Messages**. Threats made by phone,
  text, or WhatsApp are very hard to prove (community consensus). Submit the **full
  thread**, not a cropped screenshot, with the date visible.
- **Strength:** documented extortion is one of the most successful grounds.
- ⚠️ This rule binds hosts too. **Never** offer a refund, discount, or anything else in
  exchange for changing or removing a review. Doing that is itself a violation.

### D. Competition harm
- **Policy:** hosts/guests can't review listings they are **affiliated with** or **directly
  compete against**.
- **Evidence:** proof the reviewer owns, manages, or works for a competing listing.

### E. Retaliatory review
- **Policy:** a review is retaliatory only if **all three** are true:
  1. the reviewer **committed a policy violation**,
  2. they were **notified** of it (by the host or Airbnb), and
  3. they then left a **biased review because the violation was reported**.
- **Serious violations Airbnb names:** damaging the property, **overstaying**, breaking
  standard **house rules** (e.g. smoking, extra guests, pets), and an **unauthorized party
  or event**.
- **Airbnb's own example:** guest smokes in a no-smoking home. Host finds cigarette butts,
  reports it, and asks for a deep-cleaning reimbursement. Guest refuses and leaves an angry
  review. Airbnb will investigate that review.
- **Timing:** retaliatory reviews can be disputed **no matter when they were posted**
  (policy since Nov 2022).
- **Key caveat:** a review that discusses the facts or legitimacy of a **Resolution Center
  or AirCover claim is _not automatically_ retaliatory**. Timing alone isn't proof either.
- **Evidence (sequence is everything):** the house rule as published, proof of the
  violation (photos, video, noise-monitor logs, cleaner report, invoices), the warning
  message, and the report or claim. All of these should be **timestamped _before_ the review
  posted**.
- **Strength:** succeeds often when the timeline is clean and documented. Fails when the
  report came after the review.

### F. Content Policy violation
Reviews can't contain anything banned by the Content Policy (Help article 546):
1. Advertising a separate business
2. Spam / repeated disruptive content
3. Illegal content, or content promoting illegal or harmful activity
4. Sexually explicit content
5. Violent, graphic, **threatening, demeaning, insulting or harassing** content
6. **Discrimination** (violates the Nondiscrimination Policy)
7. Impersonation
8. Violating someone's rights (IP, privacy, copyright)
9. **Private information.** This includes anything that publicly discloses someone's private
   details, **including information that could identify a listing's location** (e.g. exact
   address, phone number, host's full name).

- **Strength:** slurs, threats, explicit content, and doxxing are the most reliable wins. A
  first name alone is a weak "private info" claim.

---

## 4. What will NOT get a review removed (don't waste an attempt)

Airbnb lists these explicitly:
- Disagreeing with the **star rating** alone.
- Mentions of things **outside the host's control** (e.g. noisy neighborhood, construction,
  weather, outages). Airbnb says these may still help future guests.
  _(Some blogs claim these are removable. Airbnb's own text says otherwise. Only try if
  the review also breaks another rule.)_
- **Subjective opinions** ("the kitchen is small", "beds too firm").
- Honest negative experiences, **even if we think they're exaggerated or wrong**.

→ For these, write a **public response** instead (Section 8).

---

## 5. Filing the request (step by step)

**Who can file:** the listing owner, **full-access co-hosts**, certain pro-host / team
members, and the guest on the booking. If we're filing on a client's behalf, the client
must file it or give us full-access co-host access.

**Steps (desktop):**
1. Go to the review dispute tool: `airbnb.com/resolution/review_dispute/intro` →
   **Get started**. Or use Help Center → "Remove or dispute a review" → contact us.
2. Select the review. Tip: **search using words from the review text**, not the
   reviewer's name.
3. Choose the reason that matches our single strongest ground.
4. Write the details (template in Section 7).
5. Upload supporting documents.
6. **Submit.**

**Limits and timing:**
- **Max 2 removal requests per review.** Make the first one the strongest.
- You may not be able to file again while a request is still pending.
- Decision usually comes **by email within 48 hours**. Judgment-call cases can take longer.
- No filing deadline for disputes, but file while evidence is fresh.
- **Do not upload** government IDs, health data, details about children, or criminal
  history. Airbnb says it will not consider them.
- **Don't post a public response while the dispute is pending** (unofficial, but widely
  advised).

---

## 6. Evidence. What carries weight

| Weight | Evidence |
|---|---|
| **Strongest** | Airbnb-native records: **message threads** in Airbnb Messages, Resolution Center / AirCover claims, booking details, house rules **as published on the listing** |
| **Strong** | Date-stamped photos/video (before-arrival baseline + after-checkout), smart-lock / access logs, noise-monitor logs |
| **Supporting** | Cleaner turnover reports & photos, repair invoices, cleaning receipts, police reports (serious incidents) |
| **Weak / ignored** | Our own account of events, emotional appeals, second-hand reports ("my cleaner said…"), off-platform chat screenshots |

**Sabaify angle:** our photo-checked turnover reports (time-stamped photos of the unit's
condition before and after each stay) are exactly the kind of supporting evidence that
helps retaliation and damage cases. Keep them for every turnover.

---

## 7. Writing the request

### Structure (keep it short. Facts, not feelings)
1. **One-line ground.** Name the policy violation in the first sentence.
2. **Numbered, verifiable facts.** One claim per line, with dates/times. Quote the
   house rule, the booking details and the guest's message **exactly**.
3. **Link facts to the policy.** Say which rule each fact shows was broken.
4. **Quote the offending sentence(s)** of the review.
5. **List attachments**, each with one sentence on what it shows.
6. **Close with a clear request:** "Because the review meets [ground], please remove it
   under the Reviews Policy."

**Do:** be calm, specific, chronological. **Don't:** call the guest a liar, exaggerate,
give hosting history or backstory, argue the star rating, or include sensitive personal
data.

### Template — Retaliatory review
```
Request: removal of a retaliatory review — Reservation [CODE], [listing name]

The review posted on [date] violates Airbnb's Reviews Policy on retaliatory reviews.

1. House rule (published on the listing): "[exact rule text]".
2. On [date, time] the guest [specific violation] — see attached photos/logs.
3. On [date, time] I notified the guest in Airbnb Messages (attached).
4. On [date, time] I reported it / filed Resolution Center request [ID].
5. On [date, time] — after the report — the guest posted the review, which states:
   "[quote]". This responds to the report, not to the stay.

Attachments:
- Listing house rules screenshot — shows the rule was published before booking.
- Photos dated [date] — show [violation].
- Message thread — shows the guest was notified on [date].
- Resolution Center record — shows the report preceded the review.

The guest committed a policy violation, was notified, and then left a biased review
after it was reported. Please remove it under the retaliatory-review policy.
```

### Template — Extortion / review threat
```
Request: removal of a review used for extortion — Reservation [CODE]

The guest threatened a negative review to obtain compensation, which the Reviews
Policy prohibits.

1. On [date, time] the guest wrote in Airbnb Messages: "[exact quote]".
2. On [date, time] I declined the request because [brief, factual reason].
3. On [date] the guest posted a [x]-star review stating: "[quote]".

Attachment: full Airbnb message thread (dates visible).

The review was used as leverage for a refund, then posted when the refund was declined.
Please remove it under the extortion / pressure section of the Reviews Policy.
```

### Template — Irrelevant (no-show / cancelled / off-topic)
```
Request: removal of an irrelevant review — Reservation [CODE]

The review is not based on first-hand experience of this reservation.

1. Check-in date [date]. The guest never arrived: [smart-lock log shows no entry /
   guest messaged on (date) that they would not come / reservation cancelled on (date)
   for reason: (reason unrelated to the listing)].
2. The review states: "[quote]", which describes [something they could not have
   experienced / a different service / Airbnb's platform].

Attachments: reservation status, access log, message thread.

Under the Reviews Policy, a review from a guest who never arrived (or cancelled for
reasons unrelated to the listing) is irrelevant. Please remove it.
```

### Template — Content Policy (private info / discrimination / threats)
```
Request: removal for Content Policy violation — Reservation [CODE]

The review contains [private information / discriminatory content / threatening
language], prohibited by Airbnb's Content Policy.

Offending text: "[exact quote]".
This [discloses the host's full name and the property's exact address / disparages
the host based on (protected characteristic) / threatens (…)].

Please remove the review under the Content Policy.
```

---

## 8. If the first request is denied

1. **Read the denial**: what did Airbnb say was missing?
2. **Second (final) request**: only with **new or stronger evidence** or a clearer
   argument. Don't resubmit the same text. Address exactly what the first decision missed.
3. **Escalate by phone/chat with Airbnb Support (unofficial but widely reported):** give the
   case number, quote the exact policy line, and ask for a supervisor or a different agent
   to review. Hosts report getting different outcomes from different agents.
4. **Don't spam disputes.** Repeated unfounded requests can flag the account. One host
   reports being warned after re-reporting a review Airbnb judged compliant.
5. **Last resort (US):** arbitration under Airbnb's Terms, only for serious financial harm
   (e.g. defamation). Expensive and slow. **Talk to a lawyer first.**

---

## 9. When the review stays up: public response

- Write it **for future guests**, not to the reviewer.
- **Brief, calm, factual.** Thank them, address the specific issue, and say what was fixed.
- Correct factual errors calmly ("check-in instructions were sent on [date] at [time]").
- **No** accusations you can't prove, no private details, no long defensive essays.
- Example: _"Thank you for staying. We addressed a violation of the home's no-smoking rule
  during this stay. Every guest receives the house rules before booking, and we look
  forward to hosting future guests."_
- **Dilute it:** one low review on a 4.9 average takes roughly 12–20 new 5-star stays to
  recover (unofficial estimates).

---

## 10. Prevention: set up every future dispute to win

- Keep **all guest communication in Airbnb Messages**.
- **Publish clear house rules** and restate the key ones before arrival.
- When a rule is broken: **warn in-app immediately** (naming the rule and what to fix),
  **document** (photos/video/logs), and **report or file the claim right away**. A report
  dated before the review is what makes a retaliation case.
- Take **before-and-after photos** every turnover (Sabaify checklist photos).
- If a guest hints "refund for a good review", reply calmly in-app, **don't pay**, and
  screenshot the thread.
- Never trade anything for a review.

---

## 11. Intake checklist (what to collect before we draft)

- [ ] Reservation code, listing, dates (check-in, checkout, review posted)
- [ ] Full review text and star rating (screenshot)
- [ ] Which ground applies (A–F above). Pick **one primary**.
- [ ] Full Airbnb message thread (with dates)
- [ ] Published house rules / listing description (screenshot)
- [ ] Photos / video / access logs / noise logs with timestamps
- [ ] Resolution Center / AirCover claim IDs and dates
- [ ] Cleaner turnover report and photos
- [ ] Who files (owner or full-access co-host)
- [ ] Is this attempt #1 or #2? What did any earlier denial say?

---

## 12. Open questions / conflicting claims

- **Two-attempt limit:** confirmed on Airbnb's help page ("up to two times").
- **48-hour decision:** Airbnb says "usually". Blogs report 2 days to a few weeks.
- **"Outside host's control" removals:** some blogs say yes. **Airbnb's policy says these
  generally stay up.**
- **AI triage / "conditional request" wording pushes to human review:** unverified blog
  claims.
- **Guest can edit within 48h if the host hasn't responded:** forum claim, not official.
- Enforcement "may vary by location to reflect local law".

---

## Sources

**Official (Airbnb)**
- [Reviews Policy — Help article 2673](https://www.airbnb.com/help/article/2673)
- [Review removal / Reviews policy summary — Help article 548](https://www.airbnb.com/help/article/548)
- [Reviews policy (homes, services, experiences) — Help article 3048](https://www.airbnb.com/help/article/3048)
- [Remove or dispute a review — Help article 3582](https://www.airbnb.com/help/article/3582)
- [Content Policy — Help article 546](https://www.airbnb.com/help/article/546)
- [Reviews for homes (timing) — Help article 13](https://www.airbnb.com/help/article/13)
- [Responding to reviews — Help article 32](https://www.airbnb.com/help/article/32)
- [How to handle a retaliatory review (Resource Center, Nov 2022, updated Feb 2025)](https://www.airbnb.com/resources/hosting-homes/a/how-to-handle-a-retaliatory-review-552?locale=en)
- [Airbnb Newsroom — Update on empowering Hosts (Jun 2023)](https://news.airbnb.com/an-update-on-our-work-to-empower-hosts-to-deliver-high-quality-stays/)

**Third-party guides (unofficial)**
- [Hostfully — How to get an Airbnb review removed in 2026](https://www.hostfully.com/blog/airbnb-review-removal/)
- [AirDNA — Airbnb review removal 2026](https://www.airdna.co/blog/airbnb-remove-review)
- [STR Specialist — Review disputes: what works](https://strspecialist.com/airbnb-review-disputes-what-actually-works-and-what-gets-ignored-)
- [STR Specialist — Unfair reviews guide](https://strspecialist.com/delete-that-review-the-ultimate-host-guide-to-unfair)
- [Tokeet — Retaliatory Airbnb reviews](https://blog.tokeet.com/retaliatory-airbnb-reviews/)
- [Traverse Legal — Writing an Airbnb appeal letter](https://www.traverselegal.com/blog/airbnb-appeal-letter-how-to-write/)
- [Hostaway — Airbnb reviews policy](https://www.hostaway.com/blog/airbnb-reviews-policy-how-to-remove-reviews-on-airbnb/)
- [Hospitable — Airbnb review policy](https://hospitable.com/airbnb-review-policy)
- [Nowistay — 6 grounds](https://www.nowistay.com/ressources/how-to-get-a-negative-airbnb-review-deleted)
- [Airbnb Community — Extortion policy thread](https://community.withairbnb.com/t5/Community-cafe/Airbnb-Extortion-policy/td-p/1499574)
- [Airbnb Community — Failed removal despite refund-for-review pressure](https://community.withairbnb.com/t5/Ask-about-your-listing/Airbnb-Failed-to-Remove-a-Review-Made-By-a-Guest-Who-Clearly/td-p/2086209)
