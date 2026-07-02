import io
import re

import pdfplumber
from flask import Flask, jsonify, render_template, request
from pypdf import PdfReader

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

def clean_text(raw_text: str) -> str:
    if not raw_text:
        return ""
    text = raw_text
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)          
    text = re.sub(r"\n+", " ", text)                      
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)  
    text = re.sub(r"\s{2,}", " ", text)                  
    return text.strip()


def clean_table(table: list) -> list:
    return [
        [(cell or "").replace("\n", " ").strip() for cell in row]
        for row in table
    ]


def extract_metadata(pdf_bytes: bytes, file_name: str) -> dict:
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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/extract", methods=["POST"])
def api_extract():
    pdf_bytes = request.get_data()
    if not pdf_bytes:
        return jsonify({"error": "empty request body"}), 400
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
    app.run(host="127.0.0.1", port=5000, debug=True)
