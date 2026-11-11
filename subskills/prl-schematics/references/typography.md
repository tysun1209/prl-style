# Default typography

This is the user's local default, not a claim about PRL's publisher typeface.

- English/Latin letters and digits: **Times New Roman**, with its actual bold and italic faces when needed.
- Chinese and Chinese punctuation: **宋体 (SimSun)**.
- Apply the defaults to prose, titles, captions, axes, tick values, legends, panel labels and annotations. Preserve a later explicit user override.
- Keep current font sizes and physical figure dimensions unless the rendered result needs a justified layout adjustment.

## Figures

`figure_context()` and the CSV template default to the `times` profile. Latin is the first font and SimSun supplies Chinese glyphs, so mixed labels retain Times New Roman digits. The older `sans` and `serif` profiles remain explicit opt-ins. Use the helper rather than loading the style sheet alone: it checks font availability and refreshes a stale Matplotlib font cache when needed.

Mathtext uses Times New Roman for ordinary Latin letters and digits, including italic and bold variants. Calligraphic alphabets and missing mathematical symbols use STIX; do not replace a scientific symbol to force a text font. Check actual exported math glyphs. This follows Matplotlib's [custom math font mechanism](https://matplotlib.org/stable/users/explain/text/mathtext.html).

English-only figures can render with Times New Roman when SimSun is absent. A default-style figure containing Chinese must have SimSun installed; `export_figure` rejects it before writing any requested images if that font is missing. Do not replace SimSun with a generic `serif`, Nimbus, Droid, or another CJK font and claim compliance.

## Writing and export

Use [the English REVTeX template](../assets/templates/manuscript-en.tex) or [the Chinese LaTeX working template](../assets/templates/manuscript-zh.tex) with **XeLaTeX or Tectonic**. They select Times New Roman explicitly for Latin text, digits and ordinary Latin/digit mathematics, using [mathspec](https://ctan.org/pkg/mathspec). Other math symbols retain the math-package fonts. The Chinese template selects SimSun explicitly; its bold Chinese headings use declared synthetic bold because SimSun generally has no separate bold face. It is a local working format, not an official Chinese PRL format.

For Chinese inside an otherwise English manuscript, use XeLaTeX with `xeCJK` and `\setCJKmainfont[AutoFakeBold=2]{SimSun}` (and the corresponding CJK sans/mono settings from the Chinese template). Merely selecting Times New Roman does not provide Chinese glyphs.

Markdown and chat prose cannot enforce installed fonts. Keep their content semantic and apply these defaults in the exporting document/editor. In Word, set both the Latin/ASCII and complex-script font to Times New Roman and the East Asian font to SimSun, including heading and caption styles. In HTML, use `font-family: "Times New Roman", "SimSun"` and verify the actual fonts in the browser. Do not claim a plain Markdown preview has a locked font.

## Availability and verification

Use the actual installed fonts. If unavailable, report the missing family and request its local font file/path; do not download unverified substitutes. On Linux, user-installed fonts normally live under `~/.local/share/fonts/`; after installation run `fc-cache -f` and restart the rendering process. `fc-match SimSun` alone is insufficient: it can return an unrelated substitute.

Verify PDF font resources and per-span fonts for Latin, numbers and Chinese, plus missing-glyph warnings and final-size layout. Prior gallery/layout reports document their original font settings; this default change does not retroactively restyle archived evidence.

Before a release-quality figure or manuscript check, run `scripts/check_prl_environment.py --output reports/environment-preflight.json`. The preflight refreshes Matplotlib's user-font table, records the exact family name, path and SHA-256 for Times New Roman and SimSun, and verifies the inward-tick defaults. Use `--strict` as the release gate; a diagnostic preview may proceed without it, but must remain marked as a substitute-font preview.
