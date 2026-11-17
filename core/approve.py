"""人工确认节点。

队列按 card_id 唯一：重复运行不会重复入队，已有的人工决定不被覆盖。
两类卡进队列：
  复查卡（kind=review）  原记 L2、判读为待人工
  升级卡（kind=upgrade） 漏检复查找到的候选证据；只有 accept 后才进情景列
"""

from __future__ import annotations

import csv
from pathlib import Path

INBOX = Path(__file__).resolve().parents[1] / "inbox"
QUEUE = INBOX / "approval_queue.csv"
FIELDS = [
    "card_id", "kind", "entity_name", "fiscal_year", "item", "keyword",
    "status", "label", "snippet", "reason", "decision", "reviewer", "note",
]


def card_id(c: dict) -> str:
    if c.get("kind") == "upgrade":
        return f"{c['document_id']}:{c['item']}:recall:{c['keyword']}"
    return f"{c['document_id']}:{c['item']}:{c['keyword']}"


def _read() -> dict[str, dict]:
    if not QUEUE.exists():
        return {}
    with QUEUE.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    out: dict[str, dict] = {}
    for r in rows:
        r.setdefault("kind", "review")
        prev = out.get(r["card_id"])
        # 旧版本队列可能有重复行：保留已有人工决定的那一行
        if prev is None or (prev.get("decision") == "pending" and r.get("decision") != "pending"):
            out[r["card_id"]] = r
    return out


def _write(rows: dict[str, dict]) -> None:
    INBOX.mkdir(parents=True, exist_ok=True)
    with QUEUE.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows.values())


def enqueue(cards: list[dict], entity_name: str) -> int:
    rows = _read()
    added = 0
    for c in cards:
        if c.get("status") not in {"待人工", "升级候选"}:
            continue
        cid = card_id(c)
        if cid in rows:
            continue
        rows[cid] = {
            "card_id": cid,
            "kind": c.get("kind", "review"),
            "entity_name": entity_name,
            "fiscal_year": c["fiscal_year"],
            "item": c["item"],
            "keyword": c["keyword"],
            "status": c["status"],
            "label": c.get("label", ""),
            "snippet": (c.get("snippet") or "")[:200],
            "reason": c.get("reason", ""),
            "decision": "pending",
            "reviewer": "",
            "note": "",
        }
        added += 1
    if added or QUEUE.exists():
        _write(rows)
    return added


def record_decision(cid: str, decision: str, reviewer: str, note: str = "") -> dict:
    rows = _read()
    if cid not in rows:
        raise KeyError(cid)
    r = rows[cid]
    before = r.get("decision", "pending")
    r.update(decision=decision, reviewer=reviewer, note=note)
    _write(rows)
    return {"card_id": cid, "before": before, "after": decision, "entity_name": r.get("entity_name")}


def load_decisions() -> dict[str, str]:
    return {k: r["decision"] for k, r in _read().items() if r.get("decision") not in {"", "pending", None}}


def apply_decisions(cards: list[dict], decisions: dict[str, str]) -> list[dict]:
    """复查卡：reject → 不支持，accept → 已核实。升级卡：accept → 已核实（采纳升级），reject → 不支持。"""
    for c in cards:
        d = decisions.get(card_id(c))
        if d not in {"accept", "reject"}:
            continue
        c["human_decision"] = d
        c["semantic"] = "算" if d == "accept" else "不算"
        c["status"] = "已核实" if d == "accept" else "不支持"
    return cards


def queue_stats() -> dict:
    rows = _read()
    out = {"total": len(rows), "pending": 0, "accept": 0, "reject": 0, "review": 0, "upgrade": 0}
    for r in rows.values():
        out[r.get("decision") or "pending"] = out.get(r.get("decision") or "pending", 0) + 1
        out[r.get("kind") or "review"] = out.get(r.get("kind") or "review", 0) + 1
    return out
