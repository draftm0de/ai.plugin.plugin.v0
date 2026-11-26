#!/usr/bin/env python3
"""Print the finished message for a failure that no script reported itself. Reads and writes no files.
Usage: python3 -B unknown_failure.py [--language <tag>]."""
from dataclasses import dataclass
from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parent
sys.path[:0] = [str(SCRIPTS), str(SCRIPTS.parents[1] / '_shared' / 'scripts')]

from messages_base import Failure, plugin_name_from, run  # noqa: E402
from task_messages import CATALOGUE  # noqa: E402

SKILL = 'meeting-tasks'


@dataclass(frozen=True)
class Context:
    plugin: str


def main(argv=None, context=None, out=None, err=None):
    argv = sys.argv[1:] if argv is None else argv
    context = context or Context(plugin=plugin_name_from(__file__))

    def body(args, language, stream):
        raise Failure('UNKNOWN')

    return run(SKILL, argv, context.plugin, out or sys.stdout, err or sys.stderr, lambda parser: None, body, CATALOGUE)


if __name__ == '__main__':
    sys.exit(main())
