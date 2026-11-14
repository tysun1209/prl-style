"""Deterministic, role-aware selection from the unchanged PRL palette catalog.

Scores are local design heuristics, not perceptual-uniformity or accessibility
certification. Explicit colors win. Source precedents exclude held-out papers.
"""
from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import numpy as np
from matplotlib.colors import to_rgb, to_rgba, to_hex
from prl_palette import CATALOG, get_palette, colormap

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / 'profiles/palette-selection.json'
REFERENCES = ROOT / 'references/visual-corpus-sources.json'
ROLES = {'categorical', 'sequential', 'diverging', 'cyclic', 'multihue'}
MARKS = {'line', 'point', 'fill', 'field', 'ordered_lines'}


@lru_cache(maxsize=12)
def _read_cached(path, mtime):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def _read(path):
    path = Path(path).resolve()
    return _read_cached(str(path), path.stat().st_mtime_ns)


def family_rule(family=None):
    if family is None:
        return {'role': 'categorical', 'mark': 'line'}
    rules = _read(RULES)['families']
    if family not in rules:
        raise ValueError(f'Unknown figure family: {family}')
    return dict(rules[family])


def _rgb(colors):
    return np.asarray([to_rgb(c) for c in colors], dtype=float)


def _luminance(rgb):
    linear = np.where(rgb <= .04045, rgb / 12.92, ((rgb + .055) / 1.055) ** 2.4)
    return linear @ np.array([.2126, .7152, .0722])


def _contrast(rgb, background):
    a, b = _luminance(rgb), _luminance(_rgb([background]))[0]
    return (np.maximum(a, b) + .05) / (np.minimum(a, b) + .05)


def _distance(rgb):
    # A reproducible separation heuristic; not a Delta E or color-blind test.
    return np.linalg.norm(rgb[:, None] - rgb[None, :], axis=-1) / np.sqrt(3)


def _sources(row, family, reference_path):
    index = _read(reference_path) if reference_path and Path(reference_path).is_file() else {}
    figures = index.get('figures', [])
    held_dois = {f['doi'].lower() for f in figures if f.get('held_out')}
    eligible = [s for s in row.get('sources', [])
                if not s.get('held_out') and s.get('doi', '').lower() not in held_dois]
    keys = {(s.get('doi', '').lower(), str(s.get('figure_number', ''))) for s in eligible}
    matched = [f for f in figures if not f.get('held_out') and family in f.get('family_ids', [])
               and (f['doi'].lower(), str(f.get('figure_number', ''))) in keys]
    return eligible, matched


def _category_candidate(row, n, mark, background):
    rgb = _rgb(row['colors']); contrast = _contrast(rgb, background)
    minimum = 1.15 if mark == 'fill' else 3.0
    allowed = np.flatnonzero(contrast >= minimum)
    if len(allowed) < n:
        return None
    distance = _distance(rgb)
    chroma = np.ptp(rgb, axis=1)
    lightness = np.sqrt(_luminance(rgb))
    target = .82 if mark == 'fill' else .45
    # Start with a visible, colored mark; then maximize the nearest separation.
    chroma_target = .28 if mark == 'fill' else .65
    first = max(allowed, key=lambda i: (-abs(chroma[i]-chroma_target) - abs(lightness[i]-target), -i))
    chosen = [int(first)]
    while len(chosen) < n:
        candidates = [int(i) for i in allowed if i not in chosen]
        chosen.append(max(candidates, key=lambda i: (float(distance[i, chosen].min()), -i)))
    chosen.sort()  # Preserve the source's native ordering in the chosen subset.
    sub = rgb[chosen]
    separation = float(min(distance[i, j] for i in chosen for j in chosen if i != j)) if n > 1 else .5
    light_fit = 1 - float(np.mean(abs(lightness[chosen] - target)))
    chroma_fit = 1-float(np.mean(abs(chroma[chosen]-chroma_target)))
    score = .36*min(separation/.45, 1) + .25*light_fit + .29*chroma_fit
    score += .10*min(float(contrast[chosen].min()) / (2 if mark == 'fill' else 5), 1)
    if mark == 'fill':
        score = .22*min(separation/.25, 1) + .35*light_fit + .35*chroma_fit
        score += .08*min(float(contrast[chosen].min())/1.5, 1)
        score -= .30*float(np.max(abs(lightness[chosen]-target)))
    return chosen, score, {'minimum_background_contrast': float(contrast[chosen].min()),
                          'minimum_rgb_separation': separation}, [0., 1.]


