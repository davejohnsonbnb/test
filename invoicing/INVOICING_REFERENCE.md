# Invoicing — Standing Reference

This session/repo is the hub for all client invoicing.

## Issuer (fixed on every invoice)
- B N B Pro Information Technology L.L.C
- TRN: 104844103200003
- 3 145 Office NO, Dubai, Dubai 25314
- +13322522342 · ahmed@virtupro.io · www.virtupro.io
- Title: "Tax Invoice" · Terms: "Due on receipt"

## Billing dates (active clients)
| Client | Billing date / cycle |
|---|---|
| Royal Vista Vacations Homes Co L.L.C | 1st of every month |
| BLUE BREEZE HOLIDAY HOMES L.L.C | 1st of every month |
| Kensington Holiday Homes Rental LLC | 1st of every month |
| Utopix Holiday Home LLC | 1st of every month |
| The IST Company FZE - LLC (Elite Nest) | 1st of every month |
| MKB LIVING Holiday Homes L.L.C. | 17th of every month |
| Noya Living Vacation Homes -LLC | 7th → 7th of every month |
| StayC Group | 7th → 7th of every month |
| One Stone (claims) | No fixed date — ad hoc, 20% success fee |

## Global pricing rule — minimum retainer slab
- **Minimum retainer: AED 3,000 (before VAT) on every invoice.**
- If (units × per-unit rate) < 3,000, add a top-up line so the subtotal reaches 3,000.
  Example: a client dropping to 5/6/9 units still pays the AED 3,000 minimum.
- VAT (where applicable, 5%) is charged on the slab-adjusted subtotal.
- Known exceptions: first-month waivers may apply per client (e.g. Noya OS240 waived);
  StayC Group is a separate USD retainer arrangement, not this AED slab.

## Workflow rule — unit counts
- **Before generating ANY invoice, Claude must ask the user for the live unit count**
  for that client/period. The user supplies the current count, and the invoice is
  built on that number. Never assume or carry over a previous period's count.

## Banking / receiving funds
- **Current:** payments received into **Wio (Dubai)** bank account.
- **Transitioning to Wise** (registration/setup in progress). Once live, all invoices
  will be received into Wise.
- Wise receiving details not yet provided — user will send them; update the invoice
  payment block at that point. (Do not guess account details.)

## Business line — Claims Management
Separate from the holiday-homes retainer invoicing.
- **Billing model: flat 20% of whatever we earn/recover for the client** (success fee).
- NO fixed retainer, NO minimum slab (the AED 3,000 slab does NOT apply here), NO VAT
  assumption until confirmed, and NO fixed invoice date — issued **ad hoc, only when the
  user says so**. User provides the recovered amount; invoice bills 20% of it.

### Claims clients
| Client | Contact | Phone | Fee |
|---|---|---|---|
| One Stone | Ali Raza | +1 (832) 398-4597 | 20% of amount earned/recovered |

## Invoice numbering policy (IN-HOUSE — resets old OS scheme)
- Old external "OS###" numbering is retired. We run our own per-client prefixes, each
  starting at 001 and incrementing by 1.
- Prefixes (★ = given by user, others proposed pending confirmation):
  | Client | Prefix | Currency |
  |---|---|---|
  | Kensington Holiday Homes Rental LLC | KHH ★ | AED |
  | Royal Vista Vacations Homes Co L.L.C | RV ★ | AED |
  | BLUE BREEZE HOLIDAY HOMES L.L.C | BBH | AED |
  | MKB LIVING Holiday Homes L.L.C. | MKB | AED |
  | The IST Company FZE - LLC (Elite Nest) | IST | AED |
  | Utopix Holiday Home LLC | UTX | AED |
  | Noya Living Vacation Homes -LLC | NOYA | AED |
  | StayC Group | STC | USD |
  | One Stone (claims) | ONE | USD |
- First invoice for each client under the new scheme = PREFIX + 001.

## Currency
- **USD:** StayC Group, One Stone (claims).
- **AED:** all other active clients.

## Tax (business now US-based) — UNDER REVIEW
- US has no VAT; only state sales tax. Services sold to foreign clients (UAE, Belgium)
  are generally NOT subject to US sales tax.
- **Default for now: NO tax line on invoices**, pending confirmation from a US CPA.
- ⚠️ Issuer block still shows UAE entity (BNB Pro IT L.L.C + UAE TRN + Dubai address).
  If the business is now a US entity, need new US legal name, US address, and EIN to
  update the invoice header. Not yet provided — keep old block until then.

