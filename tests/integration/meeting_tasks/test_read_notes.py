"""The notes are read unchanged and without writing; unusable files are explained. Fictional data only."""
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / 'skills/meeting-tasks/scripts/read_notes.py'
NOTES = ROOT / 'tests/fixtures/meeting_tasks/notes.md'


def call(path, language='de'):
    return subprocess.run([sys.executable, '-B', str(SCRIPT), '--file', str(path), '--language', language],
                          capture_output=True)


class ReadNotesTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.folder = Path(temporary.name).resolve()

    def test_a_markdown_file_is_printed_unchanged(self):
        result = call(NOTES)
        self.assertEqual((0, NOTES.read_bytes(), b''), (result.returncode, result.stdout, result.stderr))

    def test_unusable_files_get_a_finished_message_and_stay_as_they_are(self):
        cases = {'missing.md': (None, 'keine Notizdatei'), 'notes.pdf': (b'x', 'keine Text- oder Markdown-Datei'),
                 'latin.txt': (b'Gr\xfc\xdfe', 'nicht als UTF-8-Text'), 'blank.txt': (b' \n', 'leer ist')}
        for name, (content, wording) in cases.items():
            with self.subTest(name=name):
                path = self.folder / name
                if content is not None:
                    path.write_bytes(content)
                result = call(path)
                message = result.stderr.decode()
                self.assertEqual((1, b''), (result.returncode, result.stdout))
                self.assertIn(wording, message)
                self.assertIn(str(path), message)
                self.assertNotIn('Traceback', message)
                self.assertEqual(content, path.read_bytes() if path.exists() else None)
        self.assertEqual(3, len(list(self.folder.iterdir())))


if __name__ == '__main__':
    unittest.main()
