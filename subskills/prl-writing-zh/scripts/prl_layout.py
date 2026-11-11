"""Inside-first legends, deliberate tick sides, and measurable panel geometry.

These are local design helpers, not journal requirements. Recheck the exported
figure after changing limits, size, labels, or adding artists.
"""
import numpy as np
from matplotlib.collections import PathCollection, QuadMesh


def style_ticks(ax, *, top=False, right=False):
    """Keep inward direction separate from optional mirrored tick marks.

    Call on ordinary Cartesian data axes; style colorbars/secondary axes on
    their own reading side. Spines and tick labels are independent decisions.
    """
    ax.tick_params(axis='both', which='both', direction='in', top=top, right=right)


def _settle(fig):
    previous = None
    for _ in range(8):
        fig.canvas.draw()
        positions = np.array([a.get_position().bounds for a in fig.axes])
        if previous is not None and np.allclose(positions, previous, rtol=0, atol=1e-6):
            break
        previous = positions


def _occupied(ax, box, padding_pt=2):
    """Conservative intersection check in display coordinates, not data bounds.

    Full image/mesh areas are occupied. Filled intervals count as data even
    when pale. Custom collections/transforms still need visual inspection.
    """
    pad = padding_pt * ax.figure.dpi / 72
    box = box.padded(pad)
    renderer = ax.figure.canvas.get_renderer()
    for line in ax.lines:
        if not line.get_visible():
            continue
        path = line.get_path().transformed(line.get_transform())
        marker = line.get_marker()
        extra = line.get_markersize() * ax.figure.dpi / 144 if marker not in (None, '', ' ', 'None', 'none') else 0
        if path.intersects_bbox(box.padded(extra), filled=False):
            return True
    for collection in ax.collections:
        if not collection.get_visible():
            continue
        if isinstance(collection, QuadMesh):
            if ax.bbox.overlaps(box):
                return True
        elif isinstance(collection, PathCollection):
            offsets = collection.get_offset_transform().transform(collection.get_offsets())
            sizes = collection.get_sizes()
            radius = np.sqrt(max(sizes, default=0)) * ax.figure.dpi / 72
            if any(box.padded(radius).contains(*p) for p in offsets if np.isfinite(p).all()):
                return True
        else:
            filled = len(collection.get_facecolors()) > 0
            for path in collection.get_paths():
                if path.transformed(collection.get_transform()).intersects_bbox(box, filled=filled):
                    return True
    for patch in ax.patches:
        if patch.get_visible() and patch.get_path().transformed(patch.get_transform()).intersects_bbox(box, filled=patch.get_fill()):
            return True
    for im in ax.images:
        if im.get_visible() and im.get_window_extent(renderer).overlaps(box):
            return True
    for text in ax.texts:
        if text.get_visible() and text.get_text() and text.get_window_extent(renderer).overlaps(box):
            return True
    return any(child.get_visible() and child.bbox.overlaps(box) for child in ax.child_axes)


def place_legend(ax, *, handles=None, labels=None, ncols=1, adapt=True,
                 candidates=('upper right', 'upper left', 'lower left', 'lower right',
                             'center right', 'center left', 'upper center', 'lower center', 'center'),
                 **kwargs):
    """Use a clean interior location; otherwise put the legend above the axes.

    Call after all data, limits and panel geometry are set. Pass explicit
    handles for category keys. Do not enlarge data limits merely to fit a key.
    ncols and handlelength are initial preferences: adapt=True also tries
    other column counts and shorter keys before falling back outside. Font
    size, labels and data limits are preserved. Set adapt=False for fixed key
    geometry, or use ax.legend for a deliberate shared/custom outside legend.
    """
    if handles is None:
        handles, inferred = ax.get_legend_handles_labels()
        labels = inferred if labels is None else labels
    if not handles:
        return None
    options = dict(frameon=False, borderaxespad=.45, handlelength=1.6,
                   handletextpad=.45, columnspacing=.9, labelspacing=.3)
    options.update(kwargs)
    _settle(ax.figure)
    columns = list(dict.fromkeys([ncols, *range(1, min(len(handles), 4)+1)])) if adapt else [ncols]
    key_lengths = list(dict.fromkeys([options['handlelength'], min(options['handlelength'], 1.5)])) if adapt else [options['handlelength']]
    for key_length in key_lengths:
        for count in columns:
            trial = {**options, 'handlelength':key_length}
            for loc in candidates:
                legend = ax.legend(handles=handles, labels=labels, loc=loc, ncols=count, **trial)
                ax.figure.canvas.draw()
                box = legend.get_window_extent(ax.figure.canvas.get_renderer())
                inside = ax.bbox.contains(box.x0, box.y0) and ax.bbox.contains(box.x1, box.y1)
                if inside and not _occupied(ax, box):
                    return legend
                legend.remove()
    return ax.legend(handles=handles, labels=labels, loc='lower center',
                     bbox_to_anchor=(.5, 1.02), ncols=ncols, **options)


