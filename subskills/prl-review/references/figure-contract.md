# Structured figure contract

The contract is the JACS-inspired boundary between scientific inputs and a
renderer. It makes the claim, quantity identity, source status, conditions and
uncertainty definition explicit before a new data-backed figure is rendered.
It does not infer a result from a curve and it does not certify scientific
validity.

## Validate before rendering

Run:

```bash
python3 scripts/figure_spec.py path/to/figure-spec.json --output figure-spec-report.json
```

The report includes `passed`, actionable error codes, warnings, an input hash,
catalog counts and a `semantic_review_required` flag. A failed report is a
blocking input error. A passed report still requires inspection of the actual
PDF/PNG and the supplied source data.

## Required fields

Every specification declares:

- `kind`: one of the 36 IDs in `profiles/figure-families.json`;
- `data_status`: `real`, `synthetic`, or `illustrative`;
- `claim`: the bounded statement the figure is allowed to support;
- `profile`: a profile in `profiles/figure-defaults.json`.

Data-driven families also declare `quantity`, `unit`, `population`, and
`conditions`. `quantity_definition`, `normalization`, `unit_of_analysis`, and
`uncertainty_definition` should be supplied whenever they affect interpretation.
Schematic, network, multipanel, and wide/narrow layout specifications may use
conceptual metadata, but the distinction must remain explicit.

Use `data` or `rows`, not both; a renderable specification must include one of
these containers. Every row may carry an explicit string `id`.
Numbers must be finite and booleans are never numeric data. A missing value is
written as JSON `null` only when `missing_data_policy` states how the row is
retained and disclosed; rows are never silently discarded.

Real data require `source` or `provenance`. Synthetic and illustrative data
must identify their generator or source and are never evidence for a physical
conclusion. The gallery under `reports/coverage/gallery` remains a collection
of original demonstrations, not a citation or a PRL precedent.

## Caption boundary

`caption_mode: authored` preserves the supplied caption exactly. The default
`compose` mode may combine only explicit metadata and caller-supplied computed
facts; it never invents a sample size, uncertainty convention, trend,
significance, causal mechanism, or physical interpretation. See
`scripts/figure_caption.py` and [caption-writing](caption-writing.md).

## Render acceptance

After validation, render with the existing family recipe or `scripts/prl_figure.py`.
Keep the validated JSON, source/data provenance, caption text, facts manifest,
PDF, PNG and JSON export together. Inspect final physical dimensions, fonts,
inward ticks, labels, occlusion, legends/colorbars and the separate caption.
