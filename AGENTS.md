# AGENTS.md

## Cursor Cloud specific instructions

This is a Python CLI toolkit (no web services/databases/Docker). It converts Markdown slides into styled PDFs for Youzan (有赞) sales presentations.

### Scripts overview

All scripts live in `scripts/`. See `README.md` and `SKILL.md` for full usage.

- `generate_pdf.py` — main entry point (Markdown → PDF), auto-selects best method (weasyprint → Playwright → reportlab fallback)
- `md_to_html.py` — Markdown → styled HTML
- `html_to_pdf.py` — HTML → PDF (via weasyprint or Playwright)
- `md_to_pdf.py` — Markdown → PDF directly via reportlab
- `extract_pdf_structure.py` — PDF → structured JSON
- `extract_pdf.py` — PDF → plain text

### Running

```bash
pip install -r requirements.txt
python scripts/generate_pdf.py scripts/sample_slides.md -o output.pdf --title "有赞支付" --subtitle "收款&分账解决方案"
```

### Notes

- No linter or test framework is configured in this repo.
- The reportlab fallback uses `STSong-Light` CID font for Chinese; if unavailable, it falls back to Helvetica (Chinese may render as boxes).
- Optional deps (`playwright`, `weasyprint`, `Pillow`) improve HTML→PDF quality but are not required — scripts degrade gracefully.
