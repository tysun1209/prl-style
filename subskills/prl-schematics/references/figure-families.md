# Figure families: choose by scientific task

These 36 families are local authoring choices, not a claim that all occur equally often in PRL. The original examples use synthetic data. Source coverage is reported separately in `scripts/coverage_catalog.py` output; a family without an eligible reviewed source remains an explicitly unsupported reference gap.

Use the closest scientific role rather than the closest-looking thumbnail. For a complex figure, combine families while keeping axes, quantities, uncertainty and normalization coherent. A raster preview cannot establish a font identity or final printed size.

## Selection and output

`python scripts/select_references.py --family finite_size_collapse --query "critical scaling"` returns reviewed source metadata, with exact versus related-family tags and DOI provenance; source images are obtained separately. Inspect the actual image, caption and source page before adopting a design decision. If no eligible reference exists, use the scientific design guidance and label the result as an original design; do not invent a PRL precedent.

`python scripts/render_families.py --family finite_size_collapse --output /path/to/project/examples` renders an original demonstration. `--all` renders the complete catalog. Replace demonstration data with author data and preserve definitions; the recipes are not scientific fitting routines. Images default to PNG only at 600 dpi, alongside source data, JSON and captions. Other formats require `--formats` (for example, `--formats png pdf` or `--formats eps`); `--dpi` overrides resolution and grayscale requires `--grayscale`.

## Catalog

| ID | 图型 | Required input | Scientific decision |
|---|---|---|---|
| `line_comparison` | 曲线比较 | paired x/y series | Separate measurements, fits and predictions; disclose joins between samples. |
| `scatter` | 散点关系 | paired observations | Correlation does not establish causation; preserve all observations and encoded size semantics. |
| `uncertainty_bars` | 误差棒 | x/y plus explicit asymmetric or symmetric error extents | State SD, SEM, CI or unknown; do not infer a distribution or independence from bars. |
| `uncertainty_band` | 不确定性带 | central series and lower/upper limits | Identify pointwise versus simultaneous coverage and statistical versus model range. |
| `residuals` | 残差及基准差值 | observations and an explicitly identified reference | Declare subtraction order, units and reference status; a constructed residual is not independent validation. |
| `parity` | 预测与观测一致性 | matched observations and predictions | Identity line differs from fitted regression; retain units and comparable scales. |
| `parameter_sweep` | 连续参数扫描 | ordered parameter and one curve per setting | Use an ordered colorbar for a continuous parameter; avoid categorical color interpretations. |
| `inset_zoom` | 局部放大 | full data plus explicit zoom bounds | Keep the full context; identify changed axis scales and do not crop inconvenient evidence. |
| `histogram` | 直方图与密度 | sample observations and bin edges | State bins, counts versus density and normalization; no smoothing without a disclosed method. |
| `ecdf` | 经验累积分布 | samples including repeated values | Use a step function and correct denominator; no fitted distribution is implied. |
| `box_violin` | 箱线图与小提琴图 | independent groups of samples | Define quartiles/whiskers and kernel bandwidth; report sample size in the caption and avoid hiding small samples. |
| `joint_density` | 二维联合分布 | paired samples and binning or density method | Define bin area, counts or probability density, and preserve outlier support. |
| `survival` | 尾概率与生存曲线 | samples or time/event indicators | A raw sample CCDF is not censoring-adjusted survival; disclose censoring if present. |
| `log_scaling` | 对数标度关系 | positive observations and justified reference trend | Do not infer a power law from a straight-looking log plot; preserve fit range and uncertainty. |
| `finite_size_collapse` | 有限尺寸标度坍缩 | raw curves, sizes and declared scale factors | Retain raw view; exponents must come from author or a disclosed fit, never visual optimization. |
| `phase_discrete` | 离散相图 | categorical phase labels and control coordinates | State phase diagnostic; do not interpolate class IDs or imply precise unmeasured boundaries. |
| `phase_continuous` | 连续序参量图 | scalar diagnostic over a control grid | A color change is not itself evidence of a phase transition; define the diagnostic and uncertainty. |
| `heatmap` | 标量热图 | rectangular grid and scalar values | Specify coordinates, normalization and missing cells; log color requires positive values. |
| `contours` | 等值线 | scalar grid and explicit contour levels | Label levels and disclose interpolation; contours do not create measurements between samples. |
| `correlation_matrix` | 相关矩阵 | variables and a defined covariance/correlation estimator | State estimator and sample basis; symmetry and a centered scale do not establish significance. |
| `image_scalebar` | 实验图像与比例尺 | image plus pixel calibration and processing provenance | Do not invent spatial calibration; disclose contrast and image processing, retain scientific features. |
| `vector_field` | 矢量场 | coordinates, vector components and units | Declare arrow scaling and sampling; magnitude color and arrow length must have defined roles. |
| `streamlines` | 流线 | vector components over a defined coordinate grid | Streamlines of a field are not measured particle trajectories; disclose interpolation and seeding. |
| `space_time` | 时空图 | field samples over time and position | Label both coordinate units and orientation; common normalization across comparisons. |
| `trajectory` | 空间轨迹 | ordered spatial coordinates and time | Distinguish one realization from ensemble behavior; preserve geometry and start/end or time coding. |
| `phase_portrait` | 相空间轨线 | state pairs with time order | State coordinates and direction; a projected orbit does not alone establish stability. |
| `spectrum` | 频谱与峰形 | frequency/energy and response | Define spectral density/amplitude, units, resolution, window and broadening where relevant. |
| `dispersion` | 色散与能带 | wave vector/path coordinate and branches | Define reciprocal-space path and energy reference; do not infer unmeasured topology. |
| `energy_levels` | 能级与跃迁 | energy positions and explicit transition relations | Level positions and arrow widths only encode quantities when defined; selection rules need evidence. |
| `network` | 网络与连接关系 | nodes, edges, weights and optional positions | Graph layout is not physical distance; state directedness and weight meaning. |
| `schematic` | 机制与装置示意图 | entities and supported relationships | Distinguish conceptual relations from established causality; geometry is not to scale unless stated. |
| `polar` | 角分布与极坐标 | angles and radial observables | State angular unit, zero direction and area/radius interpretation; do not invent endpoint continuity. |
| `multipanel` | 规则多面板 | related panels and compatible axes | Each panel needs a readable scale; share limits and colorbars only for comparable quantities. |
| `wide_narrow` | 不等宽组合面板 | full-width context and narrower comparisons | An axis on a narrower panel cannot supply hidden ticks for a wider panel; retain local numerical scales. |
| `surface_3d` | 三维曲面 | two coordinates and scalar height | Justify perspective over a 2D map; document occlusion and do not encode the same quantity ambiguously. |
| `raster_events` | 事件栅格图 | event times and realization/channel IDs | Define each row and observation duration; sparse events do not imply a rate without a denominator. |

