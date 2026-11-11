---
name: prl-schematics
description: Create and revise PRL-oriented scientific schematics, model and apparatus diagrams, feedback loops, method flowcharts and mixed Fig. 1 compositions from supplied scientific content. Use for 流程图、示意图、模型图、装置图 and scientific Fig. 1 planning.
---

# PRL scientific schematics

Create an original diagram that explains the supplied science at final publication size. Read [schematic design](references/prl-schematics.md) for source-backed composition choices, arrow semantics, geometry, color roles and examples. The [100-paper source index](references/schematic-sources.json) supports targeted source lookup; read relevant entries when a precedent matters, not all 100 by default.

1. Identify the entities, spatial constraints, directed relations and operations the reader must understand. Use the user's supplied science; resolve a missing arrow meaning or boundary condition when it changes the diagram. For a simple request, plan internally and proceed.
2. Choose physical geometry, apparatus plus detail, feedback loop, process sequence, interaction diagram or a mixed schematic/data composition. Fig. 1 does not automatically require a flowchart. Use [ordinary figure design](references/figure-design.md) for quantitative panels.
3. Select and call `scripts/prl_palette.py` unless colors were specified. Keep an entity's color across panels; distinguish categorical identity from numerical fields. Record the palette and object mapping with the source.
4. Draw with editable plotting primitives. `scripts/prl_schematic.py` supplies physical-size panels, nodes and routed arrows; `scripts/render_schematics.py` provides six original examples to adapt. Physical objects need their actual geometry, not generic boxes. Preserve the meaning of motion, force, information, temporal sequence and guide lines.
5. Check actual final-size output: topology and science first, then labels, arrow crossings, aspect ratios, alignment, color and clipping. Run `Diagram.inspect()` for node/route checks and `export_figure` for font/export checks; inspect the saved image as well. Write a separate caption that defines essential symbols and states whether each panel is schematic, simulated or measured.

Default to Times New Roman for English/digits and SimSun for Chinese, with PNG only at 600 dpi. Export PDF/SVG/EPS or change resolution when requested. Do not install fonts. Keep essential object/variable/operation labels close to their subjects, preferably inside available panel space; put explanations and result commentary in the caption. Schematic panels normally have no numerical axes; quantitative panels retain their actual axes and inward ticks, with top/right marks selected per panel.

Deliver the requested figure, editable source and concise caption. Do not copy distinctive source artwork or supply invented result panels. Synthetic examples demonstrate drawing methods. Keep detailed review records separate from the figure and normal delivery prose.

Resolve linked scripts and references to their canonical targets before following relative resources. Pure schematics use entity/relation descriptions; the data-table figure contract is needed only for actual quantitative panels.
