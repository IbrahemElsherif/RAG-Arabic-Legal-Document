"""Convert the Civil Code PDF into article records (data/processed/articles.json).

Each page is a two-column table: English on the left, Arabic on the right.
One article can span several table rows and several pages.

"""

import json
import logging
from pathlib import Path

import pymupdf

from legal_rag.config import get_settings
from legal_rag.logging_config import setup_logging

logger = logging.getLogger(__name__)

# page.get_text("dict")            → a dict
#  └─ ["blocks"]                    → a list of blocks
#      └─ one block                 → a dict
#          ├─ ["type"]              → 0 means text
#          └─ ["lines"]             → a list of lines
#              └─ one line          → a dict
#                  ├─ ["bbox"]      → [x0, y0, x1, y1]   e.g. [36.1, 536.6, 284.3, 547.6]
#                  └─ ["spans"]     → a list of spans
#                      └─ one span  → a dict
#                          └─ ["text"] → "Periods of limitation will be ..."


def extract_lines(pdf_path: Path) -> list[dict]:
    """Read the PDF and return one record per non-empty text line.

    We read lines, not blocks, because some blocks (headings) span both
    columns and mix Arabic and English text.
    """
    lines = []
    with pymupdf.open(pdf_path) as doc:
        for page in doc:
            for block in page.get_text("dict")["blocks"]:
                if block["type"] != 0:  # 0 = text, 1 = image
                    continue
                for line in block["lines"]:
                    text = "".join(
                        span["text"] for span in line["spans"]
                    ).strip()  # join the text in the spane
                    x0, y0, _, _ = line["bbox"]  # get boundary box
                    if not text:
                        continue
                    lang = (
                        "ar" if x0 > 297 else "en"
                    )  # decide lang base on boundary box line dividing the data
                    lines.append({"page": page.number + 1, "y0": y0, "lang": lang, "text": text})
    return lines


def main() -> None:

    settings = get_settings()
    setup_logging(settings.log_level)
    lines = extract_lines(settings.raw_pdf_path)
    ar_stream = [line for line in lines if line["lang"] == "ar"]  # build steam based on language
    en_stream = [line for line in lines if line["lang"] == "en"]

    streams = {  # Combine the seperate streams
        "ar": ar_stream,
        "en": en_stream,
    }
    out_path = settings.corpus_path.parent / "lines.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as out:
        json.dump(streams, out, ensure_ascii=False, indent=2)
    logger.info(
        "extracted lines",
        extra={"ar": len(streams["ar"]), "en": len(streams["en"]), "path": str(out_path)},
    )


if __name__ == "__main__":
    main()
