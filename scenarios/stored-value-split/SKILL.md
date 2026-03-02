---
name: youzan-scene-stored-value-split
description: 用于生成「储值分账」场景页，强调总部统筹资金与消费触发分账。
---

# 场景：储值分账

## 对应生成逻辑

- `scene_id`: `stored_value_split`
- 脚本：`python scripts/generate_scene_slides.py --scene stored_value_split ...`

## 适用时机

- 储值资金先归总部统一管理，再按门店消费行为触发分账。

## 输入字段（JSON）

- `flow_nodes`: 资金路径节点数组
- `trigger`: 触发分账条件说明
- `split_targets`: 分账去向数组
- `benefit`: 风险收益总结

## 输出约束

- 必须区分“储值归集”与“消费触发分账”两个阶段。
- 结果要体现“资金安全 + 门店激励”双重价值。
