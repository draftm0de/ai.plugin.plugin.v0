# :meeting-tasks

**Deutsch** | [English](../../en/skills/meeting-tasks.md)

[Start](../../../README.md) · [Installation](../installation.md) · [Skills](../skills.md) · [Begriffe](../concepts.md) · [Entwicklung](../development.md) · [Gemeinsame Dateien](../files.md)

## Beschreibung

Du gibst dem Skill deine Meeting-Notizen und bekommst eine Aufgabenliste: Beschreibung, verantwortliche Person und Termin. Was in den Notizen nicht steht, wird nicht erfunden, sondern als „offen“ markiert. Er liest Text, den du einfügst, oder eine Datei mit der Endung `.txt`, `.md` oder `.markdown`. Audio, PDF und Word liest er nicht, und er überträgt nichts in andere Aufgabenwerkzeuge.

## Ablauf

1. Du nennst die Notizdatei oder fügst den Text ein.
2. Du siehst die Liste, unklare Punkte als Hinweise und den Zielpfad.
3. Du änderst, was nicht passt. Danach siehst du beides noch einmal.
4. Nach deinem Ja wird die Liste geprüft und als neue CSV-Datei gespeichert. Eine vorhandene Datei wird nie überschrieben.

## Beispiel

```text
/plugin-v0:meeting-tasks sommerfest.md
```

Aus „Mara bestellt die Bierbänke bis 2027-05-14. Die Einladungen müssen noch gedruckt werden.“ wird:

| Beschreibung | Verantwortlich | Termin |
| --- | --- | --- |
| Bierbänke bestellen | Mara | 2027-05-14 |
| Einladungen drucken | offen | offen |

## Liest und schreibt

- Liest die Notizdatei, die du nennst.
- Schreibt nach deinem Ja genau eine neue CSV-Datei, vorgeschlagen als `sommerfest-aufgaben.csv` neben den Notizen. Trennzeichen ist `;`, die Datei lässt sich in Excel öffnen. Werte, die mit `=`, `+`, `-` oder `@` beginnen, bekommen ein Hochkomma, damit sie nicht als Formel laufen.
- Merkt sich deine Bediensprache im Projekt unter `.project/operator.json`.
