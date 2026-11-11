# PRL figure workflow

Read [official rules](official-rules.md) and the relevant entries in [evidence catalog](evidence-catalog.md). Source-backed production constraints are distinct from the configurable defaults in `profiles/figure-defaults.json`.

For type selection, use the [36-family catalog](figure-families.md), including input contracts, calibrated images, fields, distributions, networks and runnable examples. Use its reference selector when a published design precedent would help; a related-family match is not direct evidence for the requested type. For integrated captions/results, use [figure-to-prose](figure-to-prose.md).

## Decide what the reader should learn

Record the claim, observable, comparison/baseline, uncertainty meaning, source data, units, intended physical width, and required panels. When inputs are incomplete, draft the layout and identify the missing scientific fact. Never manufacture measurements or silently choose a significance interpretation. A model diagram can come first when it makes later evidence understandable.

Default to Times New Roman for Latin letters and digits and 宋体 (SimSun) for Chinese; see [typography](typography.md). The `times` profile is the default; `sans` and `serif` remain explicit alternatives. These are user-selected local settings, not official PRL fonts. Preserve an explicitly requested user style unless it causes a documented readability or scientific problem. Do not use another installed style skill automatically; mixing its margins/fonts can undo the requested PRL profile.

## Default canvas text

**默认不在图片上添加小字注释。** Keep explanatory sentences, footnotes, parameter/method summaries, sample-size notes, fit statistics, caveats, source/file information and result commentary in the separate figure caption or main text. This applies to the whole exported canvas, including panel corners, whitespace and bottom margins. Increasing the font size or placing a note outside the axes does not change this default. Add such on-image explanations only on an explicit user request.

Retain text needed to read the graphic: axis quantities and units, ticks, legends or concise series labels, colorbars, panel IDs, contour levels, scale-bar values, and necessary node/state/transition labels in schematics. Distinguish these labels by their scientific role, not by whether they were created with `ax.text` or `annotate`. Do not automatically remove every Text artist or delete an uncertainty definition from the deliverable; move explanatory content to the caption. Apply the existing font and legibility settings to retained labels.

When adapting a reference or recipe, omit its optional explanatory notes by default. Before export, review extra canvas text for this distinction; keep the explanation in the delivered caption instead of burning the caption into the image.

## Choose a figure family

| Family | Design decision | Scientific check |
|---|---|---|
| Trend/comparison | Mark observations and distinguish theory/fit/reference curves | Identify uncertainty type, number of realizations, correlations and fit domain when known |
| Scaling | Pair raw and scaled quantities where it clarifies the claim | State scaling factors and finite-size/time limits; visual collapse alone is not proof |
| Phase map | Separate discrete classes from continuous fields; share normalization only for comparable quantities | Define phase diagnostic and boundary uncertainty; no interpolated phase boundary without a method |
| Distribution/spectrum | Select linear/log scales for the relevant structure; preserve normalization | Binning, smoothing, tail statistics and instrumental broadening must come from the author |
| Trajectory/snapshot | Use consistent coordinates, scales and time labels | Distinguish a representative realization from an ensemble result |
| Schematic | Use explicit directional/causal meanings; connect symbols to equations/text | Do not imply mechanisms or geometric equivalences that evidence does not establish |
| Multipanel | Arrange panels in argument order, align comparable axes, reserve space for labels | Every panel must contribute evidence or necessary explanation; shared axes must be scientifically valid |

## Rendering

For a new data-backed figure, validate the structured input with
`python3 scripts/figure_spec.py SPEC.json` before calling a recipe or
`scripts/prl_figure.py`. The contract records quantity identity, conditions,
source status and uncertainty instead of leaving them implicit in plotting
code. When a reproducible caption is needed, run
`python3 scripts/figure_caption.py SPEC.json --output CAPTION.txt --facts-output
CAPTION-FACTS.json`; inspect both outputs and then review the rendered figure.
See [figure contract](figure-contract.md).

Default major and minor ticks point inward (`in`) on both x and y axes. Apply the same direction to subplot, inset and colorbar axes. The supplied style already sets `xtick.direction: in` and `ytick.direction: in`; when styling existing axes, use `ax.tick_params(axis='both', which='both', direction='in')`. Preserve a later explicit user override and check the rendered direction for special projections. Tick direction does not require enabling additional top/right ticks or moving tick labels inside the plot.

Use `scripts/prl_figure.py`: a local `figure_context`, a figure created at the final width/height, and `export_figure`. Never globally set the user's rcParams. `assets/templates/figure_from_csv.py` accepts x/y and optional yerr and does not drop missing rows, smooth, interpolate, refit, or change units. It requires a description for uncertainty bars. For a copied template, provide `--skill-root`.

Default exports are PDF, PNG and the JSON inspection report. Generate a grayscale preview only on an explicit user request: pass `grayscale=True` to `export_figure`, or `--grayscale` to the CSV template. Grayscale generation and review are not default acceptance requirements; the recorded APS color-readability recommendation does not require an extra preview file.

If error extents are supplied but their definition is unknown, use an honest description such as `--uncertainty-description 'Supplied yerr extents; statistical definition unknown'`. Preserve the bars and mark the missing definition in the caption and review. This supports a review draft, not statistical certification. Never guess SD, SEM or a confidence level to satisfy the interface.

