"""Layout and shared catalogue of failure messages. Managed by the plugin manager, identical in every plugin.

This module is the only place that builds the layout of a failure message (standards/messages.md). A plugin extends
BASE_CATALOGUE with the entries of its own failures and calls render_failure; it never builds the layout itself."""
import argparse
import json
from pathlib import Path
import sys

LANGUAGES = ('en', 'de')
DEFAULT_LANGUAGE = 'en'


class Failure(Exception):
    """A failure a person can reach: a catalogue code plus the facts of its wording."""

    def __init__(self, code, **facts):
        super().__init__(code)
        self.code = code
        self.facts = facts


def pick_language(tag):
    """The catalogue language of a language tag (de, en-GB, pt-BR); anything else falls back to English."""
    if isinstance(tag, str):
        primary = tag.split('-')[0].lower()
        if primary in LANGUAGES:
            return primary
    return DEFAULT_LANGUAGE


def plugin_name_from(entry_file):
    """The name of the running plugin from its plugin.json, found from the location of an entry file.
    Allowed use of the file location (standards/coding.md): the name is never a constant."""
    for folder in Path(entry_file).resolve().parents:
        for relative in ('plugin.json', '.claude-plugin/plugin.json'):
            path = folder / relative
            if path.is_file():
                try:
                    name = json.loads(path.read_text(encoding='utf-8')).get('name')
                except (OSError, ValueError, AttributeError):
                    name = None
                if isinstance(name, str) and name:
                    return name
    return None


LAYOUT = {
    'en': {
        'failed': 'The {action} action could not be completed, because {cause}. {changed}',
        'stopped': 'The {action} action was stopped, because {cause}. {changed}',
        'then': 'Then call /{plugin}:{skill} again.',
        'nothing': 'Nothing was changed.',
        'unsure': 'Whether anything was changed is not known.',
    },
    'de': {
        'failed': 'Die Aktion {action} konnte nicht abgeschlossen werden, weil {cause}. {changed}',
        'stopped': 'Die Aktion {action} wurde abgebrochen, weil {cause}. {changed}',
        'then': 'Rufe danach /{plugin}:{skill} erneut auf.',
        'nothing': 'Es wurde nichts geändert.',
        'unsure': 'Ob etwas geändert wurde, ist nicht bekannt.',
    },
}

# Failures of the managed helpers (operator_language.py) and the two failures every plugin has.
BASE_CATALOGUE = {
    'LANGUAGE_TAG_INVALID': {
        'cause': {'en': 'the language tag is not valid', 'de': 'das Sprachkürzel nicht gültig ist'},
        'fix': {'en': 'Please use a tag such as de, en or pt-BR', 'de': 'Bitte verwende ein Kürzel wie de, en oder pt-BR'},
    },
    'LANGUAGE_PROJECT_MISSING': {
        'cause': {'en': 'the project folder does not exist', 'de': 'der Projektordner nicht existiert'},
        'fix': {'en': 'Please name an existing project folder', 'de': 'Bitte nenne einen vorhandenen Projektordner'},
    },
    'LANGUAGE_PATH_UNSAFE': {
        'cause': {'en': 'the path {path} contains a link', 'de': 'der Pfad {path} einen Link enthält'},
        'fix': {'en': 'Please use a project folder in which .project is a plain folder, without links',
                'de': 'Bitte verwende einen Projektordner, in dem .project ein normaler Ordner ohne Links ist'},
    },
    'LANGUAGE_PATH_CONFLICT': {
        'cause': {'en': '{path} exists but is not a folder', 'de': '{path} existiert, aber kein Ordner ist'},
        'fix': {'en': 'Please move that entry away yourself', 'de': 'Bitte verschiebe diesen Eintrag selbst'},
    },
    'LANGUAGE_FORMAT_UNSUPPORTED': {
        'cause': {'en': 'the saved language setting {path} has a format this version does not read',
                  'de': 'die gespeicherte Spracheinstellung {path} ein Format hat, das diese Version nicht liest'},
        'fix': {'en': 'Please move or rename that file (it is never converted or deleted)',
                'de': 'Bitte verschiebe oder benenne diese Datei um (sie wird nie umgewandelt oder gelöscht)'},
    },
    'ARGS_INVALID': {
        'cause': {'en': 'the call is incomplete or contains an unknown option',
                  'de': 'der Aufruf unvollständig ist oder eine unbekannte Option enthält'},
        'fix': {'en': 'Please repeat the call as the skill describes it', 'de': 'Bitte wiederhole den Aufruf, wie es im Skill beschrieben ist'},
    },
    'UNKNOWN': {
        'cause': {'en': 'the cause is not known (an unexpected error)', 'de': 'die Ursache nicht bekannt ist (ein unerwarteter Fehler)'},
        'fix': {'en': 'Please repeat the call', 'de': 'Bitte wiederhole den Aufruf'},
    },
}


