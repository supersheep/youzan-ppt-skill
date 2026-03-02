---
name: youzan-scene-split-account-overview
description: 用于生成「有赞分账场景总览」页面，覆盖来源、匹配、角色账户。
---

# 场景：分账场景总览

## 对应生成逻辑

- `scene_id`: `split_account_overview`
- 脚本：`python scripts/generate_scene_slides.py --scene split_account_overview ...`

## 适用时机

- 需要快速总览分账账户如何承接多来源订单并自动匹配规则。

## 输入字段（JSON）

- `upstream_channels`: 收款来源数组
- `match_scenarios`: 自动匹配场景数组
- `role_accounts`: 分账角色账户数组
- `rule_note`: 规则能力说明

## 输出约束

- 必须覆盖“来源 + 场景 + 角色 + 规则”四段信息。
- 语言偏业务可执行，不写空泛口号。
