#!/usr/bin/env python3
"""
将 Markdown 幻灯片转为 PDF（销售讲义格式）。
格式：用 --- 分隔幻灯片，# 为标题，- 为要点。
依赖：reportlab
"""
import argparse
import re
import sys

def parse_md(md_text):
    """解析 Markdown，返回 [(title, subtitle, bullets), ...]"""
    slides = []
    blocks = re.split(r'\n---+\n', md_text.strip())
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.split('\n')
        title, subtitle, bullets = "", "", []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith('# '):
                title = line[2:].strip()
            elif line.startswith('## '):
                subtitle = line[3:].strip()
            elif line.startswith('- ') or line.startswith('* '):
                bullets.append(line[2:].strip())
        if title or bullets:
            slides.append((title, subtitle, bullets))
    return slides

def _register_chinese_font():
    """注册中文字体，优先 STSong-Light，否则尝试系统字体。"""
    from reportlab.pdfbase import pdfmetrics
    try:
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
        return "STSong-Light"
    except Exception:
        pass
    try:
        from reportlab.pdfbase.ttfonts import TTFont
        for path in [
            "/System/Library/AssetsV2/com_apple_MobileAsset_Font7/3419f2a427639ad8c8e139149a287865a90fa17e.asset/AssetData/PingFang.ttc",
            "/System/Library/Fonts/PingFang.ttc",
            "/Library/Fonts/PingFang.ttc",
        ]:
            try:
                pdfmetrics.registerFont(TTFont("PingFang", path))
                return "PingFang"
            except Exception:
                continue
    except Exception:
        pass
    return "Helvetica"  # 回退，中文可能显示为方框

# 配色：Teal Trust（金融/支付）
COLORS = {
    "primary": (0.0078, 0.502, 0.565),   # #028090
    "secondary": (0, 0.659, 0.588),      # #00A896
    "accent": (0.0078, 0.765, 0.604),    # #02C39A
    "dark": (0.129, 0.129, 0.129),
    "muted": (0.42, 0.45, 0.5),
}

def create_pdf(slides, output_path, title="", subtitle=""):
    from reportlab.lib.pagesizes import landscape, A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import inch

    font_name = _register_chinese_font()
    w, h = landscape(A4)
    c = canvas.Canvas(output_path, pagesize=(w, h))

    footer = "杭州有赞科技有限公司 © 2012-2026 All Rights Reserved. 香港上市代码: 08083.HK"

    def draw_page(c, title_text, subtitle_text, bullets, is_cover=False):
        if is_cover:
            # 封面：纯色背景
            c.setFillColorRGB(*COLORS["primary"])
            c.rect(0, 0, w, h, fill=1)
            c.setFillColorRGB(1, 1, 1)
            c.setFont(font_name, 36)
            c.drawCentredString(w / 2, h / 2 + 0.6 * inch, title_text)
            if subtitle_text:
                c.setFont(font_name, 22)
                c.drawCentredString(w / 2, h / 2 - 0.2 * inch, subtitle_text)
            c.setFont(font_name, 14)
            c.drawCentredString(w / 2, h / 2 - 1.2 * inch, "全渠道收款    智能高效分账    门店/生意增长")
        else:
            # 内容页：浅色背景 + 彩色标题栏
            c.setFillColorRGB(0.97, 0.98, 0.99)
            c.rect(0, 0, w, h, fill=1)
            # 标题栏底色
            c.setFillColorRGB(*COLORS["primary"])
            c.roundRect(0.5 * inch, h - 1.5 * inch, w - inch, 0.9 * inch, 8, fill=1)
            c.setFillColorRGB(1, 1, 1)
            c.setFont(font_name, 26)
            c.drawString(0.7 * inch, h - 1.25 * inch, title_text)
            y = h - 2.0 * inch
            for b in bullets:
                c.setFillColorRGB(*COLORS["dark"])
                c.setFont(font_name, 14)
                # 解析 "标签：说明"
                if "：" in b or ":" in b:
                    import re
                    parts = re.split(r'[：:]', b, maxsplit=1)
                    if len(parts) == 2:
                        c.setFont(font_name, 14)
                        c.setFillColorRGB(*COLORS["primary"])
                        c.drawString(0.7 * inch, y, parts[0].strip() + "：")
                        c.setFillColorRGB(*COLORS["dark"])
                        c.drawString(0.7 * inch + c.stringWidth(parts[0].strip() + "：", font_name, 14), y, parts[1].strip())
                    else:
                        c.drawString(0.7 * inch, y, "• " + b)
                else:
                    c.drawString(0.7 * inch, y, "• " + b)
                y -= 0.38 * inch

        # 页脚（每页）
        c.setFont(font_name, 10)
        c.setFillColorRGB(*(COLORS["muted"] if not is_cover else (1, 1, 1)))
        c.drawString(0.5 * inch, 0.4 * inch, footer)

    first = slides[0] if slides else ("", "", [])
    cover_title = title or first[0]
    cover_subtitle = subtitle or (first[1] if len(first) > 1 else "")
    draw_page(c, cover_title, cover_subtitle, [], is_cover=True)
    c.showPage()

    for item in slides[1:] if len(slides) > 1 else []:
        st = item[0]
        sb = item[2] if len(item) > 2 else (item[1] if len(item) > 1 else [])
        draw_page(c, st, "", sb, is_cover=False)
        c.showPage()

    c.save()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("md_file", help="Markdown 幻灯片文件")
    ap.add_argument("-o", "--output", default="output.pdf", help="输出 PDF 路径")
    ap.add_argument("--title", default="", help="封面主标题")
    ap.add_argument("--subtitle", default="", help="封面副标题")
    args = ap.parse_args()
    with open(args.md_file, "r", encoding="utf-8") as f:
        md = f.read()
    slides = parse_md(md)
    if not slides:
        print("No slides parsed.", file=sys.stderr)
        sys.exit(1)
    create_pdf(slides, args.output, args.title, args.subtitle)
    print(f"Saved: {args.output}")

if __name__ == "__main__":
    main()
