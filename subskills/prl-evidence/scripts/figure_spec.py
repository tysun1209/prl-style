#!/usr/bin/env python3
"""Validate a structured, evidence-preserving figure specification.

The validator checks the input contract only. It does not render a figure or
infer scientific results from the rows supplied by the caller.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FAMILIES = ROOT / "profiles" / "figure-families.json"
DEFAULT_PROFILES = ROOT / "profiles" / "figure-defaults.json"

ALLOWED_STATUS = {"real", "synthetic", "illustrative"}
ALLOWED_TOP_LEVEL = {
    "schema_version", "kind", "data_status", "claim", "profile", "caption",
    "caption_mode", "quantity", "quantity_definition", "unit", "population",
    "unit_of_analysis", "conditions", "normalization", "uncertainty_definition",
    "missing_data_policy", "source", "provenance", "data", "rows", "metadata",
    "details", "panel_map", "axis_map", "encoding", "figure_id", "title",
}
RELAXED_METADATA_KINDS = {"schematic", "network", "multipanel", "wide_narrow"}


def _error(code: str, path: str, detail: str) -> dict[str, str]:
    return {"code": code, "path": path, "detail": detail}


def _sha256_object(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _load_json(path: Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _family_ids(path: Path) -> set[str]:
    obj = _load_json(path)
    rows = obj.get("families", []) if isinstance(obj, dict) else []
    return {row.get("id") for row in rows if isinstance(row, dict) and isinstance(row.get("id"), str)}


def _profile_ids(path: Path) -> set[str]:
    obj = _load_json(path)
    rows = obj.get("font_profiles", {}) if isinstance(obj, dict) else {}
    return set(rows) if isinstance(rows, dict) else set()


def _walk_data(value: Any, path: str, errors: list[dict[str, str]], null_paths: list[str]) -> None:
    if value is None:
        null_paths.append(path)
    elif isinstance(value, bool):
        errors.append(_error("boolean_numeric", path, "Boolean values are not valid data values."))
    elif isinstance(value, float) and not math.isfinite(value):
        errors.append(_error("nonfinite_numeric", path, "NaN and infinity are not valid data values."))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _walk_data(item, f"{path}[{index}]", errors, null_paths)
    elif isinstance(value, dict):
        for key, item in value.items():
            _walk_data(item, f"{path}.{key}", errors, null_paths)


def _check_duplicate_row_ids(rows: Any, errors: list[dict[str, str]]) -> None:
    if not isinstance(rows, list):
        return
    seen: set[str] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or "id" not in row:
            continue
        ident = row["id"]
        if not isinstance(ident, str) or not ident.strip():
            errors.append(_error("invalid_row_id", f"rows[{index}].id", "Row id must be a nonempty string."))
        elif ident in seen:
            errors.append(_error("duplicate_row_id", f"rows[{index}].id", f"Duplicate row id: {ident}."))
        else:
            seen.add(ident)


def validate_spec(
    spec: dict[str, Any],
    *,
    family_path: Path | None = None,
    profile_path: Path | None = None,
) -> dict[str, Any]:
    """Return a deterministic validation report without mutating *spec*."""
    original = copy.deepcopy(spec)
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []
    if not isinstance(spec, dict):
        return {
            "passed": False,
            "errors": [_error("spec_not_object", "$", "Figure specification must be one JSON object.")],
            "warnings": [],
            "input_sha256": _sha256_object(spec),
        }

    family_path = Path(family_path or DEFAULT_FAMILIES)
    profile_path = Path(profile_path or DEFAULT_PROFILES)
    try:
        families = _family_ids(family_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        families = set()
        errors.append(_error("family_catalog_error", "kind", str(exc)))
    try:
        profiles = _profile_ids(profile_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        profiles = set()
        errors.append(_error("profile_catalog_error", "profile", str(exc)))

    unknown = sorted(set(spec) - ALLOWED_TOP_LEVEL)
    for key in unknown:
        errors.append(_error("unknown_top_level_field", key, "Declare this field in the contract before using it."))

    kind = spec.get("kind")
    if not isinstance(kind, str) or kind not in families:
        errors.append(_error("unknown_kind", "kind", f"kind must be one of the {len(families)} catalog family IDs."))
    status = spec.get("data_status")
    if status not in ALLOWED_STATUS:
        errors.append(_error("invalid_data_status", "data_status", "Use real, synthetic, or illustrative."))
    for field in ("claim", "profile"):
        if not isinstance(spec.get(field), str) or not spec[field].strip():
            errors.append(_error("missing_required_field", field, f"{field} must be a nonempty string."))
    profile = spec.get("profile")
    if isinstance(profile, str) and profile not in profiles:
        errors.append(_error("unknown_profile", "profile", f"Profile is not defined in {profile_path.name}: {profile}."))
    caption_mode = spec.get("caption_mode", "compose")
    if caption_mode not in {"compose", "authored"}:
        errors.append(_error("invalid_caption_mode", "caption_mode", "Use compose or authored."))
    if caption_mode == "authored" and (not isinstance(spec.get("caption"), str) or not spec["caption"].strip()):
        errors.append(_error("authored_caption_missing", "caption", "An authored caption must be nonempty."))

    if kind not in RELAXED_METADATA_KINDS:
        for field in ("quantity", "unit", "population", "conditions"):
            if field not in spec or spec[field] is None or (isinstance(spec[field], str) and not spec[field].strip()):
                errors.append(_error("missing_metadata", field, "Data-driven figures must declare this field explicitly."))
    if "data" in spec and "rows" in spec:
        errors.append(_error("duplicate_data_container", "data", "Use either data or rows, not both."))
    data = spec.get("data", spec.get("rows"))
    if data is None:
        errors.append(_error("data_missing", "data", "A renderable specification must preserve its data or structural rows explicitly."))
    elif not isinstance(data, (list, dict)):
        errors.append(_error("invalid_data_container", "data", "data must be a list of rows or an object of named arrays."))
    else:
        null_paths: list[str] = []
        _walk_data(data, "data", errors, null_paths)
        _check_duplicate_row_ids(data, errors)
        if null_paths:
            policy = spec.get("missing_data_policy")
            if not isinstance(policy, str) or not policy.strip():
                errors.append(_error("missing_data_policy", "missing_data_policy", "Explicit null values require a missing-data policy."))
            elif policy.strip().lower() in {"drop", "discard", "ignore"}:
                errors.append(_error("silent_missing_data_drop", "missing_data_policy", "Rows with null values must be retained and disclosed."))
    if "missing_data_policy" in spec and not isinstance(spec["missing_data_policy"], str):
        errors.append(_error("invalid_missing_data_policy", "missing_data_policy", "Use a descriptive string."))
    if status in {"synthetic", "illustrative"} and not isinstance(spec.get("provenance", spec.get("source")), (str, dict)):
        warnings.append({"code": "synthetic_provenance_unstated", "path": "provenance", "detail": "Identify the generator or source of a synthetic demonstration."})
    if status == "real" and "source" not in spec and "provenance" not in spec:
        errors.append(_error("real_source_missing", "source", "Real data require an explicit source or provenance record."))
    if kind == "schematic" and spec.get("quantity") is not None:
        warnings.append({"code": "schematic_quantity_check", "path": "quantity", "detail": "A schematic quantity must be clearly labeled as conceptual."})
    if spec != original:
        errors.append(_error("input_mutated", "$", "Validator must not mutate the supplied specification."))
    return {
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "input_sha256": _sha256_object(spec),
        "counts": {"top_level_fields": len(spec), "data_rows": len(data) if isinstance(data, list) else None},
        "catalog": {"family_count": len(families), "profile_count": len(profiles)},
        "semantic_review_required": True,
    }


def load_spec(path: Path) -> dict[str, Any]:
    value = _load_json(Path(path))
    if not isinstance(value, dict):
        raise ValueError("Figure specification must be one JSON object.")
    return value


def validate_file(path: Path, *, family_path: Path | None = None, profile_path: Path | None = None) -> dict[str, Any]:
    spec = load_spec(path)
    report = validate_spec(spec, family_path=family_path, profile_path=profile_path)
    report["spec_path"] = str(Path(path))
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("--output", type=Path, help="Write the JSON report to this path.")
    args = parser.parse_args()
    try:
        report = validate_file(args.spec)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        report = {"passed": False, "errors": [_error("load_error", str(args.spec), str(exc))], "warnings": []}
    text = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if report.get("passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
