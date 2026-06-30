---
name: find-rpt
description: Locate a sell-side research PDF by Bloomberg ticker, report date, and broker, then produce a concise analyst-style research brief with inline citations that link to temp PDF copies containing burned-in highlighted source quotes. Use when the user invokes /find-rpt or asks to retrieve, summarize, brief, or analyze a broker research report from the configured corpus using ticker/date/broker inputs.
---

# Find Report

Use this skill for `/find-rpt {ticker} {date} {broker}` requests against the configured research PDF corpus.

The task is to find the matching broker PDF, extract the most relevant pages, and write a structured brief that an analyst can read in under a minute. Work only from the matched report unless the user explicitly asks for outside research.

## Inputs

- `ticker`: Bloomberg-style ticker, for example `SAP GY`, `BP/ LN`, `SHA0 GY`.
- `date`: report date. Accept common user forms, but normalize to `YYYYMMDD` for file lookup.
- `broker`: broker name as it appears, or approximately appears, in the filename.

Read `settings.yaml` before running helpers. It defines the corpus location, bundled Python virtual environment, and helper defaults.

## First-Time Venv Setup

Use a Python version that can install and import `fitz`, `pymupdf4llm`, `spacy`, and the `en_core_web_sm` model. Python 3.14 is known to work, but it is not required if another local Python version passes the smoke test below. The helper scripts must run through the skill-local virtual environment, not system Python.

