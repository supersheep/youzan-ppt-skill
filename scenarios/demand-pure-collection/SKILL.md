---
name: youzan-scene-demand-pure-collection
description: 用于生成「商家典型业务需求①：纯收款」流程页。
---

# 场景：业务需求① 纯收款

## 对应生成逻辑

- `scene_id`: `demand_pure_collection`
- 脚本：`python scripts/generate_scene_slides.py --scene demand_pure_collection ...`

## 适用时机

- 商家暂时无分账诉求，仅关注收款稳定、到账效率和对账清晰。

## 输入字段（JSON）

- `flow_nodes`: 资金路径节点数组
- `business_feature`: 业务特征说明
- `capability_focus`: 能力重点说明

## 输出约束

- 必须突出“纯收款”定位，不引入复杂分账流程。
- 用一句话收尾，说明该模式的边界与价值。
