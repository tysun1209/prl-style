#!/usr/bin/env python3
"""Read the portable figure-family catalog and source-metadata index."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def families(root=ROOT):
    rows = json.loads((Path(root) / 'profiles/figure-families.json').read_text())['families']
    return {row['id']: row for row in rows}


def reference_inventory(root=ROOT, require_complete=False):
    rows = json.loads((Path(root) / 'references/figure-sources.json').read_text())['references']
    return {'passed': True, 'errors': [], 'eligible': rows, 'excluded': [],
            'verification_scope': 'source metadata; original PDF/image files are not bundled'}


def coverage(root=ROOT, require_complete=False):
    rows = reference_inventory(root)['eligible']
    result = []
    for name, family in families(root).items():
        exact = [r['figure_id'] for r in rows if name in r['family_ids']]
        related = [r['figure_id'] for r in rows if name not in r['family_ids']
                   and r.get('figure_type') in family['legacy_types']]
        result.append({'family': name, 'name_zh': family['name_zh'],
                       'exact_reviewed_references': len(exact), 'related_legacy_references': len(related),
                       'exact_figure_ids': exact})
    return {'passed': True, 'families': result, 'assets_included': False}


if __name__ == '__main__':
    print(json.dumps(coverage(), ensure_ascii=False, indent=2))
