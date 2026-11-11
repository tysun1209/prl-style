#!/usr/bin/env python3
"""Build native editable PPTX objects from an agent-authored, image-guided scene.

This does not infer objects from pixels. Inspect the PNG and author the scene first.
Coordinates are millimetres from the top-left; object order is back-to-front.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE, MSO_CONNECTOR_TYPE, MSO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Mm, Pt


SHAPES = {'rect': MSO_AUTO_SHAPE_TYPE.RECTANGLE,
          'roundrect': MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE,
          'ellipse': MSO_AUTO_SHAPE_TYPE.OVAL}
ALIGN = {'left': PP_ALIGN.LEFT, 'center': PP_ALIGN.CENTER, 'right': PP_ALIGN.RIGHT}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def element(name, **attributes):
    item = OxmlElement(name)
    for key, value in attributes.items():
        item.set(key, str(value))
    return item


def walk(objects):
    for obj in objects:
        yield obj
        if obj['kind'] == 'group':
            yield from walk(obj['objects'])


def resolve_asset(base, name):
    path = Path(name)
    return path if path.is_absolute() else base / path


def validate_scene(scene, base):
    if scene.get('schema_version') != 1:
        raise ValueError('expected scene schema_version 1')
    width, height = scene['width_mm'], scene['height_mm']
    if not all(isinstance(v, (int, float)) and not isinstance(v, bool)
               and math.isfinite(v) and 0 < v <= 1000 for v in [width, height]):
        raise ValueError('finite positive canvas dimensions required')
    source = resolve_asset(base, scene['source_png']['path'])
    if sha256(source) != scene['source_png']['sha256']:
        raise ValueError('source PNG hash mismatch')
    with Image.open(source) as image:
        if image.format != 'PNG':
            raise ValueError('source must be PNG')
        if abs((image.width / image.height) / (width / height) - 1) > .01:
            raise ValueError('canvas aspect ratio must match the source PNG')
    objects = list(walk(scene['objects']))
    ids = [o['id'] for o in objects]
    if len(ids) != len(set(ids)):
        raise ValueError('object IDs must be unique')
    if not any(o['kind'] in {*SHAPES, 'path', 'connector'} for o in objects):
        raise ValueError('editable native geometry is required; an image/text-only slide is insufficient')
    for obj in objects:
        kind = obj['kind']
        if kind not in {*SHAPES, 'text', 'path', 'connector', 'group', 'raster'}:
            raise ValueError('unknown object kind: ' + kind)
        if kind == 'group':
            continue
        if kind in {'path', 'connector'}:
            coords = []
            commands = obj['commands'] if kind == 'path' else [['M', *obj['start']], ['L', *obj['end']]]
            if not commands or commands[0][0] != 'M':
                raise ValueError('a path must begin with M')
            for command in commands:
                expected = {'M': 2, 'L': 2, 'C': 6, 'Z': 0}.get(command[0])
                if expected is None or len(command) - 1 != expected:
                    raise ValueError('path commands support M, L, C and Z')
                coords.extend(zip(command[1::2], command[2::2]))
            if len(set(coords)) < 2:
                raise ValueError('a route needs distinct points')
            if kind == 'connector' or obj.get('arrow_end') or obj.get('arrow_start'):
                if not obj.get('meaning', '').strip():
                    raise ValueError('semantic arrows require a meaning')
            for endpoint in ('from', 'to'):
                if endpoint in obj and obj[endpoint] not in ids:
                    raise ValueError('unknown relation endpoint: ' + obj[endpoint])
        else:
            x, y, w, h = obj['box']
            if w <= 0 or h <= 0:
                raise ValueError('positive object dimensions required')
            coords = [(x, y), (x + w, y + h)]
        if any(not all(isinstance(v, (int, float)) and math.isfinite(v) for v in point)
               or not 0 <= point[0] <= width or not 0 <= point[1] <= height for point in coords):
            raise ValueError('object outside canvas or nonfinite geometry: ' + obj['id'])
        if kind == 'text':
            if not isinstance(obj.get('text'), str) or not obj['text'].strip():
                raise ValueError('text must be nonempty')
            if obj.get('align', 'center') not in ALIGN:
                raise ValueError('invalid text alignment')
            if not math.isfinite(obj.get('font_pt', 10)) or obj.get('font_pt', 10) <= 0:
                raise ValueError('positive font size required')
        if kind == 'raster':
            if not obj.get('raster_reason', '').strip():
                raise ValueError('retained raster needs a declared reason')
            if sha256(resolve_asset(base, obj['path'])) == scene['source_png']['sha256']:
                raise ValueError('the source PNG belongs on the reference slide, not the editable slide')
    return source


def rgb(value):
    return RGBColor.from_string(value.lstrip('#'))


def style(shape, obj):
    fill = obj.get('fill')
    if fill and hasattr(shape, 'fill'):
        shape.fill.solid()
        shape.fill.fore_color.rgb = rgb(fill)
    elif hasattr(shape, 'fill'):
        shape.fill.background()
    stroke = obj.get('stroke')
    if stroke:
        shape.line.color.rgb = rgb(stroke)
        shape.line.width = Pt(obj.get('line_pt', 1))
        line = shape._element.spPr.get_or_add_ln()
        line.set('cap', 'rnd')
        if obj.get('dash'):
            line.append(element('a:prstDash', val='dash'))
        for key, tag in [('arrow_start', 'a:headEnd'), ('arrow_end', 'a:tailEnd')]:
            if obj.get(key):
                line.append(element(tag, type='triangle', w='med', len='med'))
    else:
        shape.line.fill.background()


def freeform(shapes, obj):
    commands = obj['commands']
    coords = [(x, y) for c in commands for x, y in zip(c[1::2], c[2::2])]
    x0, y0 = min(p[0] for p in coords), min(p[1] for p in coords)
    w = max(max(p[0] for p in coords) - x0, .001)
    h = max(max(p[1] for p in coords) - y0, .001)
    shape = shapes.add_shape(SHAPES['rect'], Mm(x0), Mm(y0), Mm(w), Mm(h))
    props = shape._element.spPr
    props.remove(props.prstGeom)
    geometry = element('a:custGeom')
    for tag in ('a:avLst', 'a:gdLst', 'a:ahLst', 'a:cxnLst'):
        geometry.append(element(tag))
    geometry.append(element('a:rect', l='0', t='0', r='r', b='b'))
    paths = element('a:pathLst')
    path = element('a:path', w=int(Mm(w)), h=int(Mm(h)),
                   fill='norm' if obj.get('fill') else 'none', stroke='1', extrusionOk='0')
    for command in commands:
        node = element({'M': 'a:moveTo', 'L': 'a:lnTo', 'C': 'a:cubicBezTo', 'Z': 'a:close'}[command[0]])
        for x, y in zip(command[1::2], command[2::2]):
            node.append(element('a:pt', x=int(Mm(x-x0)), y=int(Mm(y-y0))))
        path.append(node)
    paths.append(path)
    geometry.append(paths)
    props.insert(1, geometry)
    return shape


def add_objects(shapes, objects, base):
    for obj in objects:
        kind = obj['kind']
        if kind == 'group':
            shape = shapes.add_group_shape()
            add_objects(shape.shapes, obj['objects'], base)
        elif kind in SHAPES:
            shape = shapes.add_shape(SHAPES[kind], *[Mm(v) for v in obj['box']])
            if kind == 'roundrect':
                shape.adjustments[0] = obj.get('roundness', .12)
            style(shape, obj)
        elif kind == 'text':
            shape = shapes.add_textbox(*[Mm(v) for v in obj['box']])
            frame = shape.text_frame
            frame.clear()
            frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
            frame.word_wrap = False
            frame.auto_size = MSO_AUTO_SIZE.NONE
            frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            for index, line in enumerate(obj['text'].split('\n')):
                para = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
                para.alignment = ALIGN[obj.get('align', 'center')]
                para.space_before = para.space_after = Pt(0)
                run = para.add_run()
                run.text = line
                run.font.name = obj.get('font', 'Times New Roman')
                run.font.size = Pt(obj.get('font_pt', 10))
                run.font.bold = obj.get('bold', False)
                run.font.italic = obj.get('italic', False)
                run.font.color.rgb = rgb(obj.get('color', '#17212B'))
                run._r.get_or_add_rPr().append(element('a:ea', typeface=obj.get('cjk_font', 'SimSun')))
        elif kind == 'connector':
            shape = shapes.add_connector(MSO_CONNECTOR_TYPE.STRAIGHT,
                                         *[Mm(v) for v in [*obj['start'], *obj['end']]])
            style(shape, obj)
        elif kind == 'path':
            shape = freeform(shapes, obj)
            style(shape, obj)
        else:
            shape = shapes.add_picture(str(resolve_asset(base, obj['path'])), *[Mm(v) for v in obj['box']])
        shape.name = obj['id']
        if hasattr(shape, 'shadow'):
            # PowerPoint's default theme otherwise adds shadows even to paths.
            shape.shadow.inherit = False
        # LibreOffice may still resolve the theme reference despite effectLst.
        for effect_ref in shape._element.xpath('./p:style/a:effectRef'):
            effect_ref.set('idx', '0')
        if obj.get('meaning'):
            nv = shape._element.xpath('.//p:cNvPr')[0]
            nv.set('descr', obj['meaning'])


def inspect_pptx(path):
    prs = Presentation(path)
    counts = {'text': 0, 'native_geometry': 0, 'raster': 0, 'groups': 0}
    names, texts = [], []

    def inspect(shapes):
        for shape in shapes:
            names.append(shape.name)
            if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
                counts['groups'] += 1
                inspect(shape.shapes)
            elif shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                counts['raster'] += 1
            elif shape.has_text_frame and shape.text.strip():
                counts['text'] += 1
                texts.append(shape.text)
            else:
                counts['native_geometry'] += 1
    inspect(prs.slides[0].shapes)
    return {'slides': len(prs.slides), 'editable_slide': 1, 'reference_slide': 2,
            'counts': counts, 'object_names': names, 'editable_text': texts,
            'all_primary_objects_native': counts['raster'] == 0}


def render_preview(pptx, output, office, dpi=600):
    import pymupdf as fitz
    if not isinstance(dpi, int) or not 36 <= dpi <= 2400:
        raise ValueError('dpi must be an integer from 36 to 2400')
    executable = shutil.which(str(office))
    if not executable:
        raise ValueError('Office renderer not found: ' + str(office))
    with tempfile.TemporaryDirectory(prefix='prl-pptx-render-') as directory:
        tmp = Path(directory)
        env = dict(os.environ, SAL_USE_VCLPLUGIN='svp')
        command = [executable, '-env:UserInstallation=' + (tmp/'profile').as_uri(),
                   '--headless', '--convert-to', 'pdf', '--outdir', str(tmp), str(Path(pptx).resolve())]
        proc = subprocess.run(command, capture_output=True, text=True, env=env, timeout=120)
        pdf = tmp / (Path(pptx).stem + '.pdf')
        if proc.returncode or not pdf.is_file():
            raise RuntimeError('PPTX rendering failed: ' + proc.stdout[-1500:] + proc.stderr[-1500:])
        with fitz.open(pdf) as doc:
            doc[0].get_pixmap(dpi=dpi, alpha=False).save(str(output))
            fonts = sorted({r[3] for r in doc[0].get_fonts()})
            text = doc[0].get_text()
    return {'status': 'rendered_not_visually_reviewed', 'engine': str(executable),
            'dpi': dpi, 'path': str(output), 'sha256': sha256(output), 'fonts': fonts,
            'extracted_text': text}


def build(scene_path, output, *, office=None, dpi=600):
    scene_path, output = Path(scene_path).resolve(), Path(output).resolve()
    if output.suffix.lower() != '.pptx':
        raise ValueError('output must end in .pptx')
    scene = json.loads(scene_path.read_text(encoding='utf-8'))
    source = validate_scene(scene, scene_path.parent)
    prs = Presentation()
    prs.slide_width, prs.slide_height = Mm(scene['width_mm']), Mm(scene['height_mm'])
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.name = 'Editable reconstruction'
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = rgb(scene.get('background', '#FFFFFF'))
    add_objects(slide.shapes, scene['objects'], scene_path.parent)
    slide.notes_slide.notes_text_frame.text = scene.get('caption', '') + '\nImage-guided native-object reconstruction.\n' + json.dumps(scene.get('provenance', {}), ensure_ascii=False)
    reference = prs.slides.add_slide(prs.slide_layouts[6])
    reference.name = 'Model-generated PNG — visual reference only'
    image = reference.shapes.add_picture(str(source), 0, 0, width=prs.slide_width, height=prs.slide_height)
    image.name = 'Reference PNG (not editable scientific objects)'
    reference.notes_slide.notes_text_frame.text = 'Original model-generated visual reference. Edit native objects on slide 1. Source SHA256: ' + sha256(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    prs.save(output)
    with Image.open(source) as image:
        pixels = list(image.size)
    report = {'pptx': str(output), 'pptx_sha256': sha256(output),
              'scene_sha256': sha256(scene_path), 'source_png_sha256': sha256(source),
              'source_pixels': pixels, 'target_width_mm': scene['width_mm'],
              'source_effective_dpi': round(pixels[0] * 25.4 / scene['width_mm'], 2),
              'source_pixels_modified': False, 'reconstruction_method': 'agent-authored semantic scene',
              'structure': inspect_pptx(output), 'retained_raster': [o['id'] for o in walk(scene['objects']) if o['kind'] == 'raster'],
              'relations': [{k: o[k] for k in ('id', 'from', 'to', 'meaning') if k in o}
                            for o in walk(scene['objects']) if o.get('meaning')],
              'preview': {'status': 'not_rendered'},
              'limitations': ['Structural checks do not prove scientific correctness or visual equivalence.',
                              'Connector endpoints and freeform points are editable; automatic attachment is not guaranteed.']}
    report_path = output.with_suffix('.export.json')
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if office:
        try:
            report['preview'] = render_preview(output, output.with_suffix('.preview.png'), office, dpi)
        except Exception as error:
            report['preview'] = {'status': 'render_failed', 'error': str(error)}
            report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            raise
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scene', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--office', help='LibreOffice/soffice executable; renders the actual PPTX for review')
    parser.add_argument('--dpi', type=int, default=600)
    args = parser.parse_args()
    print(json.dumps(build(args.scene, args.output, office=args.office, dpi=args.dpi), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
