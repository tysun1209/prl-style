---
name: prl-style
description: Design and audit PRL-oriented physics figures, scientific schematics and Fig. 1 flowcharts; draft, polish, restructure and translate scientific writing in English and native Chinese. Use for Physical Review Letters figure style, captions, Letter narratives, bilingual alignment and evidence-preserving compression. Chinese is a working adaptation, not an official PRL publication format.
---

# PRL figures and bilingual scientific writing

Writing uses v3 [calibrated, direct prose](references/assertive-writing.md): state supported results directly, place necessary conditions beside the claims they qualify, and deliver the requested prose or figure first. Keep detailed audit records separate; mention specific missing inputs that affect the requested result. An explicit `legacy_v2` request selects preserved guides through `scripts/writing_profile.py --mode legacy_v2`. The [writing profile](profiles/writing-style-profile.json) records the current mode and release status.

Reproduce the communication standards of a precise physics Letter: a clear physical question, compact evidence, legible final-size figures, and conclusions proportionate to the evidence. Preserve the user's data, technical conventions and intended meaning. A published paper is an observation, not a universal template; no single font, palette, panel sequence or stock phrase defines PRL.

This is the integrated router for the [PRL skill suite](references/skill-suite.md). Use `prl-figures`, `prl-schematics`, `prl-writing-en`, `prl-writing-zh`, `prl-bilingual`, `prl-captions`, `prl-review`, or `prl-evidence` when the request is clearly limited to that mode; keep `prl-style` for combined or ambiguous work.

## Choose the relevant mode

Read only the references needed for the task. If the request is already clear, proceed without asking the user to fill out a questionnaire.

| Request | Read and use | Deliver |
|---|---|---|
| Scientific schematic, apparatus/model diagram, feedback loop, method flowchart or mixed Fig. 1 | `prl-schematics`; [source-backed schematic design](references/prl-schematics.md); `scripts/prl_schematic.py` and original examples in `scripts/render_schematics.py` | Original 600 dpi PNG, editable source and concise caption defining entities, arrow meanings and schematic/data status |
| Figure planning, generation or revision | [Figure design](references/figure-design.md); [palette selection](references/prl-color-palettes.md); [figure families and recipes](references/figure-families.md) for type selection; [captions](references/caption-writing.md) when needed | Source/data provenance, fixed-size 600 dpi PNG, precise inspection findings; other formats on request |
| PRL color selection or palette distillation | [2025–2026 source-backed palettes](references/prl-color-palettes.md); `scripts/prl_palette.py` for colors and colormaps | Colors linked to source figures, physical roles, direction and numeric bins |
| New data-backed figure specification or reproducible caption | [Figure contract](references/figure-contract.md), [captions](references/caption-writing.md), and the relevant family recipe | Validated JSON specification, PNG/source, caption text, separate caption-facts manifest, and semantic review findings; other image formats on request |
| English draft, polish, restructure or compression | [English writing](references/writing-en.md); [claim ledger](references/claim-ledger.md) for substantial work | Faithful prose, material changes and unresolved scientific inputs |
| Chinese original draft or polish | [Chinese writing](references/writing-zh.md) | Natural Chinese argument with the same scientific standards and boundaries |
| Translation or synchronized bilingual versions | [Bilingual alignment](references/bilingual-alignment.md) and the target-language guide | Both versions mapped to common claims, protected-fact checks and semantic review |
| Integrated figure, caption and results writing | [Figure-to-prose](references/figure-to-prose.md) plus the relevant language guide | Consistent evidence, visual encoding and bounded interpretation in natural English/Chinese |
| Integrated paper/figure audit | [Review rubric](references/review-rubric.md) plus the relevant mode | Prioritized actionable findings tied to exact passages, panels and evidence |
| Corpus analysis or rule update | [Corpus method](references/corpus-method.md), [evidence catalog](references/evidence-catalog.md), [style-rule contract](references/style-rule-contract.md), [official rules](references/official-rules.md) | Source-located observations with denominators, exceptions, counterexamples and verification dates |

For submission dimensions, length or formatting, read [official rules](references/official-rules.md) and verify current APS/PRL guidance. Explicitly distinguish official requirements, recommendations, corpus observations and local defaults. Preserve unresolved conflicts, including the abstract-limit discrepancy; do not invent a convenient replacement limit.

## Shared scientific invariants

