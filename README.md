# betriebssystem-multi-agent

Ein Skill für Claude Code. Er baut ein bestehendes Claude-Code-Betriebssystem (Workspace plus Obsidian-Vault) so um, dass Claude Code, Codex und Hermes dieselben Regeln, dieselben Skills und denselben Vault nutzen.

## Was der Skill macht

- Prüft zuerst, was Codex vom System sieht und was nur Claude versteht (`scripts/audit.py`)
- Stellt die Entscheidungen vorher als Fragen, jeweils mit Empfehlung (`references/grill-fragen.md`)
- Schreibt einen Umbauplan und lässt ihn von Codex gegenlesen
- Baut erst nach Freigabe um: `AGENTS.md` als Hauptdatei, Skills zentral in `~/.agents/skills`, Themen-Router aus dem Obsidian-Vault, Suche über die Obsidian-CLI
- Testet am Ende Claude und Codex mit denselben 10 Fragen

Die Stolperfallen aus dem ersten echten Umbau stehen in `references/fallen.md`.

## Installation

```bash
git clone https://github.com/Marvinrw3/betriebssystem-multi-agent ~/.claude/skills/betriebssystem-multi-agent
```

Oder oben auf **Code → Download ZIP**, entpacken und den Ordner nach `~/.claude/skills/` legen. Danach in Claude Code mit `/betriebssystem-multi-agent` starten.

## Gut zu wissen

- Auf Deutsch geschrieben, getestet auf dem Mac
- Gelöscht wird nichts, Altes wandert ins Archiv. Skripte, die etwas verschieben, machen erst einen Probelauf und ändern nur mit `--apply`
- Die `.env`-Sperre (Hooks in `assets/hooks/`) wirkt global auf dem ganzen Rechner
- Vorher Workspace und Vault committen
