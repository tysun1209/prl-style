---
name: prl-writing-zh
description: Draft and polish natural Chinese scientific writing with PRL-level evidence boundaries, quantity identity, and faithful claim preservation.
---

# PRL Chinese writing

Use [calibrated, direct writing](references/assertive-writing.md) for prose and delivery: requested text/artifact first, specific blocking inputs only, detailed audit separate. An explicit `legacy_v2` request resolves preserved instructions with `scripts/writing_profile.py --mode legacy_v2`.

Use this skill for original Chinese scientific prose, Chinese abstracts, results explanations, figure narratives, and Chinese working drafts.

Read [Chinese writing](references/writing-zh.md), the v3 whole-article guide at `corpus/writing-prl-100/v3/rules/article-format-guide-zh.md`, and the [claim ledger](references/claim-ledger.md). For particle motion, active particles, or reinforcement learning, load the matching v3 cards in [the frozen PRL writing corpus](references/prl-writing-corpus.md) and `corpus/writing-prl-100/v3/rules/writing-style-rules-zh.jsonl`; treat them as conditional observations. Write natural Chinese rather than translating sentence structure mechanically. Preserve numerical values, units, symbols, comparison direction, uncertainty, exclusions, assumptions and causal strength. Keep a broad physical question, compact evidence chain and bounded conclusion. Chinese is a working adaptation, not an official PRL submission format; archived v1 cards are not evidence.

Use scripts/validate_claims.py for evidence-led edits. When the Chinese text must stay synchronized with English, switch to prl-bilingual and run its protected-fact checks. Do not fabricate references, mechanisms or missing results.

Resolve symlinked references and scripts to their canonical targets before following relative resource links. The writing-profile helper prints absolute paths for both writing modes.
