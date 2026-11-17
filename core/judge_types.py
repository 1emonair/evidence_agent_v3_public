"""判读结果结构。

两个轴分开记：
  semantic：这条命中是不是「本企业已落实的治理证据」—— 算 / 不算 / 待人工
  verify  ：有没有可外部核对的编号 —— 有编号 / 无编号
三态 status 由两轴合成：不支持 / 披露但未核实 / 已核实 / 待人工。
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass

COUNTS = {"held_claim", "filing_mention"}
NOT_COUNTS = {
    "abbreviation", "customer_service", "regulation_cite", "future",
    "definition", "industry_context", "method_reference", "training", "irrelevant_context",
}
LABELS = sorted(COUNTS | NOT_COUNTS | {"unclear"})

_WS = re.compile(r"\s+")

# 可外部核对的编号：证书号字样、网信算备号、ITSS/DCMM 证书号、认证机构流水号、高企证书号
CERT_ID = re.compile(
    r"证书编号|证书号|注册号|备案号|备案编号|批准号|"
    r"网信算备\d{8,}|"
    r"[A-Z]{2,6}-[A-Z0-9]{1,6}-\d-[\d-]{6,}|"
    r"(?<![A-Z])[A-Z]\d{2}[A-Z]{2}\d{4}[A-Z0-9]{2,}|"
    r"GR20\d{8,}|"
    r"(?<![A-Z0-9])[A-Z]{1,3}\d{10,}"
)


@dataclass
class Judgment:
    label: str
    confidence: float
    citation: str
    reason: str
    needs_human: bool
    backend: str = "rules"

    def to_dict(self) -> dict:
        return asdict(self)


def squash(text: str) -> str:
    """年报抽取文本常在中文字符间断行或插空格；比对前去掉全部空白。"""
    return _WS.sub("", text or "")


def cited_in(citation: str, text: str) -> bool:
    c = squash(citation).strip("…. ")
    return bool(c) and c in squash(text)


def window(text: str, keyword: str, n: int = 48) -> str:
    text = squash(text)
    k = squash(keyword)
    i = text.find(k) if k else -1
    if i < 0:
        return text[: 2 * n]
    return text[max(0, i - n): i + len(k) + n]


def semantic_of(j: Judgment) -> str:
    if j.needs_human or j.label == "unclear":
        return "待人工"
    if j.label in COUNTS:
        return "算"
    if j.label in NOT_COUNTS:
        return "不算"
    return "待人工"


def status_of(j: Judgment, cert_id_found: bool) -> str:
    sem = semantic_of(j)
    if sem == "待人工":
        return "待人工"
    if sem == "不算":
        return "不支持"
    return "已核实" if cert_id_found else "披露但未核实"
