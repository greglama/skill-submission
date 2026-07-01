# Find IMCD 2026-05-28 ING

> [$find-rpt](C://Users//grega//.codex//skills//find-rpt//SKILL.md) IMCD 2026-05-28 ING

<details><summary>16 previous messages</summary>

> I’ll use the `find-rpt` skill for this: it’s built specifically for locating the broker PDF, extracting cited evidence, and producing the brief. I’m going to read its instructions first, then I’ll search the configured corpus for `IMCD`, `2026-05-28`, `ING`.
>
> <details><summary>Ran a command</summary>
>
> - Ran `Get-Content -LiteralPath 'C:\Users\grega\.codex\skills\find-rpt\SKILL.md'`
>
> </details>
>
> The skill is clear: locate, extract, verify, then create highlighted citation PDFs before writing the brief. I’m checking the skill settings and helper readiness now, because the corpus path and venv are configured there rather than guessed.
>
> <details><summary>Ran 3 commands</summary>
>
> - Ran `Get-Content -LiteralPath 'C:\Users\grega\.codex\skills\find-rpt\settings.yaml'`
> - Ran `Test-Path -LiteralPath 'C:\Users\grega\.codex\skills\find-rpt\.venv\Scripts\python.exe'`
> - Ran `Get-Content -LiteralPath 'C:\Users\grega\.codex\skills\find-rpt\template.md'`
>
> </details>
>
> The venv is present, so I can use the bundled helpers directly. Next I’m running the locator with the normalized date `20260528`, then I’ll inspect the extraction packet for the actual investment message and source quotes.
>
> <details><summary>Ran a command</summary>
>
> - Ran `.venv\Scripts\python.exe scripts\find_pdf.py --corpus corpus --ticker "IMCD" --date 20260528 --broker "ING"`
> - Auto-review: approved
> - Auto-review risk: low
> - Auto-review rationale: Auto-review returned a low-risk allow decision.
>
> </details>
>
> There’s a match, with one small wrinkle: the filename is dated `20260528` but the report cover says `27 May 2026`. The title and ticker verify it is the ING Wholesale Banking IMCD note, so I’m extracting the relevant pages now.
>
> <details><summary>Ran a command</summary>
>
> - Ran `.venv\Scripts\python.exe scripts\extract_pdf_data.py --file "corpus\20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9.pdf" --top-pages 5 --lead-pages 3`
> - Auto-review: approved
> - Auto-review risk: low
> - Auto-review rationale: Auto-review returned a low-risk allow decision.
>
> </details>
>
> The extraction found the core story on pages 1 and 3, plus forecast tables. I need the old-versus-new revision table specifically, so I’m searching the PDF text for “changes”, “target”, and forecast table headings rather than relying on the truncated console packet.
>
> <details><summary>Ran 2 commands</summary>
>
> - Ran `.venv\Scripts\python.exe -c "import fitz, re; doc=fitz.open(r'corpus\20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9.pdf'); pats=['Changes','change','target price','previously','FY26F','consensus','Bloomberg'];
> for i,p in enumerate(doc,1):
>  t=p.get_text();
>  if any(x.lower() in t.lower() for x in pats):
>   hits=[]
>   for pat in pats:
>    if pat.lower() in t.lower(): hits.append(pat)
>   print('---PAGE',i,'HITS',hits); 
>   lines=t.splitlines();
>   for j,line in enumerate(lines):
>    if any(pat.lower() in line.lower() for pat in pats):
>     print('\n'.join(lines[max(0,j-3):min(len(lines),j+8)])); print('')"`
> - Auto-review: approved
> - Auto-review risk: low
> - Auto-review rationale: Auto-review returned a low-risk allow decision.
> - Ran `$env:PYTHONIOENCODING='utf-8'; .venv\Scripts\python.exe -c "import fitz; doc=fitz.open(r'corpus\20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9.pdf');
> for page in [12,13,15]:
>  print('---PAGE',page,'---'); print(doc[page-1].get_text())"`
> - Auto-review: approved
> - Auto-review risk: low
> - Auto-review rationale: Auto-review returned a low-risk allow decision.
>
> </details>
>
> I found the revision bridge: ING keeps Buy, cuts the target to EUR108 from EUR116.5, trims FY26 EBITA by 2%, and says the lower near-term base is offset by a better next-nine-months outlook. I’m burning the citation highlights into a temp PDF now, one quote at a time as required.
>
> <details><summary>Ran 3 commands</summary>
>
> - Ran `.venv\Scripts\python.exe scripts\highlight_pdf.py --source "corpus\20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9.pdf" --page 1 --quote "Nice momentum underway but will it last?"`
> - Auto-review: approved
> - Auto-review risk: low
> - Auto-review rationale: Auto-review returned a low-risk allow decision.
> - Ran `.venv\Scripts\python.exe scripts\highlight_pdf.py --source "corpus\20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9.pdf" --highlighted-pdf "C:\Users\grega\AppData\Local\Temp\find-rpt-highlights\20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9_dac169130b_highlighted.pdf" --page 1 --quote "Target price (12-mth) €108.0 (previously €116.5)"`
> - Auto-review: approved
> - Auto-review risk: low
> - Auto-review rationale: Auto-review returned a low-risk allow decision.
> - Ran `.venv\Scripts\python.exe scripts\highlight_pdf.py --source "corpus\20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9.pdf" --highlighted-pdf "C:\Users\grega\AppData\Local\Temp\find-rpt-highlights\20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9_dac169130b_highlighted.pdf" --page 3 --quote "This, separate from anything else will, in our view, brings a much-wanted relief for the chemical sector with trade flows changing, higher prices and here and there even higher volumes."`
> - Auto-review: approved
> - Auto-review risk: low
> - Auto-review rationale: Auto-review returned a low-risk allow decision.
>
> </details>
>
> The first highlights landed cleanly. I’m adding the estimate-change and valuation quotes next, then I’ll keep the final brief tight and only use claims that are directly backed by those highlights.
>
> <details><summary>Ran a command</summary>
>
> - Ran `.venv\Scripts\python.exe scripts\highlight_pdf.py --source "corpus\20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9.pdf" --highlighted-pdf "C:\Users\grega\AppData\Local\Temp\find-rpt-highlights\20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9_dac169130b_highlighted.pdf" --page 12 --quote "Compared with our previous estimates, our changes are modest; we estimate compared with our report in October “Challenges continue in 2H25” a 2% lower EBITA for FY26"`
> - Auto-review: approved
> - Auto-review risk: low
> - Auto-review rationale: Auto-review returned a low-risk allow decision.
>
> </details>
>
> One quote was too fussy for PowerShell because the report text contains curly quotation marks. I’m switching to a shorter exact snippet from the same sentence, which is cleaner for the highlighter and still supports the revision point.
>
> <details><summary>Ran 4 commands</summary>
>
> - Ran `.venv\Scripts\python.exe scripts\highlight_pdf.py --source "corpus\20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9.pdf" --highlighted-pdf "C:\Users\grega\AppData\Local\Temp\find-rpt-highlights\20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9_dac169130b_highlighted.pdf" --page 12 --quote "a 2% lower EBITA for FY26"`
> - Auto-review: approved
> - Auto-review risk: low
> - Auto-review rationale: Auto-review returned a low-risk allow decision.
> - Ran `.venv\Scripts\python.exe scripts\highlight_pdf.py --source "corpus\20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9.pdf" --highlighted-pdf "C:\Users\grega\AppData\Local\Temp\find-rpt-highlights\20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9_dac169130b_highlighted.pdf" --page 12 --quote "compensated by the better outlook for the next nine months"`
> - Auto-review: approved
> - Auto-review risk: low
> - Auto-review rationale: Auto-review returned a low-risk allow decision.
> - Ran `.venv\Scripts\python.exe scripts\highlight_pdf.py --source "corpus\20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9.pdf" --highlighted-pdf "C:\Users\grega\AppData\Local\Temp\find-rpt-highlights\20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9_dac169130b_highlighted.pdf" --page 13 --quote "for FY26 (2%) and 6% for FY27-28"`
> - Auto-review: approved
> - Auto-review risk: low
> - Auto-review rationale: Auto-review returned a low-risk allow decision.
> - Ran `.venv\Scripts\python.exe scripts\highlight_pdf.py --source "corpus\20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9.pdf" --highlighted-pdf "C:\Users\grega\AppData\Local\Temp\find-rpt-highlights\20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9_dac169130b_highlighted.pdf" --page 15 --quote "This new calculation leads to a target price of €108 from €116.5 before."`
> - Auto-review: approved
> - Auto-review risk: low
> - Auto-review rationale: Auto-review returned a low-risk allow decision.
>
> </details>
</details>

**IMCD - ING Wholesale Banking - 27 May 2026**
*Nice momentum underway but will it last?* ING maintains Buy but trims valuation: [Target price (12-mth) €108.0 (previously €116.5)](<~/AppData/Local/Temp/find-rpt-highlights/20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9_dac169130b_highlighted.pdf>) (p. 1).

**Moved**

| Item | Old | New | Delta / read |
|---|---:|---:|---|
| Target price | €116.5 | €108.0 | Lower blended valuation: [This new calculation leads to a target price of €108 from €116.5 before.](<~/AppData/Local/Temp/find-rpt-highlights/20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9_dac169130b_highlighted.pdf>) (p. 15) |
| FY26 EBITA | prior | new | [a 2% lower EBITA for FY26](<~/AppData/Local/Temp/find-rpt-highlights/20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9_dac169130b_highlighted.pdf>) (p. 12) |

**What changed and why now?**

- ING sees near-term relief from disrupted chemical trade flows: [trade flows changing, higher prices and here and there even higher volumes](<~/AppData/Local/Temp/find-rpt-highlights/20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9_dac169130b_highlighted.pdf>) (p. 3).
- The weaker FY25/FY26 start is partly [compensated by the better outlook for the next nine months](<~/AppData/Local/Temp/find-rpt-highlights/20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9_dac169130b_highlighted.pdf>) (p. 12).

**Estimate Picture**
ING is ahead of Bloomberg consensus on EBITA: [for FY26 (2%) and 6% for FY27-28](<~/AppData/Local/Temp/find-rpt-highlights/20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9_dac169130b_highlighted.pdf>) (p. 13).

**Source**
`20260528_ING Wholesale Banking_ca5c69b90fcd620e54f2cc25d9d0f7e9.pdf` | Analysts: Quirijn Mulder, Stijn Demeester | Links point to highlighted temp PDF.

> [$find-rpt](C://Users//grega//.codex//skills//find-rpt//SKILL.md) FBK.MI 20260511 Goldman Sachs

<details><summary>12 previous messages</summary>

> I’ll use the `find-rpt` skill again for this Goldman Sachs note. I’ve got the workflow loaded, so I’ll locate the `FBK.MI` report dated `20260511`, verify the ticker in the PDF, then build the brief with highlighted source links.
>
> <details><summary>Ran a command</summary>
>
> - Ran `.venv\Scripts\python.exe scripts\find_pdf.py --corpus corpus --ticker "FBK.MI" --date 20260511 --broker "Goldman Sachs"`
> - Auto-review: approved
> - Auto-review risk: low
> - Auto-review rationale: Auto-review returned a low-risk allow decision.
>
> </details>
>
> The locator found a single Goldman Sachs PDF and the title/ticker verify it as FinecoBank `FBK.MI`. I’m extracting the relevant pages now, with an eye on whether this is a management-meeting takeaway note rather than an estimate-change note.
>
> <details><summary>Ran a command</summary>
>
> - Ran `.venv\Scripts\python.exe scripts\extract_pdf_data.py --file "corpus\20260511_Goldman Sachs_056e83f8b6ec877143bb64acd780409e.pdf" --top-pages 5 --lead-pages 3`
> - Auto-review: approved
> - Auto-review risk: low
> - Auto-review rationale: The user requested locating and summarizing this report, and this is a read-only local extraction of the matched PDF with no destructive, security, or exfiltration side effects.
>
> </details>
>
> The note is indeed a management-meeting takeaway, not a model-revision piece. I’ve got the five themes and the Buy/PT details; now I’m creating the highlighted citation PDF for the key claims.
>
> <details><summary>Ran 2 commands</summary>
>
> - Ran `.venv\Scripts\python.exe scripts\highlight_pdf.py --source "corpus\20260511_Goldman Sachs_056e83f8b6ec877143bb64acd780409e.pdf" --page 1 --quote "FinecoBank SpA (FBK.MI): Management meeting takeaways"`
> - Auto-review: approved
> - Auto-review risk: low
> - Auto-review rationale: Auto-review returned a low-risk allow decision.
> - Ran `.venv\Scripts\python.exe scripts\highlight_pdf.py --source "corpus\20260511_Goldman Sachs_056e83f8b6ec877143bb64acd780409e.pdf" --highlighted-pdf "C:\Users\grega\AppData\Local\Temp\find-rpt-highlights\20260511_Goldman Sachs_056e83f8b6ec877143bb64acd780409e_62755cc570_highlighted.pdf" --page 1 --quote "management remains confident in the sustainability of net sales and client acquisition"`
> - Auto-review: approved
> - Auto-review risk: low
> - Auto-review rationale: The user requested this report brief, and the action only adds another local highlight to a temp PDF copy of the matched document with no meaningful destructive or external side effects.
>
> </details>
>
> One highlight missed because the PDF text layer splits “confident” oddly. I’m tightening the quote to a nearby exact phrase from the extracted text layer so the evidence still lands on the same claim.
>
> <details><summary>Ran a command</summary>
>
> - Ran `.venv\Scripts\python.exe scripts\highlight_pdf.py --source "corpus\20260511_Goldman Sachs_056e83f8b6ec877143bb64acd780409e.pdf" --highlighted-pdf "C:\Users\grega\AppData\Local\Temp\find-rpt-highlights\20260511_Goldman Sachs_056e83f8b6ec877143bb64acd780409e_62755cc570_highlighted.pdf" --page 1 --quote "sustainability of both net sales and client acquisition momentum"`
> - Auto-review: approved
> - Auto-review risk: low
> - Auto-review rationale: Auto-review returned a low-risk allow decision.
>
> </details>
>
> That revised quote highlighted successfully. I’m adding the remaining points around securities lending, ETFs/internalisation, and valuation.
>
> <details><summary>Ran 2 commands</summary>
>
> - Ran `.venv\Scripts\python.exe scripts\highlight_pdf.py --source "corpus\20260511_Goldman Sachs_056e83f8b6ec877143bb64acd780409e.pdf" --highlighted-pdf "C:\Users\grega\AppData\Local\Temp\find-rpt-highlights\20260511_Goldman Sachs_056e83f8b6ec877143bb64acd780409e_62755cc570_highlighted.pdf" --page 1 --quote "FBK sees securities lending as a promising opportunity where momentum continues to build"`
> - Auto-review: approved
> - Auto-review risk: low
> - Auto-review rationale: The user requested this report brief, and the action only adds another local highlight to a temporary PDF copy of the matched document with no destructive, privilege, or external data-transfer side effects.
> - Ran `.venv\Scripts\python.exe scripts\highlight_pdf.py --source "corpus\20260511_Goldman Sachs_056e83f8b6ec877143bb64acd780409e.pdf" --highlighted-pdf "C:\Users\grega\AppData\Local\Temp\find-rpt-highlights\20260511_Goldman Sachs_056e83f8b6ec877143bb64acd780409e_62755cc570_highlighted.pdf" --page 2 --quote "incremental monetisation opportunities, including participation in securities lending"`
> - Auto-review: approved
> - Auto-review risk: low
> - Auto-review rationale: Auto-review returned a low-risk allow decision.
>
> </details>
>
> The citation PDF now has the main business drivers highlighted. I’m doing the last valuation/risk highlights, then I’ll wrap the brief in the template with “no model-change disclosed” instead of inventing a revision.
>
> <details><summary>Ran 2 commands</summary>
>
> - Ran `.venv\Scripts\python.exe scripts\highlight_pdf.py --source "corpus\20260511_Goldman Sachs_056e83f8b6ec877143bb64acd780409e.pdf" --highlighted-pdf "C:\Users\grega\AppData\Local\Temp\find-rpt-highlights\20260511_Goldman Sachs_056e83f8b6ec877143bb64acd780409e_62755cc570_highlighted.pdf" --page 2 --quote "We are Buy rated on FinecoBank. Our 12-month price target of €25.0"`
> - Auto-review: approved
> - Auto-review risk: low
> - Auto-review rationale: Auto-review returned a low-risk allow decision.
> - Ran `.venv\Scripts\python.exe scripts\highlight_pdf.py --source "corpus\20260511_Goldman Sachs_056e83f8b6ec877143bb64acd780409e.pdf" --highlighted-pdf "C:\Users\grega\AppData\Local\Temp\find-rpt-highlights\20260511_Goldman Sachs_056e83f8b6ec877143bb64acd780409e_62755cc570_highlighted.pdf" --page 3 --quote "12m Price Target:€25.00"`
> - Auto-review: approved
> - Auto-review risk: low
> - Auto-review rationale: This is a user-requested, narrowly scoped local modification of a temporary highlighted PDF copy for the report brief, with no meaningful risk of data loss, service disruption, or external disclosure.
>
> </details>
</details>

**FBK.MI - Goldman Sachs - 11 May 2026**
*FinecoBank SpA (FBK.MI): Management meeting takeaways.* GS reiterates a constructive FinecoBank view after hosting management, with [We are Buy rated on FinecoBank. Our 12-month price target of €25.0](<~/AppData/Local/Temp/find-rpt-highlights/20260511_Goldman Sachs_056e83f8b6ec877143bb64acd780409e_62755cc570_highlighted.pdf>) (p. 2).

**Moved**

| Item | Old | New | Delta / read |
|---|---:|---:|---|
| Rating / PT | not disclosed | Buy / €25.00 | No explicit change table; snapshot shows [12m Price Target:€25.00](<~/AppData/Local/Temp/find-rpt-highlights/20260511_Goldman Sachs_056e83f8b6ec877143bb64acd780409e_62755cc570_highlighted.pdf>) (p. 3) |

**What changed and why now?**

- Management sounded comfortable on commercial momentum, citing [sustainability of both net sales and client acquisition momentum](<~/AppData/Local/Temp/find-rpt-highlights/20260511_Goldman Sachs_056e83f8b6ec877143bb64acd780409e_62755cc570_highlighted.pdf>) (p. 1).
- The meeting highlighted new revenue levers: [FBK sees securities lending as a promising opportunity where momentum continues to build](<~/AppData/Local/Temp/find-rpt-highlights/20260511_Goldman Sachs_056e83f8b6ec877143bb64acd780409e_62755cc570_highlighted.pdf>) (p. 1), plus ETF [incremental monetisation opportunities, including participation in securities lending](<~/AppData/Local/Temp/find-rpt-highlights/20260511_Goldman Sachs_056e83f8b6ec877143bb64acd780409e_62755cc570_highlighted.pdf>) (p. 2).

**Estimate Picture**
GS forecasts 2026E EPS of €1.12 and 2027E EPS of €1.27 in the snapshot table; the note does not disclose old estimates.

**Source**
`20260511_Goldman Sachs_056e83f8b6ec877143bb64acd780409e.pdf` | Analysts: Oliver Carruthers, Anshika Mehrotra, Tom Ferguson, Naimeh Sabourian | Links above point to highlighted temp PDF.
