---
name: youzan-scene-demand-mixed-channel-split
description: 用于生成「商家典型业务需求③：收款+分账（保留原通道）」流程页。
---

# 场景：业务需求③ 收款+分账（保留原通道）

## 对应生成逻辑

- `scene_id`: `demand_mixed_channel_split`
- 脚本：`python scripts/generate_scene_slides.py --scene demand_mixed_channel_split ...`

## 适用时机

- 线上愿意接入有赞，但线下需要保留原有支付机构。
- 目标是双通道共存并统一分账。

## 输入字段（JSON）

- `online_flow`: 线上流程节点数组
- `offline_flow`: 线下流程节点数组
- `summary`: 统一价值总结

## 输出约束

- 必须有“线上链路”和“线下链路”两条独立描述。
- 结论强调“兼容历史通道 + 统一分账能力”。
