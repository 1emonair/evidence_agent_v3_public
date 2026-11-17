"""把一次核验写成可读的工单，另出一封补件函。"""

from __future__ import annotations

import json
from pathlib import Path

from .constants import FOLLOWUP, HARD_LOCK


def _card_lines(c: dict) -> list[str]:
    head = f"### {c['fiscal_year']} {c['item']} · {c['keyword']} → {c['status']}"
    if c.get("kind") == "upgrade":
        head += f"（漏检复查，冻结层级 {c['frozen_level']}）"
    lines = [
        head,
        "",
        f"- 卡号：`{c['card_id']}`",
        f"- 引用：{c.get('citation') or c.get('snippet')}",
        f"- 判读：{c['label']}（语义={c['semantic']}，编号={'有' if c['cert_id_found'] else '无'}），{c.get('reason', '')}",
        f"- 后端：{c.get('backend')}，置信度 {c.get('confidence', 0):.2f}；工具：{' → '.join(c['tool_trace'])}",
    ]
    if c.get("other_support"):
        lines.append(f"- 同一年报他处支持：{c['other_support']}")
    if c.get("kind") == "review":
        lines.append(f"- 第二章审计：verdict={c['ch2_verdict']}，counts_as_L2={c['ch2_counts_as_L2']}")
    if c.get("human_decision"):
        lines.append(f"- 人工决定：{c['human_decision']}")
    if c["filing_note"]:
        lines.append(f"- 备案对照（不进分数）：{c['filing_note'][0].get('date', '')}")
    if c["followup"]:
        lines.append(f"- 补件：{c['followup']}")
    lines.append("")
    return lines


def followup_letter(result: dict) -> str:
    p = result["profile"]
    need = {}
    for c in result["cards"] + result["upgrade_cards"]:
        if c["status"] == "已核实":
            continue
        need.setdefault(c["item"], []).append(f"{c['fiscal_year']} 年报「{c['keyword']}」")
    if not need:
        return ""
    lines = [
        f"致 {p['entity_name']}：",
        "",
        "为完成算法治理证据核对，请就以下事项提供可核对的材料。未提供不影响已有评分，也不构成拒保或加费的依据。",
        "",
    ]
    for i, (item, refs) in enumerate(sorted(need.items()), 1):
        lines.append(f"{i}. {item}：{FOLLOWUP.get(item, '请提供可核对的证明材料。')}（涉及：{'、'.join(sorted(set(refs)))}）")
    lines += ["", "本函由证据核验辅助工具生成，经核保人员确认后发出。"]
    return "\n".join(lines)


def write_report(result: dict, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    p = result["profile"]
    name = p["entity_name"]
    slug = f"{name}_{result['mode']}"
    (out_dir / f"{slug}.json").write_text(
        json.dumps({"hard_lock": HARD_LOCK, **result}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    sc = result["scenario"]
    lines = [
        f"# {name} 证据核验工单",
        "",
        f"模式：{result['mode']}。硬锁：不改冻结分数，不改相对因子，不输出拒保或事故结论。",
        f"本次新入审批队列：{result.get('approval_queued', 0)} 张。",
        "",
        "## 冻结画像",
        "",
        f"- ABRI-T {p['ABRI_T']}，{p['T_tier']}，等权档 L{p['tier']}",
        f"- O {p['O_eq']}（{result['n_years']} 个年度均值），S {p['S_score']}，红旗 {p['red_flag']}，EVC {p['EVC']}",
        f"- 备案展示：{'有' if p['filed'] else '无'}（不参与计分）",
        "",
        f"## 复查卡（原记 L2，共 {len(result['cards'])} 张）",
        "",
    ]
    if not result["cards"]:
        lines += ["这家企业没有被记为 L2 的命中原文。", ""]
    for c in result["cards"]:
        lines += _card_lines(c)
    lines += [f"## 升级卡（漏检复查，共 {len(result['upgrade_cards'])} 张）", ""]
    if not result["upgrade_cards"]:
        lines += ["AI 段落语料中未发现词表外的持证或备案写法。", ""]
    for c in result["upgrade_cards"]:
        lines += _card_lines(c)

    lines += [
        "## 情景列（只读，不回写）",
        "",
        "| 口径 | O′ | 红旗′ | 翻转 | 降级格 | 升级格 |",
        "|---|---|---|---|---|---|",
        f"| 冻结 | {p['O_eq']} | {p['red_flag']} | - | - | - |",
    ]
    names = {"strict": "strict（主）", "loose": "loose（稳健性）", "strict_upper": "strict + 待定升级全采纳（上界）"}
    for k in ("strict", "loose", "strict_upper"):
        s = sc[k]
        lines.append(f"| {names[k]} | {s['O_prime']} | {s['red_flag_prime']} | {s['flip']:+d} | {s['n_down']} | {s['n_up']} |")
    lines += [
        "",
        "strict：同格全部卡不支持才降 L0。loose：另把无已核实的未核实格降 L1b。待人工的格子两档都不动。升级只采纳人工 accept 的卡。",
        "",
        "## 复核建议",
        "",
        result["suggestion"],
        "",
    ]
    md = out_dir / f"{slug}.md"
    md.write_text("\n".join(lines), encoding="utf-8")
    letter = followup_letter(result)
    if letter:
        (out_dir / f"{name}_补件函.md").write_text(letter, encoding="utf-8")
    return md
