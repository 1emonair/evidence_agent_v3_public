"""按缺口调用的只读工具。备案查询和漏检复查都不改变任何冻结状态。"""

from __future__ import annotations

import pandas as pd

from .constants import RECALL_TERMS
from .judge_types import CERT_ID, squash


class ToolKit:
    def __init__(self, evidence: pd.DataFrame, filings: pd.DataFrame, mode: str,
                 ai_corpus: dict[str, str] | None = None):
        self.evidence = evidence
        self.filings = filings
        self.mode = mode
        self.ai_corpus = ai_corpus or {}
        self.calls: list[str] = []

    def expand_context(self, row: pd.Series) -> str:
        self.calls.append("expand_context")
        parts = [str(row.get("prev") or ""), str(row.get("sentence") or ""), str(row.get("next") or "")]
        return " ".join(p for p in parts if p and p != "nan")

    def find_cert_id(self, text: str) -> bool:
        self.calls.append("find_cert_id")
        return CERT_ID.search(squash(text)) is not None

    def compare_years(self, entity_id: str, item: str, year: int) -> list[int]:
        self.calls.append("compare_years")
        same = self.evidence[
            (self.evidence["entity_id"] == entity_id) & (self.evidence["item"] == item)
        ]
        return sorted({int(y) for y in same["fiscal_year"] if int(y) != year})

    def lookup_filing(self, entity_id: str) -> list[dict]:
        self.calls.append("lookup_filing")
        if self.mode != "diligence":
            return []
        hit = self.filings[self.filings["entity_id"] == entity_id]
        rows = []
        for _, r in hit.head(5).iterrows():
            rows.append({
                "date": str(r.get("date") or ""),
                "product": str(r.get("product") or ""),
                "note": "外部登记，不写入 ABRI-T 或 L2",
            })
        return rows

    def same_doc_windows(self, document_id: str, keyword: str, n: int = 160) -> list[str]:
        """同一份年报里该关键词的其他出现：其他回链句 + AI 段落，逐处截窗口。"""
        self.calls.append("same_doc_search")
        texts = []
        same = self.evidence[self.evidence["doc_id"] == document_id]
        for col in ("prev", "sentence", "next"):
            texts += [str(x) for x in same[col] if str(x) != "nan"]
        texts.append(self.ai_corpus.get(str(document_id), ""))
        kw = squash(keyword)
        out, seen = [], set()
        for t in texts:
            flat = squash(t)
            start = 0
            while True:
                i = flat.find(kw, start)
                if i < 0:
                    break
                w = flat[max(0, i - n): i + len(kw) + n]
                if w not in seen:
                    seen.add(w)
                    out.append(w)
                start = i + len(kw)
        return out

    def recall_search(self, document_id: str, item: str) -> list[tuple[str, str]]:
        """在该文档的 AI 段落里找词表外的同义写法，返回 (命中词, 原文)。"""
        self.calls.append("recall_search")
        text = self.ai_corpus.get(str(document_id), "")
        if not text:
            return []
        flat = squash(text)
        hits = []
        for term in RECALL_TERMS.get(item, []):
            if squash(term) in flat:
                hits.append((term, text))
        return hits
