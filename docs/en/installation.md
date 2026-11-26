# ⚡ Installation

[Deutsch](../de/installation.md) | **English**

[Home](../../README.en.md) · [Installation](installation.md) · [Skills](skills.md) · [Concepts](concepts.md) · [Development](development.md) · [Shared files](files.md)

You add the marketplace once and install Plugin V0 from it. Account access, repository permissions and your organisation's policies apply. Menu labels are those of the app and may differ.

## Claude

### Claude Desktop App

The labels below are those of the German interface of the desktop app.

1. Open **Einstellungen** (settings).
2. Scroll to **Anpassungen** and select **Plugins**.
3. Select **+ Hinzufügen → Marketplace hinzufügen**, then **Aus einem Repository hinzufügen**.
4. Enter `https://github.com/draftm0de/ai.plugin.marketplace.v0` and select **Synchronisieren**.
5. Select Plugin V0 in the marketplace and install it.

The `/plugin` commands only open the plugin settings in the desktop app, so use this path there.

### Claude CLI

In a terminal session started with `claude`:

```text
/plugin marketplace add https://github.com/draftm0de/ai.plugin.marketplace.v0
/plugin install plugin-v0@ai-plugin-marketplace
```

## Codex

### ChatGPT Desktop App

1. Open the **user icon** and select **Settings**.
2. Select **Integration → Plugins**.
3. Select **+ Add → A Marketplace** and enter `https://github.com/draftm0de/ai.plugin.marketplace.v0`.
4. Select Plugin V0 and install it.

### Codex CLI

```sh
codex plugin marketplace add https://github.com/draftm0de/ai.plugin.marketplace.v0
codex plugin add plugin-v0@ai-plugin-marketplace
```

Then open a new chat.

### ChatGPT Workspace

As a workspace administrator:

1. Open **Admin → Plugins**.
2. Select **Add → Import marketplace**.
3. Enter `https://github.com/draftm0de/ai.plugin.marketplace.v0` as the repository URL.
4. Leave **Path** and **Branch/Tag/Commit** empty to use the repository root on the default branch.
5. Start the import and review the result.

This admin path does not imply identical menus in every ChatGPT interface. No plugin ZIP is required.

## Update

Claude (terminal):

```sh
claude plugin marketplace update ai-plugin-marketplace
claude plugin update plugin-v0@ai-plugin-marketplace
```

Codex:

```sh
codex plugin marketplace upgrade ai-plugin-marketplace
```

In the desktop apps update in the plugin settings, then open a new chat.

## Remove

Claude (terminal):

```sh
claude plugin uninstall plugin-v0@ai-plugin-marketplace
```

Codex:

```sh
codex plugin remove plugin-v0@ai-plugin-marketplace
```

In the desktop apps remove the plugin in the plugin settings.

<hr>

This page is created automatically by `/plugin-manager:docs`. Do not edit it by hand.
