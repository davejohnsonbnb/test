# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT

# ---- palette ----
INK      = colors.HexColor("#1f2430")   # body text
NAVY     = colors.HexColor("#161b3a")   # header band / brand
ACCENT   = colors.HexColor("#4f46e5")   # indigo accent
ACCENT_D = colors.HexColor("#3730a3")
MUTED    = colors.HexColor("#6b7280")
LIGHT    = colors.HexColor("#eef0fb")   # table row tint
LINE     = colors.HexColor("#d9dbe9")

OUT = "/tmp/claude-0/-home-user-test/4092f1ae-1bee-5dd5-8422-1bdffd2e699f/scratchpad/Back-End-Operations-Partnership-Proposal.pdf"

styles = getSampleStyleSheet()

def S(name, **kw):
    kw.setdefault("parent", styles["Normal"])
    return ParagraphStyle(name, **kw)

body = S("body", fontName="Helvetica", fontSize=9.5, leading=14, textColor=INK, spaceAfter=5)
lede = S("lede", fontName="Helvetica", fontSize=10, leading=15, textColor=INK, spaceAfter=8)
h2   = S("h2", fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=NAVY,
         spaceBefore=12, spaceAfter=5)
bullet = S("bullet", parent=body, leftIndent=12, bulletIndent=2, spaceAfter=3)
small = S("small", fontName="Helvetica", fontSize=8, leading=11, textColor=MUTED, spaceAfter=2)
tcell = S("tcell", fontName="Helvetica", fontSize=9, leading=12, textColor=INK)
tcellb= S("tcellb", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=INK)
thcell= S("thcell", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=colors.white)

def bl(txt):
    return Paragraph(txt, bullet, bulletText="–")

# ---- page furniture ----
def header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    # top brand band
    canvas.setFillColor(NAVY)
    canvas.rect(0, h-26*mm, w, 26*mm, fill=1, stroke=0)
    canvas.setFillColor(ACCENT)
    canvas.rect(0, h-26*mm, w, 2.2*mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 17)
    canvas.drawString(18*mm, h-15*mm, "VIRTUPRO")
    canvas.setFillColor(colors.HexColor("#b9bbe0"))
    canvas.setFont("Helvetica", 8.5)
    canvas.drawString(18*mm, h-20*mm, "Back-End Operations Partner")
    canvas.setFont("Helvetica", 8.5)
    canvas.drawRightString(w-18*mm, h-20*mm, "Confidential")
    # footer
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.6)
    canvas.line(18*mm, 14*mm, w-18*mm, 14*mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(18*mm, 10*mm, "VirtuPro — Back-End Operations Partnership Proposal (Confidential)")
    canvas.drawRightString(w-18*mm, 10*mm, "Page %d" % doc.page)
    canvas.restoreState()

doc = BaseDocTemplate(OUT, pagesize=A4,
                      leftMargin=18*mm, rightMargin=18*mm,
                      topMargin=32*mm, bottomMargin=18*mm)
frame = Frame(doc.leftMargin, doc.bottomMargin,
              doc.width, doc.height, id="main")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=header_footer)])

story = []

# ---- title block ----
story.append(Paragraph("Back-End Operations Partnership Proposal", S("title",
             fontName="Helvetica-Bold", fontSize=19, leading=22, textColor=NAVY, spaceAfter=2)))
story.append(Paragraph("VirtuPro as your invisible back-end operations engine",
             S("sub", fontName="Helvetica", fontSize=10.5, leading=14, textColor=ACCENT, spaceAfter=8)))

meta = Table([[
    Paragraph("<b>Prepared for</b><br/>Sem V — Founder", tcell),
    Paragraph("<b>Partnership</b><br/>VirtuPro as back-end operations partner", tcell),
    Paragraph("<b>Date</b><br/>22 July 2026", tcell),
    Paragraph("<b>Pilot start</b><br/>Pilot unit — Binghatti Apex", tcell),
]], colWidths=[38*mm, 55*mm, 28*mm, 43*mm])
meta.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1), LIGHT),
    ("BOX",(0,0),(-1,-1),0.5,LINE),
    ("INNERGRID",(0,0),(-1,-1),0.5,colors.white),
    ("VALIGN",(0,0),(-1,-1),"TOP"),
    ("TOPPADDING",(0,0),(-1,-1),6),
    ("BOTTOMPADDING",(0,0),(-1,-1),6),
    ("LEFTPADDING",(0,0),(-1,-1),8),
    ("RIGHTPADDING",(0,0),(-1,-1),8),
]))
story.append(meta)
story.append(Spacer(1, 8))

story.append(Paragraph(
    "Thanks for a great conversation today, Sem. This sets out how VirtuPro will act as the back-end "
    "operations engine for your business — running your day-to-day operations quietly behind your brand, "
    "so owners and guests only ever see you, while we carry the operational load. It's built to scale with "
    "your pipeline, from the pilot unit to 50+ properties.", lede))

