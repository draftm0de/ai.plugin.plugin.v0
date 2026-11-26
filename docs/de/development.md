# Entwicklung

**Deutsch** | [English](../en/development.md)

[Start](../../README.md) · [Installation](installation.md) · [Skills](skills.md) · [Begriffe](concepts.md) · [Entwicklung](development.md) · [Gemeinsame Dateien](files.md)

Für alle, die an diesem Plugin arbeiten. Zum Benutzen brauchst du diese Seite nicht.

## Voraussetzungen

- Git und Python 3.10 oder neuer. Make ist optional.
- Claude oder Codex mit installiertem Plugin Manager.
- Für die lokale Installation die jeweilige CLI (`claude` oder `codex`).
- Je ein GitHub-Repository für den Marketplace und für jedes Plugin, jeweils lokal geklont.

## Einrichten

Hast du den Ordner eines Repositorys nicht geklont, führe darin `git init` und `git remote add origin <Adresse>` aus; `setup` nennt dir die Befehle.

### Marketplace

Damit du ein Plugin entwickeln kannst, fordert dich `:setup` auf, es einem Marketplace zuzuordnen. Du brauchst also ein Repository, das über `/plugin-manager:setup` als Marketplace eingerichtet wurde.

Hast du noch keinen, lege auf GitHub ein leeres Repository an, klone es und öffne den Ordner. Rufe dort `/plugin-manager:setup` auf und wähle „Marketplace“. Er fragt dich unter anderem nach Name und Eigentümer. Einen Marketplace richtest du nur einmal ein; er kann viele Plugins aufnehmen.

### Plugin

Auch jedes Plugin bekommt sein eigenes Repository. Lege es auf GitHub an, klone es, öffne den Ordner und rufe `/plugin-manager:setup` auf. Wähle „Plugin“ und nenne den Ordner deines Marketplace.

Der Skill fragt dich Schritt für Schritt nach dem, was er braucht, zum Beispiel Name, Beschreibung und Lizenz. Danach liegen die gemeinsamen Dateien in deinem Repository, und das Plugin ist im Marketplace eingetragen. Committen und pushen machst du selbst, in beiden Repositorys.

### Anforderungen und Skills

Halte zuerst in `SCOPE.md` fest, was dein Plugin können soll und was nicht. Danach baust du die Skills unter `skills/<skill>/`. Dafür brauchst du keinen eigenen Befehl: Du beschreibst dem Assistenten, was du möchtest.

## Lokal testen

Ein Plugin lässt sich nicht für sich allein installieren: Claude und Codex installieren immer aus einem Marketplace. Zum Testen baut dein Marketplace deshalb aus den Ordnern auf deinem Rechner einen eigenen Entwicklungs-Marketplace `<name>-dev` und installiert daraus. Wo dein Plugin liegt, weiß er aus der lokalen Zuordnung, die `:setup` angelegt hat. Er nimmt alle gelisteten Plugins mit; fehlt der Ordner eines davon, bricht er ab, bevor er etwas installiert.

Du brauchst dafür nur einen Befehl, im Ordner deines Plugins:

```bash
make -C ../<marketplace> install-local TARGET=claude
```

Für Codex nimmst du `TARGET=codex`. Öffne danach eine neue Sitzung. Auch Änderungen, die du noch nicht committet hast, sind dabei. Vorher musst du nichts erzeugen oder prüfen; das machst du, bevor du veröffentlichst.

## Befehle

`plugin.json` ist die eine Datei, die du pflegst: Name, Beschreibung, Autor und Adresse deines Plugins. Claude liest aber eine eigene Datei, das **Host-Manifest** `.claude-plugin/plugin.json`. Es wird aus `plugin.json` erzeugt; du bearbeitest es nie von Hand. Änderst du `plugin.json`, erzeugst du es neu, sonst bekommt, wer von GitHub installiert, den alten Stand. Welche Dateien sonst zu deinem Repository gehören, steht unter [Gemeinsame Dateien](files.md).

Alle Befehle laufen im Stamm des Repositorys. `make help` listet sie auch.

| Befehl | Zweck | Variablen |
| --- | --- | --- |
| `make sync` | Host-Manifest aus `plugin.json` erzeugen | |
| `make check` | Prüfen, ob das Host-Manifest dazu passt | |
| `make test` | Deterministische Tests | `TEST_GROUP=<name>`: nur eine Komponente |
| `make verify` | Struktur nur lesend prüfen | `SOURCE=<ordner>`; `REVIEW=1`: zusätzlich Abgleich mit `SCOPE.md` |
| `make build-skeleton-hashes` | Hash-Dateien der Sync-Vorlagen neu erzeugen; ohne solche Vorlagen passiert nichts | |
| `make test-behavior` | Optionale Modellfälle, kann Credits kosten | `CLI=claude` oder `codex` |
| `make install-hooks` | Prüfung vor jedem Commit für diesen Klon aktivieren | |
| `make help` | Befehle anzeigen | |

Eigene Befehle stehen in `CUSTOM.mk`.

## CI

`.github/workflows/dm-verify.yml` läuft bei jedem Push, jedem Pull Request und auf Knopfdruck. Rot wird der Lauf, wenn ein Schritt fehlschlägt.

| Schritt | Rot, wenn |
| --- | --- |
| `python3 -B scripts/run_tests.py` | ein Test fehlschlägt |
| `python3 -B scripts/plugin.py check` | das Host-Manifest nicht zu `plugin.json` passt |
| `python3 -B scripts/verify/structure.py --source .` | Manifeste, Kataloge, Skills oder die Struktur ungültig sind |
| `python3 -B scripts/verify/standards.py --source .` | die Standards oder `AGENTS.md` abweichen oder Standardtext kopiert ist |
| `python3 -B scripts/verify/conventions.py --source .` | Befehlsdateien, Meldungen, Fehlercodes oder Testordner nicht passen |
| `python3 -B scripts/verify/docs.py --source .` | nie: fehlende Seiten, Überschriften oder Linkziele der Doku sind nur Warnungen |
| `python3 -B scripts/verify/hashes.py --source .` | Hash-Dateien nicht zu den Sync-Vorlagen passen |

Eigene Schritte stehen in einer weiteren Datei unter `.github/workflows/`. Lokal prüfst du dasselbe mit `make test check verify`.

## Gemeinsame Dateien

Plugin Manager hält einen Teil der Dateien aktuell (Sync), andere legt er nur einmal an (Seed). `.project/plugins/plugin-manager/skeleton.json` listet die Sync-Dateien. Ändere sie nicht: Eigene Regeln gehören in `CUSTOM.AGENTS.md`, eigene Befehle in `CUSTOM.mk`, eigene CI-Schritte in eine weitere Datei unter `.github/workflows/`. Änderst du eine Sync-Datei doch, fragt `/plugin-manager:setup`, ob du sie behältst oder die Vorlage übernimmst. Behältst du `AGENTS.md`, `SCOPE.md` eines Marketplace oder einen Standard unter `docs/standards/`, schlägt `verify` fehl.

## Veröffentlichen

Vor dem Commit erzeugst du das Host-Manifest neu, falls sich `plugin.json` geändert hat, und prüfst alles:

```bash
make sync
```

```bash
make check test verify
```

Committen und auf den Standard-Branch pushen; installiert wird, was dort liegt. Es gibt keine Versionen, Tags oder Releases. Ein neues Plugin zuerst pushen, danach den Marketplace mit seinem Eintrag.

<hr>

Diese Seite wird automatisch über `/plugin-manager:docs` erstellt. Ändere sie nicht von Hand.
