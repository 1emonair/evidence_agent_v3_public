"""只读第二章冻结结果和证据回链。本包不写这些文件。"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd

from .constants import ITEMS, LEVEL


def resolve_part2_data() -> Path:
    """兼容一层或两层 Part2_final_v1；可用 ABRI_PART2_DATA 覆盖。"""
    env = os.environ.get("ABRI_PART2_DATA")
    if env:
        p = Path(env)
        if (p / "01_指数结果" / "bbri_v5.csv").exists():
            return p
        raise FileNotFoundError(f"ABRI_PART2_DATA 无效：{p}")

    root = Path(__file__).resolve().parents[2]
    candidates = [
        root / "Part2_final_v1" / "Part2_final_v1" / "02_数据",
        root / "Part2_final_v1" / "02_数据",
    ]
    for c in candidates:
        if (c / "01_指数结果" / "bbri_v5.csv").exists():
            return c
    raise FileNotFoundError(
        "找不到 bbri_v5.csv。请把 Part2_final_v1 放在上级目录，"
        "或设置 ABRI_PART2_DATA 指向含 01_指数结果 的 02_数据 目录。"
    )


PART2 = resolve_part2_data()


def _read(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path, encoding="utf-8-sig")


def load_ai_corpus() -> dict[str, str]:
    """第二章的 AI 段落语料（公开年报摘取），只读。缺文件时漏检复查跳过。"""
    p = resolve_part2_data() / "02_中间数据" / "probe_ai_corpus.jsonl"
    if not p.exists():
        return {}
    out = {}
    with p.open(encoding="utf-8") as f:
        for line in f:
            d = json.loads(line)
            out[str(d["document_id"])] = d.get("ai_text") or ""
    return out


def load_frames() -> dict:
    base = resolve_part2_data()
    firm = _read(base / "01_指数结果" / "bbri_v5.csv")
    opacity = _read(base / "02_中间数据" / "opacity_v2.csv")
    evidence = _read(base / "02_中间数据" / "evi_l2_backlink_v2.csv")
    filings = _read(base / "02_中间数据" / "cac_filings_typed.csv")
    firm["entity_id"] = firm["entity_id"].astype(str).str.zfill(6)
    opacity["entity_id"] = opacity["entity_id"].astype(str).str.zfill(6)
    evidence["entity_id"] = evidence["entity_id"].astype(str).str.zfill(6)
    filings["entity_id"] = filings["entity_id"].astype(str).str.zfill(6)
    return {
        "firm": firm, "opacity": opacity, "evidence": evidence, "filings": filings,
        "ai_corpus": load_ai_corpus(),
    }


def frozen_profile(firm: pd.DataFrame, name: str) -> dict:
    hit = firm[firm["entity_name"] == name]
    if hit.empty:
        raise SystemExit(f"冻结样本中没有这家企业：{name}")
    r = hit.iloc[0]
    return {
        "entity_name": name,
        "entity_id": str(r["entity_id"]).zfill(6),
        "ABRI_T": round(float(r["ABRI_T"]), 2),
        "T_tier": str(r["T_tier"]),
        "tier": int(r["tier"]),
        "O_eq": round(float(r["O_eq"]), 2),
        "S_score": round(float(r["S_score"]), 2),
        "S_high": int(r["S_high"]),
        "red_flag": int(r["red_flag"]),
        "EVC": round(float(r["EVC"]), 2),
        "filed": int(r["filed"]),
    }


def o_from_levels(levels: list[str]) -> float:
    vals = [LEVEL[lv] for lv in levels]
    return sum(vals) / len(vals) / 3 * 100


def year_levels(opacity: pd.DataFrame, entity_id: str) -> list[dict]:
    rows = opacity[opacity["entity_id"] == entity_id]
    out = []
    for _, r in rows.iterrows():
        out.append({
            "document_id": r["document_id"],
            "fiscal_year": int(r["fiscal_year"]),
            "levels": {item: r[f"{item}_lv"] for item in ITEMS},
        })
    return out
