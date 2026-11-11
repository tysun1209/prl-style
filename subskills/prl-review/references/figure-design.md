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

The only default image export is PNG at 600 dpi; retain the JSON inspection record and source/provenance as needed. PDF, EPS, SVG, JPEG and TIFF are opt-in: pass `formats=['png', 'pdf']` to `export_figure`, or `--formats png pdf` to the CSV/gallery CLI, when both are requested. `formats=['pdf']` exports only PDF; `dpi=1200` / `--dpi 1200` overrides the raster resolution. Generate a grayscale PNG only on an explicit user request: pass `grayscale=True` or `--grayscale`. Grayscale generation and review are not default acceptance requirements; the recorded APS color-readability recommendation does not require an extra preview file.

If error extents are supplied but their definition is unknown, use an honest description such as `--uncertainty-description 'Supplied yerr extents; statistical definition unknown'`. Preserve the bars and mark the missing definition in the caption and review. This supports a review draft, not statistical certification. Never guess SD, SEM or a confidence level to satisfy the interface.

Distinguish a visual interpolation from smoothing that changes reported values and from a fitted physical model. A user-authorized visual guide may be overlaid with its method disclosed, all original observations retained, and a distinct encoding. Do not hide a local reversal, claim a monotonic trend, or identify a decay law merely to make a curve look cleaner. If the scientific role of a requested curve is ambiguous, complete the faithful data plot and identify that specific open choice.

Use colors consistently for the same physical objects across a manuscript. For categorical comparisons, add marker shape or line pattern. Continuous parameters may be encoded by a colorbar; record the normalization. Use a diverging scale only with a meaningful center. Avoid a stock palette rule detached from the observable. Consider direct labels when an extended legend slows comparison.

**Palette selection is part of ordinary plotting, not an optional separate task.** Unless the user has specified colors, read [palette selection](prl-color-palettes.md), select by physical role and load actual colors with `categorical()` / `colormap()`. Record the chosen IDs, category mapping, colormap direction and normalization in the code/provenance. `figure_context(palette_id=...)` applies catalog category colors to the local cycle; its default is `prl-070`. `default_colormap('sequential'|'diverging')` supplies catalog-backed starting maps. These are convenient local starting points, not a preferred palette for every PRL paper. Repeated physical identities keep the same colors; new data roles may use different library entries. Do not copy the old hardcoded color cycle or silently replace library maps with built-ins.

## Legends, panel geometry and tick sides

**Legends and series labels.** Prefer a compact legend inside a genuinely empty part of the data box. Try corners, vertical/horizontal arrangements and compact keys before using an external legend. A repeated descriptor can move to the caption so that the key uses concise identities, provided the mapping stays explicit (for example A–C for Particle A–C). Judge empty space against all curves, scatter markers, error extents, filled intervals, insets and important features; a pale uncertainty band is still data. `place_legend(ax)` in `scripts/prl_layout.py` tests interior locations and alternative column/key layouts against standard artists before falling back above the axes. It preserves font size and data limits; `adapt=False` keeps an explicitly required key geometry. Call it after limits and layout are set, and inspect again after any change. When a dense field or a long key leaves no usable interior, use a dedicated outside/shared legend. Never cover evidence with an opaque legend box, crop observations or inflate limits just to create room. Axis quantities/units remain outside by default. Concise series/phase labels are essential reading labels, not explanatory notes.

**Panel geometry.** For a rectangular grid, align the *drawn data boxes*, not merely the subplot slots or label bounding boxes. Fixed aspect can shrink and center a heatmap within its slot; `fig.colorbar(..., ax=ax)` can also steal width from a single panel. After drawing, compare `ax.get_window_extent()` for each column. A local working tolerance is **0.5 pt** for corresponding left/right edges. Start with a **12–18 mm** horizontal gap for ordinary 85–178 mm scientific layouts, then adjust to the actual labels; this is a design budget, not an APS rule. Do not leave a large empty strip in every row to accommodate one colorbar. Prefer a dedicated colorbar slot, or a horizontal bar below the field when its vertical gutter is easier to budget. Different-size/asymmetric argument layouts need their own declared alignments rather than forced equal boxes.

`layout_panel_grid(axes, column_gap_mm=16, row_gap_mm=18, ...)` aligns a 2-D grid after all data/limits have been set, preserving equal spatial units and keeping the canvas size fixed. Pass only data axes. Budget an external legend/colorbar in the margins or gaps; the helper does not place those decorations. It freezes automatic layout, so do not call `tight_layout` or turn constrained layout back on afterward. `measure_panel_grid(axes)` returns actual boxes, edge spread and gaps. If fixed-aspect panels would be too small, choose a better canvas height or layout, not unequal spatial scales. Top-align panels within each row; different spatial ranges may need different heights while retaining column alignment. Check the exported image for label/colorbar clearance as well as the numeric geometry.

**Tick sides.** Direction and visibility are separate decisions. Retain inward ticks, start with bottom/left marks for ordinary trends, scatter and distributions, and consider top/right marks when a framed spatial map, trajectory or long plotting range benefits from reading coordinates on the far edges. Dense field boundaries, category-only axes, small panels and adjacent colorbars often benefit from fewer marks. Choose per panel from the rendered appearance; neither four-sided ticks everywhere nor their blanket prohibition is the rule. `style_ticks(ax, top=False, right=False)` makes the choice explicit; setting either argument true enables it. Apply the direction separately on the colorbar's own reading side and on meaningful secondary axes. Spines can remain visible without tick marks; do not duplicate numeric labels merely to add opposite ticks.

