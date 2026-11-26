#!/usr/bin/env python3
"""Check a confirmed task list and save it as a new CSV file. Never overwrites.
Usage: python3 -B save_tasks.py --target <file.csv> [--language <tag>] with the list on standard input as
{"tasks": [{"description": "...", "owner": "...", "due": "..."}]}."""
import csv
from dataclasses import dataclass
import io
import json
import os
from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parent
sys.path[:0] = [str(SCRIPTS), str(SCRIPTS.parents[1] / '_shared' / 'scripts')]

from messages_base import Failure, plugin_name_from, run  # noqa: E402
from task_messages import CATALOGUE, LEFT_BEHIND  # noqa: E402

SKILL = 'meeting-tasks'
HEADERS = {'de': ('Beschreibung', 'Verantwortlich', 'Termin'), 'en': ('Description', 'Owner', 'Due')}
FIELDS = (('description', 'DESCRIPTION_MISSING'), ('owner', 'OWNER_MISSING'), ('due', 'DUE_MISSING'))
FORMULA_STARTS = ('=', '+', '-', '@')


@dataclass(frozen=True)
class Context:
    plugin: str


def checked_rows(raw):
    """The rows of the handed-over list; every task needs all three fields with text."""
    try:
        data = json.loads(raw.decode('utf-8'))
    except (UnicodeError, ValueError, RecursionError):
        raise Failure('LIST_UNREADABLE') from None
    if not isinstance(data, dict) or set(data) != {'tasks'} or not isinstance(data['tasks'], list):
        raise Failure('LIST_UNREADABLE')
    if not data['tasks']:
        raise Failure('LIST_EMPTY')
    names = {name for name, _ in FIELDS}
    rows = []
    for number, task in enumerate(data['tasks'], 1):
        if not isinstance(task, dict) or set(task) - names:
            raise Failure('LIST_UNREADABLE')
        row = []
        for name, code in FIELDS:
            value = task.get(name)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise Failure(code, number=number)
            if not isinstance(value, str) or '\0' in value:
                raise Failure('LIST_UNREADABLE')
            value = value.strip()
            # a spreadsheet would run such a value as a formula
            row.append("'" + value if value.startswith(FORMULA_STARTS) else value)
        rows.append(row)
    return rows


def parse_csv(content):
    return list(csv.reader(io.StringIO(content.decode('utf-8-sig'), newline=''), delimiter=';', strict=True))


def csv_bytes(rows, language):
    table = [list(HEADERS[language])] + rows
    text = io.StringIO(newline='')
    csv.writer(text, delimiter=';', lineterminator='\r\n').writerows(table)
    try:
        content = text.getvalue().encode('utf-8-sig')
        readable = parse_csv(content) == table
    except (UnicodeError, csv.Error):
        readable = False
    if not readable:
        raise Failure('LIST_UNREADABLE')
    return content


def checked_target(value):
    if not value or not value.strip():
        raise Failure('TARGET_MISSING')
    path = Path(value).expanduser().absolute()
    if path.suffix.lower() != '.csv':
        raise Failure('TARGET_NOT_CSV', path=path)
    if not path.parent.is_dir():
        raise Failure('TARGET_FOLDER_MISSING', path=path.parent)
    if os.path.lexists(path):
        raise Failure('TARGET_EXISTS', path=path)
    return path


def write_new(path, content, language):
    """Create the file exclusively; remove it again when it cannot be written and read back completely."""
    try:
        handle = open(path, 'xb')
    except FileExistsError:
        raise Failure('TARGET_EXISTS', path=path) from None
    except OSError:
        raise Failure('TARGET_NOT_WRITTEN', path=path) from None
    try:
        with handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        if path.read_bytes() != content:
            raise OSError('read back differs')
    except BaseException as error:
        try:
            path.unlink(missing_ok=True)
        except OSError:
            raise Failure('TARGET_LEFT_BEHIND', path=path, changed=LEFT_BEHIND[language]) from None
        if isinstance(error, OSError):
            raise Failure('TARGET_NOT_WRITTEN', path=path) from None
        raise


def main(argv=None, context=None, stdin=None, out=None, err=None):
    argv = sys.argv[1:] if argv is None else argv
    context = context or Context(plugin=plugin_name_from(__file__))
    stdin = stdin or sys.stdin.buffer
    out = out or sys.stdout
    err = err or sys.stderr

    def configure(parser):
        parser.add_argument('--target')

    def body(args, language, stream):
        path = checked_target(args.target)
        rows = checked_rows(stdin.read())
        write_new(path, csv_bytes(rows, language), language)
        stream.write(json.dumps({'saved': str(path), 'tasks': len(rows)}) + '\n')

    return run(SKILL, argv, context.plugin, out, err, configure, body, CATALOGUE)


if __name__ == '__main__':
    sys.exit(main())
