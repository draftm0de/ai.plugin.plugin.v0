#!/usr/bin/env python3
"""Generate or validate the committed host metadata of this plugin. Never publishes or installs."""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_KEY = 'io.zyris.distribution'


def strict_json(text):
    """Reject ambiguous or non-round-trippable JSON before planning writes."""
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate JSON field: ' + key)
            result[key] = value
        return result
    def invalid_constant(value):
        raise ValueError('Invalid JSON numeric constant: ' + value)
    def finite_number(value):
        import math
        from decimal import Decimal
        number = float(value)
        if not math.isfinite(number):
            raise ValueError('Invalid JSON numeric constant: ' + value)
        if Decimal(value) != Decimal(str(number)):
            raise ValueError('Unsupported JSON numeric precision: ' + value)
        return number
    return json.loads(text, object_pairs_hook=unique, parse_constant=invalid_constant, parse_float=finite_number)


def read_file(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError(f'Expected a regular source file: {path}')
    return path.read_bytes()


def source_path(root, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute() or '..' in Path(relative).parts:
        raise ValueError('Source paths must be repository-relative')
    path = root
    for part in Path(relative).parts:
        path /= part
        if path.is_symlink():
            raise ValueError(f'Symlink in source: {relative}')
    return path


def configuration(root=None):
    root = Path(root) if root is not None else ROOT
    manifest = strict_json(read_file(root / 'plugin.json'))
    if not isinstance(manifest, dict):
        raise ValueError('plugin.json must be an object')
    name = manifest.get('name')
    if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
        raise ValueError('Plugin name must be lowercase kebab-case')
    if 'version' in manifest:
        raise ValueError('Repository distribution follows commits; remove version from plugin.json')
    if not isinstance(manifest.get('description'), str) or not manifest['description'].strip():
        raise ValueError('Plugin description is required')
    if not isinstance(manifest.get('extensions', {}), dict):
        raise ValueError('extensions must be an object')
    config = manifest.get('extensions', {}).get(CONFIG_KEY, {})
    if not isinstance(config, dict) or set(config) - {'skillRoot', 'files', 'catalogs'}:
        raise ValueError('Unsupported distribution configuration')
    if not isinstance(config.get('catalogs', True), bool):
        raise ValueError('catalogs must be a boolean')
    skill_root = config.get('skillRoot', 'skills')
    if skill_root != 'skills':
        raise ValueError('Current plugin layout requires skillRoot=skills')
    if config.get('catalogs', False):
        raise ValueError('Plugin repositories must not own marketplace catalogs')
    for obsolete in ('.claude/skills', '.agents/skills', 'marketplace.json', '.claude-plugin/marketplace.json', '.agents/plugins/marketplace.json', '.codex-plugin/marketplace.json'):
        if (root/obsolete).exists() or (root/obsolete).is_symlink():
            raise ValueError('Unsupported host-local skill layout: ' + obsolete)
    source = source_path(root, skill_root)
    if not source.is_dir() or not list(source.glob('*/SKILL.md')):
        raise ValueError('skillRoot must contain canonical skill folders')
    market = name
    if 'marketplace' in config:
        raise ValueError('Unsupported distribution configuration: marketplace')
    if not isinstance(market, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', market):
        raise ValueError('Invalid marketplace name')
    extra = config.get('files', {})
    if not isinstance(extra, dict):
        raise ValueError('Distribution files must map destination paths to source paths')
    for destination, origin in extra.items():
        if (not isinstance(destination, str) or not destination or Path(destination).is_absolute()
                or any(part in ('.', '..') or part.startswith('.') for part in destination.split('/'))
                or destination == 'plugin.json'):
            raise ValueError('Unsafe or reserved distribution destination')
        if isinstance(origin, str) and (any(part.startswith('.env') for part in Path(origin).parts) or Path(origin).suffix in ('.pem', '.key')):
            raise ValueError('Private distribution source forbidden')
        for mapped in (destination, origin):
            if isinstance(mapped, str) and (set(Path(mapped).parts) & {'.git', '.local', '.tmp', 'dist', '.idea', '.venv', 'node_modules', '__pycache__', '.DS_Store'} or Path(mapped).suffix in ('.pyc', '.pyo', '.pyd')):
                raise ValueError('Generated/local files cannot be distributed: ' + mapped)
        if not source_path(root, origin).is_file():
            raise ValueError('Distribution source file missing: ' + str(origin))
    return manifest, source, market, extra


def repository_files(manifest=None):
    """Derive committed host metadata from the portable identity; no version pins."""
    manifest = manifest or configuration()[0]
    if 'version' in manifest:
        raise ValueError('Repository distribution follows commits; remove version from plugin.json')
    name = manifest['name']
    config = manifest.get('extensions', {}).get(CONFIG_KEY, {})
    market = name
    if 'marketplace' in config:
        raise ValueError('Unsupported distribution configuration: marketplace')
    interface = manifest.get('extensions', {}).get('com.openai', {}).get('interface', {})
    claude = {key: manifest[key] for key in ('name', 'description', 'author', 'homepage', 'repository', 'license', 'keywords') if key in manifest}
    display_name = manifest.get('extensions', {}).get('com.openai', {}).get('interface', {}).get('displayName')
    if display_name:
        claude['displayName'] = display_name
    if config.get('catalogs', False):
        raise ValueError('Plugin repositories must not own marketplace catalogs')
    return {'.claude-plugin/plugin.json': claude}


def repository_metadata(check=False):
    expected = repository_files()
    for relative in ('.claude-plugin/marketplace.json', '.agents/plugins/marketplace.json'):
        if (ROOT / relative).exists():
            raise ValueError('Plugin repository must not own marketplace catalogs: ' + relative)
    targets = {relative: source_path(ROOT, relative) for relative in expected}
    drift = []
    for relative, data in expected.items():
        path = targets[relative]
        if not path.is_file() or strict_json(read_file(path)) != data:
            drift.append(relative)
    if check and drift:
        raise ValueError('Repository metadata missing or stale: ' + ', '.join(drift) + '; run make sync-plugin')
    if not check:
        for relative in drift:
            path = targets[relative]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(expected[relative], ensure_ascii=False, indent=2) + '\n')
    return {'valid': True, 'files': list(expected), 'updated': [] if check else drift}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, epilog='Git + Python 3.10+; Make is optional. Local installation is run in the marketplace of this plugin (make install-local there).')
    parser.add_argument('command', choices=('check', 'sync'))
    args = parser.parse_args(argv)
    try:
        print(json.dumps(repository_metadata(check=args.command == 'check'), indent=2))
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
