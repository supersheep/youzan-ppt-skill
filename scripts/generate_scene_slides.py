#!/usr/bin/env python3
"""
按场景生成销售讲义 Markdown。

目标：让每个业务场景有独立的生成逻辑，输出可直接交给 scripts/generate_pdf.py。
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable


@dataclass(frozen=True)
class Slide:
    title: str
    subtitle: str
    bullets: list[str]


@dataclass(frozen=True)
class SceneSpec:
    scene_id: str
    display_name: str
    skill_path: str
    generator: Callable[[dict[str, Any]], Slide]


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [_clean_text(x) for x in value if _clean_text(x)]
    text = _clean_text(value)
    if not text:
        return []
    if "\n" in text:
        return [x.strip() for x in text.splitlines() if x.strip()]
    return [text]


def _pick(data: dict[str, Any], key: str, default: Any) -> Any:
    value = data.get(key, default)
    if isinstance(default, list):
        result = _as_list(value)
        return result if result else list(default)
    text = _clean_text(value)
    return text if text else default


def _join(items: list[str], sep: str = "；") -> str:
    cleaned = [_clean_text(x) for x in items if _clean_text(x)]
    return sep.join(cleaned)


def _flow(nodes: list[str]) -> str:
    cleaned = [_clean_text(x) for x in nodes if _clean_text(x)]
    return " → ".join(cleaned)


def gen_business_upgrade_dual_panel(data: dict[str, Any]) -> Slide:
    current_flow = _pick(
        data,
        "current_flow",
        ["消费者", "线上支付/线下支付", "现有支付机构", "资金结算", "商家银行账户"],
    )
    pain_points = _pick(
        data,
        "pain_points",
        [
            "风险频发：传统收款模式在线上生态内易触发风控",
            "模式单一：资金结算路径单一，利润分配难",
            "人工繁琐：涉及加盟/分销/供应商时对账复杂",
            "周期缓慢：资金链路固定，运营效率受限",
            "数据风险：信息系统安全防护投入不足",
        ],
    )
    value_points = _pick(
        data,
        "value_points",
        [
            "极稳通道：依托微信生态及多年服务经验，抗风险能力强",
            "专业护航：高并发场景持续稳定，保障交易连续性",
            "灵活适配：支持连锁、加盟、分销、供应商等自动分账",
            "持牌经营：具备央行支付牌照，合规监管",
            "顶级防护：公安部三级等保 + 国家金融科技认证",
        ],
    )
    return Slide(
        title=_pick(data, "title", "有赞支付助力商家业务模式升级"),
        subtitle=_pick(data, "subtitle", "对开页：左问题右方案"),
        bullets=[
            f"你的现有业务模式是否是这样：{_flow(current_flow)}",
            f"你是否在面临以下经营问题：{_join(pain_points)}",
            f"有赞支付助力你实现：{_join(value_points)}",
        ],
    )


def gen_one_map_overview(data: dict[str, Any]) -> Slide:
    channels = _pick(data, "channels", ["公域付款", "私域付款", "到店付款"])
    split_scenarios = _pick(
        data,
        "split_scenarios",
        ["连锁加盟分账", "品牌管理费分账", "会员储值分账", "礼品卡分账", "外卖订单分账", "同城配送订单分账"],
    )
    split_rules = _pick(
        data,
        "split_rules",
        ["按订单金额分账", "按结算金额分账", "按营业周期分账", "固定比例分账", "阶梯比例分账", "自动结算/人工结算"],
    )
    role_accounts = _pick(data, "role_accounts", ["总部账户", "门店账户", "合伙人账户", "供应商账户", "其他角色账户"])
    compliance_tags = _pick(data, "compliance_tags", ["合规持牌", "资金全保", "数据盾牌", "金融级系统"])
    return Slide(
        title=_pick(data, "title", "一图看懂有赞支付"),
        subtitle=_pick(data, "subtitle", "三列：全渠道收款 / 智能高效分账 / 门店生意增长"),
        bullets=[
            f"全渠道收款：消费者触达 { _join(channels, '、') }，统一归集到商家账户",
            f"分账场景：{_join(split_scenarios, '、')}",
            f"分账规则：{_join(split_rules, '、')}",
            f"多角色分账：{_join(role_accounts, '、')}",
            f"底部合规标签：{_join(compliance_tags, '｜')}",
        ],
    )


def gen_product_collection(data: dict[str, Any]) -> Slide:
    core_values = _pick(
        data,
        "core_values",
        [
            "统一收：整合微信、支付宝、银行卡等多渠道收款",
            "稳到账：多通道互备，保障在复杂网络环境下仍可稳定收款",
            "账对清：数字化台账管理，账目清晰可追溯",
            "无缝对接：支持私域商城、自研商城与复杂资金管理需求",
        ],
    )
    flow_nodes = _pick(data, "flow_nodes", ["公域付款", "私域付款", "门店付款", "商家账户"])
    return Slide(
        title=_pick(data, "title", "产品介绍 & 价值点：有赞收款"),
        subtitle=_pick(data, "subtitle", "有赞支付核心产品①"),
        bullets=[
            f"产品定义：{_pick(data, 'definition', '面向商家的聚合收款平台，解决收款效率与私域回流问题。')}",
            f"核心价值：{_join(core_values)}",
            f"支付流程：{_flow(flow_nodes)}",
            f"场景标签：{_pick(data, 'tags', '全渠道收款｜稳定到账｜对账清晰')}",
        ],
    )


def gen_demand_pure_collection(data: dict[str, Any]) -> Slide:
    flow_nodes = _pick(data, "flow_nodes", ["消费者", "私域商城/门店交易", "有赞收款", "商家银行账户"])
    return Slide(
        title=_pick(data, "title", "商家典型业务需求①：纯收款"),
        subtitle=_pick(data, "subtitle", "无分账诉求，聚焦收款稳定与到账效率"),
        bullets=[
            f"资金路径：{_flow(flow_nodes)}",
            f"业务特征：{_pick(data, 'business_feature', '商家以收款为主，暂不需要多角色分账。')}",
            f"能力重点：{_pick(data, 'capability_focus', '收款稳定、账务清晰、快速结算。')}",
        ],
    )


def gen_demand_collection_with_split(data: dict[str, Any]) -> Slide:
    flow_nodes = _pick(
        data,
        "flow_nodes",
        ["消费者", "私域商城/门店交易", "有赞收款（聚合支付）", "有赞分账（银行账户分账体系）", "商家银行账户/分账接收方账户"],
    )
    receivers = _pick(data, "receivers", ["分账接收方1", "分账接收方2", "分账接收方N"])
    return Slide(
        title=_pick(data, "title", "商家典型业务需求②：收款 + 分账（有赞通道）"),
        subtitle=_pick(data, "subtitle", "同一链路内完成收款、结算、提现"),
        bullets=[
            f"资金路径：{_flow(flow_nodes)}",
            f"分账接收方：{_join(receivers, '、')}",
            f"结算方式：{_pick(data, 'settlement_mode', '可按规则自动清分并提现到对应银行账户。')}",
        ],
    )


def gen_demand_mixed_channel_split(data: dict[str, Any]) -> Slide:
    online_flow = _pick(data, "online_flow", ["消费者", "私域商城", "有赞收款", "有赞分账账户"])
    offline_flow = _pick(data, "offline_flow", ["消费者", "门店交易", "现有支付机构", "有赞分账账户"])
    return Slide(
        title=_pick(data, "title", "商家典型业务需求③：收款 + 分账（保留原通道）"),
        subtitle=_pick(data, "subtitle", "线上走有赞，线下保留现有通道，统一进入分账体系"),
        bullets=[
            f"线上链路：{_flow(online_flow)}",
            f"线下链路：{_flow(offline_flow)}",
            f"统一价值：{_pick(data, 'summary', '兼容既有收款通道，同时获得统一分账能力。')}",
        ],
    )


def gen_value_pyramid(data: dict[str, Any]) -> Slide:
    foundation = _pick(data, "foundation", ["稳定支付通道", "持续沟通渠道", "十年微信经验", "深度合作机制"])
    capabilities = _pick(data, "capabilities", ["风险防控破解", "高 GMV 承载", "适配多交易场景"])
    business_values = _pick(data, "business_values", ["提升抗风险能力", "提升资金运营效率", "持续稳健增长"])
    core_values = _pick(
        data,
        "core_values",
        ["极致稳定通道", "灵活高效自动分账", "全链路合规安全管理", "多业务场景适配"],
    )
    return Slide(
        title=_pick(data, "title", "支付稳定：商业价值/核心能力/基础支持"),
        subtitle=_pick(data, "subtitle", "三层金字塔（底座→能力→价值）"),
        bullets=[
            f"基础支持：{_join(foundation, '、')}",
            f"核心能力：{_join(capabilities, '、')}",
            f"商业价值：{_join(business_values, '、')}",
            f"右侧核心价值：{_join(core_values, '；')}",
        ],
    )


def gen_split_account_overview(data: dict[str, Any]) -> Slide:
    upstream_channels = _pick(data, "upstream_channels", ["私域商城", "公域平台", "线下门店"])
    match_scenarios = _pick(
        data,
        "match_scenarios",
        ["连锁加盟分账", "门店订单分账", "公域订单分账", "会员储值分账"],
    )
    role_accounts = _pick(data, "role_accounts", ["总部账户", "门店账户", "合伙人账户", "供应商账户"])
    return Slide(
        title=_pick(data, "title", "有赞分账：分账场景总览"),
        subtitle=_pick(data, "subtitle", "自动匹配场景 + 多角色分账"),
        bullets=[
            f"收款来源：消费者下单后，资金来自 { _join(upstream_channels, '、') }",
            f"自动匹配分账场景：{_join(match_scenarios, '、')}",
            f"多角色分账目标：{_join(role_accounts, '、')}",
            f"规则能力：{_pick(data, 'rule_note', '支持按金额、比例、周期自动清分。')}",
        ],
    )


def gen_store_commission(data: dict[str, Any]) -> Slide:
    flow_nodes = _pick(data, "flow_nodes", ["消费者", "线下门店", "门店账户", "有赞分账账户", "商家总部"])
    modes = _pick(data, "commission_modes", ["阶梯比例模式", "固定比例模式"])
    tiers = _pick(data, "tiers", ["区间1：0-10万，抽3%", "区间2：10-50万，抽4%", "区间3：50万+，抽5%"])
    return Slide(
        title=_pick(data, "title", "分账核心场景：门店抽佣"),
        subtitle=_pick(data, "subtitle", "按门店流水自动计算分账金额并汇总总部"),
        bullets=[
            f"交易路径：{_flow(flow_nodes)}",
            f"分账模式：{_join(modes, ' / ')}",
            f"阶梯规则：{_join(tiers, '；')}",
            f"结算动作：{_pick(data, 'settlement_note', '系统判流水清单后自动划扣并汇总分账。')}",
        ],
    )


def gen_franchise_fee_management(data: dict[str, Any]) -> Slide:
    flow_nodes = _pick(data, "flow_nodes", ["线下门店", "商家总部", "有赞分账账户"])
    charge_modes = _pick(data, "charge_modes", ["分期收取", "一次性收取"])
    periods = _pick(data, "periods", ["第1期：第1个月流水扣款", "第2期：第2个月流水扣款", "第3期：第3个月流水扣款"])
    return Slide(
        title=_pick(data, "title", "分账核心场景：加盟费管理"),
        subtitle=_pick(data, "subtitle", "平衡门店压力与总部回款诉求"),
        bullets=[
            f"签约路径：{_flow(flow_nodes)}",
            f"收费方式：{_join(charge_modes, ' / ')}",
            f"分期规则：{_join(periods, '；')}",
            f"结算说明：{_pick(data, 'summary', '扣除门店余额后自动转入分账账户并汇总。')}",
        ],
    )


def gen_public_platform_split(data: dict[str, Any]) -> Slide:
    platforms = _pick(data, "platforms", ["抖音", "美团", "快手", "小红书", "淘宝"])
    flow_nodes = _pick(
        data,
        "flow_nodes",
        ["商家总部", "有赞（总部系统）", "公域平台", "消费者", "线下门店", "有赞分账账户"],
    )
    rules = _pick(data, "rules", ["阶梯比例模式", "固定比例模式", "门店流水比例抽佣"])
    return Slide(
        title=_pick(data, "title", "分账核心场景：公域平台分账"),
        subtitle=_pick(data, "subtitle", "平台订单自动抽佣，规则驱动资金归集"),
        bullets=[
            f"平台来源：{_join(platforms, '、')}",
            f"业务路径：{_flow(flow_nodes)}",
            f"分账规则：{_join(rules, '；')}",
            f"结果：{_pick(data, 'result', '平台交易自动归集并汇总到有赞分账账户。')}",
        ],
    )


def gen_stored_value_split(data: dict[str, Any]) -> Slide:
    flow_nodes = _pick(data, "flow_nodes", ["消费者购买储值卡", "商家总部统一管理资金", "有赞分账账户", "门店按规则分账"])
    split_targets = _pick(data, "split_targets", ["A 门店收到分账款", "B 门店收到分账款", "C 门店收到分账款"])
    return Slide(
        title=_pick(data, "title", "分账核心场景：储值分账"),
        subtitle=_pick(data, "subtitle", "储值资金归总部，消费时触发门店分账"),
        bullets=[
            f"资金路径：{_flow(flow_nodes)}",
            f"触发动作：{_pick(data, 'trigger', '消费者在门店消费后自动触发按规则分账。')}",
            f"分账去向：{_join(split_targets, '｜')}",
            f"风险收益：{_pick(data, 'benefit', '防范加盟商经营风险，提升总部资金统筹能力。')}",
        ],
    )


def gen_rights_card_split(data: dict[str, Any]) -> Slide:
    flow_nodes = _pick(data, "flow_nodes", ["消费者购买权益卡", "门店账户", "总部主导/门店销售", "总部/门店分账账户"])
    reward_modes = _pick(data, "reward_modes", ["奖励方式1：固定金额奖励", "奖励方式2：按比例奖励"])
    draw_modes = _pick(data, "draw_modes", ["抽成方式1：固定金额抽", "抽成方式2：按比例抽"])
    return Slide(
        title=_pick(data, "title", "分账核心场景：权益卡分账"),
        subtitle=_pick(data, "subtitle", "总部奖励与门店抽成可灵活并行"),
        bullets=[
            f"业务路径：{_flow(flow_nodes)}",
            f"奖励配置：{_join(reward_modes, '；')}",
            f"抽成配置：{_join(draw_modes, '；')}",
            f"目标：{_pick(data, 'goal', '激发门店销售活力，同时确保总部收益可控。')}",
        ],
    )


SCENES: dict[str, SceneSpec] = {
    "business_upgrade_dual_panel": SceneSpec(
        scene_id="business_upgrade_dual_panel",
        display_name="业务模式升级（对开页）",
        skill_path="scenarios/business-upgrade-dual-panel/SKILL.md",
        generator=gen_business_upgrade_dual_panel,
    ),
    "one_map_overview": SceneSpec(
        scene_id="one_map_overview",
        display_name="一图看懂（总览三列）",
        skill_path="scenarios/one-map-overview/SKILL.md",
        generator=gen_one_map_overview,
    ),
    "product_collection": SceneSpec(
        scene_id="product_collection",
        display_name="产品介绍（有赞收款）",
        skill_path="scenarios/product-collection/SKILL.md",
        generator=gen_product_collection,
    ),
    "demand_pure_collection": SceneSpec(
        scene_id="demand_pure_collection",
        display_name="业务需求①纯收款",
        skill_path="scenarios/demand-pure-collection/SKILL.md",
        generator=gen_demand_pure_collection,
    ),
    "demand_collection_with_split": SceneSpec(
        scene_id="demand_collection_with_split",
        display_name="业务需求②收款+分账（有赞通道）",
        skill_path="scenarios/demand-collection-with-split/SKILL.md",
        generator=gen_demand_collection_with_split,
    ),
    "demand_mixed_channel_split": SceneSpec(
        scene_id="demand_mixed_channel_split",
        display_name="业务需求③收款+分账（保留原通道）",
        skill_path="scenarios/demand-mixed-channel-split/SKILL.md",
        generator=gen_demand_mixed_channel_split,
    ),
    "value_pyramid": SceneSpec(
        scene_id="value_pyramid",
        display_name="商业价值三层金字塔",
        skill_path="scenarios/value-pyramid/SKILL.md",
        generator=gen_value_pyramid,
    ),
    "split_account_overview": SceneSpec(
        scene_id="split_account_overview",
        display_name="分账场景总览",
        skill_path="scenarios/split-account-overview/SKILL.md",
        generator=gen_split_account_overview,
    ),
    "store_commission": SceneSpec(
        scene_id="store_commission",
        display_name="门店抽佣",
        skill_path="scenarios/store-commission/SKILL.md",
        generator=gen_store_commission,
    ),
    "franchise_fee_management": SceneSpec(
        scene_id="franchise_fee_management",
        display_name="加盟费管理",
        skill_path="scenarios/franchise-fee-management/SKILL.md",
        generator=gen_franchise_fee_management,
    ),
    "public_platform_split": SceneSpec(
        scene_id="public_platform_split",
        display_name="公域平台分账",
        skill_path="scenarios/public-platform-split/SKILL.md",
        generator=gen_public_platform_split,
    ),
    "stored_value_split": SceneSpec(
        scene_id="stored_value_split",
        display_name="储值分账",
        skill_path="scenarios/stored-value-split/SKILL.md",
        generator=gen_stored_value_split,
    ),
    "rights_card_split": SceneSpec(
        scene_id="rights_card_split",
        display_name="权益卡分账",
        skill_path="scenarios/rights-card-split/SKILL.md",
        generator=gen_rights_card_split,
    ),
}


def _render_slide(slide: Slide) -> str:
    lines = [f"# {slide.title}"]
    if slide.subtitle:
        lines.append(f"## {slide.subtitle}")
    for bullet in slide.bullets:
        if _clean_text(bullet):
            lines.append(f"- {bullet}")
    return "\n".join(lines)


def _render_cover(deck_title: str, deck_subtitle: str, cover_points: list[str] | None = None) -> str:
    lines = [f"# {deck_title}"]
    if deck_subtitle:
        lines.append(f"## {deck_subtitle}")
    for point in cover_points or []:
        if _clean_text(point):
            lines.append(f"- {point}")
    return "\n".join(lines)


def _load_json_from_args(input_json: str | None, input_file: str | None) -> dict[str, Any]:
    if input_json and input_file:
        raise ValueError("--input-json 与 --input-file 只能二选一")
    if input_json:
        loaded = json.loads(input_json)
        if not isinstance(loaded, dict):
            raise ValueError("--input-json 必须是 JSON object")
        return loaded
    if input_file:
        loaded = json.loads(Path(input_file).read_text(encoding="utf-8"))
        if not isinstance(loaded, dict):
            raise ValueError("--input-file 内容必须是 JSON object")
        return loaded
    return {}


def _generate_single_scene(scene_id: str, payload: dict[str, Any]) -> str:
    if scene_id not in SCENES:
        raise ValueError(f"未知场景: {scene_id}")
    slide = SCENES[scene_id].generator(payload)
    return _render_slide(slide)


def _generate_plan(plan: dict[str, Any], include_cover: bool, deck_title: str, deck_subtitle: str) -> str:
    scenes = plan.get("scenes", [])
    if not isinstance(scenes, list) or not scenes:
        raise ValueError("plan.scenes 不能为空，且必须是数组")

    blocks: list[str] = []
    cover = plan.get("cover", {}) if isinstance(plan.get("cover", {}), dict) else {}
    if include_cover:
        blocks.append(
            _render_cover(
                deck_title=cover.get("title", deck_title),
                deck_subtitle=cover.get("subtitle", deck_subtitle),
                cover_points=_as_list(cover.get("points", [])),
            )
        )

    for idx, item in enumerate(scenes):
        if not isinstance(item, dict):
            raise ValueError(f"plan.scenes[{idx}] 必须是 object")
        scene_id = _clean_text(item.get("scene"))
        if not scene_id:
            raise ValueError(f"plan.scenes[{idx}].scene 不能为空")
        payload = item.get("input", {})
        if payload is None:
            payload = {}
        if not isinstance(payload, dict):
            raise ValueError(f"plan.scenes[{idx}].input 必须是 object")
        blocks.append(_generate_single_scene(scene_id, payload))

    return "\n\n---\n\n".join(blocks).strip() + "\n"


def _print_scene_list() -> None:
    print("可用场景：")
    for scene_id in sorted(SCENES.keys()):
        spec = SCENES[scene_id]
        print(f"- {scene_id}: {spec.display_name} ({spec.skill_path})")


def main() -> None:
    parser = argparse.ArgumentParser(description="按业务场景生成 slides.md（用于销售讲义/PPT）")
    parser.add_argument("--list-scenes", action="store_true", help="列出全部场景")
    parser.add_argument("--scene", help="单场景 ID，如 demand_pure_collection")
    parser.add_argument("--input-json", help="单场景输入 JSON 字符串")
    parser.add_argument("--input-file", help="单场景输入 JSON 文件")
    parser.add_argument("--plan-file", help="批量场景计划 JSON 文件")
    parser.add_argument("--deck-title", default="有赞支付", help="封面主标题（默认用于含封面输出）")
    parser.add_argument("--deck-subtitle", default="收款&分账解决方案", help="封面副标题")
    parser.add_argument("--no-cover", action="store_true", help="不输出封面（默认输出）")
    parser.add_argument("-o", "--output", default="", help="输出 md 文件路径；不传则打印到 stdout")
    args = parser.parse_args()

    if args.list_scenes:
        _print_scene_list()
        return

    if bool(args.scene) == bool(args.plan_file):
        print("必须且只能选择一种输入方式：--scene 或 --plan-file", file=sys.stderr)
        sys.exit(2)

    try:
        if args.scene:
            payload = _load_json_from_args(args.input_json, args.input_file)
            body = _generate_single_scene(args.scene, payload)
            if args.no_cover:
                output_md = body + "\n"
            else:
                output_md = (
                    _render_cover(args.deck_title, args.deck_subtitle)
                    + "\n\n---\n\n"
                    + body
                    + "\n"
                )
        else:
            plan = json.loads(Path(args.plan_file).read_text(encoding="utf-8"))
            if not isinstance(plan, dict):
                raise ValueError("--plan-file 内容必须是 JSON object")
            output_md = _generate_plan(
                plan=plan,
                include_cover=not args.no_cover,
                deck_title=args.deck_title,
                deck_subtitle=args.deck_subtitle,
            )
    except Exception as exc:
        print(f"生成失败: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        Path(args.output).write_text(output_md, encoding="utf-8")
        print(f"Saved: {args.output}")
    else:
        print(output_md)


if __name__ == "__main__":
    main()