Distinguish a visual interpolation from smoothing that changes reported values and from a fitted physical model. A user-authorized visual guide may be overlaid with its method disclosed, all original observations retained, and a distinct encoding. Do not hide a local reversal, claim a monotonic trend, or identify a decay law merely to make a curve look cleaner. If the scientific role of a requested curve is ambiguous, complete the faithful data plot and identify that specific open choice.

Use colors consistently for the same physical objects across a manuscript. For categorical comparisons, add marker shape or line pattern. Continuous parameters may be encoded by a colorbar; record the normalization. Use a diverging scale only with a meaningful center. Avoid a stock palette rule detached from the observable. Consider direct labels when an extended legend slows comparison.

Suppress repeated tick labels only when the retained scale is unambiguous in the exported layout. Panels using the same variable do not automatically share a readable axis: compare scale type, limits, direction, physical width/height and alignment. A full-width upper panel above two narrower panels normally needs its own numerical ticks and axis quantity. An adjacent logarithmic axis cannot supply the scale for a linear panel. Explicit common axes or genuinely aligned shared axes can avoid repetition; do not force redundant labels onto those valid layouts. Test whether a reader can locate a quoted feature on every panel without reconstructing a hidden coordinate system from the caption.

## Make the claimed difference visible

For each comparison emphasized in the prose, locate the corresponding data in the final-size figure. Distinct legend keys do not make nearly coincident trajectories separable. Record the claim, panel/range, whether its decisive difference is actually visible, and the chosen remedy (or why none is needed).

When a wide dynamic range hides a scientifically relevant difference, select a justified display: an explicitly bounded inset, a second linear-scale panel, a signed difference with its baseline defined, or direct labels for a limited comparison. Choose according to the question; do not require an inset for every figure. Keep the complete main view and all requested observations. A zoom repeats a disclosed subset rather than replacing inconvenient points. A difference/ratio needs its definition, source identities and uncertainty treatment; preserve covariance limitations rather than inventing independent errors. Do not add offsets or exaggerate a separation without stating the transformation.

For example, three MSD curves on logarithmic axes can obscure a late-time ordering that is visible on a linear late-time view. Give the inset's time and ordinate range, retain the full logarithmic panel, use the same group encodings, and distinguish visible numerical ordering from statistical significance. Verify that the new panel remains legible at final size and does not cover important main-panel data. If the claimed effect remains unreadable, revise the layout or qualify the claim; do not mark the figure accepted solely because font and line-width checks pass.

The 85 mm preset is tied to single-column planning. The 178 mm gallery width is a working two-column preview, not a measured universal PRL width. Read the real template's text width. Save fixed-size PDF and PNG without `bbox_inches='tight'`, which can change physical dimensions. Keep vector text and curves; large heatmaps can be rasterized while labels remain vector. Verify accepted upload formats at submission rather than treating every preview format as a production deliverable.

## Inspect both the figure and the page

1. Inspect source artists for small base lettering, line/marker dimensions, out-of-figure text and missing glyphs. Error-bar stems use LineCollection; caps have separate stroke widths. Both are checked explicitly.
2. Inspect exported PDF dimensions and embedded fonts. Embedded raster text, arbitrary fonts, subscripts and custom transforms need explicit visual review.
3. View the exported figure at intended physical size and a larger diagnostic size. Check overlapping labels, data occlusion, colorbar units, legend ambiguity, panel order, sparse/dense regions and mathematical symbols. If the user requested a grayscale preview, also check that its encodings and decisive comparisons remain readable.
4. Place the figure in the manuscript layout and check scaling again. A figure that passed at 85 mm can fail if subsequently reduced.
5. Review the caption using [caption writing](caption-writing.md) and verify every referenced panel and encoding. Audit the source identity of named quantities using the [quantity ledger](claim-ledger.md#physical-quantity-identity-across-sources-figures-and-text), including normalization denominators; inspect the exported `labels` rather than only the plotting code.

`inspect_figure.py` returns measurements, not a blanket publication-ready verdict. A base-font H-height estimate does not certify every glyph. Its output explicitly identifies untested perception/science dimensions. Thin filled raster boundaries and scatter marker areas are not equivalent to Line2D marker diameters.

Deliver the figure and caption first, with source/data provenance, PDF, PNG and the inspection report as linked artifacts. Follow [calibrated, direct writing](assertive-writing.md) for the explanation and mention concrete issues that affect this figure. Include a grayscale preview only when explicitly requested. Label synthetic gallery data as demonstrations.

## Commands

From the skill root, use `.venv/bin/python` if the supplied environment exists, otherwise Python with requirements.txt installed:

```bash
python assets/templates/figure_from_csv.py data.csv --output figures/result --xlabel 'Time (s)' --ylabel 'Distance (m)'
python scripts/inspect_figure.py figures/result.pdf --output figures/result-pdf-inspection.json
python scripts/render_gallery.py --output reports/gallery
```

For subsequent user work, put generated outputs in the user's project, not in this skill's corpus or reference gallery.
