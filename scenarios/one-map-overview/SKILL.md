---
name: youzan-scene-one-map-overview
description: 用于生成「一图看懂有赞支付」总览页，强调三列结构与合规标签。
---

# 场景：一图看懂（总览三列）

## 对应生成逻辑

- `scene_id`: `one_map_overview`
- 脚本：`python scripts/generate_scene_slides.py --scene one_map_overview ...`

## 适用时机

- 需要在一页内给出收款、分账、角色账户的全景图。
- 适合方案总览、领导汇报、销售开场全景介绍。

## 输入字段（JSON）

- `channels`: 收款渠道数组（公域/私域/到店）
- `split_scenarios`: 分账场景数组
- `split_rules`: 分账规则数组
- `role_accounts`: 角色账户数组
- `compliance_tags`: 底部合规标签数组

## 输出约束

- 必须覆盖三列信息：收款入口 / 分账场景与规则 / 多角色账户。
- 结尾增加合规标签，形成“能力 + 合规”闭环。
