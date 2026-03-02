---
name: youzan-scene-product-collection
description: 用于生成「有赞收款」产品介绍页，强调产品定义、核心价值、支付流程。
---

# 场景：产品介绍（有赞收款）

## 对应生成逻辑

- `scene_id`: `product_collection`
- 脚本：`python scripts/generate_scene_slides.py --scene product_collection ...`

## 适用时机

- 讲解核心产品时，需明确“是什么、解决什么、怎么流转”。
- 适合产品章节第一页或销售讲解中的产品卡片页。

## 输入字段（JSON）

- `definition`: 产品定义
- `core_values`: 核心价值数组（建议 3–4 条）
- `flow_nodes`: 流程节点数组
- `tags`: 产品标签（如“全渠道收款｜稳定到账｜对账清晰”）

## 输出约束

- 按“定义 → 价值 → 流程 → 标签”输出。
- 核心价值优先使用“标签：说明”格式。
