---
name: prl-figures
description: Create, revise, and audit physics figures with the PRL-oriented 36-family catalog, evidence-preserving data contracts, and final-size typography checks.
---

# PRL figures

Use [calibrated, direct writing](references/assertive-writing.md) for prose and delivery: requested text/artifact first, specific blocking inputs only, detailed audit separate. An explicit `legacy_v2` request resolves preserved instructions with `scripts/writing_profile.py --mode legacy_v2`.

Use this skill for planning, generating, revising, or auditing physics figures. Keep the scientific meaning and source provenance explicit while applying the PRL-oriented local defaults.

## Workflow

1. Read [figure design](references/figure-design.md) and select one of the [36 figure families](references/figure-families.md).
   For every plotting task without user-specified colors, read the [2025–2026 PRL palette library](references/prl-color-palettes.md) and call `scripts/prl_palette.py`. Select by physical role: discrete identities, continuous values, signed deviations, or numeric bins; retain the source direction and stepped colorbars. Save palette IDs and actual object–color mappings with the source/provenance.
2. For a new data-backed figure, validate the JSON input with scripts/figure_spec.py before rendering.
3. Use a family recipe, scripts/prl_figure.py, or the CSV template. Use scripts/select_references.py only for accepted calibration references and distinguish exact from related support.
4. Compose a separate caption and facts manifest with scripts/figure_caption.py when the delivery includes a structured caption.
5. Use graph-interior whitespace for legends/series labels when it fits without covering data. `scripts/prl_layout.py` provides `place_legend`, `style_ticks`, `layout_panel_grid` and `measure_panel_grid`. Keep axis quantity labels in their readable conventional positions.
6. Inspect the final PDF/PNG, physical dimensions, labels, fonts, inward ticks, legends/colorbars, clipping and occlusion. Choose top/right ticks per panel; start with bottom/left for ordinary curves and distributions, and consider opposite marks for a spatial frame or a useful scale-reading aid. For a regular grid, measure actual left/right edges per column (local tolerance 0.5 pt), compact gaps and dedicated colorbar space; preserve equal spatial units.

The default figure typography is Times New Roman for Latin letters and digits and SimSun for Chinese. Ticks point inward. Do not add small explanatory notes inside the image by default; keep methods, caveats, provenance and result commentary in the caption or manuscript. Never invent data, uncertainty or interpretation. Synthetic gallery figures are demonstrations, not research evidence.

Return the source, data/provenance, validated specification, caption/facts when used, PDF, PNG and JSON inspection report.

Resolve symlinked references and scripts to their canonical targets before following relative resource links. The writing-profile helper prints absolute paths for both writing modes.
