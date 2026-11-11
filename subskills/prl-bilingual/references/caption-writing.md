# Captions that preserve the evidence

Apply [calibrated, direct writing](assertive-writing.md). Deliver the caption first. State the plotted evidence and definitions needed to read it. If a reading-critical definition is missing, preserve its unresolved status in the draft caption or label the delivered caption incomplete and name the missing field directly beside it. Save the detailed fact manifest separately when useful; that file does not replace a definition needed to read the caption on its own.

For a new data-backed figure, validate the structured input first with
`python3 scripts/figure_spec.py SPEC.json`. Then use
`python3 scripts/figure_caption.py SPEC.json --details DETAILS.json` when a
deterministic caption and a separate fact manifest are useful. The composer
preserves `caption_mode: authored` byte-for-byte; its `compose` mode uses only
facts explicitly present in the specification or supplied by the caller. It
does not infer sample size, uncertainty, significance, trends, mechanisms or
causality. The resulting text still needs scientific and language review.

State what is plotted or drawn, identify panels, and define the encodings and experimental or computational conditions needed to read the figure. Use a short orienting phrase when useful; do not force a mini-abstract onto every caption.

By default, explanatory notes belong here or in the main text, not as small print on the image. Deliver the caption as separate text or a manuscript caption; do not render it into the figure canvas or bottom margin. Preserve relevant methods, sample sizes, uncertainty definitions and limitations when moving them out of the image. Keep essential graphic labels according to [default canvas text](figure-design.md#default-canvas-text); on-image explanatory notes require an explicit user request.

Verify each item against the actual figure and source:

1. Panel IDs and order agree with the exported image and the main-text references.
2. Axes, symbols and units have consistent meanings; normalized quantities identify the normalization.
3. Colors, line styles and marker shapes have unambiguous referents in the delivered figure. If the user requested a grayscale version, verify its encodings as well. A line joining points must not silently become a theoretical prediction or a fitted model.
4. Bars or shaded regions identify their definition (SD, SEM, confidence interval, quantiles, calibration uncertainty or another specified measure), the ensemble/sample size if supplied, and any dependence across samples when material. Never guess the convention from appearance.
5. Fits identify the fitted quantity and relevant method/range; exclusions and transformations are disclosed when they affect interpretation. A caption cannot repair an unjustified statistical method.
6. Image panels state spatial/time scales, color-bar quantities, common versus independent normalization, and image processing that affects interpretation. Schematic arrows and sizes must not imply measured magnitudes.

Separate the observation from its interpretation. A short supported result statement is welcome; a mechanistic conclusion unsupported by that panel belongs in neither caption nor body. Do not restate every tick or copy the entire results paragraph.

Trace normalization denominators and other named quantities to their source definitions, including subscripts. Define a local rename explicitly and avoid a symbol already assigned to a different quantity in the same model. Equal coefficient values do not establish equal physical meanings. Bind source-reproduction captions and actual axis labels to the [quantity ledger](claim-ledger.md#physical-quantity-identity-across-sources-figures-and-text). For a magnified or transformed view, state its range and transformation while retaining the full-view context.

Original synthetic example: “Mean response of two illustrative series. Circles and squares identify series A and B; solid and dashed curves show their generating functions. Bars indicate fixed illustrative deviations of 0.025 a.u., not estimated statistical uncertainty.” If the source only says “error bars,” leave the convention as an explicit open issue and do not guess SEM.

For Chinese use natural syntax and the same factual checklist. For translation preserve panel references, comparison direction, normalization, uncertainty and causal strength even when sentences are reorganized.