# ---- partnership model ----
story.append(Paragraph("The Partnership Model", h2))
story.append(bl("You are the client-facing brand and manager — you own the owner relationships, collect revenue, "
                "take your 15%, and pay owners."))
story.append(bl("VirtuPro is your invisible back-end team. We operate under your brand via direct account access, "
                "so nothing about the guest or owner experience points back to us."))
story.append(bl("You keep strategy, owner relationships, and dynamic pricing. We run everything operational underneath it."))

# ---- scope ----
story.append(Paragraph("Scope of Service", h2))
story.append(Paragraph("What VirtuPro handles", tcellb))
story.append(Spacer(1,2))
story.append(bl("24/7 guest communication and review management — under a 10-minute response SLA (avg 2.5–3 min)."))
story.append(bl("Cleaning &amp; maintenance scheduling — coordinating your Comfy Life cleaning and a backup vendor network."))
story.append(bl("Damage control &amp; AirCover claims — we file and manage claims to protect your owners' assets."))
story.append(bl("Listing optimization — copy, photos guidance, and content to lift conversion."))
story.append(bl("DTCM guest registration — you obtain each unit's permit; we handle all subsequent guest registrations."))
story.append(bl("Guesty PMS management — the platform our team runs fastest on."))
story.append(Spacer(1,3))
story.append(Paragraph("<b>Retained by you:</b> dynamic pricing.", body))

# ---- claims section (70/30) ----
story.append(Paragraph("Damage &amp; AirCover Claims — 70 / 30", h2))
story.append(Paragraph(
    "Claims are handled separately from the monthly management fee. On any damage or AirCover claim we "
    "recover, we work on a <b>70 / 30 basis — 70% to you, 30% to VirtuPro</b>. We only earn on claims we "
    "successfully file and recover, so our incentive is fully aligned with protecting your owners' assets.", body))

# ---- pricing ----
story.append(Paragraph("Per-Unit Pricing — Built to Scale With You", h2))
story.append(Paragraph(
    "We're waiving our standard 10-unit minimum and pricing per unit, so the partnership is viable from the "
    "pilot and rewards you as you grow. Additional units are always billed at the lower band rate — scaling "
    "only ever reduces your blended cost per unit.", body))
story.append(Spacer(1,4))

price_rows = [
    [Paragraph("Portfolio size", thcell), Paragraph("Per unit / month", thcell), Paragraph("Applies to", thcell)],
    [Paragraph("1–3 units", tcell), Paragraph("650 AED", tcellb), Paragraph("Pilot &amp; early growth (through Sep)", tcell)],
    [Paragraph("4–10 units", tcell), Paragraph("550 AED", tcellb), Paragraph("Units 4 through 10", tcell)],
    [Paragraph("11–25 units", tcell), Paragraph("450 AED", tcellb), Paragraph("Units 11 through 25", tcell)],
    [Paragraph("26+ units", tcell), Paragraph("350 AED", tcellb), Paragraph("Units 26 and beyond", tcell)],
]
pt = Table(price_rows, colWidths=[40*mm, 38*mm, 86*mm])
pt.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0), NAVY),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, LIGHT]),
    ("LINEBELOW",(0,0),(-1,-1),0.4,LINE),
    ("BOX",(0,0),(-1,-1),0.5,LINE),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("TOPPADDING",(0,0),(-1,-1),6),
    ("BOTTOMPADDING",(0,0),(-1,-1),6),
    ("LEFTPADDING",(0,0),(-1,-1),8),
]))
story.append(pt)
story.append(Spacer(1,5))

# minimum slab / options callout
slab = Table([[Paragraph(
    "<b>Minimum monthly engagement.</b> Our standard floor to run a portfolio is <b>3,000 AED / month</b>. "
    "For you we'll bring that down to <b>2,500 AED / month</b>. Alternatively, you're welcome to hold off and "
    "start with us once a few units are onboard, so the per-unit fees above stand on their own — whichever "
    "you prefer. Cleaning and maintenance are billed at cost as a pass-through (Comfy Life ~210 AED per 1-bed "
    "— Dave is negotiating a preferred rate) and are separate from the management fee.", body)]],
    colWidths=[164*mm])
slab.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,-1), LIGHT),
    ("BOX",(0,0),(-1,-1),0.8,ACCENT),
    ("LINEBEFORE",(0,0),(0,-1),3,ACCENT),
    ("TOPPADDING",(0,0),(-1,-1),8),
    ("BOTTOMPADDING",(0,0),(-1,-1),8),
    ("LEFTPADDING",(0,0),(-1,-1),10),
    ("RIGHTPADDING",(0,0),(-1,-1),10),
]))
story.append(slab)

