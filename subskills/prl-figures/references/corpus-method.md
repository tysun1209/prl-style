# Inspecting sources and extending rules

Start with [figure sources](figure-sources.json), [Fig. 1 schematic sources](schematic-sources.json), [writing sources](writing-sources.json)
and the DOI links in the palette catalog. The distribution contains original
guidance, paraphrased observations and source metadata; acquire source papers
separately when a task needs the actual figure or full text.

For a new source, record its DOI, publication date, acquisition URL and file
hash. Keep research letters separate from comments, replies and corrections.
Inspect the full figure, caption and source page before recording a design rule.
Record the figure/panel, page, crop coordinates, scientific role, observation and
review method. Treat automatic crops and PDF text as candidates until inspected;
PDF extraction can corrupt equations and reading order.

Separate development sources from held-out evaluation papers before deriving
rules. Preserve missing values as unknown. Report observed denominators,
exceptions and counterexamples, and identify whether a rule is an official
requirement, a recommendation, a sample observation or a configurable default.
Keep new source files and their review records in the user's project directory.

Use the rule schema in [style-rule contract](style-rule-contract.md). Existing
reviewer labels describe agent review, not human peer review. A convenience
sample supports source-scoped design observations, not journal-wide frequencies.
Review the rendered result at its intended size before adopting a design.

Recent cross-field visual references: [50 additional PRL papers and 14 composition patterns](crossfield-visual-design.md), with source-scoped observations and palette additions. Query `scripts/select_crossfield_references.py`; the frozen 100-paper writing corpus and previous held-out evaluation remain separate.
