#!/usr/bin/env python3
"""Convert PDF tables to Excel.

Tries to extract tables using pdfplumber. If no structured tables are found,
falls back to extracting page text into a single-column sheet.
"""
import argparse
import os
import sys
import logging

import pandas as pd

try:
    import pdfplumber
except Exception as e:  # pragma: no cover - helpful error message
    print("Missing dependency: pdfplumber. Install from requirements.txt")
    raise


def extract_tables(pdf_path, pages=None):
    dfs = []
    try:
        open_kwargs = {}
        # password passed through from caller (set on function attribute if provided)
        password = getattr(extract_tables, "password", None)
        if password:
            open_kwargs['password'] = password
        with pdfplumber.open(pdf_path, **open_kwargs) as pdf:
            total = len(pdf.pages)
            page_idxs = range(total) if pages is None else [p - 1 for p in pages if 1 <= p <= total]
            # Define multiple table-detection presets to try when default extraction fails
            presets = {
                'default': None,
                'vertical_lines': {
                    'vertical_strategy': 'lines',
                    'horizontal_strategy': 'text',
                    'intersection_tolerance': 5,
                },
                'text_snap': {
                    'vertical_strategy': 'text',
                    'horizontal_strategy': 'text',
                    'snap_tolerance': 3,
                },
                'explicit_intersection': {
                    'vertical_strategy': 'lines',
                    'horizontal_strategy': 'lines',
                    'intersection_tolerance': 2,
                },
            }

            for pi in page_idxs:
                page = pdf.pages[pi]
                page_no = pi + 1
                logging.debug('Processing page %s', page_no)

                found_any = False
                # Try each preset and tag results with strategy name
                for strategy_name, settings in presets.items():
                    try:
                        if settings is None:
                            tables = page.extract_tables()
                        else:
                            tables = page.extract_tables(table_settings=settings)
                    except Exception:
                        tables = []

                    if tables:
                        found_any = True
                        for ti, table in enumerate(tables, start=1):
                            if not table:
                                continue
                            header = table[0]
                            rows = table[1:]
                            try:
                                df = pd.DataFrame(rows, columns=header)
                            except Exception:
                                df = pd.DataFrame(table)
                            df['_source_page'] = page_no
                            df['_table_index'] = ti
                            df['_strategy'] = strategy_name
                            dfs.append(df)

                if not found_any:
                    # fallback: add plain text as one column
                    text = page.extract_text() or ''
                    lines = [l.strip() for l in text.splitlines() if l.strip()]
                    if lines:
                        df = pd.DataFrame({'text': lines})
                        df['_source_page'] = page_no
                        df['_table_index'] = 0
                        df['_strategy'] = 'text_fallback'
                        dfs.append(df)
    except pdfplumber.utils.exceptions.PdfminerException as e:
        # Common cause: PDF is password protected
        msg = str(e)
        if 'PDFPasswordIncorrect' in msg or 'password' in msg.lower():
            raise RuntimeError('PDF appears to be password-protected or requires a password. Re-run with --password <pw> or decrypt the PDF before processing.')
        raise
    return dfs


def write_excel(dfs, out_path):
    if not dfs:
        raise ValueError('No tables or text found in PDF.')
    # Ensure each dataframe has unique column names to avoid pandas concat errors
    def make_unique(cols):
        seen = {}
        out = []
        for c in cols:
            c = str(c) if c is not None else ''
            if c in seen:
                seen[c] += 1
                new = f"{c}_{seen[c]}"
            else:
                seen[c] = 0
                new = c
            out.append(new)
        return out

    clean_dfs = []
    for df in dfs:
        df = df.copy()
        df.columns = make_unique(df.columns)
        clean_dfs.append(df)

    # Concatenate tables with possibly different columns
    try:
        combined = pd.concat(clean_dfs, ignore_index=True, sort=False)
    except Exception as e:
        raise RuntimeError(f'Failed to concatenate extracted tables: {e}')
    # Write combined sheet and also separate sheets per page-table for easier review
    with pd.ExcelWriter(out_path, engine='openpyxl') as writer:
        combined.to_excel(writer, sheet_name='Combined', index=False)
        # write each unique (page,table) as separate sheet
        for (p, t), grp in combined.groupby(['_source_page', '_table_index']):
            sheet_name = f'p{p}_t{t}'
            # Excel sheet names max length 31
            sheet_name = sheet_name[:31]
            grp.to_excel(writer, sheet_name=sheet_name, index=False)


def parse_pages_arg(pages_str):
    if not pages_str:
        return None
    pages = []
    for part in pages_str.split(','):
        part = part.strip()
        if '-' in part:
            a, b = part.split('-', 1)
            pages.extend(range(int(a), int(b) + 1))
        else:
            pages.append(int(part))
    return sorted(set(pages))


def main():
    parser = argparse.ArgumentParser(description='Convert PDF tables to Excel')
    parser.add_argument('pdf', help='Input PDF file')
    parser.add_argument('out', nargs='?', help='Output XLSX file (optional)')
    parser.add_argument('--pages', help='Pages to process (e.g. 1,3-5)')
    parser.add_argument('--password', help='Password for encrypted PDF (if any)')
    parser.add_argument('--quiet', action='store_true')
    args = parser.parse_args()

    logging.basicConfig(level=logging.WARNING if args.quiet else logging.INFO,
                        format='%(levelname)s: %(message)s')

    pdf_path = args.pdf
    if not os.path.exists(pdf_path):
        logging.error('PDF not found: %s', pdf_path)
        sys.exit(2)

    out_path = args.out or os.path.splitext(pdf_path)[0] + '.xlsx'

    pages = parse_pages_arg(args.pages)
    logging.info('Reading PDF: %s', pdf_path)
    # attach password to the extractor function so it can be used when opening
    if args.password:
        setattr(extract_tables, 'password', args.password)
    dfs = extract_tables(pdf_path, pages=pages)
    if not dfs:
        logging.error('No tables or text extracted from PDF.')
        sys.exit(3)
    logging.info('Writing Excel: %s', out_path)
    write_excel(dfs, out_path)
    logging.info('Done.')


if __name__ == '__main__':
    main()
