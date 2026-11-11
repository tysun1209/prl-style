# Calibrated, direct writing (v3)

The [profile](../profiles/writing-style-profile.json) selects `assertive_calibrated`. An explicit `legacy_v2` request selects frozen English/Chinese guides through `scripts/writing_profile.py --mode legacy_v2`. This resolves writing instructions; the audit CLI checks supplied text. Scientific invariants and current figure defaults apply in both modes.

Lead with the result supported by the available evidence. Use a concrete physical subject and a verb that describes the work: measured, calculated, derived, found, or showed. An established result deserves a direct sentence. An interpretation with viable alternatives deserves its qualification. These are choices about the claim, not a ranking of impressive words.

Use this policy for English and Chinese prose, bilingual alignment, captions, figure explanations and review findings. The default deliverable is the requested prose or figure plus any specific issue that affects its use. Keep the internal evidence check out of the manuscript. A short edit does not need a user-facing ledger or audit form.

## Put information where it helps

- Keep a condition in the sentence when removing it changes the claim: a measured interval, a pooled mean, an approximation, or a comparison baseline.
- State an established method or scope once, then use that shared context while it remains clear. Repeat a condition in the abstract or caption when that item must stand alone.
- Mention an untested mechanism when the paragraph interprets a mechanism. A paragraph reporting a numerical comparison does not need a list of everything that comparison did not prove.
- Close on the established physical answer or a concrete implication. Include a remaining boundary when it changes that answer; a limitations sentence is not a required ending.
- When inputs are incomplete, write the supported portion and identify the exact missing datum for the blocked sentence. For example: “The error-bar definition is missing.”

For a draft caption whose reading-critical definition is unavailable, retain the unresolved definition in that caption or mark the caption explicitly as incomplete beside the delivered text. A detached audit file cannot make an undefined error bar interpretable. A bare measured mean need not discuss an absent comparison, and a run-count statement need not discuss convergence, unless the text makes those inferences. In a fidelity-preserving edit, retain supplied scientific qualifications or explicitly identify their relocation; concision alone does not authorize silently dropping information.

Example: “In a fixed geometry, the mean evacuation time pooled across three simulated densities is 12% lower than the shortest-path baseline.” The numerical statement is direct and scoped. Add a mechanism discussion only when the task calls for one.

中文示例：“在固定几何下，合并三个模拟密度后的平均疏散时间比最短路径基线降低12%。”条件已经限定了结果，无须在句尾追加“不能证明机制或普适性”。若接下来解释机制，则把尚未区分的解释写在该讨论处。

## Evidence and verbs

| Claim | Direct wording when supported | Qualification that changes the claim |
|---|---|---|
| Observation | measured, observed, found / 测得、观察到、发现 | measurement interval, uncertainty convention |
| Numerical comparison | calculated, increases, lower than / 计算得到、升高、低于 | baseline, aggregation and tested conditions |
| Theory | derived, proved / 推导出、证明 | exact model, assumptions, bound direction |
| Discriminating mechanism test | establishes, demonstrates / 证实、建立 | alternatives actually tested; regime of the test |
| Non-discriminating evidence | is consistent with, suggests / 与……一致、提示 | alternative explanation or conditional interpretation |

“Show” and “demonstrate” are not universal mechanism claims. Their admissibility depends on what they take as their object. Do not mechanically change “suggests a mechanism” to “establishes a mechanism” because a different sentence has strong evidence. Preserve justified exact results; `exact` is not a banned word.

The 20–35% reduction target is a batch diagnostic for eligible redundant expressions, not a per-sentence deletion quota. Plain “may/可能” can convey real uncertainty. The lexical audit separates modal candidates from editorial padding and does not certify semantic equivalence.

## Optional audit

For substantial edits, use [the v3 ledger example](../assets/templates/claim-ledger-v3.json) and [edit input](../assets/templates/assertive-edit.json). The existing v1 claim/quantity ledger API remains usable.

```bash
.venv/bin/python scripts/audit_assertive_writing.py \
  --input assets/templates/assertive-edit.json \
  --ledger assets/templates/claim-ledger-v3.json \
  --language en --section results --audit reports/assertive-writing.json
```

`--audit PATH` writes the detailed report; `--output` is an alias. Without it, the CLI prints only a short status and concrete failures. English/Chinese are selected with `--language en|zh`. `--mode assertive_calibrated|legacy_v2` records the writing policy being audited; it does not rewrite text. The agent chooses the corresponding guide when drafting.

Map each edit segment to one atomic claim ID. Split passages containing multiple claims into separate segments so one result cannot lend its evidence permissions to another. Each record preserves original/revised sentences, evidence IDs, facts, boundary constraints, verb changes and unresolved checks. Approved boundary paraphrases belong in `forms`; exact string matching alone cannot decide a new paraphrase's meaning.

`required_boundary` accepts strings or `{id, forms}` alternatives; `required_boundaries` is a legacy input alias. `protected_terms` binds baseline, comparison direction, aggregation, negation, uncertainty definitions and causal meaning. `allowed_verbs` belongs to a claim; `allowed_strengthening` permits scope terms such as “exact” only when its evidence supports them. `supporting_artifacts` refers to entries in `evidence_ids`. An unresolved claim yields `needs_evidence`, not a factual pass. Physical-quantity auditing remains in the existing ledger checker.
