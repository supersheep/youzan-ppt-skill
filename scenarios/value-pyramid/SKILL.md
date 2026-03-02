---
name: youzan-scene-value-pyramid
description: 用于生成「支付稳定」三层价值模型（金字塔）页面。
---

# 场景：商业价值三层金字塔

## 对应生成逻辑

- `scene_id`: `value_pyramid`
- 脚本：`python scripts/generate_scene_slides.py --scene value_pyramid ...`

## 适用时机

- 需要解释“基础支持 → 核心能力 → 商业价值”的能力跃迁。

## 输入字段（JSON）

- `foundation`: 基础支撑数组
- `capabilities`: 核心能力数组
- `business_values`: 商业价值数组
- `core_values`: 右侧价值摘要数组

## 输出约束

- 必须保留三层结构，不能只写平铺 bullet。
- 文案应体现“稳定、风控、增长”的递进关系。