def _continuous_candidate(row, role, mark, background):
    if row.get('interpolation') == 'stepped':
        return None  # Discrete numeric bins must be requested explicitly.
    rgb = _rgb(row['colors']); positions = np.asarray(row['positions'])
    interval = [0., 1.]
    if mark in {'line', 'point', 'ordered_lines'} and role in {'sequential', 'multihue'}:
        valid = _contrast(rgb, background) >= 3
        runs = np.split(np.flatnonzero(valid), np.where(np.diff(np.flatnonzero(valid)) != 1)[0]+1)
        runs = [r for r in runs if len(r) >= 3 and positions[r[-1]]-positions[r[0]] >= .3]
        if not runs:
            return None
        run = max(runs, key=lambda r: positions[r[-1]]-positions[r[0]])
        interval = [float(positions[run[0]]), float(positions[run[-1]])]
        rgb = rgb[run]
    light = np.sqrt(_luminance(rgb)); delta = np.diff(light)
    travel = float(np.abs(delta).sum())
    monotonicity = abs(float(light[-1]-light[0])) / max(travel, 1e-12)
    uniformity = 1/(1+float(np.std(abs(delta)))/max(float(np.mean(abs(delta))), 1e-12))
    metrics = {'lightness_monotonicity': monotonicity, 'lightness_step_regularity': uniformity,
               'source_sample_interval': interval,
               'minimum_background_contrast': float(_contrast(rgb, background).min())}
    if role == 'sequential':
        if monotonicity < .90 or np.ptp(light) < .20:
            return None
        score = .40*monotonicity + .35*uniformity + .15*min(float(np.ptp(light))/.7, 1)
    elif role == 'diverging':
        midpoint = np.array([np.interp(.5, positions, _rgb(row['colors'])[:, k]) for k in range(3)])
        center_l = float(np.sqrt(_luminance(midpoint)))
        left, right = center_l-light[0], center_l-light[-1]
        if left*right <= 0 or min(abs(left), abs(right)) < .15:
            return None
        mid = len(light)//2
        branches = [light[:mid+1], light[mid:]]
        branch_order = min(abs(float(b[-1]-b[0]))/max(float(abs(np.diff(b)).sum()),1e-12) for b in branches)
        if branch_order < .90:
            return None
        neutrality = 1-float(np.ptp(midpoint))
        balance = 1-abs(abs(left)-abs(right)) / max(abs(left), abs(right))
        metrics.update(center_neutrality=neutrality, branch_balance=float(balance), branch_monotonicity=branch_order)
        score = .30*neutrality + .20*balance + .30*branch_order + .10*min(abs(left)+abs(right), 1)
    elif role == 'cyclic':
        closure = float(np.linalg.norm(rgb[0]-rgb[-1]) / np.sqrt(3))
        metrics['endpoint_rgb_distance'] = closure
        if closure > .15:
            return None
        score = .9*(1-closure)
    else:
        score = .5  # Multihue is only selected through an explicit role.
    return list(range(len(row['colors']))), score, metrics, interval


