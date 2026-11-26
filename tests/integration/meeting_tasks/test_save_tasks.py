"""Acceptance of R4 and R5: the real script writes into temporary folders; all data is fictional."""
import csv
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / 'skills/meeting-tasks/scripts'
sys.path[:0] = [str(SCRIPTS), str(ROOT / 'skills/_shared/scripts')]

import save_tasks  # noqa: E402

TASKS = [{'description': 'Bierbänke bestellen', 'owner': 'Mara Beispiel', 'due': '2027-05-14'},
         {'description': 'Zeitplan prüfen', 'owner': 'Jonas, Mara', 'due': 'bis Freitag'},
         {'description': 'Einladungen drucken', 'owner': 'offen', 'due': 'offen'}]


class Case(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.folder = Path(temporary.name).resolve()
        self.target = self.folder / 'notes-aufgaben.csv'

    def save(self, tasks=TASKS, target=None, language='de', raw=None):
        """(exit status, standard output, standard error) of one call of the real script."""
        raw = json.dumps({'tasks': tasks}).encode() if raw is None else raw
        out, err = io.StringIO(), io.StringIO()
        argv = ['--language', language, '--target', str(self.target if target is None else target)]
        status = save_tasks.main(argv, save_tasks.Context(plugin='sample-plugin'), io.BytesIO(raw), out, err)
        return status, out.getvalue(), err.getvalue()

    def rows(self):
        with open(self.target, encoding='utf-8-sig', newline='') as handle:
            return list(csv.reader(handle, delimiter=';'))

    def files(self):
        return sorted(path.name for path in self.folder.iterdir())


class SaveTests(Case):
    def test_the_confirmed_list_is_saved_with_semicolons_bom_and_german_headers(self):
        status, out, err = self.save()
        self.assertEqual((0, ''), (status, err))
        self.assertEqual({'saved': str(self.target), 'tasks': 3}, json.loads(out))
        expected = ('﻿Beschreibung;Verantwortlich;Termin\r\n'
                    'Bierbänke bestellen;Mara Beispiel;2027-05-14\r\n'
                    'Zeitplan prüfen;Jonas, Mara;bis Freitag\r\n'
                    'Einladungen drucken;offen;offen\r\n').encode('utf-8')
        self.assertEqual(expected, self.target.read_bytes())

    def test_other_languages_get_english_headers(self):
        for number, language in enumerate(('en', 'fr')):
            self.target = self.folder / f'{number}.csv'
            self.assertEqual(0, self.save([{'description': 'Print invitations', 'owner': 'open', 'due': 'open'}],
                                          language=language)[0])
            self.assertEqual([['Description', 'Owner', 'Due'], ['Print invitations', 'open', 'open']], self.rows())

    def test_special_characters_survive_reading_the_file_again(self):
        text = 'Angebot "Zelt"; groß\nzweite Zeile'
        self.assertEqual(0, self.save([{'description': text, 'owner': 'Åse Øst', 'due': 'offen'}])[0])
        self.assertEqual([text, 'Åse Øst', 'offen'], self.rows()[1])

    def test_a_value_that_looks_like_a_formula_gets_an_apostrophe(self):
        self.assertEqual(0, self.save([{'description': '=1+1', 'owner': ' @mara', 'due': '+3 Tage'},
                                       {'description': '- Zelt holen', 'owner': 'A-B', 'due': 'offen'}])[0])
        self.assertEqual([["'=1+1", "'@mara", "'+3 Tage"], ["'- Zelt holen", 'A-B', 'offen']], self.rows()[1:])

    def test_the_command_line_works_as_the_skill_calls_it(self):
        result = subprocess.run(
            [sys.executable, '-B', str(SCRIPTS / 'save_tasks.py'), '--target', str(self.target), '--language', 'de'],
            input=json.dumps({'tasks': TASKS}).encode(), capture_output=True)
        self.assertEqual((0, b''), (result.returncode, result.stderr))
        self.assertEqual(4, len(self.rows()))


class RefusalTests(Case):
    def refused(self, result, *parts):
        status, out, err = result
        self.assertEqual((1, ''), (status, out))
        for part in parts:
            self.assertIn(part, err)
        self.assertNotIn('Traceback', err)
        self.assertEqual(2, len(err.strip().split('\n\n')), err)

    def test_a_missing_or_empty_field_is_named_and_nothing_is_written(self):
        for field, wording in (('description', 'die Beschreibung fehlt'), ('owner', 'zur verantwortlichen Person fehlt'),
                               ('due', 'zum Termin fehlt')):
            for value in ('', '  \n', None, 'absent'):
                with self.subTest(field=field, value=value):
                    task = dict(TASKS[1], **{field: value})
                    if value == 'absent':
                        del task[field]
                    self.refused(self.save([TASKS[0], task]), 'bei Aufgabe 2', wording, 'Es wurde nichts geändert.',
                                 '/sample-plugin:meeting-tasks')
                    self.assertEqual([], self.files())

    def test_an_empty_or_unreadable_list_writes_nothing(self):
        self.refused(self.save([]), 'keine Aufgabe enthält')
        for raw in (b'', b'{broken', b'\xff', b'[]', b'{"tasks": 1}', b'{"tasks": ["x"]}',
                    json.dumps({'tasks': [dict(TASKS[0], priority='hoch')]}).encode(),
                    json.dumps({'tasks': [dict(TASKS[0], owner=7)]}).encode(),
                    json.dumps({'tasks': [dict(TASKS[0], owner='\ud800')]}).encode()):
            with self.subTest(raw=raw):
                self.refused(self.save(raw=raw), 'Aufgabenliste nicht vollständig oder nicht lesbar')
                self.assertEqual([], self.files())

    def test_an_existing_target_is_never_overwritten(self):
        self.target.write_bytes(b'old content')
        self.refused(self.save(), str(self.target), 'schon existiert', 'Es wurde nichts geändert.')
        self.assertEqual(b'old content', self.target.read_bytes())
        self.assertEqual(['notes-aufgaben.csv'], self.files())

    def test_an_existing_folder_or_dangling_link_counts_as_existing(self):
        self.target.mkdir()
        self.refused(self.save(), 'schon existiert')
        self.target.rmdir()
        self.target.symlink_to(self.folder / 'elsewhere.csv')
        self.refused(self.save(), 'schon existiert')
        self.assertEqual(['notes-aufgaben.csv'], self.files())

    def test_a_file_that_appears_after_the_check_is_kept(self):
        self.target.write_bytes(b'someone else')
        with mock.patch.object(save_tasks.os.path, 'lexists', return_value=False):
            self.refused(self.save(), 'schon existiert')
        self.assertEqual(b'someone else', self.target.read_bytes())

    def test_unusable_targets_are_explained(self):
        self.refused(self.save(target=''), 'keine Zieldatei genannt')
        self.refused(self.save(target=self.folder / 'list.txt'), 'list.txt', 'nicht auf .csv endet')
        self.refused(self.save(target=self.folder / 'missing/list.csv'), str(self.folder / 'missing'), 'nicht existiert')
        self.assertEqual([], self.files())

    def test_a_call_without_a_target_option_is_explained(self):
        out, err = io.StringIO(), io.StringIO()
        status = save_tasks.main(['--language', 'en'], save_tasks.Context(plugin='sample-plugin'),
                                 io.BytesIO(b''), out, err)
        self.refused((status, out.getvalue(), err.getvalue()), 'no target file was named')

    def test_a_failing_write_leaves_no_half_file(self):
        with mock.patch.object(save_tasks.os, 'fsync', side_effect=OSError('disk full')):
            self.refused(self.save(language='en'), 'could not be written completely', 'Nothing was changed.')
        self.assertEqual([], self.files())

    def test_a_half_file_that_cannot_be_removed_is_named_truthfully(self):
        for language, wording, changed in (
                ('de', 'noch wieder entfernt', 'Dort liegt jetzt eine unvollständige Datei.'),
                ('en', 'nor removed again', 'An incomplete file is left at that path.')):
            with self.subTest(language=language):
                self.target = self.folder / f'{language}.csv'
                with mock.patch.object(save_tasks.os, 'fsync', side_effect=OSError('gone')), \
                        mock.patch.object(save_tasks.Path, 'unlink', side_effect=OSError('gone')):
                    result = self.save(language=language)
                self.refused(result, str(self.target), wording, changed)
                self.assertNotIn('Nothing was changed', result[2])
                self.assertNotIn('nichts geändert', result[2])
                self.assertTrue(self.target.exists())

    @unittest.skipIf(not hasattr(os, 'geteuid') or os.geteuid() == 0, 'needs file permissions that apply')
    def test_a_folder_without_write_permission_is_explained(self):
        self.folder.chmod(0o500)
        self.addCleanup(self.folder.chmod, 0o700)
        self.refused(self.save(), 'nicht vollständig geschrieben')
        self.assertEqual([], self.files())


if __name__ == '__main__':
    unittest.main()
