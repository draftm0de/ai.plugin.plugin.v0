#!/usr/bin/env python3
"""Build the hash files of sync templates (R16): skills/<skill>/manifests/<kind>.sync.json from templates/<kind>/sync/,
keeping the `removed` entries. A plugin without such templates has nothing to build. Managed by the plugin manager: do not edit."""
import argparse
import os
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent / 'verify'))
from hashes import kinds, read_sync, render, scan  # noqa: E402


def build(root):
    problems = []
    for base, name in kinds(root):
        sync_path = base / 'manifests' / f'{name}.sync.json'
        label = sync_path.relative_to(root).as_posix()
        old, errors = read_sync(sync_path)
        removed = old['removed'] if old else []
        if errors:
            problems += [f'{label}: {e}' for e in errors]
            continue
        files, scan_problems = scan(base / 'templates' / name / 'sync')
        problems += [f'{label}: {p}' for p in scan_problems]
        both = sorted(set(files) & set(removed))
        if both:
            problems.append(f'{label}: listed as file and as removed: {", ".join(both)}')
        if scan_problems or both:
            continue
        text = render(files, removed)
        if not sync_path.exists() or sync_path.read_text(encoding='utf-8') != text:
            sync_path.parent.mkdir(parents=True, exist_ok=True)
            descriptor, temporary = tempfile.mkstemp(prefix='.sync-', dir=sync_path.parent)
            with os.fdopen(descriptor, 'w', encoding='utf-8', newline='') as handle:
                handle.write(text)
            os.replace(temporary, sync_path)
            print(f'wrote {label}')
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[1], help='Plugin root (default: this repository)')
    problems = build(parser.parse_args(argv).source.resolve())
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        print(f'skeleton hashes: {len(problems)} problem(s)', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
