"""Wording of the failures of meeting-tasks. The layout lives in the managed messages_base.py."""
from messages_base import BASE_CATALOGUE


def _entry(cause_en, cause_de, fix_en, fix_de):
    return {'cause': {'en': cause_en, 'de': cause_de}, 'fix': {'en': fix_en, 'de': fix_de}}


# what was changed, where it is not "nothing"
LEFT_BEHIND = {'en': 'An incomplete file is left at that path.', 'de': 'Dort liegt jetzt eine unvollständige Datei.'}

CATALOGUE = dict(BASE_CATALOGUE, **{
    'NOTES_MISSING': _entry(
        'there is no notes file at {path}', 'unter {path} keine Notizdatei liegt',
        'Please name an existing notes file', 'Bitte nenne eine vorhandene Notizdatei'),
    'NOTES_TYPE': _entry(
        'the file {path} is not a text or Markdown file', 'die Datei {path} keine Text- oder Markdown-Datei ist',
        'Please either name a file ending in .txt, .md or .markdown or paste the notes as text',
        'Bitte nenne entweder eine Datei mit der Endung .txt, .md oder .markdown oder füge die Notizen als Text ein'),
    'NOTES_UNREADABLE': _entry(
        'the file {path} cannot be read as UTF-8 text', 'die Datei {path} nicht als UTF-8-Text gelesen werden kann',
        'Please either save the file as UTF-8 text and make sure you may read it or paste the notes as text',
        'Bitte speichere die Datei entweder als UTF-8-Text und prüfe, ob du sie lesen darfst, oder füge die Notizen als Text ein'),
    'NOTES_EMPTY': _entry(
        'the file {path} is empty', 'die Datei {path} leer ist',
        'Please name a file that contains your notes', 'Bitte nenne eine Datei, die deine Notizen enthält'),
    'LIST_UNREADABLE': _entry(
        'the task list handed over for saving is not complete or not readable',
        'die zum Speichern übergebene Aufgabenliste nicht vollständig oder nicht lesbar ist',
        'Please have the list shown again and confirm it', 'Bitte lass dir die Liste erneut zeigen und bestätige sie'),
    'LIST_EMPTY': _entry(
        'the list contains no task', 'die Liste keine Aufgabe enthält',
        'Please add at least one task', 'Bitte ergänze mindestens eine Aufgabe'),
    'DESCRIPTION_MISSING': _entry(
        'task {number} has no description', 'bei Aufgabe {number} die Beschreibung fehlt',
        'Please name the description of this task', 'Bitte nenne die Beschreibung dieser Aufgabe'),
    'OWNER_MISSING': _entry(
        'task {number} has no entry for the responsible person', 'bei Aufgabe {number} die Angabe zur verantwortlichen Person fehlt',
        'Please either name the responsible person or mark the entry as open',
        'Bitte nenne entweder die verantwortliche Person oder markiere die Angabe als offen'),
    'DUE_MISSING': _entry(
        'task {number} has no entry for the due date', 'bei Aufgabe {number} die Angabe zum Termin fehlt',
        'Please either name the due date or mark the entry as open',
        'Bitte nenne entweder den Termin oder markiere die Angabe als offen'),
    'TARGET_MISSING': _entry(
        'no target file was named', 'keine Zieldatei genannt wurde',
        'Please name a target file ending in .csv', 'Bitte nenne eine Zieldatei mit der Endung .csv'),
    'TARGET_NOT_CSV': _entry(
        'the target file {path} does not end in .csv', 'die Zieldatei {path} nicht auf .csv endet',
        'Please name a target file ending in .csv', 'Bitte nenne eine Zieldatei mit der Endung .csv'),
    'TARGET_FOLDER_MISSING': _entry(
        'the folder {path} does not exist', 'der Ordner {path} nicht existiert',
        'Please either create that folder yourself or name a target file in an existing folder',
        'Bitte lege diesen Ordner entweder selbst an oder nenne eine Zieldatei in einem vorhandenen Ordner'),
    'TARGET_EXISTS': _entry(
        'the target file {path} already exists', 'die Zieldatei {path} schon existiert',
        'Please either name another target file or move the existing file away yourself',
        'Bitte nenne entweder eine andere Zieldatei oder verschiebe die vorhandene Datei selbst'),
    'TARGET_NOT_WRITTEN': _entry(
        'the file {path} could not be written completely', 'die Datei {path} nicht vollständig geschrieben werden konnte',
        'Please make sure you may write in that folder and that there is free space',
        'Bitte prüfe, ob du in diesem Ordner schreiben darfst und genug Speicherplatz frei ist'),
    'TARGET_LEFT_BEHIND': _entry(
        'the file {path} could neither be written completely nor removed again',
        'die Datei {path} weder vollständig geschrieben noch wieder entfernt werden konnte',
        'Please delete that incomplete file yourself', 'Bitte lösche diese unvollständige Datei selbst'),
})
