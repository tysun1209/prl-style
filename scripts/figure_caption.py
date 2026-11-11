#!/usr/bin/env python3
"""Compose conservative captions and a separate fact manifest from a figure spec."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


DECLARED_FIELDS = (
    ("population", "Population"),
    ("unit_of_analysis", "Unit of analysis"),
    ("quantity_definition", "Quantity"),
    ("conditions", "Conditions"),
    ("normalization", "Normalization"),
    ("uncertainty_definition", "Uncertainty"),
)
DETAIL_FIELDS = (
    ("sample_counts", "Sample counts"),
    ("series_roles", "Series roles"),
    ("observed_cells", "Observed cells"),
    ("missing_cells", "Missing cells"),
    ("interval_definition", "Interval definition"),
    ("fit_range", "Fit range"),
)


def _hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _text(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(", ", ": "))
    return str(value).strip()


def _sentence(value: str) -> str:
    value = value.strip()
    if not value:
        return value
    return value if value.endswith(('.', '!', '?', '。', '！', '？')) else value + "."


def _base_caption(spec: dict[str, Any]) -> str:
    caption = spec.get("caption")
    if isinstance(caption, str) and caption.strip():
        return caption.strip()
    quantity = spec.get("quantity") or "Quantity"
    unit = spec.get("unit")
    population = spec.get("population") or "the declared population"
    conditions = spec.get("conditions") or "the declared conditions"
    quantity_text = f"{quantity} ({unit})" if unit else str(quantity)
    return _sentence(f"{quantity_text} for {population} under {conditions}")


def _explicit_sentences(spec: dict[str, Any]) -> list[str]:
    pieces = []
    for key, label in DECLARED_FIELDS:
        value = spec.get(key)
        if value is None or value == "":
            continue
        pieces.append(_sentence(f"{label}: {_text(value)}"))
    status = spec.get("data_status")
    if status in {"synthetic", "illustrative"}:
        marker = "Synthetic demonstration; not research results." if status == "synthetic" else "Illustrative construction; not research results."
        pieces.append(marker)
    return pieces


def _detail_sentences(details: dict[str, Any] | None) -> list[str]:
    if not isinstance(details, dict):
        return []
    pieces = []
    for key, label in DETAIL_FIELDS:
        if key in details and details[key] is not None and details[key] != "":
            pieces.append(_sentence(f"{label}: {_text(details[key])}"))
    return pieces


def compose_caption(spec: dict[str, Any], details: dict[str, Any] | None = None) -> str:
    """Return a deterministic caption using only declared or supplied facts."""
    if spec.get("caption_mode", "compose") == "authored":
        caption = spec.get("caption")
        if not isinstance(caption, str) or not caption.strip():
            raise ValueError("caption_mode=authored requires a nonempty caption")
        return caption
    parts = [_base_caption(spec)]
    parts.extend(_explicit_sentences(spec))
    parts.extend(_detail_sentences(details))
    return " ".join(part for part in parts if part)


def caption_facts(spec: dict[str, Any], details: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return provenance and explicit facts separately from caption prose."""
    declared = {key: copy.deepcopy(spec[key]) for key, _ in DECLARED_FIELDS if key in spec}
    supplied_details = copy.deepcopy(details) if isinstance(details, dict) else {}
    return {
        "caption_mode": spec.get("caption_mode", "compose"),
        "data_status": spec.get("data_status"),
        "declared_facts": declared,
        "computed_details": supplied_details,
        "input_sha256": _hash(spec),
        "caption_sha256": _hash(compose_caption(spec, details)),
        "semantic_review_required": True,
        "inference_policy": "No trends, uncertainty, significance, causality, mechanism, or sample size is inferred.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("--details", type=Path, help="JSON object containing caller-supplied computed facts.")
    parser.add_argument("--output", type=Path, help="Write caption text to this path.")
    parser.add_argument("--facts-output", type=Path, help="Write the fact manifest to this path.")
    args = parser.parse_args()
    try:
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        details = json.loads(args.details.read_text(encoding="utf-8")) if args.details else None
        caption = compose_caption(spec, details)
        facts = caption_facts(spec, details)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"passed": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(caption + "\n", encoding="utf-8")
    if args.facts_output:
        args.facts_output.parent.mkdir(parents=True, exist_ok=True)
        args.facts_output.write_text(json.dumps(facts, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(caption)
    if args.facts_output is None:
        print(json.dumps(facts, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
