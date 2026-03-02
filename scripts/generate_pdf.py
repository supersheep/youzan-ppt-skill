#!/usr/bin/env python3
"""
从 Markdown 生成带颜色、排版的 PDF。
优先：md_to_html + html_to_pdf（Playwright 截图，效果最佳）
回退：md_to_pdf（reportlab 带配色，无需额外依赖）
"""
import argparse
import os
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("md_file", help="Markdown 幻灯片文件")
    ap.add_argument("-o", "--output", default="output.pdf", help="输出 PDF 路径")
    ap.add_argument("--title", default="", help="封面主标题")
    ap.add_argument("--subtitle", default="", help="封面副标题")
    ap.add_argument("--method", choices=["html", "reportlab", "auto"], default="auto",
                    help="html=HTML+截图(需playwright), reportlab=直接生成(带配色), auto=自动选择")
    args = ap.parse_args()

    md_path = os.path.abspath(args.md_file)
    out_path = os.path.abspath(args.output)
    html_path = out_path.replace(".pdf", ".html")

    if args.method == "reportlab":
        _run_reportlab(md_path, out_path, args.title, args.subtitle)
        return

    if args.method == "html" or args.method == "auto":
        # 1. 生成 HTML
        import importlib.util
        spec = importlib.util.spec_from_file_location("md_to_html", os.path.join(SKILL_DIR, "scripts", "md_to_html.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with open(md_path, "r", encoding="utf-8") as f:
            slides = mod.parse_md(f.read())
        mod.create_html(slides, html_path, args.title, args.subtitle)

        # 2. HTML -> PDF
        spec2 = importlib.util.spec_from_file_location("html_to_pdf", os.path.join(SKILL_DIR, "scripts", "html_to_pdf.py"))
        mod2 = importlib.util.module_from_spec(spec2)
        spec2.loader.exec_module(mod2)
        if mod2.pdf_via_weasyprint(html_path, out_path) or mod2.pdf_via_playwright(html_path, out_path):
            print(f"Saved: {out_path}")
            return

    # 回退到 reportlab
    print("Using reportlab (colored) fallback...", file=sys.stderr)
    _run_reportlab(md_path, out_path, args.title, args.subtitle)

def _run_reportlab(md_path, out_path, title, subtitle):
    import importlib.util
    spec = importlib.util.spec_from_file_location("md_to_pdf", os.path.join(SKILL_DIR, "scripts", "md_to_pdf.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    with open(md_path, "r", encoding="utf-8") as f:
        slides = mod.parse_md(f.read())
    mod.create_pdf(slides, out_path, title, subtitle)
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    main()
