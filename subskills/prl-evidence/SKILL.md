---
name: prl-evidence
description: Find PRL figure and writing precedents, inspect source papers, and develop source-scoped scientific style rules.
---

# PRL evidence and source analysis

Use this skill to locate source precedents, analyze new papers or extend the
style rules. Read [corpus method](references/corpus-method.md),
[evidence catalog](references/evidence-catalog.md) and
[style-rule contract](references/style-rule-contract.md).

Search figure metadata with `scripts/select_references.py --family FAMILY`.
Use `references/writing-sources.json` and the source-located writing cards for
prose examples, and `scripts/prl_palette.py` for color sources. The package
contains DOI metadata and original observations, not downloaded paper PDFs or
source crops. Retrieve the actual paper when visual or full-text inspection is
needed; do not report an excluded source as locally verified.

For new sources, record source locations, hashes, review methods and the scope
of each observation. Keep development, held-out and unreviewed material separate.
Report denominators, exceptions and counterexamples. Distinguish official APS
requirements from observations and configurable defaults. Save new source
material and review records in the user's project.

Deliver requested findings directly. Apply the [writing policy](references/assertive-writing.md)
and preserve scientific facts. `scripts/writing_profile.py` resolves the current
or explicitly requested `legacy_v2` writing guides.
