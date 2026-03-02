# youzan-ppt-skill

给老婆公司做 ppt 用的。从 PDF 培训材料（底料）生成销售讲义 PDF。

参考 `~/.cursor/skills/youzan-ppt-maker` 技能（同源）。

## 场景化生成（新增）

已支持按业务场景拆分生成逻辑：每个场景都有独立 `SKILL.md` 与 scene generator。

- 场景目录：[`scenarios/`](scenarios/README.md)
- 生成脚本：`scripts/generate_scene_slides.py`

### 列出全部场景

```bash
python scripts/generate_scene_slides.py --list-scenes
```

### 批量生成 slides.md（推荐）

```bash
python scripts/generate_scene_slides.py \
  --plan-file scripts/sample_scene_plan.json \
  -o slides.md
```

### 生成单场景 slides.md

```bash
python scripts/generate_scene_slides.py \
  --scene demand_pure_collection \
  --input-json '{"flow_nodes":["消费者","私域商城/门店交易","有赞收款","商家银行账户"]}' \
  -o slides.md
```

再转 PDF：

```bash
python scripts/generate_pdf.py slides.md -o output.pdf --title "有赞支付" --subtitle "收款&分账解决方案"
```

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
