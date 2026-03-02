# 实现工具建议

基于视觉分析，以下工具可实现类似效果。

## 一、图形绘制

### SVG（推荐）

**适用**：流程图、关系图、图标、几何形状

| 元素 | SVG 实现 |
|------|----------|
| 圆形节点 | `<circle>` 或 `<ellipse>` |
| 矩形/圆角 | `<rect rx="8" ry="8">` |
| 箭头 | `<path>` + `marker-end` 或 `<defs><marker>` |
| 虚线连接 | `stroke-dasharray` |
| 文字 | `<text>`，支持 `font-size`、`fill`、`font-weight` |
| 分组 | `<g>` 包裹，便于定位 |
| 渐变 | `<linearGradient>`、`<radialGradient>` |

**示例**：资金流图

```svg
<svg viewBox="0 0 800 400">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#666"/>
    </marker>
  </defs>
  <circle cx="80" cy="200" r="40" fill="#E3F2FD"/>
  <text x="80" y="205" text-anchor="middle">消费者</text>
  <line x1="120" y1="200" x2="200" y2="200" stroke="#666" marker-end="url(#arrow)"/>
  <circle cx="280" cy="200" r="40" fill="#FFF3E0"/>
  <text x="280" y="205" text-anchor="middle">有赞收款</text>
</svg>
```

**工具**：手写 SVG、或用 Python `svgwrite` 库生成。

### HTML/CSS

**适用**：整体布局、配色、圆角、flex/grid

- 圆角：`border-radius`
- 渐变：`linear-gradient`、`radial-gradient`
- 阴影：`box-shadow`
- 图标：emoji、或内联 SVG、或 icon font（Font Awesome）

### Python 库

| 库 | 用途 |
|----|------|
| `svgwrite` | 生成 SVG |
| `reportlab` | PDF 直接绘制（已有） |
| `Pillow` | 位图合成 |
| `weasyprint` | HTML→PDF |
| `playwright` | 网页截图→PDF |

---

## 二、按页面类型的实现建议

| 页面类型 | 推荐方案 | 说明 |
|----------|----------|------|
| 封面 | HTML+CSS 渐变 + emoji/内联 SVG 图标 | 左文右图可先用占位或简单 SVG |
| 纯文字 | reportlab 或 HTML | 已有实现 |
| 对开页 | HTML 两列 + SVG 流程图 | 左侧流程图用 SVG 嵌入 |
| 三列流程图 | SVG 为主 | 节点、箭头、标签 |
| 产品页 | HTML 左文 + 右侧 SVG 图 | 流程图用 SVG |
| 业务需求流程图 | SVG | 圆形节点+箭头，易复用 |
| 过渡页 | HTML pill 按钮 | `border-radius` 即可 |
| 关系图 | SVG 节点-链接 | 中心圆+四周圆+连线 |
| 三列问题-方案 | HTML 三列 + 色块 | 绿/蓝/橙 `background` |
| 案例页 | HTML 三列 + 编号列表 | 模块化布局 |
| 结尾 | 背景图 + 白字 | 需图片资源，或纯色+大字号 |

---

## 三、当前 skill 的增强路径

1. **短期**：在 `md_to_html.py` 中为流程图类幻灯片输出内联 SVG 占位，用简单节点+箭头表示资金流。
2. **中期**：新增 `slides_to_svg.py`，根据 Markdown 中的「流程描述」生成 SVG（如「消费者→门店→有赞收款→商家」→ 自动布局节点和箭头）。
3. **长期**：支持从底料表格/结构化数据自动生成关系图、分账规则图。

---

## 四、SVG 嵌入方式

**HTML 内联**：

```html
<div class="flow-diagram">
  <svg width="100%" height="200" viewBox="0 0 600 200">
    <!-- 节点和箭头 -->
  </svg>
</div>
```

**PDF**：reportlab 可 `drawImage` 渲染 SVG（需转 PNG），或 weasyprint 直接支持 SVG。

**Markdown 扩展**：可在 slides.md 中支持：

```markdown
---
# 商家典型业务需求① 纯收款
flow: 消费者 → 私域商城/门店 → 有赞收款 → 商家银行账户
---
```

由脚本解析 `flow:` 行并生成对应 SVG。
