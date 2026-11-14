---
name: prl-figures
description: Create, revise, and audit physics figures with the PRL-oriented 36-family catalog, evidence-preserving data contracts, and final-size typography checks.
---

# PRL figures

Use [calibrated, direct writing](../../references/assertive-writing.md) for prose and delivery: requested text/artifact first, specific blocking inputs only, detailed audit separate. An explicit `legacy_v2` request resolves preserved instructions with `../../scripts/writing_profile.py --mode legacy_v2`.

Use this skill for planning, generating, revising, or auditing physics figures. Keep the scientific meaning and source provenance explicit while applying the PRL-oriented local defaults.

For scientific schematics, apparatus/model diagrams, control loops and method flowcharts, use `prl-schematics` and [schematic design](../../references/prl-schematics.md): built-in image model → PNG → editable PPTX is the default. A mixed Fig. 1 combines that workflow with the quantitative-panel rules below. Pure diagrams do not require a data-table figure specification.

## Workflow

1. Read [figure design](../../references/figure-design.md) and select one of the [36 figure families](../../references/figure-families.md).
   For every plotting task without user-specified colors, use [automatic palette selection](../../references/automatic-palette-selection.md): `../../scripts/prl_palette.py --recommend --family FAMILY --kind ROLE`, or `palette_selection.select_palette()`. Supply actual category count and mark type; color meaning overrides the family suggestion. Prefer readable line/point colors, softer region fills, ordered intensity, an explicit reference for divergence and a cyclic map only for periodic values. Use the returned plan in the actual artists, retain source direction/numeric bins, and save palette IDs, normalization and object–color mappings. Reuse mappings across related panels/figures. Explicit user choices win; the original [source-backed library](../../references/prl-color-palettes.md) remains directly callable.
2. For a new data-backed figure, validate the JSON input with ../../scripts/figure_spec.py before rendering.
3. Use a family recipe, ../../scripts/prl_figure.py, or the CSV template. Use ../../scripts/select_references.py only for accepted calibration references and distinguish exact from related support.
   For the complete 291-paper coverage, call `../../scripts/select_visual_references.py --family FAMILY`; see [full visual references](../../references/visual-corpus.md). Its 1,022 unique figures carry source-version labels and explicit color-role observations; held-out sources are excluded by default.
   For domain-specific layouts, also read [cross-field design](../../references/crossfield-visual-design.md) and call `../../scripts/select_crossfield_references.py --family FAMILY` or `--pattern PATTERN`. The additional 50 visual-development papers support 14 composition patterns, including aligned spectra/ratios, parameter maps and scientific schematics; they are separate from held-out evaluation.
4. Compose a separate caption and facts manifest with ../../scripts/figure_caption.py when the delivery includes a structured caption.
5. Use graph-interior whitespace for legends/series labels when it fits without covering data. `../../scripts/prl_layout.py` provides `place_legend`, `style_ticks`, `layout_panel_grid` and `measure_panel_grid`. Keep axis quantity labels in their readable conventional positions.
6. Inspect the final PNG (600 dpi by default), physical dimensions, labels, fonts, inward ticks, legends/colorbars, clipping and occlusion. Inspect other formats when requested. Choose top/right ticks per panel; start with bottom/left for ordinary curves and distributions, and consider opposite marks for a spatial frame or a useful scale-reading aid. For a regular grid, measure actual left/right edges per column (local tolerance 0.5 pt), compact gaps and dedicated colorbar space; preserve equal spatial units.

The default figure typography is Times New Roman for Latin letters and digits and SimSun for Chinese. Ticks point inward. Do not add small explanatory notes inside the image by default; keep methods, caveats, provenance and result commentary in the caption or manuscript. Never invent data, uncertainty or interpretation. Synthetic gallery figures are demonstrations, not research evidence.

Save only PNG images at 600 dpi by default. PDF, EPS, SVG and other formats require a user request; pass `formats=['png', 'pdf']` to `export_figure` or `--formats png pdf` to the rendering CLI when both are requested. A requested resolution overrides 600 dpi through `dpi` / `--dpi`. Return source, data/provenance, specification, caption/facts and inspection records as relevant to the task.

Resolve symlinked references and scripts to their canonical targets before following relative resource links. The writing-profile helper prints absolute paths for both writing modes.
