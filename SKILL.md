---
name: youzan-ppt-skill
description: 给老婆公司做 ppt 用的。从 PDF 底料生成销售讲义 PDF。Use when user provides @path/to/底料.pdf, 底料做销售讲义, 从底料做ppt, 给有赞做ppt.
---

# 底料 → 销售讲义（PDF）

从 PDF 培训材料（底料）生成**给销售讲的结构化 PPT**，输出为 **PDF** 格式。

**技能路径**：`~/Projects/youzan-ppt-skill` 或 `~/.cursor/skills/youzan-ppt-maker`（同源）

## 场景化工作流（新增）

当用户明确提出具体业务场景（如“门店抽佣”“公域平台分账”）时，优先走场景化生成：

1. 根据场景选择对应 `scene_id`（见 `scenarios/README.md`）
2. 读取对应场景 `SKILL.md`
3. 调用 `scripts/generate_scene_slides.py` 生成 `slides.md`
4. 再用 `scripts/generate_pdf.py` 输出 PDF

示例：

```bash
# 列出可用场景
python ~/Projects/youzan-ppt-skill/scripts/generate_scene_slides.py --list-scenes

# 批量场景生成 slides.md
python ~/Projects/youzan-ppt-skill/scripts/generate_scene_slides.py \
  --plan-file ~/Projects/youzan-ppt-skill/scripts/sample_scene_plan.json \
  -o ~/Projects/youzan-ppt-skill/ppt/slides.md

# 再转 PDF
python ~/Projects/youzan-ppt-skill/scripts/generate_pdf.py \
  ~/Projects/youzan-ppt-skill/ppt/slides.md \
  -o ~/Projects/youzan-ppt-skill/ppt/output.pdf \
  --title "有赞支付" --subtitle "收款&分账解决方案"
```

## 前置：必须「看到」的两样东西

### 1. 底料的结构（而非仅文本）

```bash
python ~/Projects/youzan-ppt-skill/scripts/extract_pdf_structure.py "<底料PDF路径>" > structure.json
```

输出包含：`sections`（层级、表格、区块）、`raw_preview`。  
纯文本补充：`pdftotext -layout "<底料PDF路径>" - > content.txt`

### 2. 目标 PDF 的结构与视觉风格

打开目标 PDF（用户提供的样例，或 `reference/【快速浏览】有赞支付解决方案+2025年最新版.pdf`）。**参考 PDF 与生成输出分离**：前者在 reference/，后者输出到 `xxx-生成.pdf`。  
- 布局与风格：[reference/style-guide.md](reference/style-guide.md)
- 逐页视觉拆解：[reference/visual-analysis.md](reference/visual-analysis.md)
- 实现工具（SVG 等）：[reference/implementation-tools.md](reference/implementation-tools.md)

## 工作流程

### 1. 提取底料结构 + 文本

```bash
python ~/Projects/youzan-ppt-skill/scripts/extract_pdf_structure.py "<底料PDF路径>" > structure.json
pdftotext -layout "<底料PDF路径>" - > content.txt
```

### 2. 浏览目标 PDF 风格

打开目标 PDF，阅读 [reference/style-guide.md](reference/style-guide.md)。

### 3. 设计幻灯片（Agent 执行）

基于 **structure.json** 按 **style-guide** 映射，输出 Markdown（`---` 分隔幻灯片）。

### 4. 生成 PDF（带颜色、排版）

**推荐**：使用 `generate_pdf.py`，自动选择最佳方式：

```bash
pip install reportlab pypdf  # 首次需安装
python ~/Projects/youzan-ppt-skill/scripts/generate_pdf.py slides.md -o output.pdf \
  --title "主标题" --subtitle "副标题"
```

- **优先**：HTML + Playwright 截图（需 `playwright install chromium`）→ 效果最佳，含渐变、图标
- **回退**：reportlab 直接生成 → 带配色、标题栏、标签高亮，无需额外依赖

**可选**：生成 HTML 后浏览器打开预览，再手动打印为 PDF：

```bash
python ~/Projects/youzan-ppt-skill/scripts/md_to_html.py slides.md -o slides.html
open slides.html  # 浏览器打开，Cmd+P 打印为 PDF
```

## 脚本与参考

| 文件 | 用途 |
|------|------|
| `scripts/extract_pdf_structure.py` | 提取层级、表格、区块，输出 JSON |
| `scripts/extract_pdf.py` | 纯文本提取（补充） |
| `scripts/generate_pdf.py` | **推荐**：Markdown → PDF（带颜色、排版） |
| `scripts/md_to_html.py` | Markdown → 带样式的 HTML |
| `scripts/html_to_pdf.py` | HTML → PDF（Playwright/weasyprint） |
| `scripts/md_to_pdf.py` | Markdown → PDF（reportlab 带配色，回退用） |
| `reference/style-guide.md` | 目标布局与视觉规范 |
| `reference/design-guide.md` | 配色与排版规范（参考 Anthropic pptx） |

## 输出命名建议

- 底料：`xxx培训材料【解决方案底料】.pdf`
- **参考 PDF**（不覆盖）：`reference/【快速浏览】xxx解决方案+年份.pdf` 或用户指定
- **生成输出**：`【快速浏览】xxx解决方案+年份-生成.pdf`（必须带 `-生成` 后缀，避免覆盖参考）

## 完整执行示例

```bash
# 1. 提取结构
python ~/Projects/youzan-ppt-skill/scripts/extract_pdf_structure.py "ppt/有赞支付培训材料【解决方案底料】.pdf" > ppt/structure.json
pdftotext -layout "ppt/有赞支付培训材料【解决方案底料】.pdf" - > ppt/content.txt

# 2. 打开参考 PDF 浏览风格：reference/【快速浏览】有赞支付解决方案+2025年最新版.pdf
# 3. Agent 设计 slides.md

# 4. 生成 PDF（输出到 -生成.pdf，不覆盖参考）
python ~/Projects/youzan-ppt-skill/scripts/generate_pdf.py ppt/slides.md \
  -o "ppt/【快速浏览】有赞支付解决方案+2025年最新版-生成.pdf" \
  --title "有赞支付" --subtitle "收款&分账解决方案"
```
