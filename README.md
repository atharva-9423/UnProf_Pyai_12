<!--
  ┌─────────────────────────────────────────────────────────────┐
  │  BEFORE PUSHING, replace these 3 placeholders everywhere:     │
  │    1. YOUR_LIVE_DEMO_URL   → your deployed app link           │
  │    2. YOUR_USERNAME        → your GitHub username             │
  │    3. (repo is assumed to be "unprof")                        │
  └─────────────────────────────────────────────────────────────┘
-->

<div align="center">

# 📄 PDF Intelligence

### Turn any PDF into clean, structured data — text, tables & metadata as JSON.

<em>Phase 2 · NLP &amp; Text AI · Day 12 — the document-ingestion step behind resume parsers, invoice readers &amp; RAG pipelines.</em>

<br/>

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-Open_App-6C5CE7?style=for-the-badge)](YOUR_LIVE_DEMO_URL)
&nbsp;
[![Made with Python](https://img.shields.io/badge/Made_with-Python-1A1A1A?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

<br/>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)
![pdfplumber](https://img.shields.io/badge/pdfplumber-0.11-BFE8D4?labelColor=1A1A1A)
![pypdf](https://img.shields.io/badge/pypdf-6.0-DCD6F7?labelColor=1A1A1A)
![Frontend](https://img.shields.io/badge/Frontend-Vanilla_JS-FFD9C7?labelColor=1A1A1A)
![License](https://img.shields.io/badge/License-MIT-CDE6F7?labelColor=1A1A1A)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-FFE8A3?labelColor=1A1A1A)

</div>

---

## ✨ Overview

**PDF Intelligence** is a single-file **Flask** web app that reads a multi-page PDF and
extracts everything useful from it:

- 📝 **Text** from every page — cleaned of PDF artifacts (broken hyphens, stray line breaks)
- 📊 **Tables** — reconstructed as real rows &amp; columns
- 🏷️ **Metadata** — title, author, page count
- 💾 **JSON** — one structured file, ready for the next stage of an AI pipeline

Drag a PDF into the browser and get animated stats, per-page tabs, and a one-click JSON download.

<div align="center">

<!-- 📸 Add a screenshot: drop a PNG next to this file and rename below -->
<img src="screenshot.png" alt="PDF Intelligence UI" width="720"/>

<sub><em>Flat pastel UI · strong typography · zero frameworks on the frontend.</em></sub>

</div>

---

## 🎯 Features

| | Feature | Detail |
|---|---|---|
| 📄 | **Multi-page reading** | Iterates every page, no page-count limit |
| 📝 | **Smart text cleaning** | De-hyphenates wrapped words, strips control chars, collapses whitespace |
| 📊 | **Table extraction** | Layout-aware detection via `pdfplumber` |
| 🏷️ | **Metadata** | Title, author, creator, total pages via `pypdf` |
| 🖱️ | **Drag &amp; drop UI** | Upload by drop or click — processed in-memory, nothing hits disk |
| 📈 | **Animated stats** | Live count-up of pages / words / tables / processing time |
| 💾 | **JSON export** | Download button + raw-JSON viewer |
| 🛡️ | **Input validation** | Checks `%PDF` magic bytes &amp; 50 MB size cap before parsing |

---

## 🧰 Tech Stack

| Layer | Tool | Why |
|-------|------|-----|
| **Web server** | `Flask` | Serves the UI + `/api/extract` JSON endpoint |
| **Metadata** | `pypdf` | Fast, lightweight — title / author / page count |
| **Text &amp; tables** | `pdfplumber` | Best pure-Python option for layout-aware tables |
| **Frontend** | Vanilla HTML/CSS/JS | No build step, no framework — one file |
| **Test data** | `reportlab` | Generates the sample PDF |

---

## 🏗️ How It Works

```mermaid
flowchart LR
    A([📄 PDF Upload]) -->|raw bytes| B{{"Flask · /api/extract"}}
    B --> C[["🧠 process_pdf()"]]
    C --> D["pypdf<br/>metadata"]
    C --> E["pdfplumber<br/>text + tables"]
    E --> F["🧹 clean_text()"]
    D --> G[("📦 JSON result")]
    F --> G
    G -->|render| H([📊 UI: stats · tabs · tables])

    style A fill:#BFE8D4,stroke:#1A1A1A,stroke-width:2px
    style B fill:#DCD6F7,stroke:#1A1A1A,stroke-width:2px
    style C fill:#FFE8A3,stroke:#1A1A1A,stroke-width:2px
    style G fill:#FFD9C7,stroke:#1A1A1A,stroke-width:2px
    style H fill:#CDE6F7,stroke:#1A1A1A,stroke-width:2px
```

### Request lifecycle

```mermaid
sequenceDiagram
    participant U as 🧑 Browser
    participant F as 🌐 Flask (app.py)
    participant P as 📚 pypdf + pdfplumber

    U->>F: POST /api/extract (raw PDF bytes)
    F->>F: validate %PDF magic bytes + size
    F->>P: read from io.BytesIO (in-memory, no temp file)
    P-->>F: metadata + per-page text & tables
    F->>F: clean_text() · build summary
    F-->>U: 200 · structured JSON
    U->>U: render stats, page tabs, tables
```

---

## 📁 Project Structure

```
day12_pdf_extractor/
├── app.py                 ⭐ single file: extraction logic + Flask server
├── templates/
│   └── index.html         🎨 the UI (flat pastel, strong typography)
├── make_sample_pdf.py     🧪 generates a 3-page sample PDF for testing
├── sample_data/
│   └── sample_report.pdf
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/unprof.git
cd unprof/day12_pdf_extractor

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) generate a sample PDF to test with
python make_sample_pdf.py

# 4. Run the app
python app.py
```

Then open 👉 **http://127.0.0.1:5000** and drop in a PDF.

> 🌍 **Live demo:** [YOUR_LIVE_DEMO_URL](YOUR_LIVE_DEMO_URL)

---

## 🔌 API Reference

| Method | Route | Body | Returns |
|--------|-------|------|---------|
| `GET`  | `/` | — | The web UI (HTML) |
| `POST` | `/api/extract` | Raw PDF bytes (`Content-Type: application/pdf`) | Extraction JSON |

**Example — cURL:**

```bash
curl -X POST http://127.0.0.1:5000/api/extract \
     -H "Content-Type: application/pdf" \
     -H "X-Filename: report.pdf" \
     --data-binary @sample_data/sample_report.pdf
```

**Response shape:**

```json
{
  "metadata": {
    "file_name": "report.pdf",
    "total_pages": 3,
    "title": "Quarterly Report",
    "author": "...",
    "creator": "..."
  },
  "pages": [
    {
      "page_number": 1,
      "text": "cleaned text of the page...",
      "word_count": 51,
      "table_count": 1,
      "tables": [
        [ ["Region", "Q1", "Q2"], ["North America", "1,240", "1,510"] ]
      ]
    }
  ],
  "summary": { "total_pages": 3, "total_words": 119, "total_tables": 2 }
}
```

---

## 🧹 Text Cleaning — why it's needed

PDFs store *where glyphs are painted*, not sentences — so raw extraction is messy.
`clean_text()` fixes four common artifacts:

| # | Problem | Example | Fix |
|---|---------|---------|-----|
| 1 | Hyphenated wrap | `docu-⏎ment` | `document` |
| 2 | Hard line breaks | `line1⏎line2` | `line1 line2` |
| 3 | Control chars | `\x0c`, `\x07` | removed |
| 4 | Repeated spaces | `a·····b` | `a b` |

---

## 🗺️ Roadmap

- [x] Multi-page text extraction
- [x] Table extraction
- [x] Text cleaning
- [x] JSON export
- [x] Flask web UI
- [x] Live deployment
- [ ] OCR for scanned PDFs (`pytesseract`)
- [ ] Batch upload (multiple PDFs)
- [ ] Chunk + embed → vector DB (RAG stage 2)

---

## 🧠 Why This Matters for AI

> Every **RAG (Retrieval-Augmented Generation)** pipeline starts with **document ingestion** —
> you can't embed or retrieve what you can't extract.

This project is **stage one** of an AI document assistant. The `pages[].text` field it
produces is exactly what gets **chunked → embedded → stored in a vector database** in the
next phase of the internship. 🚀

```mermaid
flowchart LR
    A["📄 PDF"] --> B["📝 Extract<br/>(this project)"]
    B --> C["✂️ Chunk"]
    C --> D["🔢 Embed"]
    D --> E["🗄️ Vector DB"]
    E --> F["🤖 Retrieve + Generate"]

    style B fill:#BFE8D4,stroke:#1A1A1A,stroke-width:2px
```

---

<div align="center">

### 🛠️ Built during Phase 2 · Day 12 of my Python &amp; AI internship

**Libraries:** `flask` · `pdfplumber` · `pypdf`

⭐ Star this repo if it helped you!

<br/>

![Made with love](https://img.shields.io/badge/Made_with-☕_&_curiosity-FFD9C7?labelColor=1A1A1A&style=for-the-badge)

</div>
