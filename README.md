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
