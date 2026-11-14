#!/usr/bin/env python3
"""Select source-backed PRL figure colors without changing global rcParams."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

CATALOG = Path(__file__).resolve().parents[1] / "profiles/prl-color-palettes.json"
CONTINUOUS = {"sequential", "diverging", "cyclic", "multihue"}


def load_catalog(path: Path | str = CATALOG):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("Unsupported palette catalog schema")
    return data


def find_palettes(kind=None, query=None, min_colors=2, path=CATALOG):
    rows = load_catalog(path)["palettes"]
    if kind:
        rows = [r for r in rows if r["kind"] == kind]
    if query:
        query = query.casefold()
        rows = [r for r in rows if query in json.dumps(r, ensure_ascii=False).casefold()]
    return [r for r in rows if len(r["colors"]) >= min_colors]


def get_palette(palette_id, path=CATALOG):
    for row in load_catalog(path)["palettes"]:
        if row["id"] == palette_id:
            return row
    raise KeyError(f"Unknown palette: {palette_id}")


def categorical(palette_id, n=None, *, path=CATALOG):
    """Return an explicit color list; never interpolate categorical identities."""
    row = get_palette(palette_id, path)
    if row["kind"] != "categorical":
        raise ValueError("Use colormap() for an ordered continuous palette")
    colors = row["colors"]
    if n is None:
        return list(colors)
    if isinstance(n, bool) or not isinstance(n, int) or not 1 <= n <= len(colors):
        raise ValueError(f"n must be an integer between 1 and {len(colors)}")
    return list(colors[:n])


def colormap(palette_id, *, reverse=False, path=CATALOG):
    """Reconstruct a sampled sRGB ramp in its reviewed low-to-high direction.

    This approximates the rendered source colorbar, not its unpublished native
    colormap function. It never chooses a data normalization for the caller.
    """
    from matplotlib.colors import LinearSegmentedColormap, ListedColormap
    row = get_palette(palette_id, path)
    if row["kind"] not in CONTINUOUS:
        raise ValueError("Use categorical() for discrete identities")
    points = list(zip(row["positions"], row["colors"]))
    if row.get('interpolation') == 'stepped':
        cmap = ListedColormap(row['colors'], name=row['id'])
    else:
        cmap = LinearSegmentedColormap.from_list(row["id"], points, N=256)
    return cmap.reversed() if reverse else cmap


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("palette_id", nargs="?")
    parser.add_argument("--kind", choices=["categorical", *sorted(CONTINUOUS)])
    parser.add_argument("--query")
    parser.add_argument("--min-colors", type=int, default=2)
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    parser.add_argument('--recommend', action='store_true', help='Choose by color meaning, family and mark visibility')
    parser.add_argument('--family', help='Figure family; physical role takes precedence')
    parser.add_argument('--n-colors', type=int)
    parser.add_argument('--mark', choices=['line','point','fill','field','ordered_lines'])
    parser.add_argument('--background', default='#FFFFFF')
    args = parser.parse_args()
    if args.recommend:
        from palette_selection import select_palette
        result = select_palette(args.family, role=args.kind, n_colors=args.n_colors,
                                mark=args.mark, background=args.background,
                                palette_id=args.palette_id, path=args.catalog)
    else:
        if args.family or args.n_colors or args.mark:
            parser.error('--family, --n-colors and --mark require --recommend')
        result = get_palette(args.palette_id, args.catalog) if args.palette_id else [
        {k: r[k] for k in ("id", "name_zh", "kind", "colors", "uses")}
        for r in find_palettes(args.kind, args.query, args.min_colors, args.catalog)]
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
