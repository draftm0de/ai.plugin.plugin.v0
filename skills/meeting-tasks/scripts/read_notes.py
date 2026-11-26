#!/usr/bin/env python3
"""Print the text of a notes file (.txt, .md, .markdown; UTF-8). Read-only.
Usage: python3 -B read_notes.py --file <notes> [--language <tag>]."""
from dataclasses import dataclass
from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parent
sys.path[:0] = [str(SCRIPTS), str(SCRIPTS.parents[1] / '_shared' / 'scripts')]

from messages_base import Failure, plugin_name_from, run  # noqa: E402
from task_messages import CATALOGUE  # noqa: E402

SKILL = 'meeting-tasks'
SUFFIXES = ('.txt', '.md', '.markdown')


@dataclass(frozen=True)
class Context:
    plugin: str


def read_notes(path):
    if not path.is_file():
        raise Failure('NOTES_MISSING', path=path)
    if path.suffix.lower() not in SUFFIXES:
        raise Failure('NOTES_TYPE', path=path)
    try:
        text = path.read_bytes().decode('utf-8-sig')
    except (OSError, UnicodeError):
        raise Failure('NOTES_UNREADABLE', path=path) from None
    if '\0' in text:
        raise Failure('NOTES_UNREADABLE', path=path)
    if not text.strip():
        raise Failure('NOTES_EMPTY', path=path)
    return text


def main(argv=None, context=None, out=None, err=None):
    argv = sys.argv[1:] if argv is None else argv
    context = context or Context(plugin=plugin_name_from(__file__))
    out = out or sys.stdout.buffer
    err = err or sys.stderr

    def configure(parser):
        parser.add_argument('--file')

    def body(args, language, stream):
        if not args.file:
            raise Failure('ARGS_INVALID')
        # bytes, so that the notes arrive unchanged whatever the console encoding is
        stream.write(read_notes(Path(args.file).expanduser().absolute()).encode('utf-8'))

    return run(SKILL, argv, context.plugin, out, err, configure, body, CATALOGUE)


if __name__ == '__main__':
    sys.exit(main())
