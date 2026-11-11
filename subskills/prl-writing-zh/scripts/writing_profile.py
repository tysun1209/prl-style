#!/usr/bin/env python3
"""Resolve selectable editorial instructions, including the preserved v2 route."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def resolve(mode=None):
    profile = json.loads((ROOT / 'profiles/writing-style-profile.json').read_text())
    mode = mode or profile['default_mode']
    if mode not in profile['modes']:
        raise ValueError('Unknown writing mode: ' + mode)
    selected = profile['modes'][mode]
    paths = {k: str(ROOT / v) for k, v in selected.items() if k in ('policy', 'english', 'chinese', 'rule_root')}
    missing = [p for p in paths.values() if not Path(p).exists()]
    if missing: raise ValueError('Missing writing resources: ' + ', '.join(missing))
    return {'mode': mode, 'release_status': profile['release_status'], 'resources': paths}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=['assertive_calibrated', 'legacy_v2'])
    args = parser.parse_args()
    print(json.dumps(resolve(args.mode), ensure_ascii=False, indent=2))
