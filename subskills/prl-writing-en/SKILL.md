---
name: prl-writing-en
description: Draft, polish, compress, and restructure English physics Letter prose while preserving claims, quantities, uncertainty, and evidentiary scope.
---

# PRL English writing

Use [calibrated, direct writing](references/assertive-writing.md) for prose and delivery: requested text/artifact first, specific blocking inputs only, detailed audit separate. An explicit `legacy_v2` request resolves preserved instructions with `scripts/writing_profile.py --mode legacy_v2`.

Use this skill for English abstracts, introductions, results, conclusions, figure narratives, captions, and Letter restructuring.

Read [English writing](references/writing-en.md), the v3 whole-article guide at `corpus/writing-prl-100/v3/rules/article-format-guide-en.md`, and use the [claim ledger](references/claim-ledger.md) for substantial edits. If the topic is particle motion, active particles, or reinforcement learning, load the scoped v3 cards in [the frozen PRL writing corpus](references/prl-writing-corpus.md) and `corpus/writing-prl-100/v3/rules/writing-style-rules-en.jsonl`; use only cards whose section/topic scope matches. Keep the problem, contribution, evidence, boundary conditions and uncertainty distinct. Preserve signs, units, ranges, negations, causal strength, citations and physical-quantity identity. A request for stronger prose does not authorize a stronger scientific conclusion. The archived v1 cards are not evidence.

Run scripts/validate_claims.py for a ledger and scripts/check_manuscript.py for an English inventory. Compile the actual manuscript when possible, then use scripts/check_layout.py and inspect every rendered page. Separate official APS requirements from local defaults and corpus observations. Return the revised prose first, followed by material changes or specific missing inputs when applicable.

Resolve symlinked references and scripts to their canonical targets before following relative resource links. The writing-profile helper prints absolute paths for both writing modes.
