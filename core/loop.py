"""证据核验循环：复查（原记 L2 的命中是否成立）+ 漏检复查（词表外写法），双向出卡。"""

from __future__ import annotations

import pandas as pd

from .approve import apply_decisions, card_id, enqueue, load_decisions
from .audit import append_event
from .constants import DEFAULT_POLICY, FOLLOWUP, RECALL_TERMS
from .data import year_levels
from .judge import judge
from .judge_types import semantic_of, status_of, window
from .scenario import compute
from .tools import ToolKit


def _needs_context(label: str, keyword: str) -> bool:
    return label in {"unclear", "abbreviation", "customer_service"} or keyword in {
        "DPO", "CMMI", "ITIL", "DCMM",
    }


def verify_row(row: pd.Series, tools: ToolKit) -> dict:
    keyword = str(row["keyword"])
    item = str(row["item"])
    sentence = str(row.get("sentence") or "")
    trace = []

    j = judge(sentence, keyword, item)
    trace.append(f"judge:{j.label}/{j.backend}/{j.confidence:.2f}")
    text = sentence
    if _needs_context(j.label, keyword) or j.needs_human:
        text = tools.expand_context(row)
        j = judge(text, keyword, item)
        trace.append(f"expand_context→{j.label}/{j.backend}")

    # 回链只存了关键词的一处出现；命中句不成立时，同一年报别处成立则该格不算失败
    other = None
    if semantic_of(j) == "不算":
        for w in tools.same_doc_windows(row["doc_id"], keyword):
            alt = judge(w, keyword, item)
            if semantic_of(alt) == "算":
                other = {"label": alt.label, "citation": alt.citation, "cert_id_found": tools.find_cert_id(w)}
                trace.append(f"same_doc_search→{alt.label}")
                break
        else:
            trace.append("same_doc_search:无其他支持")

    cert_id = False
    if semantic_of(j) == "算" or j.needs_human:
        cert_id = tools.find_cert_id(text)
        trace.append(f"find_cert_id:{cert_id}")

    if j.needs_human:
        years = tools.compare_years(str(row["entity_id"]), item, int(row["fiscal_year"]))
        trace.append(f"compare_years:{years}")

    filing_note = []
    if item == "M4" or "备案" in keyword:
        filing_note = tools.lookup_filing(str(row["entity_id"]))
        trace.append(f"lookup_filing:{len(filing_note)}")

    status = status_of(j, cert_id)
    reason = j.reason
    if other:
        status = "已核实" if other["cert_id_found"] else "披露但未核实"
        reason = f"命中句本身不成立（{j.label}）；同一年报他处支持（{other['label']}），该格不降级。"
    return {
        "kind": "review",
        "entity_name": row["entity_name"],
        "fiscal_year": int(row["fiscal_year"]),
        "document_id": row["doc_id"],
        "item": item,
        "keyword": keyword,
        "frozen_level": "L2",
        "ch2_counts_as_L2": int(row.get("counts_as_L2") or 0),
        "ch2_verdict": str(row.get("verdict") or ""),
        "semantic": semantic_of(j),
        "cert_id_found": bool(cert_id),
        "status": status,
        "label": j.label,
        "confidence": j.confidence,
        "citation": j.citation,
        "other_support": other["citation"] if other else "",
        "reason": reason,
        "needs_human": j.needs_human,
        "backend": j.backend,
        "snippet": window(text, keyword, 36),
        "tool_trace": trace,
        "filing_note": filing_note,
        "followup": FOLLOWUP.get(item, "请提供可核对的证明材料。") if status != "已核实" else "",
    }


def recall_cards(entity_name: str, years: list[dict], tools: ToolKit) -> list[dict]:
    out = []
    for doc in years:
        for item, frozen in doc["levels"].items():
            if frozen == "L2" or item not in RECALL_TERMS:
                continue
            for term, text in tools.recall_search(doc["document_id"], item):
                j = judge(text, term, item)
                if semantic_of(j) != "算":
                    continue
                cert = tools.find_cert_id(window(text, term, 80))
                out.append({
                    "kind": "upgrade",
                    "entity_name": entity_name,
                    "fiscal_year": doc["fiscal_year"],
                    "document_id": doc["document_id"],
                    "item": item,
                    "keyword": term,
                    "frozen_level": frozen,
                    "semantic": "算",
                    "cert_id_found": bool(cert),
                    "status": "升级候选",
                    "label": j.label,
                    "confidence": j.confidence,
                    "citation": j.citation,
                    "reason": "词表外写法命中，判读为本企业持证/已备案；需人工确认后才升 L2。" + j.reason,
                    "needs_human": True,
                    "backend": j.backend,
                    "snippet": window(text, term, 36),
                    "tool_trace": [f"recall_search:{term}", f"judge:{j.label}/{j.backend}", f"find_cert_id:{cert}"],
                    "filing_note": [],
                    "followup": FOLLOWUP.get(item, "请提供可核对的证明材料。"),
                })
                break  # 每格一张升级卡足够
    return out


