"""A failure no script reported itself gets a finished message from the real script."""
from pathlib import Path
import subprocess
import sys
import unittest

SCRIPT = Path(__file__).resolve().parents[3] / 'skills/meeting-tasks/scripts/unknown_failure.py'


class UnknownFailureTests(unittest.TestCase):
    def test_it_prints_the_not_known_message_in_the_language(self):
        for language, wording in (('de', 'die Ursache nicht bekannt ist'), ('en', 'the cause is not known')):
            with self.subTest(language=language):
                result = subprocess.run([sys.executable, '-B', str(SCRIPT), '--language', language], capture_output=True)
                message = result.stderr.decode()
                self.assertEqual((1, b''), (result.returncode, result.stdout))
                self.assertIn(wording, message)
                self.assertIn('/plugin-v0:meeting-tasks', message)
                self.assertEqual(2, len(message.strip().split('\n\n')))


if __name__ == '__main__':
    unittest.main()
