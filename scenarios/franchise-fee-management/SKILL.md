---
name: youzan-scene-franchise-fee-management
description: 用于生成「加盟费管理」场景页，支持分期/一次性收取方案。
---

# 场景：加盟费管理

## 对应生成逻辑

- `scene_id`: `franchise_fee_management`
- 脚本：`python scripts/generate_scene_slides.py --scene franchise_fee_management ...`

## 适用时机

- 需要平衡门店现金流与总部回款，设计可执行加盟费方案。

## 输入字段（JSON）

- `flow_nodes`: 签约与资金路径节点数组
- `charge_modes`: 收费方式数组
- `periods`: 分期规则数组
- `summary`: 收尾总结

## 输出约束

- 必须体现“分期 + 一次性”两类收取方式。
- 若是分期，至少给 2 段期次规则。