def _dedup(cards: list[dict]) -> list[dict]:
    seen, out = set(), []
    for c in cards:
        cid = card_id(c)
        if cid in seen:
            continue
        seen.add(cid)
        c["card_id"] = cid
        out.append(c)
    return out


CERT_VALID_YEARS = 3


def _cross_year(cards: list[dict], tools: ToolKit) -> list[dict]:
    """某年判不支持、但相邻有效期内同一关键词有持证陈述：不自动降级，转人工。"""
    held = {}
    for c in cards:
        if c["semantic"] == "算" or c.get("other_support"):
            held.setdefault((c["item"], c["keyword"]), set()).add(c["fiscal_year"])
    for c in cards:
        if c["status"] != "不支持":
            continue
        yrs = held.get((c["item"], c["keyword"]), set())
        near = sorted(y for y in yrs if 0 < abs(y - c["fiscal_year"]) <= CERT_VALID_YEARS)
        if near:
            tools.calls.append("compare_years")
            c["status"] = "待人工"
            c["needs_human"] = True
            c["tool_trace"].append(f"compare_years→{near}有持证陈述")
            c["reason"] += f" 但 {near} 年同一关键词有持证陈述，可能仍在有效期内，不自动降级。"
    return cards


def _suggest(profile: dict, sc: dict, review: list[dict], upgrades: list[dict]) -> str:
    main = sc[DEFAULT_POLICY]
    parts = []
    if main["flip"]:
        parts.append(f"strict 情景红旗 {profile['red_flag']}→{main['red_flag_prime']}，转人工复核 O 的证据基础。")
    if sc["loose"]["flip"] and not main["flip"]:
        parts.append("仅在 loose 口径下红旗翻转，属口径敏感，不作结论。")
    if sc["strict_upper"]["flip"] and not main["flip"]:
        parts.append("若待定升级卡被人工采纳，红旗会翻转；请优先审批这些升级卡。")
    if any(c["status"] == "不支持" for c in review):
        parts.append("部分原记 L2 的命中不构成本企业证据，已出补件项。")
    if any(c["status"] == "待人工" for c in review) or upgrades:
        parts.append("有卡片待人工确认，已写入审批队列。")
    if not review and not upgrades:
        parts.append("无 L2 原文可复查、也未发现词表外证据。按未披露处理，不把沉默当作治理失败。")
    if profile["tier"] >= 4 and profile["EVC"] <= 0:
        parts.append("冻结口径为高暴露且无可核验证据。")
    parts.append("本 Agent 不改冻结分数、相对因子和承保结论。")
    return " ".join(parts)


def run_firm(name: str, frames: dict, profile: dict, mode: str, enqueue_cards: bool = True,
             audit: bool = True) -> dict:
    tools = ToolKit(frames["evidence"], frames["filings"], mode, frames.get("ai_corpus"))
    rows = frames["evidence"][frames["evidence"]["entity_name"] == name]
    years = year_levels(frames["opacity"], profile["entity_id"])

    review = _cross_year(_dedup([verify_row(row, tools) for _, row in rows.iterrows()]), tools)
    upgrades = _dedup(recall_cards(name, years, tools))

    n_queued = enqueue(review + upgrades, name) if enqueue_cards else 0
    decisions = load_decisions()
    review = apply_decisions(review, decisions)
    upgrades = apply_decisions(upgrades, decisions)

    sc = compute(profile, years, review, upgrades)
    result = {
        "mode": mode,
        "profile": profile,
        "cards": review,
        "upgrade_cards": upgrades,
        "scenario": sc,
        "suggestion": _suggest(profile, sc, review, upgrades),
        "tools_used": tools.calls,
        "approval_queued": n_queued,
        "n_years": len(years),
    }
    if audit:
        append_event({
            "event": "firm_run",
            "mode": mode,
            "entity_name": name,
            "n_review": len(review),
            "n_upgrade": len(upgrades),
            "n_unsupported": sum(c["status"] == "不支持" for c in review),
            "n_pending": sum(c["status"] == "待人工" for c in review),
            "approval_queued": n_queued,
            "O_strict": sc["strict"]["O_prime"],
            "O_loose": sc["loose"]["O_prime"],
            "red_strict": sc["strict"]["red_flag_prime"],
            "red_loose": sc["loose"]["red_flag_prime"],
            "human_decisions_applied": sum(1 for c in review + upgrades if c.get("human_decision")),
        })
    return result
