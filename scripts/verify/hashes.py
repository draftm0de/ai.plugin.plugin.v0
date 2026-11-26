#!/usr/bin/env python3
"""Hash check (R47): skills/<skill>/manifests/<kind>.sync.json names exactly the files of templates/<kind>/sync/. Read-only.
A plugin without such templates has nothing to check. Usage: python3 -B scripts/verify/hashes.py --source <plugin>. Managed by the plugin manager: do not edit."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys

SHA256 = re.compile(r'[0-9a-f]{64}')
KEYS = {'schema_version', 'files', 'removed'}


def safe(path):
    return (isinstance(path, str) and path != '' and not path.startswith('/') and '\\' not in path
            and all(part not in ('', '.', '..') for part in path.split('/')))


def kinds(root):
    """[(skill folder, kind)] of every sync structure: a sync/ folder or a hash file."""
    found = []
    for base in sorted(path for path in (Path(root) / 'skills').glob('*') if path.is_dir()):
        names = {path.parent.name for path in base.glob('templates/*/sync')}
        names |= {path.name[:-len('.sync.json')] for path in base.glob('manifests/*.sync.json')}
        found += [(base, name) for name in sorted(names)]
    return found


def scan(sync_dir):
    """Actual files below sync/: {path: {sha256, executable}}; symlinks and special files are errors."""
    found, problems = {}, []
    if not sync_dir.is_dir():
        return found, problems
    for current, directories, names in os.walk(sync_dir):
        for entry in [*directories, *names]:
            full = Path(current) / entry
            relative = str(full.relative_to(sync_dir))
            if full.is_symlink():
                problems.append(f'{relative}: symlink in sync/')
            elif entry in names and '__pycache__' not in full.parts:
                mode = full.stat().st_mode
                found[relative] = {'sha256': hashlib.sha256(full.read_bytes()).hexdigest(), 'executable': bool(mode & 0o111)}
    return found, problems


def render(files, removed):
    return json.dumps({'schema_version': 1, 'files': dict(sorted(files.items())), 'removed': sorted(removed)}, indent=2) + '\n'


def read_sync(path):
    """(data, problems); a missing file returns (None, [])."""
    if not path.is_file():
        return None, []
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except (ValueError, UnicodeDecodeError) as exc:
        return None, [f'{path.name}: invalid JSON ({exc})']
    problems = []
    if not (isinstance(data, dict) and set(data) == KEYS and type(data['schema_version']) is int and data['schema_version'] == 1
            and isinstance(data['files'], dict) and isinstance(data['removed'], list)):
        return None, [f'{path.name}: unsupported format (schema_version 1 with files and removed)']
    for key, value in data['files'].items():
        if not (safe(key) and isinstance(value, dict) and set(value) == {'sha256', 'executable'}
                and isinstance(value['sha256'], str) and SHA256.fullmatch(value['sha256']) and type(value['executable']) is bool):
            problems.append(f'{path.name}: invalid entry {key!r}')
    if not all(safe(v) for v in data['removed']) or len(set(data['removed'])) != len(data['removed']):
        problems.append(f'{path.name}: invalid or duplicate removed entries')
    return (None if problems else data), problems


def check(root):
    problems = []
    for base, name in kinds(root):
        sync_path = base / 'manifests' / f'{name}.sync.json'
        label = sync_path.relative_to(root).as_posix()
        data, errors = read_sync(sync_path)
        if data is None and not errors:
            problems.append(f'{label}: missing (run make build-skeleton-hashes)')
        problems += [f'{label}: {e}' for e in errors]
        if data is None:
            continue
        overlap = sorted(set(data['files']) & set(data['removed']))
        if overlap:
            problems.append(f'{label}: listed as file and as removed: {", ".join(overlap)}')
        actual, scan_problems = scan(base / 'templates' / name / 'sync')
        problems += [f'{label}: {p}' for p in scan_problems]
        for path in sorted(set(data['files']) - set(actual)):
            problems.append(f'{label}: {path}: listed but missing in sync/')
        for path in sorted(set(actual) - set(data['files'])):
            problems.append(f'{label}: {path}: in sync/ but not listed')
        for path in sorted(set(actual) & set(data['files'])):
            if actual[path]['sha256'] != data['files'][path]['sha256']:
                problems.append(f'{label}: {path}: hash differs from sync file')
            elif actual[path]['executable'] != data['files'][path]['executable']:
                problems.append(f'{label}: {path}: executable bit differs from sync file')
        if not overlap and sync_path.read_text(encoding='utf-8') != render(data['files'], data['removed']):
            problems.append(f'{label}: not in canonical form (sorted, 2-space JSON, trailing newline)')
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path.cwd(), help='Plugin repository root')
    root = parser.parse_args(argv).source.resolve()
    problems = check(root)
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        print(f'skeleton hashes: {len(problems)} problem(s); run make build-skeleton-hashes', file=sys.stderr)
        return 1
    print('skeleton hashes: ok' if kinds(root) else 'skeleton hashes: no sync templates')
    return 0


if __name__ == '__main__':
    sys.exit(main())