def select_palette(family=None, *, role=None, n_colors=None, mark=None,
                   background='#FFFFFF', palette_id=None, colors=None,
                   objects=None, path=CATALOG, reference_path=REFERENCES):
    """Return a JSON-serializable plan; no drawing or global rcParams mutation.

    Supply physical `role` for general fields; negative values and the word
    phase are not sufficient to infer a diverging/cyclic encoding. Reuse the
    returned object mapping across a manuscript. Explicit palettes retain
    their native order; auto category subsets never interpolate or cycle.
    """
    rule = family_rule(family)
    role = role or rule['role']
    mark = mark or (rule['mark'] if family or role == 'categorical' else 'field')
    if role not in ROLES or mark not in MARKS:
        raise ValueError('Unknown color role or mark type')
    if palette_id is not None and colors is not None:
        raise ValueError('Supply palette_id or explicit colors, not both')
    if to_rgba(background)[3] != 1:
        raise ValueError('Specify the actual opaque background for contrast screening')
    background = to_hex(background).upper()
    if objects is not None:
        objects = list(objects)
        if not objects or any(not isinstance(v, str) for v in objects) or len(set(objects)) != len(objects):
            raise ValueError('objects must be nonempty unique string identities')
        if role != 'categorical':
            raise ValueError('Object identities require a categorical plan')
        if n_colors is not None and n_colors != len(objects):
            raise ValueError('n_colors must match the object identity count')
        n_colors = len(objects)
    if n_colors is not None and (isinstance(n_colors, bool) or not isinstance(n_colors, int) or n_colors < 1):
        raise ValueError('n_colors must be a positive integer')
    if role != 'categorical' and n_colors is not None:
        raise ValueError('Use numeric normalization for continuous values, not n_colors')
    if colors is not None:
        if role != 'categorical' or isinstance(colors, str) or not len(colors):
            raise ValueError('Explicit colors must be a nonempty categorical sequence')
        selected = [to_hex(c, keep_alpha=to_rgba(c)[3] != 1).upper() for c in colors]
        if n_colors is not None and len(selected) != n_colors:
            raise ValueError('Provide one explicit color per object')
        return {'palette_id': None, 'role': role, 'family': family, 'mark': mark,
                'colors': selected, 'background': background, 'selection': 'user_colors',
                'object_colors': dict(zip(objects or [], selected)), 'source_dois': [],
                'reason': 'Explicit user colors take precedence.', 'warnings': []}
    rows = [get_palette(palette_id, path)] if palette_id else _read(path)['palettes']
    if palette_id and rows[0]['kind'] != role:
        raise ValueError(f'{palette_id} is {rows[0]["kind"]}; requested role is {role}')
    n = n_colors if n_colors is not None else (len(rows[0]['colors']) if palette_id and role == 'categorical' else 3)
    candidates = []
    for row in rows:
        if row['kind'] != role or (role == 'categorical' and len(row['colors']) < n):
            continue
        sources, matches = _sources(row, family, reference_path)
        if not palette_id and row.get('sources') and not sources:
            continue
        if palette_id:
            result = (list(range(n if role == 'categorical' else len(row['colors']))), 1., {}, [0., 1.])
        elif role == 'categorical':
            result = _category_candidate(row, n, mark, background)
        else:
            result = _continuous_candidate(row, role, mark, background)
        if result is None:
            continue
        indices, score, metrics, interval = result
        score += .10*bool(matches)
        candidates.append((score, row, indices, metrics, interval, sources, matches))
    if not candidates:
        raise ValueError(f'No suitable {role} palette for {family or "figure"} ({n if role == "categorical" else mark}). '
                         'Reduce category count, change the encoding, or supply explicit colors/palette_id.')
    candidates.sort(key=lambda c: (-c[0], c[1]['id']))
    score, row, indices, metrics, interval, sources, matches = candidates[0]
    selected = [row['colors'][i] for i in indices]
    warnings = []
    if role == 'categorical':
        if n > 6:
            warnings.append('Many categories: retain distinct markers/line styles or split panels.')
        if metrics.get('minimum_rgb_separation', 1) < .16:
            warnings.append('Some category colors are close; use redundant markers or a different palette.')
    elif mark in {'line','point','ordered_lines'} and metrics.get('minimum_background_contrast',3) < 3:
        warnings.append('Some encoded values are pale on this background; use visible outlines/markers. '
                        'The diverging center or full cyclic period is retained, not cropped for contrast.')
    reason = ('Explicit palette; native color order retained.' if palette_id else
              f'{role} encoding; {mark} visibility on {background}; '
              + ('matching calibration figure family.' if matches else 'role/visibility fit; no exact-family precedent.'))
    return {'palette_id': row['id'], 'role': role, 'family': family, 'mark': mark,
            'colors': selected, 'selected_indices': indices, 'background': background,
            'sample_interval': interval, 'interpolation': row.get('interpolation'),
            'bin_edges_normalized': row.get('bin_edges_normalized'),
            'selection': 'user_palette' if palette_id else 'automatic',
            'object_colors': dict(zip(objects or [], selected)),
            'source_dois': sorted({s['doi'] for s in sources}),
            'matched_source_figures': [f['id'] for f in matches],
            'source_scope': 'non-held-out sources only; source match is a figure-level precedent, not a universal rule',
            'reason': reason, 'metrics': metrics, 'warnings': warnings,
            'alternatives': [{'palette_id': c[1]['id'], 'score': round(c[0], 6)} for c in candidates[1:4]],
            'score': round(score, 6), 'score_scope': 'local heuristics; not color-vision certification'}


