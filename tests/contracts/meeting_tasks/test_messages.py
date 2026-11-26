"""Every failure of meeting-tasks has a catalogue entry with the two-paragraph layout in both languages."""
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / 'skills/meeting-tasks/scripts'
sys.path[:0] = [str(SCRIPTS), str(ROOT / 'skills/_shared/scripts')]

from messages_base import LANGUAGES, render_failure  # noqa: E402
from task_messages import CATALOGUE  # noqa: E402

TECHNICAL = re.compile(r'\b(json|schema|exit|script|skript|helper|generator|hash|lock|manifest|migration|traceback|'
                       r'heredoc|utf8)\b|save_tasks|read_notes', re.IGNORECASE)


class MessageTests(unittest.TestCase):
    def test_every_entry_has_the_layout_in_every_language_without_technical_words(self):
        for code in CATALOGUE:
            for language in LANGUAGES:
                with self.subTest(code=code, language=language):
                    message = render_failure(CATALOGUE, code, language, 'sample-plugin', 'meeting-tasks',
                                             path='/tmp/sample.csv', number=1)
                    paragraphs = message.split('\n\n')
                    self.assertEqual(2, len(paragraphs))
                    self.assertTrue(all('\n' not in paragraph for paragraph in paragraphs))
                    self.assertNotRegex(message, r'[{}]')
                    self.assertIsNone(TECHNICAL.search(message), message)
                    self.assertIn('/sample-plugin:meeting-tasks', paragraphs[1])

    def test_every_code_the_scripts_name_is_in_the_catalogue(self):
        text = ''.join((SCRIPTS / name).read_text(encoding='utf-8') for name in ('read_notes.py', 'save_tasks.py'))
        codes = set(re.findall(r"'((?:ARGS|NOTES|LIST|TARGET|DESCRIPTION|OWNER|DUE)_[A-Z_]+)'", text))
        self.assertTrue(codes)
        self.assertEqual(set(), codes - set(CATALOGUE))


if __name__ == '__main__':
    unittest.main()
