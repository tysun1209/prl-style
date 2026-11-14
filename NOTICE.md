# Distribution notes

This independent project supplies PRL-oriented scientific writing and figure
guidance. It is not an APS or PRL product.

The package contains original code, instructions, paraphrased observations,
templates and synthetic examples, together with bibliographic metadata and
source-linked color values. Original papers, extracted paper text, source
figure crops and font files are excluded. Source DOIs and locators remain
available for inspection. Color values are approximate sRGB samples, not the
authors' unpublished plotting constants.

Third-party Python dependencies are installed separately under their own licenses.
Times New Roman, SimSun and LaTeX distributions are external dependencies when
the requested output requires them.

## Validation

The distributed resources are checked for integrity, relocation, independent
installation and core runtime behavior. Development test suites and detailed
test outputs remain outside the public package. Codex is the development host;
Claude Code and OpenCode directory layouts are tested locally, without claiming
that their agent models have completed the same workflow evaluations.

Exact-SimSun Chinese manuscript compilation and page inspection were not
completed in the development environment. Font availability is reported by
`scripts/check_prl_environment.py`; use `--strict` when both exact fonts are
required. Pure-text writing does not depend on these fonts.

For a research deliverable, inspect the actual exported figures or compiled
manuscript and verify scientific meaning against the supplied evidence.

## License status

No open-source license has been selected for the original project content.
This package does not itself grant a new open-source license; contact the
project owner for the applicable terms before redistributing or modifying it.
