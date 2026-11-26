# Gemeinsame Dateien

**Deutsch** | [English](../en/files.md)

[Start](../../README.md) · [Installation](installation.md) · [Skills](skills.md) · [Begriffe](concepts.md) · [Entwicklung](development.md) · [Gemeinsame Dateien](files.md)

Wenn `setup` dein Repository einrichtet, legt er Dateien hinein. Damit alle Plugins und Marketplaces gleich funktionieren, gehören nicht alle davon dir. Es gibt zwei Arten.

## Sync-Dateien

Sync-Dateien sind in jedem Repository derselben Art gleich: die Regeln für den Assistenten, die Prüfskripte, das `Makefile`, die CI. Ihr Inhalt kommt vom Plugin Manager, und dort wird er auch geändert. Du bearbeitest sie nicht.

**So kommen sie zu dir:** Wenn es eine neue Fassung gibt, aktualisierst du zuerst den installierten Plugin Manager und rufst dann in deinem Repository `/plugin-manager:setup` auf. Er nennt die Dateien, die er anlegen, ändern oder löschen will, und schreibt nach deinem Ja. Von selbst ändert sich in deinem Repository nichts. Committen und pushen machst du.

Welche Dateien bei dir Sync-Dateien sind, steht in `.project/plugins/plugin-manager/skeleton.json`.

## Seed-Dateien

Seed-Dateien sind ein Startpunkt: zum Beispiel `SCOPE.md` eines Plugins oder `CUSTOM.mk`. `setup` legt sie einmal an, wenn dein Repository neu eingerichtet wird. Danach gehören sie dir. Du füllst sie, änderst sie oder löschst sie, und niemand überschreibt sie. Eine neue Vorlage kommt bei dir nicht an.

## Wer ist wofür zuständig

| | Sync-Datei | Seed-Datei |
| --- | --- | --- |
| Wer bestimmt den Inhalt? | Plugin Manager | du |
| Wer bringt ihn in dein Repository? | du, mit `setup` | `setup`, einmal beim Einrichten |
| Du hast sie geändert | `setup` fragt beim nächsten Lauf | nichts passiert |
| Du hast sie gelöscht | `setup` will sie wieder anlegen | sie bleibt weg |

## Eine Sync-Datei ändern

Meistens musst du das nicht, weil es für Eigenes eine eigene Datei gibt:

- Du willst dem Assistenten eigene Regeln mitgeben: schreib sie in `CUSTOM.AGENTS.md`, nicht in `AGENTS.md`.
- Du willst eigene Befehle: schreib sie in `CUSTOM.mk`, nicht ins `Makefile`.
- Du willst eigene Schritte in der CI: lege eine weitere Datei unter `.github/workflows/` an, nicht in `dm-verify.yml`.

Änderst du eine Sync-Datei trotzdem, passiert zunächst nichts. Beim nächsten `setup` merkt er, dass deine Fassung von der Vorlage abweicht, und fragt dich für jede solche Datei einzeln:

1. **Lokal behalten:** Deine Fassung bleibt. Er fragt erst wieder, wenn du sie erneut änderst oder eine neue Vorlage kommt.
2. **Vorlage übernehmen:** Deine Fassung wird ersetzt. Was du behalten willst, sicherst du vorher, zum Beispiel mit einem Commit.

Den Unterschied zeigt `setup` nicht an; sieh ihn dir vorher mit Git an.

**Behalten geht nicht überall folgenlos.** `AGENTS.md`, bei Plugins die Standards unter `docs/standards/` und bei Marketplaces `SCOPE.md` sind verbindlich. Weicht eine davon ab, schlagen `verify` und die CI fehl, auch wenn du „behalten“ gewählt hast.

## Zurück in den Sync

Du hast eine Datei behalten und willst nun doch wieder die Vorlage? `setup` fragt von sich aus nicht mehr danach, du musst es ihm sagen:

