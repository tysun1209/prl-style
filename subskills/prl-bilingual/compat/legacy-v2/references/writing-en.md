# English Letters: decisions, evidence, and compression

Read for English drafting, rewriting, polishing and compression. This is a local editorial workflow informed by [reviewed examples](../../../references/evidence-catalog.md); it does not prescribe one compulsory PRL voice. Submission requirements come from [official rules](../../../references/official-rules.md), not from rhetorical frequency.

When the manuscript concerns particle motion, active particles, or reinforcement learning, also read [the frozen 100-paper corpus protocol and rule cards](../../../references/prl-writing-corpus.md) and load the English JSONL cards at `../../../corpus/writing-prl-100/writing-style-rules-en.jsonl`. Apply only cards whose section and topic scope matches the task. They are source-traceable development observations with explicit counterexample searches and extraction limitations, not APS policy or a universal PRL template.

## Establish the editing contract

Default typesetting uses Times New Roman for English and digits, including captions and ordinary Latin/digit mathematics. Follow [typography](../../../references/typography.md) and the [XeLaTeX/Tectonic REVTeX template](../../../assets/templates/manuscript-en.tex); Markdown alone does not enforce a font. Chinese text, if present, uses SimSun.

| Request | Allowed work | Must remain invariant |
|---|---|---|
| Polish | Grammar, idiom, sentence rhythm, explicit referents | Claims, numbers, qualifications, citation support and intended emphasis |
| Restructure | Move or combine paragraphs and evidence; explain major moves | The claim–evidence relationship and logical dependencies |
| Draft | Build prose from supplied facts, figures and verified sources | No invented outcomes, controls, mechanisms, citations or significance |
| Compress | Remove repetition, redundant derivations and tangents | Main result, decisive evidence, definitions and conditions needed to interpret it |

For an ordinary short edit, use an internal claim map; do not burden the user with a form. For a full draft, multiple figures, disputed claims, or bilingual conversion, create the [claim ledger](../../../references/claim-ledger.md). If evidence is missing, write the supported part and list the exact open issue. Do not invent a number to make a sentence look finished. Do not strengthen a weak result merely because the user asks for a more PRL-like tone.

## Design the argument before the sentences

Identify the physical question, what earlier understanding cannot resolve, the new result, the evidence that discriminates it from alternatives, and its boundary. These are reasoning functions, not mandatory paragraph counts. Ask whether a neighboring-field physicist can understand why the result changes an existing expectation. Do not manufacture a field-wide crisis or a claim of priority.

Sketch the evidence order: observation → quantitative characterization → mechanism test or derivation → domain of validity. Change that order when the scientific dependency demands it: a theoretical construction may need its assumptions first; an apparatus paper may need the measurement principle before the signal. A first figure can be a result, mechanism, apparatus or system definition. The corpus supplies counterexamples to a universal first-panel rule.

One paragraph should advance a claim or a necessary dependency. Its opening should orient the reader; subsequent sentences should supply evidence, interpretation and a transition when needed. These functions need not be separate sentences or use stock phrases. Read the paragraph without its first sentence: if nothing is lost, replace the generic opening with a concrete point.

Protect the aggregation level. A pooled or aggregated mean reduction across three conditions does not establish an improvement at every condition, nor the same reduction in each. If only the pooled result is supplied, say “the mean aggregated over the three sampled conditions” and leave condition-resolved behavior open. If the input merely says “across,” do not assume either pooling or a per-condition result. Preserve the reported magnitude with the aggregation level explicitly unresolved, and seek that specific clarification before selecting either interpretation.

## Section-level choices

**Title.** Name the phenomenon and the discriminating feature. Use a result title only when that result is actually established; otherwise a precise descriptive title is stronger than overstated causality. Remove empty emphasis such as “novel,” “unprecedented” or “a comprehensive study of.” Preserve a necessary system or regime qualifier. There is no locally imposed word limit.

**Abstract.** Make the physical question, approach, central finding and bounded implication intelligible without the main text. Prefer a quantitative result when supplied and meaningful. Define indispensable nonstandard abbreviations; omit literature surveys, numbered citations and procedural trivia. Do not force all abstracts into identical four-sentence templates. Check the unresolved official character-limit conflict before submission; retain a faithful long version if compression would erase essential conditions.

**Introduction.** Establish the physics and the specific obstacle using verified literature. Separate what is known from what is conjectured. Explain the present advance by stating what is now established, not by claiming that “few studies exist” without a search. End with the contribution and its physical significance; avoid a tour of section numbers unless it helps an unusually complicated argument.

**Theory and methods.** Introduce assumptions before the conclusions that depend on them. Define symbols at first use and keep dimensionless and dimensional versions distinguishable. Preserve boundary conditions, ensemble, approximations, finite sizes and numerical convergence information that affect the claim. Move specialist derivations to End Matter or supplemental material only if the core remains independently convincing.

**Results.** State the result, identify the exact panel or analysis supporting it, quantify it, then interpret it at the justified level. A smooth fit does not establish a mechanism. A collapse is not by itself proof of universality; a finite-size trend is not an established thermodynamic limit. Describe the comparison baseline and uncertainty convention where they matter. Do not walk through every marker or repeat the caption as prose.

Identify whether a curve is an independent prediction, a fitted result, or a reference supplied with a data release. Agreement imposed by the construction of a released product is not an independent confirmation. Keep reference identity and residual sign clear without burying the physical comparison in processing details. For small differences emphasized in the paragraph, verify that the cited panel actually resolves them at final size; state numerical ordering separately from significance. Preserve source-defined quantity symbols across the paragraph, axis and caption, or explicitly define a noncolliding local notation.

