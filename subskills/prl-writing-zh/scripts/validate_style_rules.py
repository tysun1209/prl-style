#!/usr/bin/env python3
"""Validate source-scoped style-rule cards without turning observations into mandates."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "rule_id", "status", "scope", "recommendation", "supporting_figures",
    "counterexamples", "limitations", "source_type", "source_locators",
)
ALLOWED_STATUS = {"official_requirement", "official_recommendation", "conditional_observation", "local_default", "local_design_rule"}
ALLOWED_SOURCE = {"official", "accepted_corpus_review", "local_default", "local_design_rule"}


def _err(code: str, where: str, detail: str) -> dict[str, str]:
    return {"code": code, "where": where, "detail": detail}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line_no, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {line_no}: {exc}") from exc
        if not isinstance(row, dict):
            raise ValueError(f"line {line_no}: rule must be a JSON object")
        row["_line"] = line_no
        rows.append(row)
    return rows


def _locator_exists(locator: str) -> bool:
    if locator.startswith(("http://", "https://", "doi:")):
        return True
    value = locator.split("#", 1)[0].split(":", 1)[0]
    return (ROOT / value).exists()


def validate_rules(rows: list[dict[str, Any]], *, review_rows: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    seen: set[str] = set()
    reviews = {row.get("figure_id"): row for row in (review_rows or []) if isinstance(row, dict)}
    for index, row in enumerate(rows):
        where = f"rules[{index}]"
        for field in REQUIRED:
            if field not in row:
                errors.append(_err("missing_field", f"{where}.{field}", "Every rule card must declare this field."))
        ident = row.get("rule_id")
        if not isinstance(ident, str) or not ident.strip():
            errors.append(_err("invalid_rule_id", f"{where}.rule_id", "rule_id must be a nonempty string."))
        elif ident in seen:
            errors.append(_err("duplicate_rule_id", f"{where}.rule_id", f"Duplicate rule_id: {ident}."))
        else:
            seen.add(ident)
        status = row.get("status")
        source_type = row.get("source_type")
        if status not in ALLOWED_STATUS:
            errors.append(_err("invalid_status", f"{where}.status", f"Use one of {sorted(ALLOWED_STATUS)}."))
        if source_type not in ALLOWED_SOURCE:
            errors.append(_err("invalid_source_type", f"{where}.source_type", f"Use one of {sorted(ALLOWED_SOURCE)}."))
        for field in ("scope", "recommendation", "limitations"):
            if not isinstance(row.get(field), str) or not row[field].strip():
                errors.append(_err("empty_text", f"{where}.{field}", "This field must state a bounded, reviewable rule."))
        for field in ("supporting_figures", "counterexamples", "source_locators"):
            if not isinstance(row.get(field), list):
                errors.append(_err("invalid_list", f"{where}.{field}", "Use an explicit JSON list, including [] when none are available."))
        for locator in row.get("source_locators", []) if isinstance(row.get("source_locators"), list) else []:
            if not isinstance(locator, str) or not locator.strip():
                errors.append(_err("invalid_locator", f"{where}.source_locators", "Locators must be nonempty strings."))
            elif not _locator_exists(locator):
                errors.append(_err("missing_locator", f"{where}.source_locators", f"Cannot resolve local source locator: {locator}"))
        figures = row.get("supporting_figures", []) if isinstance(row.get("supporting_figures"), list) else []
        if any(not isinstance(figure, str) or not figure.strip() for figure in figures):
            errors.append(_err("invalid_supporting_figure", f"{where}.supporting_figures", "Figure IDs must be nonempty strings."))
        if status == "conditional_observation":
            if source_type != "accepted_corpus_review":
                errors.append(_err("observation_source_mismatch", f"{where}.source_type", "Conditional observations require accepted corpus review provenance."))
            if not figures:
                errors.append(_err("observation_without_support", f"{where}.supporting_figures", "A conditional observation needs at least one accepted support figure."))
            for figure in figures:
                review = reviews.get(figure)
                if not review or review.get("status") != "accepted":
                    errors.append(_err("unsupported_figure", f"{where}.supporting_figures", f"Figure is not an accepted review row: {figure}"))
                elif review.get("split") in {"holdout", "test"}:
                    errors.append(_err("heldout_support", f"{where}.supporting_figures", f"Held-out figure cannot support a calibration rule: {figure}"))
        if status in {"official_requirement", "official_recommendation"}:
            if source_type != "official":
                errors.append(_err("official_source_mismatch", f"{where}.source_type", "Official rules require source_type=official."))
            if not any(isinstance(x, str) and x.startswith(("http://", "https://")) for x in row.get("source_locators", [])):
                errors.append(_err("official_locator_missing", f"{where}.source_locators", "Official rules require an authoritative URL."))
        if source_type == "accepted_corpus_review" and status != "conditional_observation":
            errors.append(_err("corpus_source_status_mismatch", f"{where}.status", "Accepted corpus evidence must be labeled conditional_observation."))
        if not row.get("counterexamples") and "none" not in str(row.get("limitations", "")).lower():
            errors.append(_err("counterexample_explanation_missing", f"{where}.limitations", "An empty counterexample list must be explained in limitations."))
        if source_type in {"local_default", "local_design_rule"} and status not in {"local_default", "local_design_rule"}:
            errors.append(_err("local_scope_status_mismatch", f"{where}.status", "Local source cards must use a local status."))
    return {
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "counts": {"rules": len(rows), "accepted_support_rows": len(reviews)},
        "evidence_policy": "Conditional observations are descriptive and scoped; local defaults are not APS requirements.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("rules", type=Path)
    parser.add_argument("--reviews", type=Path, help="Accepted review JSONL used to verify supporting figure IDs.")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        rows = load_jsonl(args.rules)
        reviews = load_jsonl(args.reviews) if args.reviews else []
        report = validate_rules(rows, review_rows=reviews)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        report = {"passed": False, "errors": [_err("load_error", str(args.rules), str(exc))], "warnings": []}
    text = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if report.get("passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
