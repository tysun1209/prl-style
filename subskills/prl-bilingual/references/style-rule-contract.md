# Source-scoped style-rule cards

JACS separates a reusable recommendation from the evidence that supports it.
The PRL skill uses the same boundary. A rule card is not a hidden style law:
it must state where it applies, what it recommends, what could contradict it,
what the review did not establish, and where the source can be inspected.

Validate the checked-in cards with:

```bash
python3 scripts/validate_style_rules.py references/figure-style-rules.jsonl \
  --reviews corpus/metadata/figure_reviews.jsonl
```

## Evidence classes

`official_requirement` and `official_recommendation` require an authoritative
URL and `source_type: official`. `conditional_observation` requires accepted
corpus review rows and is descriptive only. `local_default` and
`local_design_rule` describe this skill's configurable workflow; they are never
attributed to APS. Related-only and held-out references cannot be silently
promoted to exact calibration support.

Each card includes an explicit `counterexamples` list. An empty list is valid
only when `limitations` says that counterexamples were not recorded. This makes
absence of evidence visible rather than turning it into universal advice.

## Review discipline

Use a card to decide what to inspect, then inspect the actual source figure and
the final export. The rule validator checks provenance and bookkeeping; it
does not certify typography, scientific correctness, accessibility, or journal
acceptance. Update a card only with a new source locator, support denominator,
counterexample review, and verification date when those facts are available.
