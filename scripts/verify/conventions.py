#!/usr/bin/env python3
"""Conventions check of a plugin (R32): command files, one message layout, a catalogue entry per failure code and test folders. Read-only.
Usage: python3 -B scripts/verify/conventions.py --source <plugin>. Managed by the plugin manager: do not edit."""
import argparse
import json
from pathlib import Path
import re
import sys
from common import outcome


LAYOUT_PHRASES = ('could not be completed' + ', because', 'was stopped' + ', because',  # written in two pieces: this file builds no message
                  'konnte nicht abgeschlossen werden' + ', weil', 'wurde abgebrochen' + ', weil')


TEST_FOLDERS = {'unit', 'integration', 'contracts', 'behavior', 'native', 'fixtures', 'support'}


CODE_USE = re.compile(r"(?:Failure|failure|OperatorLanguageError)\(\s*'([A-Za-z_]+)'")


def conventions(root):
    """R32: what the standards fix mechanically, read from the files without running anything: a command file for
    every skill, the failure layout in one place, the failure codes in a catalogue and the test folders by type."""
    problems = []
    skills = sorted(path.parent.name for path in (root / 'skills').glob('*/SKILL.md'))
    for name in skills if len(skills) > 1 else ():  # a plugin with exactly one skill is called bare and needs no command file
        if not (root / 'commands' / (name + '.md')).is_file():
            problems.append('skill ' + name + ' has no commands/' + name + '.md')
    sources = [path for path in sorted((root / 'skills').rglob('*.py')) if '__pycache__' not in path.parts and not path.is_symlink()]
    texts = {path: path.read_text(encoding='utf-8', errors='replace') for path in sources}
    for path, text in texts.items():
        if path.name not in ('messages_base.py', 'messages.py') and any(phrase in text for phrase in LAYOUT_PHRASES):
            problems.append(str(path.relative_to(root)) + ' builds a failure message itself (the layout lives in messages_base.py)')
    catalogue = '\n'.join(texts.values())
    codes = sorted({code for text in texts.values() for code in CODE_USE.findall(text)})
    missing = [code for code in codes if not re.search(r"'" + re.escape(code) + r"'\s*:", catalogue)]
    if missing:
        problems.append('failure codes without a catalogue entry: ' + ', '.join(missing))
    tests = root / 'tests'
    if tests.is_dir():
        for entry in sorted(tests.iterdir()):
            if entry.is_dir() and entry.name not in TEST_FOLDERS and entry.name != '__pycache__' and not entry.name.startswith('.'):
                problems.append('tests/' + entry.name + ' is not a test folder of the standard (unit, integration, contracts, behavior, native, fixtures, support)')
        for test in sorted(tests.rglob('test_*.py')):
            if '__pycache__' in test.parts:
                continue
            folder = test.parent
            while folder != root:
                if not (folder / '__init__.py').is_file():
                    problems.append(str(folder.relative_to(root)) + ' has test files but no __init__.py')
                    break
                folder = folder.parent
    if problems:
        raise ValueError('The plugin does not follow the standards: ' + '; '.join(sorted(set(problems))) + '. See docs/standards/.')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path.cwd(), help='Project repository root')
    args = parser.parse_args(argv)
    result = outcome('conventions', args.source, conventions)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['valid'] else 1


if __name__ == '__main__':
    sys.exit(main())
