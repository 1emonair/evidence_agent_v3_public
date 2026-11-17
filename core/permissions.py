"""权限与材料边界：模式 × 材料来源 决定能做什么，运行前检查并写审计日志。

材料来源分三类：
  public       年报、公告等公开披露（第二章语料即此类）
  authorized   企业经授权提供、已脱敏的材料
  internal_raw 未脱敏的内部材料
外部模型（境外或第三方 API）只能接收 public；authorized 需显式打开开关；
internal_raw 一律不出本机，只能用规则或本地模型判读。
"""

from __future__ import annotations

import hashlib
import os

ALLOWED_MODES = {"research", "diligence"}
SOURCE_TYPES = {"public", "authorized", "internal_raw"}

POLICY = {
    "score_writes": False,
    "pricing_writes": False,
    "auto_decline": False,
    "auto_surcharge": False,
    "filing_in_research_score": False,
    "external_materials_in_score": False,
    "web_text_as_instruction": False,
    "tools_read_only": True,
    "contact_firm_or_submit": False,
    "default_sources": ["年报公开披露", "第二章冻结指标"],
    "diligence_extra_sources": ["算法备案库（只读展示）", "经授权材料（仅证据卡）"],
}


def check_mode(mode: str) -> dict:
    if mode not in ALLOWED_MODES:
        raise ValueError(f"未知模式：{mode}，允许 {ALLOWED_MODES}")
    return {
        "mode": mode,
        "policy": POLICY,
        "filing_query_allowed": mode == "diligence",
        "note": "研究模式不查备案库；尽调模式可查询但注明不进分数。",
    }


def external_llm_allowed(source: str) -> tuple[bool, str]:
    if source not in SOURCE_TYPES:
        return False, f"未知材料来源 {source}，按不出本机处理"
    if source == "public":
        return True, "公开披露材料，允许发送外部模型"
    if source == "authorized" and os.environ.get("EVIDENCE_ALLOW_AUTHORIZED_EXTERNAL") == "1":
        return True, "经授权脱敏材料，已显式开启外发开关"
    if os.environ.get("EVIDENCE_LLM_LOCAL") == "1":
        return True, "本地模型，不出本机"
    return False, f"{source} 材料不发送外部模型，改用规则判读"


def text_digest(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()[:16]
