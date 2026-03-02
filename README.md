# youzan-ppt-skill

给老婆公司做 ppt 用的。从 PDF 培训材料（底料）生成销售讲义 PDF。

参考 `~/.cursor/skills/youzan-ppt-maker` 技能（同源）。

## 快速开始

```bash
pip install -r requirements.txt

# 1. 提取底料结构
python scripts/extract_pdf_structure.py "<底料PDF路径>" > structure.json

# 2. Agent 设计 slides.md（参考 reference/style-guide.md）

# 3. 生成 PDF
python scripts/generate_pdf.py slides.md -o output.pdf --title "主标题" --subtitle "副标题"
```

## 目录

- `scripts/` - 提取、转换、生成脚本
- `reference/` - 风格指南、设计规范
