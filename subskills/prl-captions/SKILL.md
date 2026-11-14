---
name: prl-captions
description: Generate and audit evidence-preserving physics figure captions with explicit metadata and a separate fact manifest.
---

# PRL captions

Use [calibrated, direct writing](../../references/assertive-writing.md) for prose and delivery: requested text/artifact first, specific blocking inputs only, detailed audit separate. An explicit `legacy_v2` request resolves preserved instructions with `../../scripts/writing_profile.py --mode legacy_v2`.

Use this skill when a figure needs a new caption, caption audit, or reproducible caption/facts delivery. Read [caption writing](../../references/caption-writing.md) and the [figure contract](../../references/figure-contract.md).

For a new data-backed figure, validate the specification first:

    python3 ../../scripts/figure_spec.py SPEC.json --output SPEC-REPORT.json
    python3 ../../scripts/figure_caption.py SPEC.json --details DETAILS.json --output CAPTION.txt --facts-output CAPTION-FACTS.json

caption_mode: authored preserves supplied prose exactly. compose uses only declared metadata and caller-supplied computed facts. Never infer sample size, error convention, significance, trend, mechanism or causality. Keep explanatory notes in the separate caption rather than adding small text to the canvas. Inspect panel order, axes, units, normalization, uncertainty, image scales, labels and the final export.

Resolve symlinked references and scripts to their canonical targets before following relative resource links. The writing-profile helper prints absolute paths for both writing modes.
