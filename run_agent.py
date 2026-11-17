"""科创企业算法治理证据核验与核保辅助 Agent（v3）。

    python run_agent.py demo
    python run_agent.py firm --name 金现代
    python run_agent.py firm --name 天源迪科 --judge llm
    python run_agent.py boundary                 # 红旗可翻转的企业：strict / loose / 上界
    python run_agent.py sweep                    # 369 家全量：待人工名单 + 补件函
    python run_agent.py queue                    # 审批队列概况
    python run_agent.py approve --card-id DOC:ITEM:KW --decision reject --reviewer alice
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from core.approve import QUEUE, queue_stats, record_decision  # noqa: E402
from core.audit import append_event  # noqa: E402
from core.data import frozen_profile, load_frames, resolve_part2_data  # noqa: E402
from core.loop import run_firm  # noqa: E402
from core.permissions import check_mode  # noqa: E402
from core.report import followup_letter, write_report  # noqa: E402

# 客户服务撞词、算法缩写撞词、运维理念撞词、备案提及、无 L2 的红旗户、红旗户 ITIL、法规引用、客户培训
DEMO = ["国华网安", "新开普", "网宿科技", "天源迪科", "科大讯飞", "金现代", "中孚信息", "梦网科技"]
OUT = Path(__file__).resolve().parent / "output"


def _line(result: dict) -> str:
    p, sc = result["profile"], result["scenario"]
    n_bad = sum(c["status"] == "不支持" for c in result["cards"])
    n_pending = sum(c["status"] == "待人工" for c in result["cards"])

    def f(k):
        s = sc[k]
        return f"{s['O_prime']}/{s['red_flag_prime']}{'*' if s['flip'] else ''}"

    return (
        f"{p['entity_name']} ABRI-T={p['ABRI_T']} {p['T_tier']} O={p['O_eq']} 红旗={p['red_flag']} | "
        f"复查卡={len(result['cards'])} 不支持={n_bad} 待人工={n_pending} 升级卡={len(result['upgrade_cards'])} | "
        f"strict {f('strict')}  loose {f('loose')}  上界 {f('strict_upper')}"
    )


def once(frames, name: str, mode: str) -> dict:
    check_mode(mode)
    profile = frozen_profile(frames["firm"], name)
    result = run_firm(name, frames, profile, mode)
    path = write_report(result, OUT)
    print(_line(result))
    print(f"  → {path}")
    return result


def _flip_reachable(firm) -> list[str]:
    """只有 T4/T5 且 S 高的企业，红旗才可能随 O′ 翻转。"""
    m = firm[firm["T_tier"].isin(["T4", "T5"]) & (firm["S_high"] == 1)]
    return m.sort_values("O_eq", ascending=False)["entity_name"].tolist()


def _summary_row(result: dict) -> dict:
    p, sc = result["profile"], result["scenario"]
    row = {
        "entity_name": p["entity_name"], "ABRI_T": p["ABRI_T"], "T_tier": p["T_tier"],
        "S_high": p["S_high"], "O_frozen": p["O_eq"], "red_frozen": p["red_flag"],
        "n_review": len(result["cards"]),
        "n_unsupported": sum(c["status"] == "不支持" for c in result["cards"]),
        "n_unverified": sum(c["status"] == "披露但未核实" for c in result["cards"]),
        "n_verified": sum(c["status"] == "已核实" for c in result["cards"]),
        "n_pending": sum(c["status"] == "待人工" for c in result["cards"]),
        "n_upgrade": len(result["upgrade_cards"]),
    }
    for k in ("strict", "loose", "strict_upper"):
        row[f"O_{k}"] = sc[k]["O_prime"]
        row[f"red_{k}"] = sc[k]["red_flag_prime"]
        row[f"flip_{k}"] = sc[k]["flip"]
    return row


def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8-sig")
        return
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def _flip_report(rows: list[dict]) -> None:
    for k in ("strict", "loose", "strict_upper"):
        down = [r["entity_name"] for r in rows if r[f"flip_{k}"] < 0]
        up = [r["entity_name"] for r in rows if r[f"flip_{k}"] > 0]
        print(f"  {k:<13} 红旗 1→0：{len(down)} 家 {down}")
        print(f"  {'':<13} 红旗 0→1：{len(up)} 家 {up}")


def cmd_boundary(frames, mode: str) -> None:
    names = _flip_reachable(frames["firm"])
    print(f"红旗可翻转集合（T4/T5 且 S 高）：{len(names)} 家，其中冻结红旗 "
          f"{int(frames['firm'][frames['firm'].entity_name.isin(names)].red_flag.sum())} 家")
    rows = []
    for n in names:
        r = run_firm(n, frames, frozen_profile(frames["firm"], n), mode)
        write_report(r, OUT / "boundary")
        rows.append(_summary_row(r))
        print(" ", _line(r))
    _write_csv(OUT / "boundary" / "boundary_summary.csv", rows)
    print("\n翻转汇总：")
    _flip_report(rows)
    print(f"  → {OUT / 'boundary' / 'boundary_summary.csv'}")


def cmd_sweep(frames, mode: str) -> None:
    t0 = time.perf_counter()
    names = frames["firm"]["entity_name"].tolist()
    rows, pending, letters = [], [], []
    for n in names:
        r = run_firm(n, frames, frozen_profile(frames["firm"], n), mode, audit=False)
        rows.append(_summary_row(r))
        for c in r["cards"] + r["upgrade_cards"]:
            if c["status"] in {"待人工", "升级候选"}:
                pending.append({
                    "card_id": c["card_id"], "kind": c["kind"], "entity_name": n,
                    "fiscal_year": c["fiscal_year"], "item": c["item"], "keyword": c["keyword"],
                    "status": c["status"], "label": c["label"], "snippet": c["snippet"],
                })
        letter = followup_letter(r)
        if letter:
            letters.append(f"## {n}\n\n{letter}\n")
    sec = time.perf_counter() - t0
    d = OUT / "sweep"
    _write_csv(d / "sweep_summary.csv", rows)
    _write_csv(d / "待人工名单.csv", pending)
    (d / "补件函_汇总.md").write_text("# 补件函汇总\n\n" + "\n".join(letters), encoding="utf-8")
    tot = {k: sum(r[k] for r in rows) for k in ("n_review", "n_unsupported", "n_unverified", "n_verified", "n_pending", "n_upgrade")}
    append_event({"event": "sweep", "mode": mode, "n_firms": len(rows), **tot, "seconds": round(sec, 2)})
    print(f"全量 {len(rows)} 家，用时 {sec:.1f}s")
    print(f"  复查卡 {tot['n_review']}：不支持 {tot['n_unsupported']}，披露但未核实 {tot['n_unverified']}，"
          f"已核实 {tot['n_verified']}，待人工 {tot['n_pending']}")
    print(f"  升级卡 {tot['n_upgrade']}；待人工名单 {len(pending)} 行；补件函 {len(letters)} 封")
    _flip_report(rows)
    print(f"  → {d}")


def cmd_approve(args: argparse.Namespace) -> None:
    try:
        rec = record_decision(args.card_id, args.decision, args.reviewer, args.note or "")
    except KeyError:
        raise SystemExit(f"队列中没有 {args.card_id}")
    append_event({"event": "human_approval", **rec, "reviewer": args.reviewer, "note": args.note or ""})
    print(f"已记录：{args.card_id} {rec['before']} → {rec['after']} by {args.reviewer}")
    print(f"重新运行 `python run_agent.py firm --name {rec['entity_name']}` 即可看到情景列变化。")


def main() -> None:
    parser = argparse.ArgumentParser(description="证据核验 Agent v3（不改冻结分数）")
    parser.add_argument("--judge", choices=["rules", "llm"], default=None, help="覆盖 EVIDENCE_JUDGE")
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("demo", "boundary", "sweep"):
        sp = sub.add_parser(name)
        sp.add_argument("--mode", choices=["research", "diligence"], default="research")
    firm = sub.add_parser("firm")
    firm.add_argument("--name", required=True)
    firm.add_argument("--mode", choices=["research", "diligence"], default="research")
    batch = sub.add_parser("batch")
    batch.add_argument("--names", required=True, help="逗号分隔企业名")
    batch.add_argument("--mode", choices=["research", "diligence"], default="research")
    ap = sub.add_parser("approve")
    ap.add_argument("--card-id", required=True)
    ap.add_argument("--decision", choices=["accept", "reject"], required=True)
    ap.add_argument("--reviewer", required=True)
    ap.add_argument("--note", default="")
    sub.add_parser("queue")
    sub.add_parser("info")

    args = parser.parse_args()
    if args.judge:
        os.environ["EVIDENCE_JUDGE"] = args.judge

    if args.cmd == "info":
        print("PART2_DATA =", resolve_part2_data())
        print("EVIDENCE_JUDGE =", os.environ.get("EVIDENCE_JUDGE", "rules"))
        print("LLM key set =", bool(os.environ.get("EVIDENCE_LLM_API_KEY") or os.environ.get("OPENAI_API_KEY")))
        print("QUEUE =", QUEUE, queue_stats())
        return
    if args.cmd == "queue":
        print(QUEUE, queue_stats())
        return
    if args.cmd == "approve":
        cmd_approve(args)
        return

    frames = load_frames()
    if args.cmd == "demo":
        for name in DEMO:
            once(frames, name, args.mode)
    elif args.cmd == "batch":
        for name in [x.strip() for x in args.names.split(",") if x.strip()]:
            once(frames, name, args.mode)
    elif args.cmd == "boundary":
        cmd_boundary(frames, args.mode)
    elif args.cmd == "sweep":
        cmd_sweep(frames, args.mode)
    else:
        once(frames, args.name, args.mode)


if __name__ == "__main__":
    main()
