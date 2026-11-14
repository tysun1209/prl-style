#!/usr/bin/env python3
"""Verify a PRL distribution or installed skill without third-party packages."""
import argparse
import hashlib
import json
from pathlib import Path

IGNORED_PARTS = {'.venv', '__pycache__', '.git', '.pytest_cache'}
IGNORED_FILES = {'MANIFEST.json', '.prl-package.json'}
DEVELOPMENT_DIRS = {'tests', 'evals', 'benchmarks', 'audit', 'tmp', 'output', 'outputs', 'promo', 'dist'}
PALETTE_PUBLIC_FILES = {'index.html', 'palette-atlas.pdf', 'usage-examples.png',
                        'usage-examples.pdf', 'usage-examples-caption.md', 'distillation-report.md'}


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    return {p.relative_to(root).as_posix(): file_hash(p)
            for p in sorted(root.rglob('*')) if p.is_file() and not p.is_symlink()
            and not set(p.relative_to(root).parts) & IGNORED_PARTS
            and not (p.parent == root and p.name in IGNORED_FILES) and p.suffix != '.pyc'}


def write_manifest(root):
    files = inventory(root)
    data = {'schema': 'prl-distribution-manifest-1', 'files': files}
    (root / 'MANIFEST.json').write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    return data


def publication_errors(files):
    """Reject development outputs even if somebody regenerates the manifest."""
    errors = []
    for name in files:
        p = Path(name)
        if set(p.parts) & DEVELOPMENT_DIRS or p.name.startswith('test_'):
            errors.append('development-only file: ' + name)
        if p.parts[0] == 'reports' and (len(p.parts) != 3 or
                p.parts[1] != 'prl-colors-2025-2026' or p.name not in PALETTE_PUBLIC_FILES):
            errors.append('non-public report: ' + name)
        if p.parts[0] == 'subskills':
            entry = len(p.parts) == 3 and p.name in {'SKILL.md', 'MANIFEST.json'}
            metadata = len(p.parts) == 4 and p.parts[2:] == ('agents', 'openai.yaml')
            if not (entry or metadata):
                errors.append('duplicated subskill resource: ' + name)
    return errors


def verify(root):
    root = Path(root).resolve()
    errors = []
    try:
        manifest = json.loads((root / 'MANIFEST.json').read_text(encoding='utf-8'))
        expected = manifest['files']
        if manifest.get('schema') != 'prl-distribution-manifest-1' or not expected:
            raise ValueError('invalid manifest schema or empty inventory')
        for name in expected:
            p = Path(name)
            if p.is_absolute() or '..' in p.parts or '\\' in name:
                raise ValueError('unsafe manifest path: ' + name)
        for p in root.rglob('*'):
            if not set(p.relative_to(root).parts) & IGNORED_PARTS and p.is_symlink():
                errors.append('symlink: ' + p.relative_to(root).as_posix())
        actual = inventory(root)
        if (root / 'install.py').is_file():
            errors.extend(publication_errors(actual))
        errors.extend('missing: ' + name for name in sorted(expected.keys() - actual.keys()))
        errors.extend('changed: ' + name for name in sorted(expected.keys() & actual.keys())
                      if expected[name] != actual[name])
        errors.extend('unexpected: ' + name for name in sorted(actual.keys() - expected.keys()))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        errors.append(str(exc))
        expected = {}
    return {'passed': not errors, 'files_checked': len(expected), 'errors': errors}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    result = verify(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['passed'] else 1)
