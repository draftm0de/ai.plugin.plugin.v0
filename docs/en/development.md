# Development

[Deutsch](../de/development.md) | **English**

[Home](../../README.en.md) · [Installation](installation.md) · [Skills](skills.md) · [Concepts](concepts.md) · [Development](development.md) · [Shared files](files.md)

For people who work on this plugin. You do not need this page to use it.

## Requirements

- Git and Python 3.10 or newer. Make is optional.
- Claude or Codex with the Plugin Manager installed.
- For a local installation the CLI of the host (`claude` or `codex`).
- One GitHub repository for the marketplace and one per plugin, each cloned locally.

## Set up

If you did not clone the folder of a repository, run `git init` and `git remote add origin <address>` in it; `setup` names the commands for you.

### Marketplace

To develop a plugin, `:setup` asks you to associate it with a marketplace. So you need a repository that has been set up as a marketplace with `/plugin-manager:setup`.

If you do not have one yet, create an empty repository on GitHub, clone it and open the folder. Call `/plugin-manager:setup` there and choose "Marketplace". Among other things it asks for the name and the owner. You set up a marketplace only once; it can hold many plugins.

### Plugin

Every plugin gets its own repository too. Create it on GitHub, clone it, open the folder and call `/plugin-manager:setup`. Choose "Plugin" and name the folder of your marketplace.

The skill asks you step by step for what it needs, for example name, description and licence. After that the shared files are in your repository and the plugin is listed in the marketplace. You commit and push yourself, in both repositories.

### Requirements and skills

First record in `SCOPE.md` what your plugin should and should not do. Then build the skills under `skills/<skill>/`. You need no command of its own for that: you describe to the assistant what you want.

## Test locally

A plugin cannot be installed on its own: Claude and Codex always install from a marketplace. For testing, your marketplace therefore builds a separate development marketplace `<name>-dev` from the folders on your machine and installs from it. It knows where your plugin lies from the local association that `:setup` created. It takes all listed plugins; if the folder of one of them is missing, it stops before it installs anything.

You need just one command for that, in the folder of your plugin:

```bash
make -C ../<marketplace> install-local TARGET=claude
```

For Codex use `TARGET=codex`. Open a new session afterwards. Changes you have not committed yet are included. You do not have to generate or check anything first; you do that before you publish.

## Commands

`plugin.json` is the one file you maintain: name, description, author and address of your plugin. Claude reads a file of its own, the **host manifest** `.claude-plugin/plugin.json`. It is generated from `plugin.json`; you never edit it by hand. When you change `plugin.json`, generate it again, otherwise whoever installs from GitHub gets the old state. Which other files belong to your repository is described under [Shared files](files.md).

All commands run in the root of the repository. `make help` lists them too.

| Command | Purpose | Variables |
| --- | --- | --- |
| `make sync` | Generate the host manifest from `plugin.json` | |
| `make check` | Check that the host manifest matches | |
| `make test` | Deterministic tests | `TEST_GROUP=<name>`: one component only |
| `make verify` | Read-only structure check | `SOURCE=<folder>`; `REVIEW=1`: also compare with `SCOPE.md` |
| `make build-skeleton-hashes` | Rebuild the hash files of sync templates; without such templates nothing happens | |
| `make test-behavior` | Optional model cases, may consume credits | `CLI=claude` or `codex` |
| `make install-hooks` | Activate the check before every commit for this clone | |
| `make help` | Show the commands | |

Your own commands belong into `CUSTOM.mk`.

## CI

`.github/workflows/dm-verify.yml` runs on every push, every pull request and on demand. The run fails when a step fails.

| Step | Fails when |
| --- | --- |
| `python3 -B scripts/run_tests.py` | a test fails |
| `python3 -B scripts/plugin.py check` | the host manifest does not match `plugin.json` |
| `python3 -B scripts/verify/structure.py --source .` | manifests, catalogs, skills or the structure are invalid |
| `python3 -B scripts/verify/standards.py --source .` | the standards or `AGENTS.md` differ or standard text is copied |
| `python3 -B scripts/verify/conventions.py --source .` | command files, messages, failure codes or test folders do not fit |
| `python3 -B scripts/verify/docs.py --source .` | never: missing pages, headings or link targets of the documentation are only warnings |
| `python3 -B scripts/verify/hashes.py --source .` | hash files do not fit the sync templates |

Your own steps belong into another file under `.github/workflows/`. Locally you check the same with `make test check verify`.

## Shared files

Plugin Manager keeps some files up to date (synced) and creates others only once (seed). `.project/plugins/plugin-manager/skeleton.json` lists the synced files. Do not change them: your own rules belong into `CUSTOM.AGENTS.md`, your own commands into `CUSTOM.mk`, your own CI steps into another file under `.github/workflows/`. If you change a synced file anyway, `/plugin-manager:setup` asks whether to keep it or adopt the template. If you keep `AGENTS.md`, the `SCOPE.md` of a marketplace or a standard under `docs/standards/`, `verify` fails.

## Publish

Before the commit, generate the host manifest again if `plugin.json` changed, and check everything:

```bash
make sync
```

```bash
make check test verify
```

Commit and push to the default branch; hosts install what lies there. There are no versions, tags or releases. Push a new plugin first, then the marketplace with its entry.

<hr>

This page is created automatically by `/plugin-manager:docs`. Do not edit it by hand.
