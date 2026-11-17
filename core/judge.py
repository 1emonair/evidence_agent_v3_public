"""判读入口：rules | llm。

    EVIDENCE_JUDGE=rules   仅增强规则（默认，可复算）
    EVIDENCE_JUDGE=llm     大模型；无密钥或材料不允许外发时回退规则并标明 rules_fallback
"""

from __future__ import annotations

import os

from .judge_llm import judge_llm
from .judge_rules import judge_rules
from .judge_types import Judgment, semantic_of, status_of, window  # noqa: F401  re-export


def judge(text: str, keyword: str, item: str, source: str = "public") -> Judgment:
    backend = (os.environ.get("EVIDENCE_JUDGE") or "rules").lower()
    if backend == "llm":
        return judge_llm(text, keyword, item, source)
    return judge_rules(text, keyword, item)