Resolve the referent of every statistical and temporal qualification. Covariance between two input series is distinct from uncertainty of their difference; “its covariance” after a sentence about a difference can name the wrong object. State the two quantities when the antecedent is ambiguous. Observation dates, release dates and analysis dates also have different roles even if the numerals survive an edit. For a spread statistic, identify the values across which it is calculated; day-to-day spread is not automatically within-day variation or the standard error of a monthly mean.

Calibrate negative claims as carefully as positive ones. Distinguish “not calculated here,” “not established by this comparison,” and “impossible from the available information.” Before declaring an inference impossible, inspect the information actually required. Missing off-diagonal parameter covariance does not by itself prevent a conditional approximate interval for one parameter whose marginal standard deviation is supplied, under explicit suitable assumptions. It can still prevent an unsupported joint or response-band calculation. Do not manufacture an interval, assume coverage, or equate a model asymptote with an observed plateau; state precisely which analysis and assumptions are absent.

**Conclusion.** Return to the physical question with the supported answer, then identify the resulting implication and remaining boundary. Distinguish demonstrated reach from a plausible next test. Avoid ungrounded technology claims and generic “opens new avenues” endings. The most useful final sentence often states a specific testable consequence or scope constraint.

**Captions.** Follow [caption-writing.md](../../../references/caption-writing.md). The caption explains how to read the evidence; the main text develops its role in the argument.

For integrated figure/result paragraphs, use [figure-to-prose](../../../references/figure-to-prose.md) and its eight original bilingual fact-packet examples. Select a scientific role, preserve the packet's evidence limits, and adapt the argument rather than reusing a stock sentence.

## Sentence craft without a slogan vocabulary

- Use concrete physical subjects: “The relaxation time increases…” is usually clearer than “It can be clearly observed that…”. Keep passive voice when the procedure or quantity is the relevant subject.
- Put conditions close to the claim they limit. “For the three simulated densities…” prevents a local result from becoming a global assertion.
- Place new information where it connects to the preceding sentence. Reduce nested modifiers and chains of nouns; do not replace all long sentences with choppy fragments.
- Choose verbs by evidence: measured/observed for measurements; calculated/found for numerical results; derived/proved for a result within explicit assumptions; suggests/is consistent with for nondiscriminating evidence. “Demonstrates” is contextual, not automatically banned or automatically justified.
- “Significant” must not imply a statistical test that was never performed. If the meaning is merely a large change, report the size. “Robust” needs named variations; “universal” needs a specified sense and evidence; “first” needs a substantiated literature claim.
- Use American spelling consistently. Preserve field terms, notation and the author's chosen technical conventions unless a change fixes a demonstrated ambiguity.
- Do not add rhetorical excitement to compensate for missing physics. Scientific precision supplies authority.

## Original, synthetic editorial examples

All facts below are constructed editing fixtures, not published results or empirical evidence.

**Numerical example.** Inputs: the mean evacuation time aggregated over three simulated densities is 12% lower than a shortest-path baseline in one fixed geometry; density-resolved changes are not supplied; no hypothesis test or mechanism ablation was supplied.

Weak: “Our innovative strategy significantly improves evacuation in complex environments and reveals a universal mechanism.”

Faithful: “In a fixed geometry, the mean evacuation time aggregated over the three simulated densities is 12% lower than that of the shortest-path baseline. This aggregate reduction does not establish an improvement at each density, identify its mechanism, or establish performance in other geometries.”

Possible title: “Reduced aggregate mean evacuation time in a fixed-geometry routing model.” It preserves scope; it does not claim a new law of collective motion. An abstract would still need the actual physical question and model information, so do not expand these facts into a fabricated complete paper.

**Experimental example.** Inputs: a peak shifts from 2.00 to 2.06 GHz as temperature changes from 10 to 20 K; calibration uncertainty is 0.01 GHz; no microscopic mechanism comparison exists.

Faithful: “The resonance shifts from 2.00 to 2.06 GHz between 10 and 20 K, compared with a calibration uncertainty of 0.01 GHz. The shift establishes a temperature dependence over this interval, but the measurement alone does not distinguish its microscopic origin.” Do not rewrite this as “a phase transition at 20 K” or attach a confidence interval to the calibration uncertainty.

**Theoretical example.** Inputs: an analytical upper bound is derived for a finite chain with nearest-neighbor interactions under a stated weak-coupling approximation; the approximation is not controlled at strong coupling.

Faithful: “Within the weak-coupling approximation, we derive an upper bound for the finite chain with nearest-neighbor interactions. Its behavior outside that regime remains undetermined.” Do not drop “upper,” turn finite into infinite, or describe the approximation-dependent statement as exact for the full model.

**Compression example.** Replace “It is important to point out that the effect is only seen in the finite systems that we studied” with “The effect is established only for the finite systems studied.” Never compress it to “The effect is universal.”

## Finish with two different reviews

First compare claims, protected facts, scope, uncertainty, exclusions, citations and figure IDs against the input. Then assess coherence, information density, readability across subfields, and the relation between captions and prose. A polished sentence that changes the evidence fails the first review regardless of stylistic quality.

For a full manuscript return the edited text, a concise explanation of substantive restructuring, exact remaining scientific questions, and a mechanical-check report. For a short polish return the revised passage and only material caveats. Never represent a length checker, agent assessment or REVTeX rendering as editorial acceptance.
