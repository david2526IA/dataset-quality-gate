"""Validate CSV-like mappings against an explicit, compact schema."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def _check(value: str, rule: dict[str, Any]) -> str | None:
    if rule.get("required") and not value.strip():
        return "required"
    if not value.strip():
        return None
    kind = rule.get("type", "string")
    try:
        numeric = float(value) if kind in {"number", "integer"} else None
        if kind == "integer" and not numeric.is_integer():
            return "expected integer"
        if kind not in {"string", "number", "integer"}:
            return f"unknown type {kind}"
    except ValueError:
        return f"expected {kind}"
    if "min" in rule and numeric is not None and numeric < rule["min"]:
        return f"below minimum {rule['min']}"
    if "max" in rule and numeric is not None and numeric > rule["max"]:
        return f"above maximum {rule['max']}"
    return None


def validate_rows(rows: Iterable[dict[str, str]], schema: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Return accepted rows and source-preserving rejected rows with reasons."""
    accepted: list[dict[str, str]] = []
    rejected: list[dict[str, Any]] = []
    for line, row in enumerate(rows, start=2):
        reasons = []
        for field, rule in schema.items():
            if field not in row:
                reasons.append({"field": field, "reason": "missing column"})
                continue
            error = _check(row[field], rule)
            if error:
                reasons.append({"field": field, "reason": error})
        if reasons:
            rejected.append({"line": line, "row": row, "reasons": reasons})
        else:
            accepted.append(row)
    return {"accepted": accepted, "rejected": rejected, "summary": {"accepted_rows": len(accepted), "rejected_rows": len(rejected), "total_rows": len(accepted) + len(rejected)}}
