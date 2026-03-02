# 场景化技能目录

本目录将你这批「有赞支付方案」拆成多个**独立场景**。  
每个场景都包含单独的 `SKILL.md`（提示词约束）和对应的生成逻辑（`scripts/generate_scene_slides.py` 中的同名 scene_id 函数）。

## 场景清单

| scene_id | 场景目录 | 说明 |
|---|---|---|
| `business_upgrade_dual_panel` | `business-upgrade-dual-panel/` | 业务模式升级（左问题右方案） |
| `one_map_overview` | `one-map-overview/` | 一图看懂（全渠道收款/智能分账/增长） |
| `product_collection` | `product-collection/` | 产品介绍：有赞收款 |
| `demand_pure_collection` | `demand-pure-collection/` | 商家需求①：纯收款 |
| `demand_collection_with_split` | `demand-collection-with-split/` | 商家需求②：收款+分账（有赞通道） |
| `demand_mixed_channel_split` | `demand-mixed-channel-split/` | 商家需求③：收款+分账（保留原通道） |
| `value_pyramid` | `value-pyramid/` | 支付稳定：三层价值模型 |
| `split_account_overview` | `split-account-overview/` | 分账场景总览 |
| `store_commission` | `store-commission/` | 门店抽佣 |
| `franchise_fee_management` | `franchise-fee-management/` | 加盟费管理 |
| `public_platform_split` | `public-platform-split/` | 公域平台分账 |
| `stored_value_split` | `stored-value-split/` | 储值分账 |
| `rights_card_split` | `rights-card-split/` | 权益卡分账 |

## 生成方式

### 1) 查看可用场景

```bash
python scripts/generate_scene_slides.py --list-scenes
```

### 2) 生成单场景 slides.md

```bash
python scripts/generate_scene_slides.py \
  --scene demand_pure_collection \
  --input-json '{"flow_nodes":["消费者","私域商城/门店交易","有赞收款","商家银行账户"]}' \
  -o slides.md
```

### 3) 按计划批量生成（推荐）

```bash
python scripts/generate_scene_slides.py --plan-file scripts/sample_scene_plan.json -o slides.md
```

然后使用现有脚本转 PDF：

```bash
python scripts/generate_pdf.py slides.md -o output.pdf --title "有赞支付" --subtitle "收款&分账解决方案"
```