1. Ruf `setup` auf und bitte darum, zum Beispiel: „Nimm das Makefile wieder in den Sync.“
2. Er nennt die Datei und fragt, ob er die Vorlage übernehmen soll.
3. Nach deinem Ja ersetzt die Vorlage deine Fassung. Ab dann ist die Datei wieder wie alle anderen Sync-Dateien.

Es geht auch ohne diese Bitte: Lösche die Datei und rufe `setup` auf, dann will er sie neu anlegen.

## Wenn eine Vorlage entfällt

Manchmal braucht der Plugin Manager eine Datei nicht mehr. Hast du sie nie geändert, entfernt `setup` sie, nachdem er sie genannt hat und du zugestimmt hast. Hast du sie geändert, entscheidest du: behalten oder löschen.

## Dateien und Ordner eines Plugins

In einem Plugin sorgen die Sync-Dateien für gemeinsame Regeln, Prüfungen und CI. `skills/_shared/` enthält Bausteine, die jedes Plugin für seine Skills braucht.

### Sync

```text
.
├── .github/
│   └── workflows/
│       └── dm-verify.yml
├── docs/
│   ├── standards/
│   │   ├── coding.md
│   │   ├── messages.md
│   │   ├── skills.md
│   │   └── testing.md
│   └── prerequisites.md
├── githooks/
│   └── pre-commit
├── scripts/
│   ├── verify/
│   │   ├── common.py
│   │   ├── conventions.py
│   │   ├── docs.py
│   │   ├── hashes.py
│   │   ├── scope.py
│   │   ├── standards.py
│   │   └── structure.py
│   ├── build_hashes.py
│   ├── plugin.py
│   └── run_tests.py
├── skills/
│   └── _shared/
│       ├── references/
│       │   ├── operator-language-helper.md
│       │   └── operator-language.md
│       └── scripts/
│           ├── messages_base.py
│           └── operator_language.py
├── tests/
│   ├── behavior/
│   │   └── run_cases.py
│   ├── contracts/
│   │   └── test_operator_language.py
│   └── README.md
├── AGENTS.md
├── CLAUDE.md
└── Makefile
```

### Seed

```text
.
├── assets/
│   └── icon.png
├── docs/
│   ├── architecture.md
│   └── style.md
├── tests/
│   ├── contracts/
│   │   ├── __init__.py
│   │   └── test_structure.py
│   └── __init__.py
├── .gitignore
├── CUSTOM.AGENTS.md
├── CUSTOM.mk
└── SCOPE.md
```

## Dateien und Ordner eines Marketplace

In einem Marketplace sorgen die Sync-Dateien für die Katalog-Erzeugung, die lokale Installation, die Prüfungen und die CI. Selbst gepflegt wird vor allem `marketplace.json`.

### Sync

```text
.
├── .github/
│   └── workflows/
│       └── dm-verify.yml
├── docs/
│   └── prerequisites.md
├── scripts/
│   ├── verify/
│   │   ├── common.py
│   │   ├── docs.py
│   │   ├── scope.py
│   │   ├── standards.py
│   │   └── structure.py
│   ├── local_plugins.py
│   ├── marketplace.py
│   ├── plugin_payload.py
│   └── run_tests.py
├── tests/
│   ├── contracts/
│   │   ├── test_local_plugins.py
│   │   ├── test_marketplace_catalogs.py
│   │   ├── test_plugin_payload.py
│   │   └── test_run_tests.py
│   └── README.md
├── AGENTS.md
├── CLAUDE.md
├── Makefile
└── SCOPE.md
```

### Seed

```text
.
├── assets/
│   └── icon.png
├── docs/
│   ├── architecture.md
│   └── style.md
├── tests/
│   ├── contracts/
│   │   ├── __init__.py
│   │   └── test_structure.py
│   └── __init__.py
├── CUSTOM.AGENTS.md
├── CUSTOM.mk
└── local-marketplace.example.json
```

`<lang>` steht für jede gewählte Dokumentationssprache. In `.gitignore` werden nur fehlende Regeln ergänzt.

<hr>

Diese Seite wird automatisch über `/plugin-manager:docs` erstellt. Ändere sie nicht von Hand.
