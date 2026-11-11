# Source-backed PRL rules

Read for production dimensions, manuscript accounting, submission checks, and conflicts. Machine-readable values are in [official-rules.json](../profiles/official-rules.json). Verified 2026-10-15; recheck submission-critical requirements when actually preparing a submission. Freshness intervals are local maintenance defaults, not APS rules.

## Authority and scope

- [PRL author guidance](https://journals.aps.org/prl/authors): short research Letters, American English, core and End Matter organization, broad physical readership.
- [APS length guide](https://journals.aps.org/authors/length-guide): count eligible prose plus the specified equivalents for displayed math, figures and tables. Abstracts and references are excluded; captions and subsidiary remarks are included.
- [APS Style Basics](https://journals.aps.org/authors/style-basics): final-size lettering, data points, lines, units, captions and accessible color use.
- [February 2026 APS Style Guide](https://res.cloudinary.com/apsphysics/image/upload/APS_Journals_Style_Guide_Authors022326_guzwhx.pdf): PRL-specific abstract and heading details, especially PDF pages 11 and 15.
- [REVTeX](https://journals.aps.org/revtex): author templates. An author manuscript is not a replica of publisher production typesetting.

## Recorded numerical constraints

PRL core: 3,750 equivalent words. End Matter: up to two pages, separate from the core. Ordinary single-column figure planning width: 85 mm. Full-width figures use the actual document text width, including the column gap, rather than twice the single-column width. Figure capital/numeral height: at least 2 mm; data-point diameter: at least 1 mm; curve line width: at least 0.5 pt. The JSON records the source for each value.

Measure the visible glyph, not its font point size or PDF text span box. Treat embedded rasters, transformed text, math scripts, thin contour details and clipped artists as inspection limitations, not automatic compliance.

## Unresolved abstract limit

The 2026 PDF explicitly gives PRL a 600-character limit. The general HTML abstract advice gives a different word-based limit, and published examples in this corpus are longer than 600 characters. These statements are retained as a conflict. A long abstract must receive a `requires_confirmation` finding in submission checks. Do not quietly change the threshold to 150/250/500 words, infer permission from publication, or discard scientific conditions solely to fit an unverified alternative. Drafting may preserve the longer version and offer a separately labeled condensed candidate.

## Four rule classes

1. Official requirement: traceable and scoped; report deviations.
2. Official recommendation: consider purpose and document justified alternatives.
3. Corpus observation: specify denominator, sample, counterexamples and applicability.
4. Local default: configurable design choice, never attribute to APS.

No official universal font family, color cycle, panel count, mandatory first-panel role, or fixed introduction length was established by this review. The gallery's typography and palettes are local defaults. Accepted papers may contain practices we should not imitate.
