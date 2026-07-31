# PDF → Excel Converter

Simple utility to extract tables (and fallback text) from PDFs into an Excel workbook.

Prerequisites
- Python 3.8+
- Install dependencies:

```bash
pip install -r pdf_to_excel/requirements.txt
```

Usage

```bash
python pdf_to_excel/convert_pdf_to_excel.py input.pdf [output.xlsx]
```

Options
- `--pages` — pages to process, e.g. `1,3-5`.
- `--quiet` — reduce logging.

Behavior
- The script tries to detect tabular data on each page. If tables are found, it writes a combined sheet plus one sheet per page/table.
- If no tables are found on a page, the page text is written into a simple `text` column.

Notes
- For best results with strictly tabular PDFs (bank statements, invoices), `pdfplumber` should detect tables. If extraction is poor, consider trying `camelot` or `tabula` which sometimes perform better but require extra system dependencies.