## Combinations and alternatives

- Use residuals with the full comparison when a small discrepancy is the claim; define the reference and sign. Use a zoom only when it clarifies the same observable without concealing context.
- Prefer a two-dimensional map or contours when a three-dimensional surface hides values. Use 3D only when geometric structure benefits from perspective and provide a view that resolves important occlusion.
- Use ECDFs for sample distributions without arbitrary bins. Use histograms when bin structure matters; report edges and normalization. A violin depends on a density estimator, so small samples may be better shown as points plus a summary.
- Distinguish discrete class maps from continuous observables. Never average categorical phase IDs to produce a smooth transition.
- Streamlines describe an instantaneous field. Particle paths describe a time-ordered history. A projected state-space portrait is another scientific object; name it precisely.
- Network layout, apparatus geometry and energy-level positions each encode different information. State which distances, arrow widths and node sizes are quantitative.
- For 3D/vector/network figures, typography and font checks are necessary but do not assess occlusion, arrow calibration or graph semantics. Inspect these explicitly.
- For calibrated images, distinguish pixel centers from outer edges. Derive `imshow` extents from the declared calibration. A scale bar should use a rectangle or butt-ended stroke so its visible length matches its declared coordinate span; projecting or round caps can lengthen it.

## Publication context

APS recommends designing for the actual column width and checking readability at that final size. The supplied 85 mm and 178 mm layouts are configurable authoring presets; use the manuscript’s measured text width for placement. See [APS Style Basics](https://journals.aps.org/authors/style-basics#figures), checked 2026-10-16. Preserve the user’s opt-in grayscale policy.

