#!/usr/bin/env python3
"""从 PDF 提取文本，输出到 stdout。优先用 pypdf，否则尝试 subprocess 调用 pdftotext。"""
import subprocess
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: extract_pdf.py <pdf_path>", file=sys.stderr)
        sys.exit(1)
    path = sys.argv[1]
    try:
        from pypdf import PdfReader
        reader = PdfReader(path)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                print(text)
    except ImportError:
        # 回退到 pdftotext（poppler-utils）
        try:
            r = subprocess.run(
                ["pdftotext", "-layout", path, "-"],
                capture_output=True, text=True, timeout=60
            )
            if r.returncode == 0:
                print(r.stdout)
            else:
                print(f"pdftotext error: {r.stderr}", file=sys.stderr)
                sys.exit(1)
        except FileNotFoundError:
            print("Install: pip install pypdf 或 brew install poppler", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
