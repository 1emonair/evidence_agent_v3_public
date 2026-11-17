"""构建评测集（v3）。

三层标签，来源分开记，绝不混成一个「金标」：
  gold    gold_seeds.csv 逐条读原文给出的语义标签（seed_v2 + agent_draft；后者需两名人工复核）
  silver  第二章审计结论：counts_as_L2=0（BARE/NEG/DEF/WEAK）→ 不算；POS/LIST → 算
  human   annotation_sheet.csv 中已填 adjudicated 的行（双人标注后才有）

评测轴只用「语义」：这条命中算不算本企业已落实的治理证据。
是否有编号（核实轴）单独统计，不进准确率。

按企业划分 dev/test（企业名 md5 奇偶），同一企业不跨集合。
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.data import load_frames  # noqa: E402
from core.judge_types import window  # noqa: E402

HERE = Path(__file__).resolve().parent
SEEDS = HERE / "gold_seeds.csv"
SHEET = HERE / "annotation_sheet.csv"
OUT = HERE / "eval_set.csv"
SEED = 20261115
SILVER_POS_PER_FIRM = 4
TARGET_ROWS = 300
SHEET_ROWS = 250


def split_of(name: str) -> str:
    return "test" if int(hashlib.md5(name.encode("utf-8")).hexdigest(), 16) % 2 else "dev"


def main() -> None:
    ev = load_frames()["evidence"].copy()
    ev["row_key"] = ev.index
    ev["fiscal_year"] = ev["fiscal_year"].astype(int)
    ev = ev.drop_duplicates(["doc_id", "item", "keyword"]).copy()

    seeds = pd.read_csv(SEEDS, encoding="utf-8-sig")
    seeds["fiscal_year"] = seeds["fiscal_year"].astype(int)
    keys = ["entity_name", "fiscal_year", "item", "keyword"]
    g = ev.merge(seeds, on=keys, how="inner").drop_duplicates(keys)
    missing = seeds.merge(g[keys], on=keys, how="left", indicator=True)
    missing = missing[missing["_merge"] == "left_only"]
    if len(missing):
        print("种子未匹配到回链行：")
        print(missing[keys].to_string(index=False))
    g = g.assign(gold=g["gold_semantic"], label_source=g["source"].map(lambda s: f"gold:{s}"))

    used = set(g["row_key"])
    neg = ev[(ev["counts_as_L2"] == 0) & ~ev["row_key"].isin(used)]
    neg = neg.assign(gold="不算", label_source="silver:ch2_" + neg["verdict"].astype(str), reason_type="", note="")

    pos_pool = ev[(ev["counts_as_L2"] == 1) & ~ev["row_key"].isin(used)]
    n_pos = max(TARGET_ROWS - len(g) - len(neg), 0)
    pos = (
        pos_pool.groupby("entity_name", group_keys=False)
        .apply(lambda d: d.sample(min(len(d), SILVER_POS_PER_FIRM), random_state=SEED))
        .sample(frac=1.0, random_state=SEED)
        .head(n_pos)
    )
    pos = pos.assign(gold="算", label_source="silver:ch2_" + pos["verdict"].astype(str), reason_type="", note="")

    cols = ["row_key", "entity_name", "entity_id", "fiscal_year", "item", "keyword", "verdict", "counts_as_L2",
            "sentence", "prev", "next", "doc_id", "gold", "label_source", "reason_type", "note"]
    df = pd.concat([g[cols], neg[cols], pos[cols]], ignore_index=True)

    if SHEET.exists():
        sh = pd.read_csv(SHEET, encoding="utf-8-sig")
        done = sh[sh["adjudicated"].astype(str).isin(["算", "不算"])]
        if len(done):
            h = ev.merge(done[keys + ["adjudicated"]], on=keys, how="inner")
            h = h.assign(gold=h["adjudicated"], label_source="human:adjudicated", reason_type="", note="")
            df = df[~df.set_index(keys).index.isin(h.set_index(keys).index)]
            df = pd.concat([df, h[cols]], ignore_index=True)
            print(f"并入人工双标 {len(h)} 行")

    df["split"] = df["entity_name"].map(split_of)
    df.to_csv(OUT, index=False, encoding="utf-8-sig")
    print(f"评测集 {len(df)} 行，{df.entity_name.nunique()} 家企业 → {OUT}")
    print(df.groupby(["label_source", "gold"]).size().to_string())
    print(df.groupby(["split", "gold"]).size().to_string())

    if not SHEET.exists():
        rest = ev[~ev["row_key"].isin(set(df["row_key"]))]
        rest = rest[rest["entity_name"].map(split_of) == "test"]
        sample = (
            rest.groupby("entity_name", group_keys=False)
            .apply(lambda d: d.sample(min(len(d), 3), random_state=SEED))
            .sample(frac=1.0, random_state=SEED)
            .head(SHEET_ROWS)
        )
        txt = [
            window(" ".join(str(x) for x in (r.prev, r.sentence, r.next) if str(x) != "nan"), r.keyword, 90)
            for r in sample.itertuples()
        ]
        out = sample[keys].assign(
            text=txt, annotator_1="", annotator_2="", adjudicated="", reason_type="", comment="",
        )
        out.to_csv(SHEET, index=False, encoding="utf-8-sig")
        print(f"双人标注单 {len(out)} 行（test 侧企业）→ {SHEET}")


if __name__ == "__main__":
    main()
