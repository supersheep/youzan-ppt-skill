#!/usr/bin/env python3
"""
从 PDF 提取结构化内容（层级、表格、区块），输出 JSON。
让 Agent 能「看到」底料的结构，而非仅纯文本。
"""
import json
import re
import subprocess
import sys

def get_text(path):
    """获取 PDF 文本，优先 pypdf 再 pdftotext。"""
    try:
        from pypdf import PdfReader
        reader = PdfReader(path)
        return "\n".join(p.extract_text() or "" for p in reader.pages)
    except ImportError:
        r = subprocess.run(
            ["pdftotext", "-layout", path, "-"],
            capture_output=True, text=True, timeout=60
        )
        return r.stdout if r.returncode == 0 else ""

def parse_structure(text):
    """解析文本为结构化数据。"""
    lines = text.split("\n")
    sections = []
    current_section = None
    current_table = None
    i = 0

    # 标题正则：1. 1.1 1.2 2. 2.1 等
    heading_re = re.compile(r'^(\d+(?:\.\d+)*\.?)\s+(.+)$')
    # 表格行：多列用 tab 或 2+ 空格分隔
    table_cell_re = re.compile(r'\t+|\s{2,}')
    # 区块标记
    block_markers = ('💥', '🌟', '📣', '•', '◦')

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # 分页标记
        if re.match(r'^--\s*\d+\s+of\s+\d+\s*--', stripped):
            i += 1
            continue

        # 一级/二级标题
        m = heading_re.match(stripped)
        if m and len(m.group(1)) <= 4:  # 1. 1.1 1.2 2. 等
            if current_section:
                sections.append(current_section)
            current_section = {
                "type": "section",
                "level": m.group(1).count('.') + 1,
                "number": m.group(1).rstrip('.'),
                "title": m.group(2).strip(),
                "content": [],
                "tables": [],
                "blocks": []
            }
            current_table = None
            i += 1
            continue

        # 表格检测：连续多行含 tab 或多空格分隔的多列
        if current_section and (('\t' in line) or re.search(r'\s{3,}', line)):
            row = [c.strip() for c in re.split(r'\t+|\s{2,}', line) if c.strip()]
            if len(row) >= 2:
                if current_table is None:
                    current_table = {"headers": row, "rows": []}
                else:
                    current_table["rows"].append(row)
                i += 1
                continue

        if current_table and current_section:
            current_section["tables"].append(current_table)
            current_table = None

        # 区块（emoji 开头）
        if stripped and any(stripped.startswith(m) for m in block_markers):
            block = {"marker": stripped[0] if stripped[0] in block_markers else "•", "text": stripped}
            if current_section:
                current_section["blocks"].append(block)
            i += 1
            continue

        # 普通段落
        if stripped and current_section:
            # 子要点
            if stripped.startswith(('◦', '•', '-', '*')):
                current_section["content"].append({"type": "bullet", "text": stripped.lstrip('◦•-*').strip()})
            else:
                current_section["content"].append({"type": "paragraph", "text": stripped})
        i += 1

    if current_section:
        sections.append(current_section)
    if current_table and current_section:
        current_section["tables"].append(current_table)

    return sections

def main():
    if len(sys.argv) < 2:
        print("Usage: extract_pdf_structure.py <pdf_path> [--json]", file=sys.stderr)
        sys.exit(1)
    path = sys.argv[1]
    text = get_text(path)
    if not text.strip():
        print("No text extracted.", file=sys.stderr)
        sys.exit(1)
    sections = parse_structure(text)
    out = {"source": path, "sections": sections, "raw_preview": text[:2000]}
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