def render_failure(catalogue, code, language, plugin, skill, changed=None, stopped=False, **facts):
    """The finished two-paragraph message. A code outside the catalogue is reported as not known.
    `changed` is the sentence about what was already changed (default: nothing was changed). An entry whose fix is
    made of shell commands lists them in `commands` (and may add a sentence per language in `after`): the request then
    ends with a colon, the commands stand in one code block and the remaining sentences follow it."""
    if code not in catalogue:
        code, facts = 'UNKNOWN', {}
    language = pick_language(language)
    layout = LAYOUT[language]
    entry = catalogue[code]
    values = dict(facts, plugin=plugin or '', skill=skill or '')
    first = layout['stopped' if stopped else 'failed'].format(
        action=skill or 'language', cause=entry['cause'][language].format_map(_Facts(values)),
        changed=changed or layout['nothing'])
    request = entry['fix'][language].format_map(_Facts(values))
    rest = [entry['after'][language].format_map(_Facts(values))] if entry.get('after') else []
    if plugin and skill:
        rest.append(layout['then'].format(plugin=plugin, skill=skill))
    if entry.get('commands'):
        block = '\n'.join(line.format_map(_Facts(values)) for line in entry['commands'])
        return '\n\n'.join([first, request + ':\n\n```bash\n' + block + '\n```'] + ([' '.join(rest)] if rest else []))
    return first + '\n\n' + ' '.join([request + '.'] + rest)


class _Facts(dict):
    def __missing__(self, key):
        return '{' + key + '}'


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise Failure('ARGS_INVALID')


def language_in(argv):
    """The message language named by --language in an argument list, before the arguments are parsed."""
    for index, item in enumerate(argv[:-1]):
        if item == '--language':
            return pick_language(argv[index + 1])
    return DEFAULT_LANGUAGE


def run(skill, argv, plugin, out, err, configure, body, catalogue=None):
    """The command frame every skill script uses: parse the arguments (a bad call is ARGS_INVALID), run
    body(args, language, out) and print a failure as its finished message on `err`. Returns the exit status (0 or 1).
    Anything that is not a Failure is reported as not known; no raw error text or traceback reaches the person."""
    catalogue = catalogue or BASE_CATALOGUE
    language = language_in(argv)
    try:
        parser = _Parser(prog=skill, add_help=False)
        parser.add_argument('--language')
        configure(parser)
        args = parser.parse_args(argv)
        language = pick_language(args.language)
        body(args, language, out)
        return 0
    except Failure as failure:
        code, facts = failure.code, failure.facts
    except Exception:
        code, facts = 'UNKNOWN', {}
    err.write(render_failure(catalogue, code, language, plugin, skill, **facts) + '\n')
    return 1


def main(argv=None, out=None, err=None):
    """The finished "cause not known" message for a failure no script reported (a command of the host failed):
    python3 -B messages_base.py --skill <skill> [--language <tag>]. The model writes it unchanged."""
    argv = sys.argv[1:] if argv is None else argv
    out = out or sys.stdout
    err = err or sys.stderr
    plugin, language = plugin_name_from(__file__), language_in(argv)
    try:
        parser = _Parser(prog='messages_base', add_help=False)
        parser.add_argument('--skill', required=True)
        parser.add_argument('--language')
        args = parser.parse_args(argv)
    except Failure as failure:
        err.write(render_failure(BASE_CATALOGUE, failure.code, language, plugin, None) + '\n')
        return 1
    language = pick_language(args.language)
    out.write(render_failure(BASE_CATALOGUE, 'UNKNOWN', language, plugin, args.skill, changed=LAYOUT[language]['unsure']) + '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