def layout_panel_grid(axes, *, left_mm=14, right_mm=5, bottom_mm=14,
                      top_mm=8, column_gap_mm=16, row_gap_mm=18,
                      auto_height_ratio=.7):
    """Align a rectangular grid's actual data boxes at fixed canvas size.

    Axes are a 2-D array in reading order; colorbar axes must be excluded.
    Colorbars need a dedicated gutter or horizontal slot budgeted in margins
    or row gaps. Call after setting data and limits, before final legends.
    Equal data aspect and limits are preserved. Auto-aspect panels fill each
    row's height; fixed-aspect panels are top-aligned at the same column width.
    The routine freezes automatic layout; later text must be visually checked.
    """
    axes = np.asarray(axes, dtype=object)
    if axes.ndim != 2 or not axes.size:
        raise ValueError('axes must be a nonempty 2-D data-axis grid')
    fig = axes.flat[0].figure
    if any(ax.figure is not fig for ax in axes.flat):
        raise ValueError('all panels must belong to the same figure')
    dims = [left_mm, right_mm, bottom_mm, top_mm, column_gap_mm, row_gap_mm, auto_height_ratio]
    if not np.isfinite(dims).all() or min(dims) < 0 or auto_height_ratio == 0:
        raise ValueError('finite nonnegative margins/gaps and positive height ratio required')
    _settle(fig)
    fw, fh = fig.get_size_inches() * 25.4
    nr, nc = axes.shape
    usable_w = fw-left_mm-right_mm-(nc-1)*column_gap_mm
    usable_h = fh-bottom_mm-top_mm-(nr-1)*row_gap_mm
    if min(usable_w, usable_h) <= 0:
        raise ValueError('canvas cannot contain the requested margins and gutters')
    ratios = np.array([[auto_height_ratio if ax.get_aspect() == 'auto'
                        else float(ax.get_aspect())*ax.get_data_ratio() for ax in row] for row in axes])
    if not np.isfinite(ratios).all() or np.any(ratios <= 0):
        raise ValueError('panel aspect ratios must be positive and finite')
    row_ratios = ratios.max(axis=1)
    width = min(usable_w/nc, usable_h/row_ratios.sum())
    row_heights = width*row_ratios
    start_x = left_mm+(usable_w-width*nc)/2
    top = fh-top_mm
    fig.set_layout_engine(None)
    for i, row in enumerate(axes):
        for j, ax in enumerate(row):
            h = row_heights[i] if ax.get_aspect() == 'auto' else width*ratios[i, j]
            if ax.get_aspect() != 'auto':
                ax.set_adjustable('box')
            ax.set_anchor('NW')
            ax.set_position([(start_x+j*(width+column_gap_mm))/fw, (top-h)/fh, width/fw, h/fh])
        top -= row_heights[i]+row_gap_mm
    fig.canvas.draw()
    return measure_panel_grid(axes)


def measure_panel_grid(axes):
    """Measure drawn edges (not GridSpec slots), excluding any colorbar axes."""
    axes = np.asarray(axes, dtype=object)
    if axes.ndim != 2 or not axes.size:
        raise ValueError('axes must be a nonempty 2-D grid')
    fig = axes.flat[0].figure
    _settle(fig)
    boxes = np.array([[ax.bbox.extents for ax in row] for row in axes])*25.4/fig.dpi
    spreads = [float(np.ptp(boxes[:, col, edge])) for col in range(axes.shape[1]) for edge in (0, 2)]
    gaps = [float(boxes[row, col+1, 0]-boxes[row, col, 2])
            for row in range(axes.shape[0]) for col in range(axes.shape[1]-1)]
    return {'boxes_mm': boxes.tolist(), 'column_edge_spread_max_mm': max(spreads, default=0),
            'column_gaps_mm': gaps}
