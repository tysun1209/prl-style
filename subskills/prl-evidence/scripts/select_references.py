#!/usr/bin/env python3
"""Search source-linked figure metadata; acquire original images separately for inspection."""
import argparse
import json
import re
from pathlib import Path
from coverage_catalog import ROOT, families, reference_inventory


def select_references(family, query='', limit=5, root=ROOT):
    if limit < 1:
        raise ValueError('limit must be positive')
    catalog = families(root)
    if family not in catalog:
        raise ValueError('unknown family: ' + family)
    words = set(re.findall(r'\w+', query.casefold()))
    rows = []
    for row in reference_inventory(root)['eligible']:
        exact = family in row['family_ids']
        if not exact and row.get('figure_type') not in catalog[family]['legacy_types']:
            continue
        text = ' '.join(str(row.get(k, '')) for k in ['title', 'observations']).casefold()
        rows.append({**row, 'match': 'exact_reviewed_family' if exact else 'related_legacy_type',
                     'query_matches': sum(word in text for word in words)})
    rows.sort(key=lambda r: (r['match'] != 'exact_reviewed_family', -r['query_matches'], r['figure_id']))
    count = sum(r['match'] == 'exact_reviewed_family' for r in rows)
    return {'family': family, 'query': query, 'exact_matches_available': count,
            'related_matches_available': len(rows) - count, 'references': rows[:limit],
            'assets_included': False,
            'notice': 'Metadata from reviewed sources. Open the DOI and inspect the source figure before reuse; this package does not contain or reverify original PDF/image files.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--family', required=True, choices=sorted(families()))
    parser.add_argument('--query', default='')
    parser.add_argument('--limit', type=int, default=5)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = select_references(args.family, args.query, args.limit)
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding='utf-8')
    else:
        print(text, end='')