If `.venv\Scripts\python.exe` is missing, create it from the skill directory:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -c "import fitz, pymupdf4llm, spacy; spacy.load('en_core_web_sm'); print('find-rpt venv ok')"
```

Preferred Windows bootstrap:

```powershell
.\scripts\bootstrap_venv.ps1
```

If no local Python can create the venv or pass the import smoke test, stop and ask the user to install a compatible Python or restore the bundled `.venv`. If dependency installation fails because network access is unavailable, stop and ask the user to restore the bundled `.venv` or approve package installation.

## Workflow

1. Normalize the date to `YYYYMMDD` and preserve the original ticker/broker spelling for display.
2. Run the PDF locator helper to identify candidate reports by date and broker, then verify the ticker from the report content.
3. If exactly one report matches, run the extraction helper on that PDF.
4. Read the extracted packet and, if needed, inspect additional pages from the PDF for missing rationale, analyst names, estimate tables, or valuation context.
5. Select the exact source quotes that will back the brief's citations.
6. Run the highlighter helper for each quote sequentially, one command at a time. Reuse the returned highlighted PDF path for later highlights.
7. Write the brief using `template.md`.
8. Link citations to the exact absolute path of the highlighted temp PDF and add the page note in plain text.
9. If estimate revisions exist but the report does not clearly explain why, surface an analyst email draft and stop. Never send email.

## Python Helpers

Use the bundled virtual environment for all helper commands. From the skill directory, run the configured Python interpreter at `.venv\Scripts\python.exe` on Windows, or `.venv/bin/python` on Unix-like systems if the skill is copied there. The extractor configures UTF-8 output internally for Windows consoles.

Windows example:

```bash
.venv\Scripts\python.exe scripts\find_pdf.py --corpus corpus --ticker "SHA0 GY" --date 20260622 --broker "Kepler Cheuvreux"
```

Use the locator output to choose the report. On a single match, pass the returned file path to the extractor:

```bash
.venv\Scripts\python.exe scripts\extract_pdf_data.py --file "corpus/20260622_Kepler Cheuvreux_098dda895ab76d9a8e9b4c3a3408485a.pdf" --top-pages 5 --lead-pages 3
```

The extractor returns JSON with the source filename, title, selected relevant pages, selected page numbers, raw page text, and parsed Markdown tables. It always includes the first pages by default because the cover, summary table, thesis, and valuation bridge often sit there. Use the packet as context for the brief, but verify important claims against the source text.

If the locator returns multiple candidates, compare titles, first-page text, ticker/company mentions, and report context. Ask the user only if the evidence remains ambiguous.

## Highlighted Citation PDFs

Use `scripts/highlight_pdf.py` before writing the final brief. It creates a copy of the original PDF in the system temp folder and burns visible highlight rectangles onto the copied PDF. Use the returned `highlighted_pdf` path for citation links.

First citation:

```bash
.venv\Scripts\python.exe scripts\highlight_pdf.py --source "corpus/20260622_Kepler Cheuvreux_098dda895ab76d9a8e9b4c3a3408485a.pdf" --page 1 --quote "better margins"
```

Later citations in the same report should reuse the returned copy:

```bash
.venv\Scripts\python.exe scripts\highlight_pdf.py --source "corpus/20260622_Kepler Cheuvreux_098dda895ab76d9a8e9b4c3a3408485a.pdf" --highlighted-pdf "C:\Users\grega\AppData\Local\Temp\find-rpt-highlights\example_highlighted.pdf" --page 3 --quote "WACC of 9.8%"
```

Run every highlight command sequentially. Do not parallelize highlighter calls, do not start multiple commands that write to the same `--highlighted-pdf`, and do not use batch/parallel tool execution for citations from the same report. Each call opens, modifies, and saves the highlighted copy; concurrent writes can overwrite prior highlights. Wait for one helper response, confirm `status: "highlighted"`, then pass that returned `highlighted_pdf` path into the next call.

The helper first tries exact PDF search, then falls back to normalized word matching for awkward PDF text layers. If it still returns `status: "not_found"`, choose a shorter exact quote from the extracted page text and rerun. Do not link to an unhighlighted PDF for a cited claim unless highlighting fails after a reasonable retry and you say so.

## Citation Rules

- Every material claim needs an inline source link at the point of the claim.
- Link to the exact absolute path returned by the highlighter helper, not to the original corpus path.
- Use Markdown angle brackets around Windows paths: `[quoted source text](<C:\...\highlighted.pdf>) (p. 3)`.
- The linked citation text should be the exact source quote that was highlighted.
- Put the page number in adjacent text, for example `(p. 3)`.
- Prefer quotes from the exact estimate table, rationale paragraph, valuation call, context statement, or analyst attribution.
- Do not cite only a filename at the end.

Example link:

```markdown
[better margins](<C:\Users\grega\AppData\Local\Temp\find-rpt-highlights\20260622_Kepler Cheuvreux_098dda895ab76d9a8e9b4c3a3408485a_highlighted.pdf>) (p. 1)
```

## Brief Requirements

Follow `template.md` closely. Keep the final answer short: target 120-180 words excluding the source line and any compact table. The brief must include:

- Header with ticker, broker, date, title, and one-line takeaway.
- What changed: the highest-signal estimate/rating/PT revisions in one compact table or 1-2 bullets.
- Why it changed, and why now: no more than two short bullets or one tight paragraph in plain English.
- Estimate picture: one sentence on broker old vs new, vs consensus, range/scenario table, or valuation frame when available.
- Inline citations throughout.
- Analyst/source line.
- Any first-read item only if it materially changes the investment view.

Explain broker shorthand or house KPIs the first time they appear. Keep accepted finance terms such as EPS, EBIT, EBITDA, revenue, margin, consensus, and P/E if they are clear in context.

## Ambiguity Escalation

When estimate revisions are present but the rationale is unclear:

1. Say the report shows revisions, but the driver is not clearly explained.
2. Offer to draft an email to the covering analyst.
3. Auto-compose the draft in the response.
4. Identify the analyst by name from the report when possible.
5. Use `[TODO: address]` if the analyst email address is not visible.
6. Stop after showing the draft.

Never send email or include an auto-send path.

Email draft shape:

```text
To: [TODO: address]
Subject: Question on {ticker} estimate revisions in {broker} note dated {date}

Hi {Analyst Name},

I was reading your {date} note on {ticker}. I can see the revisions to {metric/year}, but I could not find a clear explanation of the underlying driver.

Could you clarify:
- What operational or accounting factor drove the revision?
- Whether the change is mainly volume, price/mix, margin, FX, M&A, tax, buyback, or another item?
- Whether this is a one-off adjustment or a change to the forward run-rate?

Best,
```

Adjust as needed with specifics (don't be too generic), but keep it short like above.
