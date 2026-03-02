---
name: youzan-scene-rights-card-split
description: 用于生成「权益卡分账」场景页，支持奖励与抽成双配置。
---

# 场景：权益卡分账

## 对应生成逻辑

- `scene_id`: `rights_card_split`
- 脚本：`python scripts/generate_scene_slides.py --scene rights_card_split ...`

## 适用时机

- 权益卡销售涉及总部奖励与门店抽成，需灵活配置分配方式。

## 输入字段（JSON）

- `flow_nodes`: 业务路径节点数组
- `reward_modes`: 奖励方式数组
- `draw_modes`: 抽成方式数组
- `goal`: 场景目标

## 输出约束

- 必须同时描述“奖励配置”和“抽成配置”。
- 收尾要明确“激励门店 + 收益可控”。
