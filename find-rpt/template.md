# Brief Template

Use this template for every `/find-rpt` answer. Keep the output tight: target 120-180 words excluding the source line and any compact table.

```markdown
**{TICKER} - {BROKER} - {REPORT DATE}**
{Report title}. {One-line takeaway with the main rating/estimate/valuation message and an inline citation to the highlighted PDF plus page note.}

**Moved**

| Item | Old | New | Delta / read |
|---|---:|---:|---|
| {metric/rating/PT} | {old} | {new} | {change or short read with highlighted source quote link plus page note} |

**What changed and why now?**

- {Actual driver in plain English, not just the revision. Add a highlighted source quote link and page note.}
- {Context: preview, review, initiation, reiteration, roadshow, management meeting, event reaction, valuation call, or not stated. Add a highlighted source quote link and page note.}

**Estimate Picture**
{One sentence on old vs new, consensus/street, scenario/range, or valuation frame. Add a highlighted source quote link and page note.}

**Watch**
{Optional one short sentence only if there is a material caveat, catalyst, risk, or debate. Add a highlighted source quote link and page note.}

**Source**
{PDF filename} | Analyst(s): {names or "not visible"} | Links above point to highlighted temp PDFs.
```

Rules:

- Use no more than one table and three rows unless the user asks for detail.
- Replace unavailable fields with `not disclosed` or omit the row if it is not material.
- Do not invent consensus, old estimates, analyst names, ratings, or target prices.
- Every PDF link must use the exact absolute highlighted PDF path returned by `highlight_pdf.py`.
- Wrap Windows paths in Markdown angle brackets, for example `[exact quote](<C:\...\highlighted.pdf>) (p. 2)`.
- The linked citation text must be the exact quote highlighted in the PDF.
- Do not leave uncited factual claims about the broker's view, estimate changes, context, or valuation.
- If revisions are present but rationale is unclear, use the ambiguity escalation email draft in `SKILL.md` and stop.
