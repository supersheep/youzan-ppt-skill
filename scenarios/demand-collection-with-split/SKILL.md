---
name: youzan-scene-demand-collection-with-split
description: 用于生成「商家典型业务需求②：收款+分账（有赞通道）」流程页。
---

# 场景：业务需求② 收款+分账（有赞通道）

## 对应生成逻辑

- `scene_id`: `demand_collection_with_split`
- 脚本：`python scripts/generate_scene_slides.py --scene demand_collection_with_split ...`

## 适用时机

- 需要展示在有赞链路内完成聚合收款、自动分账、提现闭环。

## 输入字段（JSON）

- `flow_nodes`: 主流程节点数组
- `receivers`: 分账接收方数组
- `settlement_mode`: 清分与提现说明

## 输出约束

- 必须体现“收款系统”与“分账系统”两个核心节点。
- 必须出现“接收方1..N”的可扩展结构。
