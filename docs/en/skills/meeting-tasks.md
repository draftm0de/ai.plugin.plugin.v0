# :meeting-tasks

[Deutsch](../../de/skills/meeting-tasks.md) | **English**

[Home](../../../README.en.md) · [Installation](../installation.md) · [Skills](../skills.md) · [Concepts](../concepts.md) · [Development](../development.md) · [Shared files](../files.md)

## Description

You give the skill your meeting notes and get a task list: description, owner and due date. What the notes do not say is not made up but marked as "open". It reads text you paste or a file ending in `.txt`, `.md` or `.markdown`. It does not read audio, PDF or Word, and it sends nothing to other task tools.

## Workflow

1. You name the notes file or paste the text.
2. You see the list, unclear points as hints and the target path.
3. You change what does not fit. Then you see both again.
4. After your yes the list is checked and saved as a new CSV file. An existing file is never overwritten.

## Example

```text
/plugin-v0:meeting-tasks summer-party.md
```

"Mara orders the benches by 2027-05-14. The invitations still need to be printed." becomes:

| Description | Owner | Due |
| --- | --- | --- |
| Order the benches | Mara | 2027-05-14 |
| Print the invitations | open | open |

## Reads and writes

- Reads the notes file you name.
- After your yes it writes exactly one new CSV file, suggested as `summer-party-aufgaben.csv` next to the notes. The separator is `;` and the file opens in Excel. Values starting with `=`, `+`, `-` or `@` get an apostrophe so that they do not run as a formula.
- Remembers your operator language in the project under `.project/operator.json`.
