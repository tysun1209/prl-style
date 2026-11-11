#!/usr/bin/env python3
"""Preflight the exact fonts and local defaults required by the PRL skill.

The report distinguishes an exact font-family match from fontconfig's fallback.
Use ``--strict`` in a release gate; without it the command records a useful
diagnostic report and exits successfully even when a requested font is absent.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from matplotlib import font_manager
from matplotlib.ft2font import FT2Font
from typography import _refresh_fonts

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def resolve_exact(family: str) -> dict:
    prop = font_manager.FontProperties(family=family)
    attempts = []
    for fallback in (False, True):
        try:
            path = Path(font_manager.findfont(prop, fallback_to_default=fallback))
            actual = FT2Font(str(path)).family_name
            item = {
                "fallback_to_default": fallback,
                "path": str(path),
                "family_name": actual,
                "exact": actual.casefold() == family.casefold(),
            }
            if path.is_file():
                item["sha256"] = sha256(path)
            attempts.append(item)
            if item["exact"]:
                return {"requested": family, "available": True, "selected": item, "attempts": attempts}
        except (OSError, ValueError, RuntimeError) as exc:
            attempts.append({"fallback_to_default": fallback, "error": str(exc)})
    return {"requested": family, "available": False, "selected": attempts[-1] if attempts else None, "attempts": attempts}


def fc_match(family: str) -> dict:
    try:
        result = subprocess.run(
            ["fc-match", "-f", "%{family}|%{file}\\n", family],
            check=False,
            capture_output=True,
            text=True,
        )
        line = result.stdout.strip().splitlines()[0] if result.stdout.strip() else ""
        matched, _, path = line.partition("|")
        return {"family": matched, "path": path, "returncode": result.returncode}
    except OSError as exc:
        return {"error": str(exc)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="write a JSON report")
    parser.add_argument("--strict", action="store_true", help="fail unless Times New Roman and SimSun are exact matches")
    args = parser.parse_args()

    # Match the runtime used by prl_figure.py: user-installed fonts may not be
    # present in Matplotlib's in-memory table until the cache is refreshed.
    _refresh_fonts()
    fonts = {name: resolve_exact(name) for name in ("Times New Roman", "SimSun")}
    style = ROOT / "assets/styles/prl.mplstyle"
    defaults = ROOT / "profiles/figure-defaults.json"
    style_text = style.read_text(encoding="utf-8")
    defaults_data = json.loads(defaults.read_text(encoding="utf-8"))
    report = {
        "schema_version": "prl-environment-preflight-1",
        "fonts": fonts,
        "fontconfig": {name: fc_match(name) for name in fonts},
        "defaults": {
            "default_font_profile": defaults_data.get("default_font_profile"),
            "latin_family": defaults_data.get("font_profiles", {}).get("times", {}).get("family"),
            "cjk_family": defaults_data.get("font_profiles", {}).get("times", {}).get("cjk_family"),
            "style_sha256": sha256(style),
            "defaults_sha256": sha256(defaults),
            "x_tick_direction": next((line.split(":", 1)[1].strip() for line in style_text.splitlines() if line.startswith("xtick.direction:")), None),
            "y_tick_direction": next((line.split(":", 1)[1].strip() for line in style_text.splitlines() if line.startswith("ytick.direction:")), None),
        },
        "strict_ready": all(fonts[name]["available"] for name in fonts),
        "limitations": [
            "A font-family match does not certify every glyph, math symbol, or final PDF embedding.",
            "FandolSong and other substitutes are diagnostic previews only when SimSun is unavailable.",
        ],
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if (not args.strict or report["strict_ready"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
