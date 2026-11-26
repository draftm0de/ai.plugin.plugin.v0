# ⚡ Installation

**Deutsch** | [English](../en/installation.md)

[Start](../../README.md) · [Installation](installation.md) · [Skills](skills.md) · [Begriffe](concepts.md) · [Entwicklung](development.md) · [Gemeinsame Dateien](files.md)

Du fügst den Marketplace einmal hinzu und installierst daraus Plugin V0. Zugang, Repository-Berechtigungen und die Richtlinien deiner Organisation gelten. Die Menübezeichnungen entsprechen der jeweiligen App und können abweichen.

## Claude

### Claude Desktop App

1. Öffne **Einstellungen**.
2. Scrolle zu **Anpassungen** und wähle **Plugins**.
3. Wähle **+ Hinzufügen → Marketplace hinzufügen** und dann **Aus einem Repository hinzufügen**.
4. Gib `https://github.com/draftm0de/ai.plugin.marketplace.v0` ein und wähle **Synchronisieren**.
5. Wähle Plugin V0 im Marketplace und installiere es.

Die `/plugin`-Befehle führen in der Desktop-App nur zu den Plugin-Einstellungen. Nutze deshalb diesen Weg.

### Claude CLI

In einer mit `claude` gestarteten Sitzung im Terminal:

```text
/plugin marketplace add https://github.com/draftm0de/ai.plugin.marketplace.v0
/plugin install plugin-v0@ai-plugin-marketplace
```

## Codex

### ChatGPT Desktop App

1. Öffne das **Nutzer-Icon** und wähle **Settings**.
2. Wähle **Integration → Plugins**.
3. Wähle **+ Add → A Marketplace** und gib `https://github.com/draftm0de/ai.plugin.marketplace.v0` ein.
4. Wähle Plugin V0 und installiere es.

### Codex CLI

```sh
codex plugin marketplace add https://github.com/draftm0de/ai.plugin.marketplace.v0
codex plugin add plugin-v0@ai-plugin-marketplace
```

Öffne danach einen neuen Chat.

### ChatGPT Workspace

Als Administrator eines Workspace:

1. Öffne **Admin → Plugins**.
2. Wähle **Add → Import marketplace**.
3. Gib `https://github.com/draftm0de/ai.plugin.marketplace.v0` als Repository-URL ein.
4. Lasse **Path** und **Branch/Tag/Commit** leer, um den Repository-Root auf dem Standardbranch zu verwenden.
5. Starte den Import und prüfe das Ergebnis.

Dieser Admin-Weg ist keine Behauptung identischer Menüs in jeder ChatGPT-Oberfläche. Kein Plugin-ZIP erforderlich.

## Aktualisieren

Claude (Terminal):

```sh
claude plugin marketplace update ai-plugin-marketplace
claude plugin update plugin-v0@ai-plugin-marketplace
```

Codex:

```sh
codex plugin marketplace upgrade ai-plugin-marketplace
```

In den Desktop-Apps aktualisierst du in den Plugin-Einstellungen. Öffne danach einen neuen Chat.

## Entfernen

Claude (Terminal):

```sh
claude plugin uninstall plugin-v0@ai-plugin-marketplace
```

Codex:

```sh
codex plugin remove plugin-v0@ai-plugin-marketplace
```

In den Desktop-Apps entfernst du das Plugin in den Plugin-Einstellungen.

<hr>

Diese Seite wird automatisch über `/plugin-manager:docs` erstellt. Ändere sie nicht von Hand.
