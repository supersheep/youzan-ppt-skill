#!/usr/bin/env python3
"""
将 Markdown 幻灯片转为带颜色、排版的 HTML。
参考 Anthropic pptx skill 设计原则：配色、视觉元素、版式变化。
"""
import argparse
import html
import re
import sys

# 配色：Teal Trust（金融/支付场景）
PALETTE = {
    "primary": "#028090",    # 主色
    "secondary": "#00A896",  # 辅色
    "accent": "#02C39A",     # 强调
    "dark": "#212121",
    "light": "#F7F9FC",
    "muted": "#6B7280",
}

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

def esc(s):
    return html.escape(s, quote=True)

def render_slide(i, title, subtitle, bullets, is_cover, palette):
    if is_cover:
        return f'''
<section class="slide slide-cover" data-slide="{i}">
  <div class="cover-badge">💰</div>
  <div class="cover-content">
    <h1 class="cover-title">{esc(title)}</h1>
    <h2 class="cover-subtitle">{esc(subtitle)}</h2>
    <div class="cover-slogan">
      <span>📱 全渠道收款</span>
      <span>📊 智能高效分账</span>
      <span>🏪 门店/生意增长</span>
    </div>
  </div>
  <footer class="slide-footer">{esc("杭州有赞科技有限公司 © 2012-2026 All Rights Reserved. 香港上市代码: 08083.HK")}</footer>
</section>'''
    else:
        bullets_html = ""
        for j, b in enumerate(bullets):
            # 解析 "标签：说明" 格式
            if "：" in b or ":" in b:
                parts = re.split(r'[：:]', b, maxsplit=1)
                if len(parts) == 2:
                    label, desc = parts[0].strip(), parts[1].strip()
                    bullets_html += f'<li><span class="bullet-label">{esc(label)}</span>：{esc(desc)}</li>'
                else:
                    bullets_html += f'<li>{esc(b)}</li>'
            else:
                bullets_html += f'<li>{esc(b)}</li>'
        return f'''
<section class="slide slide-content" data-slide="{i}">
  <div class="slide-header">
    <span class="slide-icon">◆</span>
    <h2 class="slide-title">{esc(title)}</h2>
  </div>
  <div class="slide-body">
    <ul class="bullet-list">{bullets_html}</ul>
  </div>
  <footer class="slide-footer">{esc("杭州有赞科技有限公司 © 2012-2026 All Rights Reserved. 香港上市代码: 08083.HK")}</footer>
</section>'''

def create_html(slides, output_path, title="", subtitle=""):
    first = slides[0] if slides else ("", "", [])
    cover_title = title or first[0]
    cover_subtitle = subtitle or (first[1] if len(first) > 1 else "")

    slides_html = render_slide(0, cover_title, cover_subtitle, [], True, PALETTE)
    for i, item in enumerate(slides[1:] if len(slides) > 1 else []):
        st = item[0]
        sb = item[2] if len(item) > 2 else (item[1] if len(item) > 1 else [])
        slides_html += render_slide(i + 1, st, "", sb, False, PALETTE)

    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1280, height=720">
  <title>有赞支付 - 销售讲义</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif; }}
    
    .slide {{
      width: 1280px;
      height: 720px;
      position: relative;
      display: flex;
      flex-direction: column;
      padding: 48px 56px;
      page-break-after: always;
    }}
    
    .slide-cover {{
      background: linear-gradient(135deg, {PALETTE["primary"]} 0%, {PALETTE["secondary"]} 50%, {PALETTE["accent"]} 100%);
      justify-content: center;
      align-items: center;
    }}
    
    .cover-badge {{
      position: absolute;
      top: 48px;
      right: 56px;
      width: 64px;
      height: 64px;
      background: rgba(255,255,255,0.25);
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;
      color: white;
    }}
    .cover-content {{ text-align: center; color: white; }}
    .cover-title {{ font-size: 48px; font-weight: 700; margin-bottom: 16px; text-shadow: 0 2px 4px rgba(0,0,0,0.2); }}
    .cover-subtitle {{ font-size: 28px; font-weight: 500; opacity: 0.95; margin-bottom: 48px; }}
    .cover-slogan {{
      display: flex;
      gap: 32px;
      justify-content: center;
      font-size: 20px;
      font-weight: 500;
      opacity: 0.9;
    }}
    .cover-slogan span {{
      padding: 10px 24px;
      background: rgba(255,255,255,0.25);
      border-radius: 10px;
      display: inline-flex;
      align-items: center;
      gap: 8px;
    }}
    
    .slide-content {{
      background: {PALETTE["light"]};
    }}
    
    .slide-header {{
      display: flex;
      align-items: center;
      gap: 16px;
      margin-bottom: 32px;
      padding-bottom: 20px;
      border-bottom: 4px solid {PALETTE["primary"]};
    }}
    .slide-icon {{
      width: 44px;
      height: 44px;
      background: {PALETTE["primary"]};
      color: white;
      border-radius: 10px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      flex-shrink: 0;
    }}
    .slide-title {{
      font-size: 32px;
      font-weight: 700;
      color: {PALETTE["dark"]};
    }}
    
    .slide-body {{ flex: 1; }}
    .bullet-list {{
      list-style: none;
      font-size: 18px;
      line-height: 1.8;
      color: {PALETTE["dark"]};
    }}
    .bullet-list li {{
      padding: 12px 0;
      padding-left: 28px;
      position: relative;
    }}
    .bullet-list li::before {{
      content: "";
      position: absolute;
      left: 0;
      top: 1.2em;
      width: 10px;
      height: 10px;
      background: {PALETTE["accent"]};
      border-radius: 50%;
    }}
    .bullet-label {{
      font-weight: 700;
      color: {PALETTE["primary"]};
    }}
    
    .slide-footer {{
      position: absolute;
      bottom: 24px;
      left: 56px;
      right: 56px;
      font-size: 11px;
      color: {PALETTE["muted"]};
    }}
    
    @media print {{
      .slide {{ page-break-after: always; }}
    }}
  </style>
</head>
<body>
{slides_html}
</body>
</html>'''

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("md_file", help="Markdown 幻灯片文件")
    ap.add_argument("-o", "--output", default="slides.html", help="输出 HTML 路径")
    ap.add_argument("--title", default="", help="封面主标题")
    ap.add_argument("--subtitle", default="", help="封面副标题")
    args = ap.parse_args()
    with open(args.md_file, "r", encoding="utf-8") as f:
        md = f.read()
    slides = parse_md(md)
    if not slides:
        print("No slides parsed.", file=sys.stderr)
        sys.exit(1)
    create_html(slides, args.output, args.title, args.subtitle)
    print(f"Saved: {args.output}")

if __name__ == "__main__":
    main()
