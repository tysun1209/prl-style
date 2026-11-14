"""Build the README's native vector artwork and 600 dpi PNG display assets."""
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
NAVY = '#102747'


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
    body = f'''<defs>
      <clipPath id="clip"><rect width="1440" height="430" rx="24"/></clipPath>
    </defs><g clip-path="url(#clip)"><rect width="1440" height="430" fill="{NAVY}"/>
    <rect width="480" height="7" fill="{BLUE}"/><rect x="480" width="480" height="7" fill="{TEAL}"/><rect x="960" width="480" height="7" fill="{ORANGE}"/>
    <circle cx="1250" cy="200" r="275" fill="{TEAL}" opacity=".055"/>
    <circle cx="1250" cy="200" r="202" fill="none" stroke="#ADC9DC" stroke-width="1" opacity=".13"/>
    <circle cx="1250" cy="200" r="145" fill="none" stroke="#ADC9DC" stroke-width="1" opacity=".12"/>
    <path d="M850 340 C1000 330 1000 65 1140 85 S1290 355 1450 200" fill="none" stroke="{BLUE}" stroke-width="9"/>
    <path d="M850 355 C970 300 1050 370 1120 230 S1300 110 1460 125" fill="none" stroke="{TEAL}" stroke-width="7"/>
    <path d="M875 370 C1030 370 1060 305 1170 310 S1330 220 1460 245" fill="none" stroke="{ORANGE}" stroke-width="7"/>
    <circle cx="1140" cy="85" r="11" fill="{BLUE}" stroke="#E9F1F8" stroke-width="3"/>
    <circle cx="1120" cy="230" r="10" fill="{TEAL}" stroke="#E9F1F8" stroke-width="3"/>
    <circle cx="1170" cy="310" r="10" fill="{ORANGE}" stroke="#E9F1F8" stroke-width="3"/>
    <rect x="76" y="91" width="70" height="5" rx="2" fill="{TEAL}"/>
    <rect x="156" y="91" width="38" height="5" rx="2" fill="{ORANGE}"/>
    {letters('PRL Style', 68, 241, 148, '#FFFFFF')}
    {letters('Scientific figures. Bilingual writing.', 78, 309, 35, '#CDDFEA')}
    <path d="M78 350 H710" stroke="#7893AD" opacity=".35"/>
    </g>'''
    save('readme-hero', 1440, 430, body, 'PRL Style — Scientific figures and bilingual writing')
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
        'purpose': 'README branding; decorative curves do not encode research data',
        'palette_ids': ['prl-081', 'prl-070'],
        'colors': {'figures': BLUE, 'palettes': TEAL, 'visual_papers': ORANGE, 'writing_papers': PURPLE},
        'neutral_background': NAVY,
        'font': 'Times New Roman', 'svg_text': 'outlined paths; no font files bundled',
        'png_dpi': 600,
    }, indent=2) + '\n')


if __name__ == '__main__':
    main()