Final review for these choices: (1) use available inside space without occlusion, (2) measure column edges and inter-panel gaps, (3) confirm palette IDs actually supplied the artist colors/maps, (4) review each panel's visible tick sides. Record detailed measurements separately from the figure canvas.

Matplotlib's [layout guide](https://matplotlib.org/stable/users/explain/axes/constrainedlayout_guide.html), [legend API](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.legend.html) and [tick API](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.tick_params.html) explain the underlying controls. Layout and `loc='best'` are starting tools, not substitutes for the final rendered check.

Suppress repeated tick labels only when the retained scale is unambiguous in the exported layout. Panels using the same variable do not automatically share a readable axis: compare scale type, limits, direction, physical width/height and alignment. A full-width upper panel above two narrower panels normally needs its own numerical ticks and axis quantity. An adjacent logarithmic axis cannot supply the scale for a linear panel. Explicit common axes or genuinely aligned shared axes can avoid repetition; do not force redundant labels onto those valid layouts. Test whether a reader can locate a quoted feature on every panel without reconstructing a hidden coordinate system from the caption.

## Make the claimed difference visible

For each comparison emphasized in the prose, locate the corresponding data in the final-size figure. Distinct legend keys do not make nearly coincident trajectories separable. Record the claim, panel/range, whether its decisive difference is actually visible, and the chosen remedy (or why none is needed).

When a wide dynamic range hides a scientifically relevant difference, select a justified display: an explicitly bounded inset, a second linear-scale panel, a signed difference with its baseline defined, or direct labels for a limited comparison. Choose according to the question; do not require an inset for every figure. Keep the complete main view and all requested observations. A zoom repeats a disclosed subset rather than replacing inconvenient points. A difference/ratio needs its definition, source identities and uncertainty treatment; preserve covariance limitations rather than inventing independent errors. Do not add offsets or exaggerate a separation without stating the transformation.

For example, three MSD curves on logarithmic axes can obscure a late-time ordering that is visible on a linear late-time view. Give the inset's time and ordinate range, retain the full logarithmic panel, use the same group encodings, and distinguish visible numerical ordering from statistical significance. Verify that the new panel remains legible at final size and does not cover important main-panel data. If the claimed effect remains unreadable, revise the layout or qualify the claim; do not mark the figure accepted solely because font and line-width checks pass.

The 85 mm preset is tied to single-column planning. The 178 mm gallery width is a working two-column preview, not a measured universal PRL width. Read the real template's text width. Save fixed-size PNG at 600 dpi without `bbox_inches='tight'`, which can change physical dimensions. Check the actual pixel dimensions and dpi metadata against that size. If vector output is requested, retain vector text and curves; large heatmaps may be rasterized at the requested dpi. Verify accepted upload formats at submission rather than treating every working format as a production deliverable.

## Inspect both the figure and the page

1. Inspect source artists for small base lettering, line/marker dimensions, out-of-figure text and missing glyphs. Error-bar stems use LineCollection; caps have separate stroke widths. Both are checked explicitly.
2. Inspect the actual PNG dimensions, dpi metadata and rendered typography. Only when PDF is requested, inspect PDF dimensions and embedded fonts. Embedded raster text, arbitrary fonts, subscripts and custom transforms need explicit visual review.
3. View the exported figure at intended physical size and a larger diagnostic size. Check overlapping labels, data occlusion, colorbar units, legend ambiguity, panel order, sparse/dense regions and mathematical symbols. If the user requested a grayscale preview, also check that its encodings and decisive comparisons remain readable.
4. Place the figure in the manuscript layout and check scaling again. A figure that passed at 85 mm can fail if subsequently reduced.
5. Review the caption using [caption writing](caption-writing.md) and verify every referenced panel and encoding. Audit the source identity of named quantities using the [quantity ledger](claim-ledger.md#physical-quantity-identity-across-sources-figures-and-text), including normalization denominators; inspect the exported `labels` rather than only the plotting code.

`inspect_figure.py` returns measurements, not a blanket publication-ready verdict. A base-font H-height estimate does not certify every glyph. Its output explicitly identifies untested perception/science dimensions. Thin filled raster boundaries and scatter marker areas are not equivalent to Line2D marker diameters.

Deliver the PNG and requested caption first, with source/data provenance and inspection records as relevant linked artifacts. Include other image formats only when requested. Follow [calibrated, direct writing](assertive-writing.md) for the explanation and mention concrete issues that affect this figure. Include a grayscale preview only when explicitly requested. Label synthetic gallery data as demonstrations.

## Commands

From the skill root, use `.venv/bin/python` if the supplied environment exists, otherwise Python with requirements.txt installed:

```bash
python assets/templates/figure_from_csv.py data.csv --output figures/result --xlabel 'Time (s)' --ylabel 'Distance (m)'
python scripts/render_gallery.py --output reports/gallery
```

When PDF is requested, add `--formats png pdf` to the CSV command; then
`python scripts/inspect_figure.py figures/result.pdf --output figures/result-pdf-inspection.json`
can inspect the exported PDF.

For subsequent user work, put generated outputs in the user's project, not in this skill's corpus or reference gallery.
