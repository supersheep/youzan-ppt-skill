---
name: youzan-scene-store-commission
description: 用于生成「门店抽佣」场景页，强调阶梯/固定比例规则和自动清分。
---

# 场景：门店抽佣

## 对应生成逻辑

- `scene_id`: `store_commission`
- 脚本：`python scripts/generate_scene_slides.py --scene store_commission ...`

## 适用时机

- 连锁品牌需对门店流水进行自动抽佣并汇总总部。

## 输入字段（JSON）

- `flow_nodes`: 交易路径节点数组
- `commission_modes`: 抽佣模式数组
- `tiers`: 阶梯规则数组
- `settlement_note`: 结算动作说明

## 输出约束

- 必须同时出现“阶梯比例”和“固定比例”两个模式（可按实际覆盖）。
- 结论要强调“自动判定 + 自动划扣 + 汇总总部”。
