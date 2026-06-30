import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

import fitz


def configure_stdout():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def default_highlight_path(source: Path) -> Path:
    digest = hashlib.sha1(str(source.resolve()).encode("utf-8")).hexdigest()[:10]
    temp_dir = Path(tempfile.gettempdir()) / "find-rpt-highlights"
    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir / f"{source.stem}_{digest}_highlighted.pdf"


def prepare_highlight_pdf(source: Path, highlighted_pdf: Path | None, output: Path | None) -> Path:
    target = highlighted_pdf or output or default_highlight_path(source)
    if source.resolve() == target.resolve():
        raise ValueError("highlight target must be a copy, not the source PDF")

    target.parent.mkdir(parents=True, exist_ok=True)

    if highlighted_pdf and highlighted_pdf.exists():
        return highlighted_pdf.resolve()

    shutil.copy2(source, target)
    return target.resolve()


def candidate_quotes(quote: str) -> list[str]:
    compact = " ".join(quote.split())
    candidates = [quote]
    if compact != quote:
        candidates.append(compact)
    return [c for c in candidates if c]


def normalize_text(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.casefold())


def word_rects_for_quote(page, quote: str):
    words = page.get_text("words")
    quote_tokens = [normalize_text(token) for token in quote.split()]
    quote_tokens = [token for token in quote_tokens if token]
    if not quote_tokens:
        return []

    normalized_words = [normalize_text(word[4]) for word in words]
    normalized_words = [word for word in normalized_words]

    rects = []
    token_count = len(quote_tokens)
    for start in range(0, max(len(normalized_words) - token_count + 1, 0)):
        window = normalized_words[start:start + token_count]
        if window == quote_tokens:
            rects.extend(fitz.Rect(word[:4]) for word in words[start:start + token_count])

    if rects:
        return rects

    quote_joined = "".join(quote_tokens)
    for start in range(len(normalized_words)):
        acc = ""
        current_rects = []
        for index in range(start, len(normalized_words)):
            acc += normalized_words[index]
            current_rects.append(fitz.Rect(words[index][:4]))
            if acc == quote_joined:
                return current_rects
            if not quote_joined.startswith(acc):
                break

    return []


def draw_burned_in_highlights(page, rects, color: tuple[float, float, float], opacity: float):
    for rect in rects:
        page.draw_rect(rect, color=None, fill=color, fill_opacity=opacity, overlay=True)


def add_highlights(pdf_path: Path, quote: str, page_num: int | None, color: tuple[float, float, float], opacity: float):
    doc = fitz.open(pdf_path)
    matches = []

    page_indices = [page_num - 1] if page_num else range(doc.page_count)
    for page_index in page_indices:
        if page_index < 0 or page_index >= doc.page_count:
            continue

        page = doc[page_index]
        rects = []
        matched_quote = None
        match_method = None
        for candidate in candidate_quotes(quote):
            rects = page.search_for(candidate)
            if rects:
                matched_quote = candidate
                match_method = "search"
                break

        if not rects:
            rects = word_rects_for_quote(page, quote)
            if rects:
                matched_quote = quote
                match_method = "word_fuzzy"

        if rects:
            draw_burned_in_highlights(page, rects, color, opacity)
            matches.append({
                "page": page_index + 1,
                "match_count": len(rects),
                "matched_quote": matched_quote,
                "match_method": match_method,
            })

    if matches:
        doc.saveIncr()
    doc.close()
    return matches


def main():
    configure_stdout()

    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path, help="Original PDF path")
    parser.add_argument("--quote", required=True, help="Exact citation text to highlight")
    parser.add_argument("--page", type=int, help="1-based page number to search")
    parser.add_argument("--highlighted-pdf", type=Path, help="Existing highlighted copy to reuse and modify")
    parser.add_argument("--output", type=Path, help="Path for a new highlighted copy")
    parser.add_argument("--color", default="1,1,0", help="RGB highlight color as floats, default yellow")
    parser.add_argument("--opacity", default=0.35, type=float, help="Burned-in rectangle opacity")

    args = parser.parse_args()
    color = tuple(float(part) for part in args.color.split(","))
    if len(color) != 3:
        raise ValueError("--color must contain three comma-separated RGB floats")

    source = args.source.resolve()
    if not source.exists():
        raise FileNotFoundError(source)

    highlighted_pdf = prepare_highlight_pdf(source, args.highlighted_pdf, args.output)
    matches = add_highlights(highlighted_pdf, args.quote, args.page, color, args.opacity)

    result = {
        "source_pdf": str(source),
        "highlighted_pdf": str(highlighted_pdf),
        "markdown_link_target": str(highlighted_pdf),
        "quote": args.quote,
        "page_requested": args.page,
        "matches": matches,
        "rendering": "burned_in_rectangles",
        "status": "highlighted" if matches else "not_found",
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
