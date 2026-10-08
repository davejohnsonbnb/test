# Invoice Ledger

System of record for all BNB Pro invoicing. Numbering is **per-client** (sequences
may overlap across clients). Keep this updated on every issue and every payment.

Status legend: **Issued** (sent, awaiting payment) · **Paid** · **Draft** (not yet issued).
Terms are "due on receipt" unless noted, so anything Issued and unpaid is Outstanding.

## StayC Group — USD, Zero Rated (0%)
| Invoice | Period | Issue date | Subtotal | VAT | Total | Status | Paid date |
|---|---|---|---|---|---|---|---|
| OS242 | 7 Jul–7 Aug 2026 | 07/07/2026 | 3,000.00 | 0.00 | USD 3,000.00 | Issued (legacy) | — |
| OS243 | 7 Aug–7 Sep 2026 | 07/08/2026 | 5,568.00 | 0.00 | USD 5,568.00 | Issued | — |
| OS244 | 7 Sep–7 Oct 2026 | 07/09/2026 | 5,568.00 | 0.00 | USD 5,568.00 | Issued | — |

## SKY Vacation Home Rental L.L.C — AED, Standard Rated 5% (DXB)
| Invoice | Period | Issue date | Subtotal | VAT | Total | Status | Paid date |
|---|---|---|---|---|---|---|---|
| OS249 | 18 Aug–17 Sep 2026 | — | 9,360.00 | 468.00 | AED 9,828.00 | Issued (original) | — |
| OS249* | 18 Aug–17 Sep 2026 | — | 7,929.00 | 396.45 | AED 8,325.45 | Draft edit (33@180 −15%, 32@90) | — |

> ⚠️ Two versions of OS249 exist — confirm which was actually sent to the client.
> Also: master sheet lists SKY per-unit at AED 300, but OS249 used 180/90 — reconcile.

## Noya Living Vacation Homes -LLC — AED, Standard Rated 5% (DXB)
Per-client sequence. Min AED 3,000/month before VAT (waived month 1). Cycle now 7th→7th.
| Invoice | Period | Issue date | Subtotal | VAT | Total | Status | Paid date |
|---|---|---|---|---|---|---|---|
| OS240 | 15 Aug–15 Sep 2026 | — | 2,100.00 | 105.00 | AED 2,205.00 | Issued (min waived) | — |
| OS241 | 15 Sep–7 Oct 2026 (22d) | 09/30/2026 | 2,200.00 | 110.00 | AED 2,310.00 | Issued (prorated min) | — |
| OS242 | 7 Oct–7 Nov 2026 | — | 3,000.00 | 150.00 | AED 3,150.00 | Draft (not issued) | — |

## Cash-flow snapshot (outstanding = Issued & unpaid)
Payment status not yet provided for any invoice — all Issued invoices are currently
treated as Outstanding. Update "Paid date" as payments arrive to keep this accurate.

| Currency | Outstanding (Issued, unpaid) |
|---|---|
| USD | 3,000 + 5,568 + 5,568 = **USD 14,136.00** |
| AED (SKY) | OS249 — confirm which version (9,828.00 or 8,325.45) |
| AED (Noya) | 2,205.00 + 2,310.00 = **AED 4,515.00** |
