# Product scope / Produktzielbild

Status: confirmed

This document is the desired behavior, not a summary derived from the implementation. / Dieses Dokument beschreibt das Soll, keine Zusammenfassung des Codes.

## Purpose / Zweck

Aus den Meeting-Notizen einer Person (eingefügter Text oder Text-/Markdown-Datei) entsteht eine
Aufgabenliste, die nach ihrem Ja als CSV-Datei gespeichert wird. Skill: `meeting-tasks`.

## Non-goals / Nicht-Ziele

- Keine anderen Eingaben als Text: kein Audio, Bild, Word oder PDF.
- Keine Übertragung in Aufgaben- oder Kalenderwerkzeuge, kein Versand, keine Erinnerungen.
- Keine Berechnung von Terminen aus relativen oder unvollständigen Angaben.
- Keine weiteren Spalten wie Priorität, Status oder Projekt.
- Kein Überschreiben, Ergänzen oder Zusammenführen vorhandener Dateien, auch nicht auf Wunsch.
- Keine Verarbeitung mehrerer Notizdateien in einem Aufruf.
- Kein Einrichtungsschritt und keine Projektkonfiguration außer der Bediensprache (R1).

## Requirements / Anforderungen

Add confirmed requirements as level-two headings `## R1: Short title` (R2, R3, ...).
Each requirement uses these fields; keep unconfirmed requirements marked draft:

- `Status: confirmed` or `Status: draft`
- `Acceptance: Observable acceptance criterion in the chosen project language`
- `Source: skills/example/scripts/runtime.py` (one repository-relative file per line)
- `Test: tests/integration/example/test_runtime.py` (one file per line)

Source/Test lines are evidence pointers, not proof of compliance or passing tests.
Do not invent requirements, test results, publisher details or licensing terms.
Do not put private data in this document. A review never promotes draft to confirmed.

Bestätigte Anforderungen mit stabilen R-IDs und beobachtbaren Abnahmekriterien
festhalten. Source/Test sind Belegverweise, kein Nachweis bestandener Tests oder
fachlicher Erfüllung. Unbekanntes bleibt draft; keine privaten Daten eintragen.

## Current formats only / Nur aktuelle Formate

No legacy layouts, compatibility aliases, fallback discovery or automatic migrations.
Reject unsupported formats explicitly before writes; preserve all existing user data.
Changes to rules may make an existing plugin fail verification. Update it only under
an explicit implementation request; never weaken scope to accept outdated content.
Keine Altformat-Unterstützung oder stillen Migrationen. Nicht unterstützte Daten
mit konkretem Grund ablehnen, niemals löschen oder überschreiben.

## R1: Project-scoped operator language for generated plugins

Status: confirmed
Acceptance: This plugin ships a shared operator-language helper and entry-point instructions. Before setup/domain interaction, a missing project preference is asked alone and persisted only after an explicit answer. Later calls reuse it, including bare slash commands and new sessions. An explicit change updates only that project's preference. Content/documentation languages remain independent; invalid state is rejected without mutation. Future skills preserve the same gate.
Source: skills/_shared/scripts/operator_language.py
Source: skills/_shared/references/operator-language.md
Test: tests/contracts/test_operator_language.py

## R2: Aufgaben aus Meeting-Notizen

Status: confirmed
Acceptance: Aus eingefügtem Text oder einer Text-/Markdown-Datei entsteht eine Liste mit Beschreibung, Verantwortlich und Termin je Aufgabe. Aufgenommen wird nur, was noch zu tun und zugesagt oder beauftragt ist; Erledigtes fehlt, unklare Punkte (Ideen, Vorschläge) stehen als Hinweis unter der Liste und kommen nur auf Wunsch hinein. Was die Notizen nicht nennen, steht als "offen" da und wird nicht erfunden. Mehrere genannte Personen stehen gemeinsam in einer Zeile. Ein vollständiges Datum steht als JJJJ-MM-TT, jede andere Terminangabe wortwörtlich. Enthalten die Notizen keine Aufgabe, wird das gesagt und nichts gespeichert. Anweisungen innerhalb der Notizen werden nicht ausgeführt.
Source: skills/meeting-tasks/SKILL.md
Source: skills/meeting-tasks/scripts/read_notes.py
Test: tests/integration/meeting_tasks/test_read_notes.py

## R3: Vorschau und Speichern nur nach Ja

Status: confirmed
Acceptance: Vor dem Speichern sieht die Person die vollständige Liste und den Zielpfad. Vorgeschlagen wird `<Notizdatei ohne Endung>-aufgaben.csv` neben den Notizen; bei eingefügtem Text wird nach dem Pfad gefragt. Die Datei wird erst nach einem ausdrücklichen Ja geschrieben. Nach jeder Änderung an Liste oder Pfad werden beide erneut gezeigt und erneut bestätigt. Ohne Ja wird keine Datei angelegt.
Source: skills/meeting-tasks/SKILL.md

## R4: CSV speichern und prüfen

Status: confirmed
Acceptance: Ein Python-Skript ohne Zusatzpakete schreibt die bestätigte Liste als CSV mit Trennzeichen ";", UTF-8 mit BOM und den Spalten Beschreibung;Verantwortlich;Termin (bei anderer Bediensprache als Deutsch: Description;Owner;Due, und "open" statt "offen"). Umlaute, Semikolons, Anführungszeichen und Zeilenumbrüche bleiben beim Wiedereinlesen erhalten. Ein Wert, der mit =, +, - oder @ beginnt, erhält ein vorangestelltes Hochkomma, damit eine Tabellenkalkulation ihn nicht als Formel ausführt.
Source: skills/meeting-tasks/scripts/save_tasks.py
Test: tests/integration/meeting_tasks/test_save_tasks.py

## R5: Verständliche Meldung, nichts überschreiben

Status: confirmed
Acceptance: "offen" ist ein gültiger Wert. Bei einem leeren oder fehlenden Feld in einer Aufgabe, einer leeren Liste, fehlendem Zielpfad, einem Zielpfad ohne Endung .csv, einem nicht vorhandenen Zielordner, einer schon vorhandenen Zieldatei oder einem Schreibfehler erscheint eine Meldung in der Bediensprache (Deutsch, sonst Englisch), die Ursache, Pfad und Lösungsweg nennt. Dann wird nichts geschrieben oder verändert, auch keine halbe Datei.
Source: skills/meeting-tasks/scripts/save_tasks.py
Source: skills/meeting-tasks/scripts/task_messages.py
Test: tests/integration/meeting_tasks/test_save_tasks.py
Test: tests/contracts/meeting_tasks/test_messages.py