# ---- why not in-house ----
story.append(Paragraph("Why This Beats Building It In-House", h2))
story.append(Paragraph(
    "To match our 24/7 coverage on your own, you'd be staffing <b>three 8-hour shifts</b> of in-house people. "
    "That works out to a materially <b>higher monthly cost — for less expertise</b>: you'd be paying full "
    "salaries for generalists still learning the tools, instead of tapping a trained team that already runs "
    "this operation at scale every day. With VirtuPro you get the round-the-clock coverage and the expertise, "
    "at a fraction of a three-shift payroll.", body))

# ---- growth roadmap ----
story.append(Paragraph("Your Growth Roadmap — and What It Costs", h2))
road_rows = [
    [Paragraph("Milestone", thcell), Paragraph("Units", thcell), Paragraph("Indicative monthly fee", thcell)],
    [Paragraph("Now — pilot", tcell), Paragraph("1", tcell), Paragraph("2,500 AED (minimum engagement)", tcellb)],
    [Paragraph("1 September 2026", tcell), Paragraph("3", tcell), Paragraph("2,500 AED (minimum engagement)", tcellb)],
    [Paragraph("End of 2026", tcell), Paragraph("15–20", tcell), Paragraph("~8,000–10,300 AED", tcellb)],
    [Paragraph("2027", tcell), Paragraph("~50", tcell), Paragraph("~21,000 AED", tcellb)],
]
rt = Table(road_rows, colWidths=[52*mm, 26*mm, 86*mm])
rt.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0), NAVY),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, LIGHT]),
    ("LINEBELOW",(0,0),(-1,-1),0.4,LINE),
    ("BOX",(0,0),(-1,-1),0.5,LINE),
    ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("TOPPADDING",(0,0),(-1,-1),6),
    ("BOTTOMPADDING",(0,0),(-1,-1),6),
    ("LEFTPADDING",(0,0),(-1,-1),8),
]))
story.append(rt)
story.append(Spacer(1,3))
story.append(Paragraph(
    "Indicative fees on the per-unit bands above, subject to the minimum monthly engagement while the portfolio "
    "is small. As the mix shifts to larger apartments and villas, we'll confirm any villa-specific scope together.", small))

# ---- onboarding workflow ----
story.append(Paragraph("Pilot &amp; Onboarding Workflow", h2))
ob_rows = [
    [Paragraph("Step", thcell), Paragraph("What happens", thcell), Paragraph("Owner", thcell)],
    [Paragraph("1 · Property Information Sheet", tcell),
     Paragraph("Lockbox, Wi-Fi, access, house rules and unit details captured up front", tcell),
     Paragraph("Sem", tcell)],
    [Paragraph("2 · Account access", tcell),
     Paragraph("Direct Airbnb login (not co-host) so everything stays under your brand", tcell),
     Paragraph("Sem", tcell)],
    [Paragraph("3 · PMS setup", tcell),
     Paragraph("Unit onboarded into Guesty", tcell),
     Paragraph("VirtuPro", tcell)],
    [Paragraph("4 · DTCM permit", tcell),
     Paragraph("Permit obtained per unit; we handle all guest registrations thereafter", tcell),
     Paragraph("Sem → VirtuPro", tcell)],
    [Paragraph("5 · Shared WhatsApp group", tcell),
     Paragraph("You added as admin — active during the pilot, then delegated to your admins", tcell),
     Paragraph("VirtuPro", tcell)],
    [Paragraph("6 · Go-live", tcell),
     Paragraph("Pilot unit live; we refine workflows before the September scale-up", tcell),
     Paragraph("Both", tcell)],
]
ot = Table(ob_rows, colWidths=[46*mm, 92*mm, 26*mm])
ot.setStyle(TableStyle([
    ("BACKGROUND",(0,0),(-1,0), NAVY),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white, LIGHT]),
    ("LINEBELOW",(0,0),(-1,-1),0.4,LINE),
    ("BOX",(0,0),(-1,-1),0.5,LINE),
    ("VALIGN",(0,0),(-1,-1),"TOP"),
    ("TOPPADDING",(0,0),(-1,-1),6),
    ("BOTTOMPADDING",(0,0),(-1,-1),6),
    ("LEFTPADDING",(0,0),(-1,-1),8),
]))
story.append(ot)
story.append(Spacer(1,3))
story.append(Paragraph(
    "During the pilot you stay close in the WhatsApp group to learn the workflow; we'll add approval parameters "
    "(e.g. discount ranges) to the onboarding sheet so your admins can fully delegate as you scale.", small))

# ---- closing ----
story.append(Spacer(1,10))
story.append(HRFlowable(width="100%", thickness=0.6, color=LINE, spaceAfter=8))
story.append(Paragraph(
    "We're excited to be the engine behind your growth — the same operation that runs 250 units for a group in "
    "Belgium and 67 for an operator in Dubai, working quietly behind your brand.", body))
story.append(Spacer(1,4))
story.append(Paragraph("Muneeb Wasif · CEO &amp; COO, VirtuPro · Prepared 22 July 2026", tcellb))

doc.build(story)
print("WROTE", OUT)
