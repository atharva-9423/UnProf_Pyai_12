"""
app.py — PDF Text Extractor (Day 12) as a single Flask app
==========================================================
Everything in ONE file: the PDF extraction logic + the web server.

Libraries and WHY:
- pypdf       -> fast, lightweight; used for document METADATA (title, author, pages)
- pdfplumber  -> layout-aware; used for TEXT and TABLE extraction
- flask       -> serves the UI (templates/index.html) and a JSON API endpoint

Routes:
- GET  /             -> renders templates/index.html (the UI)
- POST /api/extract  -> receives raw PDF bytes, returns the extraction as JSON

Run:
    pip install -r requirements.txt
    python app.py
    # then open  http://127.0.0.1:5000
"""

import io
import re

import pdfplumber
from flask import Flask, jsonify, render_template, request
from pypdf import PdfReader

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # reject uploads over 50 MB


# ======================================================================
#  PDF EXTRACTION LOGIC
#  We read the PDF straight from an in-memory bytes stream (io.BytesIO)
#  instead of writing a temp file. This is faster AND avoids a Windows
#  bug where an open temp file is locked and can't be reopened by path.
# ======================================================================
def clean_text(raw_text: str) -> str:
    """
    Clean extracted PDF text. PDFs are a *visual* format, so raw text often
    contains artifacts:
    - hyphenated line breaks:  "docu-\nment" -> "document"
    - hard line breaks inside sentences -> joined into one line
    - repeated spaces / tabs -> single space
    - non-printable control characters -> removed
    """
    if not raw_text:
        return ""
    text = raw_text
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)          # 1. de-hyphenate wrapped words
    text = re.sub(r"\n+", " ", text)                       # 2. newlines -> spaces
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)  # 3. strip control chars
    text = re.sub(r"\s{2,}", " ", text)                    # 4. collapse whitespace
    return text.strip()


def clean_table(table: list) -> list:
    """Normalize a pdfplumber table: None cells -> '', strip stray newlines."""
    return [
        [(cell or "").replace("\n", " ").strip() for cell in row]
        for row in table
    ]


def extract_metadata(pdf_bytes: bytes, file_name: str) -> dict:
    """Read document-level info with pypdf (fast, no layout analysis)."""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    meta = reader.metadata or {}
    return {
        "file_name": file_name,
        "total_pages": len(reader.pages),
        "title": meta.get("/Title"),
        "author": meta.get("/Author"),
        "creator": meta.get("/Creator"),
    }


def extract_pages(pdf_bytes: bytes) -> list:
    """Walk every page with pdfplumber, pulling cleaned text and any tables."""
    pages_data = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = clean_text(page.extract_text() or "")
            tables = [clean_table(t) for t in page.extract_tables()]
            pages_data.append({
                "page_number": page_number,
                "text": text,
                "word_count": len(text.split()),
                "table_count": len(tables),
                "tables": tables,
            })
    return pages_data


def process_pdf(pdf_bytes: bytes, file_name: str = "uploaded.pdf") -> dict:
    """Run the full pipeline and return one structured dict (ready for JSON)."""
    result = {
        "metadata": extract_metadata(pdf_bytes, file_name),
        "pages": extract_pages(pdf_bytes),
    }
    result["summary"] = {
        "total_pages": result["metadata"]["total_pages"],
        "total_words": sum(p["word_count"] for p in result["pages"]),
        "total_tables": sum(p["table_count"] for p in result["pages"]),
    }
    return result


# ======================================================================
#  WEB ROUTES
# ======================================================================
@app.route("/")
def index():
    """Serve the single-page UI."""
    return render_template("index.html")


@app.route("/api/extract", methods=["POST"])
def api_extract():
    """Receive raw PDF bytes in the request body, return extraction JSON."""
    pdf_bytes = request.get_data()
    if not pdf_bytes:
        return jsonify({"error": "empty request body"}), 400
    # %PDF magic bytes — reject non-PDF uploads before parsing
    if not pdf_bytes.startswith(b"%PDF"):
        return jsonify({"error": "that file is not a valid PDF"}), 400

    file_name = request.headers.get("X-Filename", "uploaded.pdf")
    try:
        result = process_pdf(pdf_bytes, file_name=file_name)
        return jsonify(result)
    except Exception as exc:
        app.logger.exception("extraction failed")
        return jsonify({"error": f"failed to process the PDF: {exc}"}), 500


if __name__ == "__main__":
    # debug=True gives auto-reload + helpful error pages while developing
    app.run(host="127.0.0.1", port=5000, debug=True)