## Template
- **House standard = the Noya teal template (OS241 style)** for ALL clients.
  (US Letter, Helvetica, teal #0E909A accents, header band #D6ECEE, reportlab.)
- Still need: the OS241 reference PDF (exact match) and the real logo file.

---

## Client: StayC Group
- Address: Soenenspark 1, 9051 Gent, Belgium · VAT BE0792754175
- Currency: **USD only** (no AED / no FX line)
- Tax: Zero Rated (VAT @ 0%)
- Typical lines: "E-Services — StayC" (3,000.00) and "E-Services — StayC Organisation" (2,568.00)
- Per-unit rate when billed per unit: 12.00
- Billing cycle: monthly, period "7 <month> to 7 <next month>"
- Layout: HTML template (dark header band), rendered to A4 PDF via Chromium.

## Client: SKY VACATION HOME RENTAL L.L.C  — **INACTIVE (no longer a client)**
- Address / VAT / TRN: NOT CAPTURED (uploaded invoice omitted them)
- Currency: **AED**
- Tax: Standard Rated 5% (DXB)
- Typical lines: "E-Services" @ 180.00 + "E-Services (Discounted Units)" @ 90.00
- Billing cycle: monthly, period "18 <month> to 17 <next month>"

## Client: NOYA LIVING VACATION HOMES -LLC
- Currency: **AED** · Terms: due on receipt
- Tax: VAT 5%, line tax code "SR  Standard Rated (DXB)"
- Pricing: 7 units @ AED 300 per unit per month
- **Minimum monthly charge AED 3,000 (before VAT).** If units × rate < 3,000, add a
  top-up line to reach 3,000. (Minimum was WAIVED for the first month, OS240.)
- Billing cycle: previously 15th→15th; now **7th → 7th** of every month.
- Partial periods prorated over a 30-day month (days / 30).
- Full-month steady state: 7 × 300 = 2,100 + top-up 900 = 3,000 + VAT 150 = **AED 3,150.00**.
  Same every full month until unit count exceeds 10.
- Layout: **match OS241 exactly** — US Letter, Helvetica/Helvetica-Bold; accent teal
  #0E909A (title, column heads, rule); header band fill #D6ECEE; title "Tax Invoice" 23pt
  teal; columns DATE, DESCRIPTION, TAX, QTY, RATE, AMOUNT; each line "Services" bold + period
  + grey note; totals SUBTOTAL / VAT TOTAL / TOTAL / BALANCE DUE (15pt bold); VAT SUMMARY
  table RATE, VAT, NET. Built with Python **reportlab** → `noya_invoice_template.py`.
- TODO: real logo file still needed (original PDF had a broken black box; removed).
- TODO: the reportlab template `noya_invoice_template.py` has NOT yet been rebuilt in this
  repo; to match OS241 pixel-for-pixel I need the OS241 PDF. Build + verify at next generation.
- OS241 minimum = **prorated** (AED 2,310.00), per confirmation.

---

## Client master directory (source: BNB_Clients_detial.xlsx)
All AED / UAE unless noted. "Per unit" = monthly per-unit cost.

| Client | Address | Per unit | TRN / VAT |
|---|---|---|---|
| ~~Authors Vacation Rental~~ **(INACTIVE — no longer a client)** | — | AED 300 | — |
| Royal Vista Vacations Homes Co L.L.C | Dubai Business Bay, Churchill Tower, Office 508, Dubai, UAE | AED 300 (AED 200 if ≥ 20 listings) | 104892061300003 |
| BLUE BREEZE HOLIDAY HOMES L.L.C | Mashreq Globe HQ, Umminiyat Street, Downtown Burj Khalifa Community, Dubai | AED 250 | 104611129800003 |
| Kensington Holiday Homes Rental LLC | Dubai, مبنى الديار ملك عبدالرحمن الرستامين, الوصل | Minimum slab of AED 3,000 ("we effect minimum slab of 3k") | — |
| MKB LIVING Holiday Homes L.L.C. | Al Khabeesi bldg, plot 128-246-9, Dubai, UAE | AED 300 | — |
| ~~SKY VACATION HOME RENTAL L.L.C~~ **(INACTIVE — no longer a client)** | — | AED 300 (historic; OS249 used 180 / 90) | — |
| The IST Company FZE - LLC — **known internally as "ELITE NEST"** (paperwork & invoices MUST use legal name "The IST Company FZE - LLC") | Business Centre, Sharjah Publishing City Free Zone, UAE | AED 300 | 104154605000003 |
| Utopix Holiday Home LLC | — | AED 300 | — |
| StayC Group | Soenenspark 1, 9051 Gent, Belgium | Invoice for USD 3,000 (zero-rated, USD) | BE0792754175 |

Notes / gaps:
- Addresses/TRNs blank above were blank in the source sheet.
- Noya Living is not in the sheet; its profile is captured above from the Noya brief.
- Royal Vista has a volume tier: AED 200/unit once 20+ listings are reached.