- Establish which claim each paragraph or figure supports, its evidence, scope and uncertainty. For a short edit do this internally; for a full manuscript maintain a [claim ledger](references/claim-ledger.md).
- Never fabricate data, references, novelty, error definitions, controls, mechanisms or statistical significance. Missing evidence produces a bounded draft and a concrete open issue. A request for stronger prose does not authorize a stronger scientific conclusion.
- Preserve numerical values, signs, units, bounds, baselines, negations, assumptions, figure/citation references and causal strength. Inspect scientific meaning before judging elegance. A smooth rewrite or a passing script cannot compensate for changed meaning.
- Preserve physical quantity identity across source equations, axes, captions and both languages. Equal values do not justify substituting symbols. For source reproduction or integrated figure/text work, use the [quantity ledger extension](references/claim-ledger.md#physical-quantity-identity-across-sources-figures-and-text) and bind it to actual exported labels and text; explicitly define any noncolliding rename.
- Do not discard inconvenient data, change uncertainty, normalize away a discrepancy, or crop away evidence for appearance. Any scientifically motivated transformation must be supported, disclosed and reproducible.
- Respect user-selected fonts, colors, structures and terminology where compatible with the task; explain concrete conflicts. Local defaults are configurable, not editorial mandates.
- **默认图件只保存 PNG，分辨率为 600 dpi。** PDF、EPS、SVG 等格式仅在用户提出相应需求时导出；用户指定其他分辨率时按其要求执行。源码、数据来源、图注和检查记录按任务需要交付。
- **默认刻度线朝内（`in`）**：横纵轴的主刻度和次刻度均朝向图内，子图、局部放大图和色标沿用此设置。仅在用户明确要求时改用其他方向；特殊投影需检查实际渲染效果。
- **图例优先放在图内空白处**，保持数据、误差带和关键结构可见；没有合适空白时再外置或共用图例。轴名称和单位不因此搬入图内。上侧、右侧刻度逐面板选择，不能把“朝内”理解为全部开启四边刻度。
- Default typography for figures and writing: **Times New Roman for English/Latin letters and digits; 宋体 (SimSun) for Chinese**, including captions, labels, ticks, legends and annotations. Follow [typography](references/typography.md) for math, font availability and document export. Do not silently substitute another typeface when the requested font is missing.
- **默认不在图片上添加小字注释。** Put explanatory notes in the separate caption or main text, including method/parameter summaries, fit statistics, caveats, provenance and result commentary. Do not place them in panel corners or canvas margins. Keep essential reading labels (axes/units, ticks, legends, colorbars, panel IDs, scale bars and necessary diagram labels). Add explanatory text on the image only when the user explicitly requests it; see [figure design](references/figure-design.md#default-canvas-text).
- Do not copy a particular paper's prose or distinctive artwork. Use original phrasing and original diagrams based on the supplied science.

## Execution and validation

Resolve symlinked SKILL.md and reference files to their canonical targets, then resolve relative resource paths there. Run helpers with a Python environment satisfying [requirements.txt](requirements.txt); `.venv/bin/python` is the tested local interpreter when present. Do not install or change global packages merely to read or edit prose.

**Figures:** choose from the [36-family catalog](references/figure-families.md), then use a suitable recipe, [the CSV template](assets/templates/figure_from_csv.py) or `scripts/prl_figure.py`. For a new data-backed figure, validate `figure-spec.json` with `scripts/figure_spec.py` before rendering; compose a caption and fact manifest with `scripts/figure_caption.py` when a structured delivery is requested. `scripts/select_references.py` searches reviewed source metadata and distinguishes exact family tags from related examples. Original source PDFs and crops are not bundled; open the DOI and inspect the source figure and caption before adapting. Preserve final physical dimensions; inspect the exported PNG, labels, curve/point sizes and caption. Review custom math, scatter, images and occlusion separately. Return the 600 dpi PNG, source, data provenance and relevant specification/caption/inspection records. Export additional or alternative formats only on request using `export_figure(..., formats=['png', 'pdf'])` or CLI `--formats png pdf`; use `dpi` / `--dpi` for a requested resolution override. Inspect PDF dimensions and embedded fonts only when PDF was requested. Generate and review a grayscale preview only when explicitly requested. The 36 runnable recipes generate original synthetic demonstrations, not research results or proof of a PRL precedent for every family.

For every ordinary figure task, select and **call** `scripts/prl_palette.py` by physical role unless the user supplies colors; record the palette ID and object–color mapping in source/provenance. A library reference alone is not palette use. Use `scripts/prl_layout.py` for inside-first legends, independent tick-side choices and actual panel-edge measurements. In a regular panel grid, align the drawn left/right edges of each column and budget colorbars separately; check final gaps after fixed-aspect axes have settled. See the concrete [layout criteria](references/figure-design.md#legends-panel-geometry-and-tick-sides).

**Writing:** choose polish/restructure/draft/compress permissions explicitly from the request. Use the [English REVTeX demonstration](assets/templates/manuscript-en.tex), [Chinese working fragment](assets/templates/manuscript-zh.md), or [bilingual figure narratives](assets/templates/figure-narratives.json) only as scaffolding; replace all fictional facts with actual evidence. Run `scripts/validate_claims.py` for a ledger and `scripts/check_manuscript.py` for an audited English inventory. The length checker is not an arbitrary LaTeX parser. Before release-quality figure or manuscript work, run `scripts/check_prl_environment.py`; use `--strict` only when exact Times New Roman and SimSun are required. Compile actual manuscripts when an engine is available, then use `scripts/check_layout.py` and inspect every rendered page; preserve the compile command and logs. A successful exit does not establish legible glyphs, correct references or balanced pages. See [local layout validation](references/figure-to-prose.md#在实际页面上验收); otherwise state that compilation remains unverified.

**Bilingual:** run `scripts/check_bilingual.py` when maintaining structured protected spans. It detects declared lexical/numerical problems; independently compare scientific meaning, exclusions and argument flow. Never label lexical consistency as proof of semantic equivalence.

**Final review:** compare scientific meaning with evidence, then review language or final-size appearance. Deliver the artifact first, followed by material findings and exact missing inputs when applicable. Save detailed records separately; `scripts/audit_assertive_writing.py --audit PATH` provides optional writing audits. Distinguish mechanical checks, agent assessment and actual expert review.

## Sources and distribution

The public [source indexes](references/corpus-method.md) retain DOI links and
source-scoped observations. Original source papers, crops and historical
development evaluations are not included. Source hashes identify development
inputs; do not claim those absent assets were verified on the user's machine.
Read [distribution notes](NOTICE.md) for the validation scope. Run
`python3 scripts/verify_package.py` for distributed-file integrity.
