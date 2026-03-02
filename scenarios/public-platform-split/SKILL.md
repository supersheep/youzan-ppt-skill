---
name: youzan-scene-public-platform-split
description: 用于生成「公域平台分账」场景页，覆盖平台订单、核销抽佣、规则清分。
---

# 场景：公域平台分账

## 对应生成逻辑

- `scene_id`: `public_platform_split`
- 脚本：`python scripts/generate_scene_slides.py --scene public_platform_split ...`

## 适用时机

- 涉及抖音/美团/快手/小红书等公域订单，需要自动抽佣和统一归集。

## 输入字段（JSON）

- `platforms`: 平台数组
- `flow_nodes`: 业务路径节点数组
- `rules`: 分账规则数组
- `result`: 结果说明

## 输出约束

- 必须体现“平台订单 → 门店核销 → 分账规则”的关键链路。
- 规则描述至少包含“阶梯比例”或“固定比例”之一。
