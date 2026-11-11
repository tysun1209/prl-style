# Review order and acceptance

Apply [v3 calibrated assertiveness](assertive-writing.md): check that established results are direct, necessary qualifications modify the right claim, and repeated generic disclaimers are removed. A clear, scoped result does not need a final limitations sentence. The 20–35% redundant-hedge target is a batch diagnostic; assess naturalness in context.

Use this rubric to audit a complete manuscript, figure set or bilingual deliverable. Findings must name the source passage, panel, evidence or artifact; avoid scoring an impression without a concrete reason.

## Noncompensable failures

Any changed scientific fact, unsupported claim, fabricated citation, misleading transformation, unresolved reference essential to the argument, or unreadable decisive evidence prevents acceptance. Stylistic fluency, compactness and visual attractiveness cannot offset these failures. Explain a precise correction or identify the missing input.

Mechanical tools check only the invariants they implement. `passed` is always scoped to that tool. “No errors found” is not “scientifically valid,” “semantically equivalent,” or “ready to submit.”

## Editorial dimensions

| Dimension | Evidence to inspect | Passing behavior |
|---|---|---|
| Scientific fidelity | Input data/claims versus output | Facts, assumptions, uncertainty and strength preserved |
| Physical argument | Question → contribution → discriminating evidence → boundary | Reader can explain what changed and why evidence supports it |
| Cross-field readability | Unfamiliar terms, definitions, motivating problem | Neighboring-field physicist can follow without generic background padding |
| Information density | Each paragraph's role; repeated captions/results | Necessary details retained, redundancy removed |
| Figure communication | Final-size PDF, labels, panel semantics | Main comparison readable; no ambiguity from color or layout |
| Caption independence | Encodings, conditions, error convention | Figure can be read correctly without guessing |
| Native language quality | English idiom or Chinese syntax in context | Precise, connected prose without translation artifacts or hype |
| Bilingual fidelity | Claim-level comparison, including absent claims | Same evidence, scope, negative statements and causal implications |
| Production compliance | Current APS rules, inventory, compiled layout | Measurable requirements checked; unresolved conflicts reported |

Use `pass`, `revise`, or `unassessed` for each applicable dimension with a short reason. Do not average a failed scientific invariant into a high overall score. Distinguish inaccessible evidence from a demonstrated error.

For source reproduction, trace each central physical quantity through its source definition, plotted label, caption and both versions of the prose. An undeclared symbol substitution can remain ambiguous even when all numerical checks pass. Record separately whether the finding is a numerical error, a definition conflict, or a notation clarification; do not inflate an editorial issue into a demonstrated scientific error.

For dense curves, identify the precise comparison the text emphasizes and inspect that range at final size. State whether a reader can follow the relevant groups and see the claimed separation. A legend alone is insufficient. Generate and assess a grayscale preview only if the user explicitly requested one; its absence is otherwise not a review defect. If a zoom or transformed panel is used, verify full-view retention, ranges, definitions and uncertainty. For native Chinese quality, quote the phrase and explain the improvement in context; neither keyword matches nor eliminating all Latin letters establishes naturalness.

For every quantitative panel, locate the visible numerical scale and quantity name, whether local or explicitly shared. If tick labels are suppressed, verify that the retained axis has matching limits, scale and geometric alignment. Different panel widths or a log/linear change can make apparently shared ticks unusable. Record such omissions as figure-communication defects even when all plotted values and page dimensions pass mechanical checks.

During sentence-level review, identify the operands of a stated transformation and the objects modified by dates, uncertainty terms and pronouns. A preserved numeral attached to a release date instead of an observation interval is still a meaning change. A processed-quantity prefix absorbed into a Chinese operation verb is an ambiguity even when the plotted subtraction is correct. Keep computational errors, semantic changes and optional phrasing improvements separate in the record, and preserve the original verdict when a corrected copy is retested.

## Task-dependent checks

For experiments inspect units, calibration, noise/uncertainty and controls. For theory inspect assumptions, bound direction, equality versus approximation and validity regime. For simulations inspect finite size, convergence, random seeds/ensembles when supplied, baselines and parameter coverage. For images inspect scale bars and processing. These are review questions, not permission to invent missing analysis.

For a style comparison, first control for subject and figure role. Compare against multiple source-located examples; explain counterexamples. Blind comparison can evaluate perceived stylistic similarity but cannot prove scientific merit or represent every PRL subfield. A real physicist's external assessment is distinct from an agent evaluation and must be labeled honestly.

## Delivery and change control

Return corrected artifacts when authorized, a short prioritized list of material changes, reproducible mechanical checks and remaining scientific questions. Include hashes for archived review artifacts. If reviewed bytes change, the corresponding review becomes stale and must be repeated or invalidated.

The repository's six-stage plan records local development gates. A later change to a checker, evidence record or rendered artifact requires revalidation of affected gates. A final acceptance report lists executable regressions separately from source-located and independent agent reviews; never describe these as one undifferentiated set of “tests.”
