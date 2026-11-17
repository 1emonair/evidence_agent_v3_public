"""情景列 O′ / 红旗′。只读冻结层级，输出另起一列，不回写第二章任何文件。

降级以「文档 × 指标项」格子为单位，一张卡失败不连坐同格的其他卡：
  strict（主结果）：格子内全部复查卡都是「不支持」→ L2 降到 L0
  loose（稳健性）  ：格子内没有已核实、没有待人工，且全部卡是不支持/披露但未核实
                     → 全不支持降 L0，否则降 L1b
  任何一张卡仍待人工 → 该格两档都不动
升级：漏检复查的升级卡，人工 accept 后把该格升到 L2（两档相同）。
upper 列另算「如果待定升级卡全部被采纳」，只作上界展示。
"""

from __future__ import annotations

from collections import defaultdict

from .constants import ITEMS, O_MEDIAN, POLICIES
from .data import o_from_levels


def _cell_level(frozen: str, statuses: list[str], policy: str) -> str:
    if frozen != "L2" or not statuses:
        return frozen
    if "待人工" in statuses or "已核实" in statuses:
        return frozen
    if all(s == "不支持" for s in statuses):
        return "L0"
    if policy == "loose" and all(s in {"不支持", "披露但未核实"} for s in statuses):
        return "L1b"
    return frozen


def _red(profile: dict, o: float) -> int:
    return int(profile["T_tier"] in {"T4", "T5"} and profile["S_high"] == 1 and o >= O_MEDIAN)


def compute(profile: dict, years: list[dict], review: list[dict], upgrades: list[dict]) -> dict:
    by_cell = defaultdict(list)
    for c in review:
        by_cell[(c["document_id"], c["item"])].append(c["status"])
    accepted = {(c["document_id"], c["item"]) for c in upgrades if c["status"] == "已核实"}
    pending_up = {(c["document_id"], c["item"]) for c in upgrades if c["status"] == "升级候选"}

    out = {}
    variants = [(p, False) for p in POLICIES] + [("strict", True)]
    for policy, with_pending in variants:
        key = "strict_upper" if with_pending else policy
        os_, changes = [], []
        for doc in years:
            levels = []
            for item in ITEMS:
                frozen = doc["levels"][item]
                cell = (doc["document_id"], item)
                lv = _cell_level(frozen, by_cell.get(cell, []), policy)
                if frozen != "L2" and (cell in accepted or (with_pending and cell in pending_up)):
                    lv = "L2"
                if lv != frozen:
                    changes.append({
                        "document_id": doc["document_id"], "fiscal_year": doc["fiscal_year"],
                        "item": item, "from": frozen, "to": lv,
                    })
                levels.append(lv)
            os_.append(o_from_levels(levels))
        o_prime = round(sum(os_) / len(os_), 2) if os_ else profile["O_eq"]
        red = _red(profile, o_prime)
        out[key] = {
            "O_prime": o_prime,
            "red_flag_prime": red,
            "flip": red - profile["red_flag"],
            "n_down": sum(1 for x in changes if x["to"] in {"L0", "L1b"}),
            "n_up": sum(1 for x in changes if x["to"] == "L2"),
            "changes": changes,
        }
    return out
