#!/usr/bin/env python3
"""
将 HTML 幻灯片转为 PDF。
方式：Playwright 截图每页后合并，或 weasyprint 直接渲染。
"""
import argparse
import os
import subprocess
import sys

SLIDE_W, SLIDE_H = 1280, 720

def pdf_via_playwright(html_path, output_path):
    """用 Playwright 截图每页并合并为 PDF。"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False

    html_abs = os.path.abspath(html_path)
    url = f"file://{html_abs}"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": SLIDE_W, "height": SLIDE_H})
            page.goto(url, wait_until="networkidle")
            slides = page.query_selector_all("section.slide")
            images = []
            for i, slide in enumerate(slides):
                img_path = output_path.replace(".pdf", f"_slide{i:02d}.png")
                slide.screenshot(path=img_path)
                images.append(img_path)
            browser.close()

        from reportlab.pdfgen import canvas
        from PIL import Image
        w_pt, h_pt = SLIDE_W * 72 / 96, SLIDE_H * 72 / 96
        c = canvas.Canvas(output_path, pagesize=(w_pt, h_pt))
        for img_path in images:
            c.drawImage(img_path, 0, 0, width=w_pt, height=h_pt)
            c.showPage()
        c.save()
        for p in images:
            os.remove(p)
        return True
    except Exception as e:
        if "Executable doesn't exist" in str(e):
            print("Run: playwright install chromium", file=sys.stderr)
        return False

def pdf_via_weasyprint(html_path, output_path):
    """用 weasyprint 直接渲染 HTML 为 PDF。"""
    try:
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration

        font_config = FontConfiguration()
        html_doc = HTML(filename=os.path.abspath(html_path))
        css = CSS(string=f'''
            @page {{ size: {SLIDE_W}px {SLIDE_H}px; margin: 0; }}
            body {{ margin: 0; }}
            .slide {{ width: {SLIDE_W}px; height: {SLIDE_H}px; page-break-after: always; }}
        ''')
        html_doc.write_pdf(output_path, stylesheets=[css], font_config=font_config)
        return True
    except ImportError:
        return False
    except Exception as e:
        print(f"WeasyPrint error: {e}", file=sys.stderr)
        return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html_file", help="HTML 幻灯片文件")
    ap.add_argument("-o", "--output", default="output.pdf", help="输出 PDF 路径")
    ap.add_argument("--method", choices=["playwright", "weasyprint", "auto"], default="auto",
                    help="转换方式：playwright=截图合并, weasyprint=直接渲染, auto=自动选择")
    args = ap.parse_args()

    ok = False
    if args.method == "weasyprint":
        ok = pdf_via_weasyprint(args.html_file, args.output)
    elif args.method == "playwright":
        ok = pdf_via_playwright(args.html_file, args.output)
    else:
        ok = pdf_via_weasyprint(args.html_file, args.output)
        if not ok:
            ok = pdf_via_playwright(args.html_file, args.output)

    if not ok:
        print("Need: pip install playwright Pillow reportlab && playwright install chromium", file=sys.stderr)
        sys.exit(1)
    print(f"Saved: {args.output}")

if __name__ == "__main__":
    main()
