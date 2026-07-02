# 📄 PDF Intelligence — Text & Table Extractor (Day 12)

**Phase 2: NLP & Text AI** — a Flask web app that reads a **multi-page PDF**,
extracts **text and tables** from every page, **cleans** the text, and returns
a structured **JSON** result. This is the exact document-ingestion step used in
resume parsers, invoice readers, and RAG (Retrieval-Augmented Generation) pipelines.

Everything lives in **one Python file** (`app.py`) with the UI in `templates/index.html`.

## 🧰 Libraries Used

| Library      | Why it's used |
|--------------|---------------|
| `flask`      | Serves the UI and the `/api/extract` JSON endpoint |
| `pypdf`      | Fast, lightweight — reads **document metadata** (title, author, page count) |
| `pdfplumber` | Layout-aware — extracts **text** and **tables** (best pure-Python option for tables) |
| `reportlab`  | Only for `make_sample_pdf.py`, which generates a test PDF |

## 📁 Project Structure

```
day12_pdf_extractor/
├── app.py                 # ⭐ single file: extraction logic + Flask server
├── templates/
│   └── index.html         # the UI (flat pastel, strong typography)
├── sample_data/
│   └── sample_report.pdf
├── requirements.txt
└── README.md
```

## 🔄 How It Works

```
Browser ──POST /api/extract (raw PDF bytes)──▶  app.py
                                                  ├── pypdf       → metadata
                                                  ├── pdfplumber  → text + tables
                                                  └── clean_text  → tidy the text
Browser ◀──────────── JSON result ◀───────────────┘
```

The same functions (`process_pdf`, `extract_pages`, `clean_text`) power the API —
one file, no imports across modules.

## 🚀 How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the Flask app
python app.py
```

Then open the live demo in your browser:

### 👉 http://127.0.0.1:5000

Drag & drop any PDF and get animated stats, per-page tabs with cleaned text and
rendered tables, a raw-JSON viewer, and one-click **Download JSON**.

## 🧹 Text-Cleaning Steps (`clean_text`)

PDFs are a *visual* format, so raw extracted text contains artifacts:

1. **Hyphenated line breaks** — `docu-\nment` → `document`
2. **Hard line breaks** inside sentences → joined with spaces
3. **Control / non-printable characters** → removed
4. **Repeated whitespace** → collapsed to a single space

## 📦 Output JSON Structure

```json
{
  "metadata": { "file_name": "...", "total_pages": 3, "title": "...", "author": "..." },
  "pages": [
    {
      "page_number": 1,
      "text": "cleaned text of the page...",
      "word_count": 51,
      "table_count": 1,
      "tables": [ [ ["header1", "header2"], ["row1col1", "row1col2"] ] ]
    }
  ],
  "summary": { "total_pages": 3, "total_words": 119, "total_tables": 2 }
}
```

## ⚠️ Limitations

- Works on **digital (text-based) PDFs**. Scanned/image PDFs need OCR
  (e.g. `pytesseract`) — a possible future extension.
- Borderless tables may not always be detected.

## 🔗 Why This Matters for AI

Every RAG pipeline starts with **document ingestion** — you can't embed or
retrieve what you can't extract. This is stage one of an AI document assistant:
next comes chunking the text, embedding it, and storing it in a vector database.
