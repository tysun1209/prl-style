# English Letters: a clear result and its evidence

Use [calibrated, direct writing](assertive-writing.md) for drafting, polishing, restructuring and compression. The v3 [whole-article guide](../corpus/writing-prl-100/v3/rules/article-format-guide-en.md) and [source-bound cards](prl-writing-corpus.md) support section-specific decisions. User-requested `legacy_v2` selects the preserved instructions through `scripts/writing_profile.py --mode legacy_v2`.

## Match the edit to the request

| Task | Work to do | Preserve |
|---|---|---|
| Polish | Improve grammar, idiom, rhythm and referents | Meaning, emphasis, evidence and scope |
| Restructure | Reorder the argument and explain material moves | Logical dependencies and claim support |
| Draft | Build an argument from supplied results and sources | Actual evidence, definitions and citations |
| Compress | Remove repetition and process narration | Decisive result, definitions and necessary conditions |

For a short edit, maintain the claim map internally and return the passage. For a full manuscript, use the [claim ledger](claim-ledger.md) to track results and evidence. If a sentence lacks an essential input, complete the supported portion and identify the missing datum after the prose.

## Build the argument

The title names the physical object and distinguishing phenomenon or method. The abstract makes the principal result understandable, including a quantitative comparison when available and the condition that determines its meaning. Choose its opening according to the contribution; a result, puzzle, construction or measurement restriction can each work.

The introduction connects an accessible physical question to the unresolved issue and the contribution. Let each citation establish a relevant fact, contrast or gap. Introduce the model and approximations when the reader needs them. Organize results by what each calculation, observation, comparison or control resolves. Descriptive headings can help a multistep derivation; continuous prose can work for a short evidence sequence.

A result paragraph states a physical finding, identifies its evidence and develops the implication the evidence supports. Shared conditions can live in the setup; an aggregation level, baseline or special regime belongs beside the dependent result. Explain what a comparison changes rather than narrating each curve. Use [figure-to-prose](figure-to-prose.md) when drafting captions and results together.

A closing paragraph answers the physical question and gives a concrete consequence. Include a specific unresolved question when it follows from the result. A catalogue of untested possibilities is unnecessary for a paragraph that makes no claim about them.

## Write direct, precise sentences

Choose the physical object or observable as the subject. Prefer a verb that states what was done or established: measured, calculated, derived, found. A numerical result can be stated directly within its actual scope. A mechanism interpretation remains qualified when alternative explanations are still viable. Exactness and universality are legitimate when a derivation establishes them for the specified model.

Keep numbers, signs, units, ranges, comparison direction, baselines, negations and citation/figure references intact. A pooled mean is distinct from every subgroup; agreement with a fit is distinct from independent validation; lack of a detected difference is distinct from equivalence. Preserve the definition of uncertainty and the identity of the quantity. Check what modifiers and pronouns refer to, including observation dates versus publication dates and the operands of a subtraction.

Remove ceremonial wording such as “it is important to note” when it adds no scientific information. Keep a modal that expresses an untested prediction. For a justified reduction in certainty, qualify the affected clause instead of weakening every sentence in the paragraph.

Original editing example, with synthetic facts: a fixed geometry, three simulated densities, a pooled 12% reduction against a shortest-path baseline. Write: “In a fixed geometry, the mean evacuation time pooled across three simulated densities is 12% lower than the shortest-path baseline.” This is a complete numerical claim. If the task asks about a mechanism, address that separate claim using its own evidence.

## Verify and deliver

Compare the revised passage with its evidence, then review coherence and readability. Return the prose first, followed by material restructuring or exact missing inputs when relevant. Optional `--audit` records the evidence contract and changes separately; see [audit usage](assertive-writing.md#optional-audit).

Default typography is Times New Roman for English/digits and SimSun for Chinese. Follow [typography](typography.md) and the [English template](../assets/templates/manuscript-en.tex) for export. For a complete manuscript, compile it, run `scripts/check_layout.py`, and inspect each rendered page. Use [current official rules](official-rules.md) when the task includes submission formatting.
