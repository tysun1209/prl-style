#!/usr/bin/env python3
"""Install independent copies of all eight PRL skills. Python 3.10+, no extra packages."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
from verify_package import verify, write_manifest

SHARED = ('references', 'assets', 'profiles', 'scripts', 'corpus', 'compat', 'evals', 'reports')
PUBLIC_FILES = ('README.md', 'VERSION', 'NOTICE.md', 'LICENSE', 'requirements.txt')
MARKER = '.prl-package.json'


def default_destination(agent):
    if agent == 'codex':
        return Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills'
    if agent == 'claude-code':
        return Path.home() / '.claude' / 'skills'
    return Path(os.environ.get('XDG_CONFIG_HOME', str(Path.home() / '.config'))) / 'opencode' / 'skills'


def entries(source):
    return [('prl-style', source)] + [(p.name, p) for p in sorted((source / 'subskills').iterdir())
                                    if (p / 'SKILL.md').is_file()]


def managed(target, name):
    if target.is_symlink() or not target.is_dir():
        return False
    try:
        marker = json.loads((target / MARKER).read_text(encoding='utf-8'))
        return marker.get('package') == 'prl-style' and marker.get('skill') == name
    except (OSError, ValueError):
        return False


def install(source, destination):
    source, destination = Path(source).resolve(), Path(destination).expanduser().absolute()
    check = verify(source)
    if not check['passed']:
        raise ValueError('source integrity failed: ' + '; '.join(check['errors']))
    if destination.resolve() == source or source in destination.resolve().parents:
        raise ValueError('installation must be outside the source directory')
    selected = entries(source)
    for name, _ in selected:
        target = destination / name
        if (target.exists() or target.is_symlink()) and not managed(target, name):
            raise ValueError('existing unmanaged skill; choose another --destination: ' + str(target))
    destination.mkdir(parents=True, exist_ok=True)
    version = (source / 'VERSION').read_text().strip()
    backups, published = [], []
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
    with tempfile.TemporaryDirectory(prefix='.prl-stage-', dir=destination) as temporary:
        stage = Path(temporary)
        for name, entry in selected:
            view = stage / name
            view.mkdir()
            for folder in SHARED:
                if (source / folder).is_dir():
                    shutil.copytree(source / folder, view / folder,
                                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            for filename in PUBLIC_FILES:
                if (source / filename).is_file():
                    shutil.copy2(source / filename, view / filename)
            shutil.copy2(entry / 'SKILL.md', view / 'SKILL.md')
            if (entry / 'agents').is_dir():
                shutil.copytree(entry / 'agents', view / 'agents')
            (view / MARKER).write_text(json.dumps({'package': 'prl-style', 'skill': name,
                'version': version, 'installation': 'independent-copy'}, indent=2) + '\n')
            write_manifest(view)
        try:
            for name, _ in selected:
                target = destination / name
                if target.exists():
                    backup = destination / '.prl-backups' / stamp / name
                    backup.parent.mkdir(parents=True, exist_ok=True)
                    target.rename(backup)
                    backups.append((target, backup))
                (stage / name).rename(target)
                published.append(target)
        except OSError:
            for target in reversed(published):
                shutil.rmtree(target)
            for target, backup in reversed(backups):
                backup.rename(target)
            raise
    return {'passed': True, 'version': version, 'destination': str(destination),
            'skills': [name for name, _ in selected], 'backups': [str(b) for _, b in backups]}


def check_installation(source, destination):
    results = {}
    for name, _ in entries(source):
        target = destination / name
        result = verify(target)
        if not managed(target, name):
            result['passed'] = False
            result['errors'].append('missing or invalid installation marker')
        points = [p.relative_to(target).as_posix() for p in target.rglob('SKILL.md')]
        if points != ['SKILL.md']:
            result['passed'] = False
            result['errors'].append('expected exactly one skill entrypoint')
        results[name] = result
    return {'passed': all(r['passed'] for r in results.values()), 'skills': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agent', choices=['codex', 'claude-code', 'opencode'], default='codex')
    parser.add_argument('--destination', type=Path, help='override the parent skills directory')
    parser.add_argument('--check', action='store_true', help='verify an existing installation')
    args = parser.parse_args()
    destination = (args.destination or default_destination(args.agent)).expanduser()
    try:
        result = check_installation(ROOT, destination) if args.check else install(ROOT, destination)
    except (OSError, ValueError) as exc:
        result = {'passed': False, 'errors': [str(exc)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
