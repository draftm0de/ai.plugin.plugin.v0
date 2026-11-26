# Shared files

[Deutsch](../de/files.md) | **English**

[Home](../../README.en.md) · [Installation](installation.md) · [Skills](skills.md) · [Concepts](concepts.md) · [Development](development.md) · [Shared files](files.md)

When `setup` sets up your repository, it puts files into it. So that all plugins and marketplaces work the same way, not all of them are yours. There are two kinds.

## Synced files

Synced files are identical in every repository of the same kind: the rules for the assistant, the check scripts, the `Makefile`, the CI. Their content comes from Plugin Manager, and that is where it is changed. You do not edit them.

**How they reach you:** when there is a new version, you first update the installed Plugin Manager and then call `/plugin-manager:setup` in your repository. It names the files it wants to create, change or delete, and writes after your yes. Nothing in your repository changes by itself. You commit and push.

Which files are synced in your repository is listed in `.project/plugins/plugin-manager/skeleton.json`.

## Seed files

Seed files are a starting point, for example the `SCOPE.md` of a plugin or `CUSTOM.mk`. `setup` creates them once, when your repository is newly set up. After that they are yours. You fill them, change them or delete them, and nobody overwrites them. A new template does not reach you.

## Who is responsible for what

| | Synced file | Seed file |
| --- | --- | --- |
| Who decides the content? | Plugin Manager | you |
| Who brings it into your repository? | you, with `setup` | `setup`, once during the setup |
| You changed it | `setup` asks at its next run | nothing happens |
| You deleted it | `setup` wants to create it again | it stays away |

## Changing a synced file

Mostly you do not need to, because there is a file of your own for your own things:

- You want to give the assistant rules of your own: write them into `CUSTOM.AGENTS.md`, not into `AGENTS.md`.
- You want commands of your own: write them into `CUSTOM.mk`, not into the `Makefile`.
- You want steps of your own in CI: add another file under `.github/workflows/`, not into `dm-verify.yml`.

If you change a synced file anyway, nothing happens at first. At the next `setup` it notices that your version differs from the template and asks you about each such file:

1. **Keep local file:** your version stays. It asks again only when you change it again or a new template arrives.
2. **Adopt template:** your version is replaced. Save what you want to keep first, for example with a commit.

`setup` does not show the difference; look at it with Git beforehand.

**Keeping is not always without consequences.** `AGENTS.md`, in plugins the standards under `docs/standards/` and in marketplaces `SCOPE.md` are binding. When one of them differs, `verify` and CI fail, even if you chose to keep it.

## Back into the sync

You kept a file and now want the template after all? `setup` does not ask about it by itself anymore, you have to tell it:

1. Call `setup` and ask for it, for example: "Take the Makefile back into the sync."
2. It names the file and asks whether it should adopt the template.
3. After your yes the template replaces your version. From then on the file is like all other synced files again.

It also works without asking: delete the file and call `setup`, then it wants to create it anew.

## When a template is removed

Sometimes Plugin Manager no longer needs a file. If you never changed it, `setup` removes it after naming it and getting your yes. If you changed it, you decide: keep or delete.

## Files and folders of a plugin

In a plugin the synced files provide shared rules, checks and CI. `skills/_shared/` holds the building blocks every plugin needs for its skills.

### Synced

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

## Files and folders of a marketplace

In a marketplace the synced files provide catalog generation, local installation, checks and CI. What you maintain yourself is mainly `marketplace.json`.

### Synced

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

`<lang>` stands for each selected documentation language. In `.gitignore` only missing rules are added.

<hr>

This page is created automatically by `/plugin-manager:docs`. Do not edit it by hand.
