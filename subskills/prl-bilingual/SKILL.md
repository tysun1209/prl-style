---
name: prl-bilingual
description: Align English and Chinese physics writing while protecting numbers, units, symbols, exclusions, citations, panels, and causal strength.
---

# PRL bilingual alignment

Use [calibrated, direct writing](../../references/assertive-writing.md) for prose and delivery: requested text/artifact first, specific blocking inputs only, detailed audit separate. An explicit `legacy_v2` request resolves preserved instructions with `../../scripts/writing_profile.py --mode legacy_v2`.

Use this skill when English and Chinese versions must remain scientifically equivalent. Read [bilingual alignment](../../references/bilingual-alignment.md), then the relevant [English](../../references/writing-en.md) and [Chinese](../../references/writing-zh.md) guides.

Create a shared claim and quantity map before substantial translation. Preserve numbers, ranges, units, symbols, negations, conditions, panel references, citations and uncertainty definitions. Natural sentence reordering is allowed; a stronger or weaker causal claim is not. ../../scripts/check_bilingual.py detects declared lexical and protected-fact mismatches, but it cannot prove semantic equivalence; perform an independent scientific comparison.

Return both language versions first; link the protected-fact report and identify any specific unresolved semantic issue. Do not silently normalize terminology or values to make the versions look similar.

Resolve symlinked references and scripts to their canonical targets before following relative resource links. The writing-profile helper prints absolute paths for both writing modes.
