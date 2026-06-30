import argparse
import json
from pathlib import Path
import re
import unicodedata

from typing import Dict, List

import pymupdf4llm


def list_relevant_files(corpus_path:Path, date:str, broker:str) -> List[Path]:
    broker = broker.strip().casefold()
    date = date.strip().casefold()

    candidate_files = []
    for file_path in corpus_path.glob("*.pdf"):
        normalized_file_path = str(file_path).strip().casefold()

        if broker in normalized_file_path and date in normalized_file_path:
            candidate_files.append(file_path)

    return candidate_files


def read_first_page(pdf_path:str) -> Dict[str,str]:
    chunks = pymupdf4llm.to_markdown(pdf_path,
                                     use_ocr=False, # no image recognition
                                     page_chunks=True,
                                     pages=[0, 1]) # only first 2 pages
    return {
        "file":pdf_path,
        "title":chunks[0]["metadata"]["title"],
        "text":chunks[0]["text"][:3500]
    }

def normalize_str(s):
    """Normalize string for comparison.
    Convert non ascii charcter to their base version (é -> e).
    Remove punctuations and non alphanumeric characters.
    """
    s = unicodedata.normalize("NFKD", s.strip().casefold())
    s = s.encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def assess_ticker_match(first_page:Dict[str,str], ticker:str) -> bool:
    first_page_normalized = normalize_str(first_page["text"])
    title_normalized = normalize_str(first_page["title"])
    ticker_normalized = normalize_str(ticker)

    if ticker_normalized in title_normalized or ticker_normalized in first_page_normalized:
        return True
    else:
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", required=True, type=Path)
    parser.add_argument("--ticker", required=True, type=str, help="ticker as in file name")
    parser.add_argument("--date", required=True, type=str, help="Report date as YYYYMMDD")
    parser.add_argument("--broker", required=True, type=str, help="broker name as in file name")

    args = parser.parse_args()

    candidates_files = list_relevant_files(corpus_path=args.corpus,
                                           date=args.date, 
                                           broker=args.broker)
    
    files_first_pages = [read_first_page(str(path)) for path in candidates_files]

    files_matched = list(filter(lambda page:assess_ticker_match(page, args.ticker), files_first_pages))

    if len(candidates_files) == 0:
        print("No File Found. Check broker or ticker spelling?")
    
    elif len(files_matched) == 1:
        print("[MATCH FOUND]")
        print(json.dumps(files_matched[0], indent=2))
    
    else:
        print("[WARNING] !! Multiple files matched the request !!")
        print(json.dumps(files_first_pages, indent=2))

if __name__ == "__main__":
    main()
