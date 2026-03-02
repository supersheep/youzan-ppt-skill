---
name: youzan-scene-business-upgrade-dual-panel
description: 用于生成「业务模式升级」对开页。左侧现状与痛点，右侧解决方案与价值点。
---

# 场景：业务模式升级（对开页）

## 对应生成逻辑

- `scene_id`: `business_upgrade_dual_panel`
- 脚本：`python scripts/generate_scene_slides.py --scene business_upgrade_dual_panel ...`

## 适用时机

- 需要展示「现状问题」到「有赞方案价值」的转化。
- 页面结构是左问题右方案，且有 3–6 条痛点与价值点。

## 输入字段（JSON）

- `title` / `subtitle`
- `current_flow`: 当前交易路径节点数组
- `pain_points`: 痛点数组
- `value_points`: 价值点数组（建议“标签：说明”）

## 输出约束

- 必须包含三段：现状路径、经营问题、解决方案价值。
- 每段不超过 1 行，整体 3–5 条 bullet。
- 措辞偏销售化，突出“稳定、合规、效率、增长”。
