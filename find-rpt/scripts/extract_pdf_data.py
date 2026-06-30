import argparse
import json
from pathlib import Path
import re
import sys

import pymupdf4llm
import spacy

FIN_KEYWORDS = {
    "eps", "ebit", "ebitda", "revenue", "sales", "margin", "profit",
    "estimate", "revision", "raise", "lower", "cut", "upgrade", "downgrade",
    "consensus", "street", "guidance", "target", "valuation", "price",
    "fy", "forecast"
}

TABLE_RE = re.compile(r"(?:^\s*\|.*\|\s*$\n?){2,}", re.M)
FY_RE = re.compile(r"\b(?:FY)?20\d{2}E?|\bFY\d{2}E?\b", re.I)
FIN_NUM_RE = re.compile(r"[-+]?\d+(?:\.\d+)?\s?(?:%|x|bp|bps|m|bn|eur|€|£|\$)?", re.I)

def md_tables_to_json(md: str):
    tables = []

    for match in TABLE_RE.finditer(md):
        lines = [l.strip() for l in match.group(0).splitlines() if "|" in l]
        rows = [
            [c.strip() for c in line.strip("|").split("|")]
            for line in lines
            if not re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", line)
        ]

        if len(rows) < 2:
            continue

        headers = rows[0]
        for row in rows[1:]:
            row = row + [""] * (len(headers) - len(row))
            tables.append(dict(zip(headers, row[:len(headers)])))

    return tables


def light_text(text: str, nlp):
    doc = nlp(text[:15000])
    return " ".join(
        t.lemma_.casefold()
        for t in doc
        if not t.is_stop
        and not t.is_punct
        and not t.is_space
        and len(t.text) > 1
    )


def page_score(raw_text: str, lite_text: str, tables: list, nlp):
    doc = nlp(raw_text)

    keyword_hits = sum(1 for k in FIN_KEYWORDS if k in lite_text)
    financial_entities = sum(
        1 for e in doc.ents
        if e.label_ in {"MONEY", "PERCENT", "CARDINAL", "QUANTITY", "DATE"}
    )

    numbers = len(FIN_NUM_RE.findall(raw_text))
    fiscal_years = len(FY_RE.findall(raw_text))

    return ( # more weight on spacy entities because regexes might miss details
        keyword_hits
        + financial_entities * 5
        + numbers
        + fiscal_years
        + min(len(tables), 50) # adding a min because markdown tables can quickly become huge
    )

def configure_stdout():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def pdf_to_llm_packet(pdf_path: str, top_pages: int = 5, lead_pages: int = 3):
    nlp = spacy.load("en_core_web_sm")

    chunks = pymupdf4llm.to_markdown(pdf_path, page_chunks=True)

    pages = []
    title = None

    for i, chunk in enumerate(chunks, start=1):
        raw = chunk.get("text", "") if isinstance(chunk, dict) else str(chunk)

        if title is None:
            heading = re.search(r"^#\s+(.+)$", raw, re.M)
            title = heading.group(1).strip() if heading else raw.strip().splitlines()[0][:120]

        tables = md_tables_to_json(raw)
        lite = light_text(raw, nlp)
        score = page_score(raw, lite, tables, nlp)

        pages.append({
            "page_num": chunk.get("metadata", {}).get("page", i) if isinstance(chunk, dict) else i,
            "score": score,
            "raw_text": raw,
            "tables": tables,
        })

    lead = pages[:max(lead_pages, 1)]
    lead_page_nums = {p["page_num"] for p in lead}
    other_pages = [p for p in pages if p["page_num"] not in lead_page_nums]

    selected_others = sorted(
        other_pages,
        key=lambda p: p["score"],
        reverse=True
    )[:max(top_pages - len(lead), 0)]

    relevant = sorted(lead + selected_others, key=lambda p: p["page_num"])

    return {
        "file_name": str(pdf_path),
        "title": title,
        "selection": {
            "lead_pages": lead_pages,
            "top_pages": top_pages,
            "selected_page_nums": [p["page_num"] for p in relevant],
        },
        "relevant_pages": [
            {
                "page_num": p["page_num"],
                "raw_text": p["raw_text"],
                "tables": p["tables"],
            }
            for p in relevant
        ],
    }

def main():
    configure_stdout()

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, type=Path)
    parser.add_argument("--top-pages", default=5, type=int, help="Total pages to return")
    parser.add_argument("--lead-pages", default=3, type=int, help="Always include the first N pages")

    args = parser.parse_args()
    packet = pdf_to_llm_packet(args.file,
                               top_pages=args.top_pages,
                               lead_pages=args.lead_pages)
    
    print(json.dumps(packet, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
