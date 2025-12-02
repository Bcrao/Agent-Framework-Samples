"""Utility helpers for the marketing workflow."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

_JSON_BLOCK_RE = re.compile(r"```(?:json)?(.*?)```", re.DOTALL | re.IGNORECASE)
_NON_ALNUM_RE = re.compile(r"[^a-z0-9]+", re.IGNORECASE)


def slugify(value: str, *, max_length: int = 60) -> str:
    """Convert arbitrary text into a filesystem-friendly slug."""

    value_ascii = value.strip().lower()
    slug = _NON_ALNUM_RE.sub("-", value_ascii).strip("-")
    if not slug:
        slug = "campaign"
    return slug[:max_length]


def extract_json_object(payload: str) -> str:
    """Best-effort extraction of a JSON object from agent text output."""

    if not payload:
        raise ValueError("Empty payload cannot be parsed as JSON")

    text = payload.strip()
    fenced_match = _JSON_BLOCK_RE.search(text)
    if fenced_match:
        text = fenced_match.group(1).strip()

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("Could not locate JSON object boundaries in agent output")

    json_str = text[start : end + 1]

    # Try to validate and fix common JSON issues
    try:
        # Attempt to parse to validate
        json.loads(json_str)
        return json_str
    except json.JSONDecodeError:
        # Try to fix common issues: trailing commas, unescaped quotes in strings
        # Remove trailing commas before ] or }
        fixed = re.sub(r',(\s*[}\]])', r'\1', json_str)
        try:
            json.loads(fixed)
            return fixed
        except json.JSONDecodeError:
            # Return original and let caller handle the error
            return json_str


def ensure_directory(path: str | Path) -> Path:
    """Create the directory if necessary and return it as a Path."""

    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def dump_json(data: Any, path: Path) -> None:
    """Write JSON to disk with UTF-8 encoding."""

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, default=str), encoding="utf-8")


def timestamp_id() -> str:
    """Return a compact UTC timestamp for folder naming."""

    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")
