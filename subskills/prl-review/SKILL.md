---
name: prl-review
description: Audit PRL-oriented figures, bilingual physics prose, captions, layout, evidence scope, and source-backed style rules.
---

# PRL review

Use [calibrated, direct writing](references/assertive-writing.md) for prose and delivery: requested text/artifact first, specific blocking inputs only, detailed audit separate. An explicit `legacy_v2` request resolves preserved instructions with `scripts/writing_profile.py --mode legacy_v2`.

Use this skill for an integrated figure, manuscript, caption, bilingual, or submission-readiness audit. Read the [review rubric](references/review-rubric.md) and only the mode-specific references needed for the artifact. For particle-motion, active-particle, or reinforcement-learning prose, consult [the frozen corpus](references/prl-writing-corpus.md) and verify that any applied rule card is in scope; do not treat corpus observations as official APS policy.

Separate mechanical checks, agent visual/semantic assessment, corpus observations, official APS rules, local defaults and actual human review. For writing style, consult the v3 whole-article guide and source-hash-bound v3 cards; v1 cards are archived and must not be cited. Check claim-to-evidence scope, physical quantities, protected facts, caption/figure consistency, final-size legibility, fonts, inward ticks, clipping, panel references, citations and layout. A passing script does not establish scientific validity or journal acceptance.

Use scripts/figure_spec.py, scripts/validate_claims.py, scripts/check_bilingual.py, scripts/check_layout.py, and scripts/validate_style_rules.py as applicable. Report exact findings, evidence locators, severity, unknowns and concrete remediation steps.

Resolve symlinked references and scripts to their canonical targets before following relative resource links. The writing-profile helper prints absolute paths for both writing modes.
