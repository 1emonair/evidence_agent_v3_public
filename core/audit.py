"""操作日志：模型/规则版本、工具调用、人工修改。不写业务分数。"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parents[1] / "logs"
PROMPT_VERSION = "evidence_judge_v3"
RULES_VERSION = "two_axis_def_reg_method_v3"
AGENT_VERSION = "evidence_agent_v3"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_event(event: dict) -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    day = datetime.now(timezone.utc).strftime("%Y%m%d")
    path = LOG_DIR / f"audit_{day}.jsonl"
    payload = {
        "ts": _now(),
        "agent_version": AGENT_VERSION,
        "prompt_version": PROMPT_VERSION,
        "rules_version": RULES_VERSION,
        "judge_backend": os.environ.get("EVIDENCE_JUDGE", "rules"),
        "llm_model": os.environ.get("EVIDENCE_LLM_MODEL", ""),
        "mode": event.get("mode"),
        **event,
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return path
