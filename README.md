# find-rpt

`find-rpt` finds a sell-side research PDF, extracts the key pages, and returns a short brief with clickable citations to a highlighted PDF copy.

## Enable The Skill

Put the `find-rpt` skill folder where your agent can discover skills.

- Codex: install it as a local skill
- Claude Code or another tool: point that tool at the skill folder, or copy the folder into its skills/plugins directory

## Configuration

The skill reads `settings.yaml` for:

- the PDF corpus location
- the helper script paths
- the bundled `.venv`

## Python Setup

Use Python 3.14.

From the skill folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -c "import fitz, pymupdf4llm, spacy, click; spacy.load('en_core_web_sm'); print('find-rpt venv ok')"
```

If you prefer, run:

```powershell
.\scripts\bootstrap_venv.ps1
```

Note: `spacy.load('en_core_web_sm')` is needed to download the smallest nlp model of the Spacy library.

## Use It

Call the skill with ticker, date, and broker, for example:

```text
find-rpt FBK.MI 2026-05-11 Goldman
```

The skill will locate the report, highlight the cited quotes in a temp PDF copy, and return the brief.

## Architecture

Three scripts try to keep the skill deterministic and token efficient:  
- `find_pdf.py` locates the report,  
- `extract_pdf_data.py` pulls only the most relevant PDF pages to stay token efficient,  
- `highlight_pdf.py` highlights citation into a PDF copy in system Temp. Clicking a citation opens that highlighted PDF inside Codex. This highlighted version is a copy and the corpus is never touched.  

3 designs choices:
- Convert the PDF pages to Markdown to ease the LLM reading 
- Output JSON format from all the python scripts (known to be well structured for LLM)
- `extract_pdf_data.py` extracts the tables from the pdf in a separate object alongside the text in JSON output. The LLM sees the table twice, once in the text in markdown, and a 2nd time in a json format. This limits number hallucination and bad understanding due to formatting.   

To guide the AI in building the skill I asked it to start from a scaffolding I put together.  
I coded the first script and only wrote a skeleton for the 2nd. While the AI wrote the highlight completly on its own.  
