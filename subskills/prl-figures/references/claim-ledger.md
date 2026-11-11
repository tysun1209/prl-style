# Claims and evidence

For v3 evidence-conditioned wording, use [the extension example](../assets/templates/claim-ledger-v3.json) and [optional assertion audit](assertive-writing.md#optional-audit). The existing v1 ledger and quantity extension remain supported. Map verbs and meaning constraints to each claim; keep this working record separate from ordinary prose delivery.

Use a ledger for long drafting, multiple evidence sources, bilingual work, or substantive rewriting. For a short polish, preserve the same invariants without requiring a separate artifact.

The complete [synthetic example](../assets/templates/claim-ledger.json) is the schema example. The validator checks structure and identifiers. It cannot decide whether evidence entails a claim, verify a cited paper from its ID alone, or establish scientific truth.

## Required records

- `evidence`: unique `id`, `kind` (`author_supplied`, `computed`, `published_verified`, `synthetic_demo`), `source`, exact `locator`, and `description`. Use an input file and hash when available; use a dated author statement if that is the only evidence, and state its limitations. A source URI is not proof of verification.
- `claims`: unique `id`, `text`, `scope`, `strength`, `uncertainty`, `status` (`supported` or `open`), `evidence_ids`, `figure_ids`, `citation_ids`, and `protected_facts`.
- Each protected fact: `id`, scientific `meaning`, normalized string `value`, and `unit` (use `dimensionless` when appropriate). Protect thresholds, ranges, signs, baselines, error conventions and exclusions as well as headline values. Multiple numbers may share a phrase but must remain separate facts.
- `figures`: unique IDs linking to actual figure artifacts when present. `citations`: unique IDs, verified source and `verification: verified`; never create a fabricated DOI or bibliographic entry to satisfy a schema.
- `open_issue`: on an open claim, state the evidence needed. Missing inputs do not become supported claims.

## Evidence audit

For each claim, inspect the actual data, derivation or cited passage. Ask what would make the claim false and whether that alternative was tested. Record whether the statement is observation, model-dependent inference, conjecture, negative result or established derivation. Do not infer a mechanism from correlation, an absence from a nonsignificant result, or universality from a visually appealing collapse.

Make figure–caption–body consistency bidirectional: every emphasized claim should have the promised evidence, and every panel or numerical summary invoked must exist with the described meaning. Do not treat absence of errors in the ID lists as evidence that the prose uses those IDs correctly.

## Physical quantity identity across sources, figures and text

When reproducing a source figure or connecting notation across data, equations and bilingual prose, add `quantities` and `quantity_usages` to the ledger. Equal numerical values do not make two physical quantities interchangeable. Preserve the source symbol by default; if a local rename helps, define it where the reader can see it and avoid another quantity's symbol in the same model scope.

Each quantity has `id`, `meaning`, `source_symbol`, `unit`, `scope`, `evidence_id`, and `source_locator` (page/equation/column). Record unknown units explicitly as `unspecified in source`; do not infer them from typical values. A scope distinguishes unrelated models legitimately reusing a letter. It must not be split artificially to hide a collision within one model.

Each usage has `quantity_id`, `symbol`, `artifact_id`, and `locator`. For figures use locators from the actual `labels` inventory in `export_figure`'s JSON, such as `axes[0].ylabel` or `axes[0].inset[0].xlabel`. For an actual caption or manuscript file the locator is `text`. Declare numerator and denominator separately for a ratio; bind important occurrences in the English and Chinese captions/body as well as the axes. The returned audit includes actual text, source symbol, meaning and unit for each declared location.

Optional `aliases` on a quantity contain `symbol`, `reason`, `definition`, `artifact_id`, `locator`. The definition must appear verbatim in the supplied real text and mention both source and local symbols. The checker rejects aliases colliding with another source symbol/alias in the same scope. It does not infer whether the definition is physically valid. Match only presentation-equivalent TeX forms (such as subscript braces); do not equate distinct subscripts, cases or semantic conventions.

Descriptive source labels and aliases such as `TT power` or `Cosmic variance` are supported; bind them to the actual source definition as for mathematical symbols. Ordinary whitespace is normalized, including line breaks, but word boundaries remain: `TT power` and `TTpower` are distinct names. Matching remains case-sensitive and does not translate labels, infer synonyms or establish scientific equivalence.

A runnable synthetic illustration is [quantity-example.py](../assets/templates/quantity-example.py). It deliberately assigns the same value to two different diffusivities, exports actual labels, binds bilingual captions and verifies the intended identity. It is an API demonstration, not research data.

```bash
.venv/bin/python assets/templates/quantity-example.py --output /tmp/prl-quantity-example
.venv/bin/python scripts/validate_claims.py /tmp/prl-quantity-example/ledger.json \
  --figure-report F=/tmp/prl-quantity-example/figure.json \
  --text captions=/tmp/prl-quantity-example/captions.txt
```

The loader verifies that each figure report still matches its sibling PDF hash. The label inventory records artist text, not a fresh semantic extraction from the PDF; visually inspect the rendered symbols. An old ledger with no quantity extension reports `not_requested`, not a successful identity audit. Declared quantities without real artifacts fail. This bounded check cannot discover omitted quantities, certify source truth, verify all dimensional conversions, or identify arbitrary symbols in unrestricted LaTeX. Review completeness against the real source and every final artifact.

## Commands

From the skill directory:

```bash
.venv/bin/python scripts/validate_claims.py assets/templates/claim-ledger.json
.venv/bin/python scripts/check_manuscript.py assets/templates/manuscript-inventory.json
```

The manuscript inventory is explicit English plain text (`body`, `captions`, `notes`), with separate equation rows, figure dimensions and column span, table line counts, citation IDs and references used. Include all scientific footnotes/endnotes; exclude only categories recorded in the official length guide. Inventory End Matter separately and measure its rendered page count. Do not double count equation or table contents as prose. A 1.5-column item needs manual accounting; the script refuses to silently round it.

`inventory_complete` is an author's or reviewer's attestation, not a machine finding. Compare the inventory with the final manuscript. Unsupported TeX commands or Chinese text are refused by the English word counter. For arbitrary LaTeX, prepare an audited prose inventory or use APS's documented counting procedure; never strip unknown macros and report a confident total.

Exit status: ledger `0` means structural checks passed, `1` means errors. Manuscript `0` means checks passed without the abstract conflict, `1` means errors, `2` means abstract-limit confirmation is required. Every result still needs semantic and rendered-document review.