def plan_colormap(plan, *, path=CATALOG):
    """Keep reviewed direction and stepped boundaries; crop only recorded ranges."""
    from matplotlib.colors import LinearSegmentedColormap
    if plan['role'] == 'categorical':
        raise ValueError('Categorical colors are explicit identities, not a continuous colormap')
    base = colormap(plan['palette_id'], path=path)
    low, high = plan.get('sample_interval', [0., 1.])
    if (low, high) == (0., 1.):
        return base
    return LinearSegmentedColormap.from_list(base.name, base(np.linspace(low, high, 256)), N=256)


def plan_norm(plan, vmin=None, vmax=None, *, center=None, boundaries=None):
    """Construct explicit numerical mapping, never infer a physical reference."""
    from matplotlib.colors import BoundaryNorm, Normalize, TwoSlopeNorm
    if plan['role'] == 'categorical':
        raise ValueError('Use categorical boundaries and explicit identity labels')
    if boundaries is not None:
        if plan.get('interpolation') != 'stepped':
            raise ValueError('Numeric bins require an explicitly selected stepped palette')
        edges = np.asarray(boundaries, dtype=float)
        if edges.ndim != 1 or len(edges) != len(plan['colors'])+1 or not np.isfinite(edges).all() or not np.all(np.diff(edges)>0):
            raise ValueError('Provide one increasing finite boundary per bin edge')
        if center is not None:
            raise ValueError('Numeric boundaries already define the color mapping')
        return BoundaryNorm(edges, len(plan['colors']))
    if vmin is None or vmax is None or not np.isfinite([vmin, vmax]).all() or vmin >= vmax:
        raise ValueError('Supply finite vmin < vmax; do not invent a scale for constant/empty data')
    if plan.get('interpolation') == 'stepped':
        edges = plan.get('bin_edges_normalized')
        if not edges:
            raise ValueError('Stepped palette requires explicit numeric boundaries')
        return plan_norm(plan, boundaries=vmin+np.asarray(edges)*(vmax-vmin), center=center)
    if plan['role'] == 'diverging':
        if center is None or not np.isfinite(center) or not vmin < center < vmax:
            raise ValueError('Diverging colors require an explicit center inside the data range')
        return TwoSlopeNorm(vcenter=center, vmin=vmin, vmax=vmax)
    if center is not None:
        raise ValueError('A center is only meaningful for a diverging encoding')
    return Normalize(vmin, vmax)
