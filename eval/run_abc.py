"""A / A′ / B / C 对照（语义轴：这条命中算不算本企业治理证据）。

A   冻结口径的实际行为：关键词命中即记 L2（第二章 O 就是这么算的）
A′  第二章审计结论 counts_as_L2（只在 gold 上有意义；silver 标签就来自它）
B   只调 judge()，只看命中句
C   Agent 循环：judge → 按缺口扩上下文 / 查编号 / 跨年比对

待人工不算错，单列为覆盖率：
  coverage          自动给出结论的比例
  acc_decided       自动结论的准确率
  不算类 P/R/F1     待人工按「保持原判=算」计（保守口径）
  flag_recall       不算类中「被判不算或送人工」的比例（核保实际能看到的召回）

    python eval/run_abc.py               # 规则
    python eval/run_abc.py --judge llm   # 有密钥时 B/C 用大模型
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

HERE = Path(__file__).resolve().parent
EVAL = HERE / "eval_set.csv"


def metrics(gold: list[str], pred: list[str]) -> dict:
    n = len(gold)
    decided = [(g, p) for g, p in zip(gold, pred) if p != "待人工"]
    cov = len(decided) / n if n else 0.0
    acc_d = sum(g == p for g, p in decided) / len(decided) if decided else 0.0
    keep = ["算" if p == "待人工" else p for p in pred]
    tp = sum(g == "不算" and p == "不算" for g, p in zip(gold, keep))
    fp = sum(g != "不算" and p == "不算" for g, p in zip(gold, keep))
    fn = sum(g == "不算" and p != "不算" for g, p in zip(gold, keep))
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    n_neg = sum(g == "不算" for g in gold)
    flagged = sum(g == "不算" and p in {"不算", "待人工"} for g, p in zip(gold, pred))
    n_pos = sum(g == "算" for g in gold)
    pos_sent = sum(g == "算" and p != "算" for g, p in zip(gold, pred))
    return {
        "n": n, "n_不算": n_neg, "n_算": n_pos,
        "coverage": round(cov, 4),
        "acc_decided": round(acc_d, 4),
        "acc_pending_as_keep": round(sum(g == k for g, k in zip(gold, keep)) / n, 4) if n else 0.0,
        "不算_precision": round(prec, 4),
        "不算_recall": round(rec, 4),
        "不算_f1": round(2 * prec * rec / (prec + rec), 4) if prec + rec else 0.0,
        "flag_recall": round(flagged / n_neg, 4) if n_neg else None,
        "算_被打扰率": round(pos_sent / n_pos, 4) if n_pos else None,
        "tp": tp, "fp": fp, "fn": fn,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--judge", choices=["rules", "llm"], default="rules")
    args = ap.parse_args()
    os.environ["EVIDENCE_JUDGE"] = args.judge

    from core.data import load_frames
    from core.judge import judge, semantic_of
    from core.loop import verify_row
    from core.tools import ToolKit

    if not EVAL.exists():
        raise SystemExit("先运行：python eval/build_eval_set.py")
    df = pd.read_csv(EVAL, encoding="utf-8-sig")
    df["entity_id"] = df["entity_id"].astype(str).str.zfill(6)
    frames = load_frames()
    tools = ToolKit(frames["evidence"], frames["filings"], "research", frames["ai_corpus"])

    preds, secs = {}, {}
    t0 = time.perf_counter()
    preds["A_keyword"] = ["算"] * len(df)
    secs["A_keyword"] = time.perf_counter() - t0
    preds["A2_ch2_audit"] = ["算" if int(x) == 1 else "不算" for x in df["counts_as_L2"]]
    secs["A2_ch2_audit"] = 0.0

    t0 = time.perf_counter()
    b, backends = [], []
    for r in df.itertuples():
        j = judge(str(r.sentence), str(r.keyword), str(r.item))
        b.append(semantic_of(j))
        backends.append(j.backend)
    preds["B_judge_only"] = b
    secs["B_judge_only"] = time.perf_counter() - t0

    t0 = time.perf_counter()
    c, cert, cite_ok, labels, rescued = [], [], [], [], []
    for _, r in df.iterrows():
        card = verify_row(r, tools)
        rescued.append(bool(card.get("other_support")))
        c.append(card["semantic"])
        cert.append(card["cert_id_found"])
        cite_ok.append(bool(card.get("citation")))
        labels.append(card["label"])
    preds["C_agent"] = c
    secs["C_agent"] = time.perf_counter() - t0

    subsets = {
        "gold_all": df["label_source"].str.startswith("gold"),
        "gold_dev": df["label_source"].str.startswith("gold") & (df["split"] == "dev"),
        "gold_test": df["label_source"].str.startswith("gold") & (df["split"] == "test"),
        "silver_all": df["label_source"].str.startswith("silver"),
        "human": df["label_source"].str.startswith("human"),
    }
    res = {
        "judge_backend": args.judge,
        "backends_seen": sorted(set(backends)),
        "n_rows": len(df), "n_firms": int(df.entity_name.nunique()),
        "label_sources": {k: int(v) for k, v in df["label_source"].value_counts().items()},
        "seconds_per_row": {k: round(v / max(len(df), 1), 6) for k, v in secs.items()},
        "subsets": {},
    }
    for name, mask in subsets.items():
        if not mask.any():
            continue
        gold = df.loc[mask, "gold"].tolist()
        idx = [i for i, m in enumerate(mask) if m]
        res["subsets"][name] = {
            sys_: metrics(gold, [p[i] for i in idx])
            for sys_, p in preds.items()
            if not (sys_ == "A2_ch2_audit" and name == "silver_all")
        }
    c_pos = [i for i, s in enumerate(c) if s == "算"]
    res["verify_axis"] = {
        "C_判为算的行": len(c_pos),
        "其中找到编号": int(sum(cert[i] for i in c_pos)),
        "编号率": round(sum(cert[i] for i in c_pos) / len(c_pos), 4) if c_pos else 0.0,
    }
    res["citation_rate_C"] = round(sum(cite_ok) / len(df), 4)
    gmask = df["label_source"].str.startswith("gold")
    res["same_doc_search"] = {
        "命中句不算_但同年报他处支持的行": int(sum(rescued)),
        "其中gold为不算的行": int(sum(1 for i, x in enumerate(rescued) if x and gmask.iloc[i] and df["gold"].iloc[i] == "不算")),
        "含义": "这些行命中句本身不成立，但该格不应降级；只影响情景列，不影响命中级准确率",
    }
    res["note"] = (
        "全部为实测。gold 中 agent_draft 由开发者读原文标注，规则 v3 开发时这些原文可见，"
        "dev/test 拆分只能防企业内泄漏、不能防开发者泄漏；对外结论应以 annotation_sheet 双人标注结果为准。"
    )

    tag = args.judge
    (HERE / f"abc_results_{tag}.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    out = df[["entity_name", "fiscal_year", "item", "keyword", "gold", "label_source", "split"]].copy()
    for k, v in preds.items():
        out[f"pred_{k}"] = v
    out["C_label"] = labels
    out["C_cert_id"] = cert
    out["C_same_doc_support"] = rescued
    out.to_csv(HERE / f"abc_predictions_{tag}.csv", index=False, encoding="utf-8-sig")

    print(f"backend={tag} seen={res['backends_seen']}  rows={len(df)} firms={res['n_firms']}")
    hdr = f"{'subset':<11}{'system':<14}{'n':>4}{'cov':>7}{'accD':>7}{'P不算':>7}{'R不算':>7}{'F1':>7}{'flagR':>7}{'扰算':>7}"
    print(hdr)
    for sname, d in res["subsets"].items():
        for sys_, m in d.items():
            fr = "-" if m["flag_recall"] is None else f"{m['flag_recall']:.2f}"
            dr = "-" if m["算_被打扰率"] is None else f"{m['算_被打扰率']:.2f}"
            print(f"{sname:<11}{sys_:<14}{m['n']:>4}{m['coverage']:>7.2f}{m['acc_decided']:>7.2f}"
                  f"{m['不算_precision']:>7.2f}{m['不算_recall']:>7.2f}{m['不算_f1']:>7.2f}{fr:>7}{dr:>7}")
    print("verify_axis", res["verify_axis"], "citation_rate_C", res["citation_rate_C"])
    print("seconds/row", res["seconds_per_row"])


if __name__ == "__main__":
    main()
