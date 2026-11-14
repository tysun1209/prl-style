"""Build the four README statistic cards; preserve the model-generated cover."""
from pathlib import Path
import json
import sys

import pymupdf
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath
from matplotlib.path import Path as MplPath

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from prl_palette import categorical
from typography import resolve_font

OUT = Path(__file__).resolve().parent
FONT = FontProperties(fname=resolve_font('Times New Roman'))
BASE = categorical('prl-081')
BLUE, TEAL, ORANGE = BASE[0], BASE[2], BASE[3]
PURPLE = categorical('prl-070')[0]


def letters(text, x, y, size, color, center=False):
    path = TextPath((0, 0), text, size=size, prop=FONT)
    if center:
        x -= path.get_extents().width / 2 + path.get_extents().x0
    segments = []
    for points, code in path.iter_segments(curves=True, simplify=False):
        values = ' '.join(f'{v:.3f}' for v in points)
        segments.append({MplPath.MOVETO: 'M', MplPath.LINETO: 'L',
                         MplPath.CURVE3: 'Q', MplPath.CURVE4: 'C',
                         MplPath.CLOSEPOLY: 'Z'}[code] + ('' if code == MplPath.CLOSEPOLY else values))
    return f'<path fill="{color}" transform="translate({x:.3f} {y}) scale(1 -1)" d="{" ".join(segments)}"/>'


def save(name, width, height, body, title):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
           f'viewBox="0 0 {width} {height}" role="img"><title>{title}</title>{body}</svg>')
    (OUT / (name + '.svg')).write_text(svg)
    with pymupdf.open(stream=svg.encode(), filetype='svg') as source:
        pdf = source.convert_to_pdf()
    with pymupdf.open(stream=pdf, filetype='pdf') as source:
        image = source[0].get_pixmap(matrix=pymupdf.Matrix(2, 2), alpha=True)
        image.set_dpi(600, 600)
        image.save(OUT / (name + '.png'))


def main():
    for name, value, label, color in [
        ('figures', '36', 'FIGURE TYPES', BLUE),
        ('palettes', '555', 'PALETTES', TEAL),
        ('visual-papers', '291', 'VISUAL REFERENCES', ORANGE),
        ('writing-papers', '100', 'WRITING REFERENCES', PURPLE),
    ]:
        body = (f'<rect width="310" height="122" rx="14" fill="{color}"/>'
                '<path d="M245 -10 L320 65 V-10 Z" fill="#FFFFFF" opacity=".09"/>'
                '<path d="M0 87 H310 V108 Q310 122 296 122 H14 Q0 122 0 108 Z" fill="#07182D" opacity=".28"/>'
                + letters(value, 155, 75, 70, '#FFFFFF', center=True)
                + letters(label, 155, 110, 20, '#FFFFFF', center=True))
        save('readme-stat-' + name, 310, 122, body, value + ' ' + label)
    (OUT / 'readme-branding.json').write_text(json.dumps({
        'purpose': 'Four README statistic cards; the model-generated cover has separate provenance in readme-hero.json',
        'palette_ids': ['prl-081', 'prl-070'],
        'colors': {'figures': BLUE, 'palettes': TEAL, 'visual_papers': ORANGE, 'writing_papers': PURPLE},
        'font': 'Times New Roman', 'svg_text': 'outlined paths; no font files bundled',
        'png_dpi': 600,
    }, indent=2) + '\n')


if __name__ == '__main__':
    main()
