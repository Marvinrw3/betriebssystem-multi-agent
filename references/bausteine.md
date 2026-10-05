# Umbau Schritt für Schritt

Reihenfolge einhalten: Jeder Schritt baut auf dem vorigen auf, und nach Schritt 0 gibt es immer einen Stand, auf den man zurück kann. `<skill>` ist der Ordner dieses Skills, `<ws>` der Workspace, `<vault>` das Brain.

## 0. Sicherungspunkt

- Workspace und Vault: offenen Stand gezielt stagen (`git add <pfad>`, nie `-A`), Diff auf Schlüssel prüfen, committen, pushen
- `~/.agents` als Repo, falls noch keins:
  ```bash
  cd ~/.agents && printf '.DS_Store\n.env\n.env.*\n!.env.example\n**/outputs/\n**/__pycache__/\n**/node_modules/\n' > .gitignore
  git init -b main && git add .gitignore AGENTS.md skills && git commit -m "Globale Regeln und Skills versionieren"
  gh repo create <user>/agents-global --private --source=. --remote=origin --push
  ```
- Vor jedem Commit: `git diff --cached | grep -E "sk-ant-|sk-[A-Za-z0-9]{20}|ghp_|AKIA|-----BEGIN"` muss leer sein

## 1. Anweisungsdateien

- Workspace: Inhalt der `CLAUDE.md` nach `AGENTS.md` (`git mv CLAUDE.md AGENTS.md`, dann neue `CLAUDE.md` mit `@AGENTS.md`)
- Jeden `@`-Import auflösen: Inhalt ausschreiben (wenn immer gültig) oder nach `regeln/` mit Auslöser-Zeile (wenn nur in bestimmten Momenten gebraucht)
- Global: `~/.claude/CLAUDE.md` samt `~/.claude/rules/*` nach `~/.agents/AGENTS.md`, Altes nach `~/.claude/archive/<jahr-monat>/`, dann verknüpfen (Befehle in `assets/agents-md-bausteine.md`)
- Commands (`.claude/commands/*.md`, global und lokal) werden Skills in `.agents/skills/<name>/SKILL.md` mit `disable-model-invocation: true` und `agents/openai.yaml`. Codex ruft sie mit `$name` auf
- Codex-Grenze prüfen: `project_doc_max_bytes` in `~/.codex/config.toml` größer als beide `AGENTS.md` zusammen
- Workspace-Skills: `<ws>/.agents/skills/` echt, `<ws>/.claude/skills` als Symlink darauf

## 2. Regeln nach Auslöser

- Globale Teile mit klarem Auslöser nach `~/.agents/regeln/` (git, vault-konventionen, code, context7)
- Workspace-Teile mit klarem Auslöser nach `<ws>/regeln/` (z. B. Kundenarbeit, Behörden und Fristen, Skills bauen, Sub-Agents, Befehlsübersicht)
- Pro Datei ein Kopf: "Ausgelagert aus ... am <Datum>. Wird gelesen, wenn der Auslöser dort greift."
- In beiden `AGENTS.md` die Tabelle "Regeln nach Auslöser". Eine Kurzregel, die immer gelten muss (z. B. "Kundenarbeit nie hier"), bleibt zusätzlich als Satz drin
- Danach alle Verweise nachziehen: `rg -n "Abschnitt <alt>|rules/|<alte-datei>.md" ~/.agents <ws>` und in Skills auf die neuen Pfade umbiegen. Skills, die Start-Kontext lesen, bekommen die neuen Dateien in ihre Leseliste (z. B. Fristen-Datei im Start-Skill)

## 3. Lernprotokoll global

- Fälle unverändert nach `~/.agents/regeln/lernprotokoll-faelle.md`, veraltete Verweise darin auf neue Pfade umstellen
- Pro Eintrag ein Einzeiler in `~/.agents/AGENTS.md`
- Gestrichene Regeln bleiben als Fall mit Nachtrag "am <Datum> gestrichen", ohne Einzeiler

## 4. Skills

```bash
python3 <skill>/scripts/skills_zentralisieren.py            # Probelauf lesen
python3 <skill>/scripts/skills_zentralisieren.py --apply
python3 <skill>/scripts/skill_frontmatter_fix.py ~/.agents/skills <ws>/.agents/skills            # Probelauf
python3 <skill>/scripts/skill_frontmatter_fix.py ~/.agents/skills <ws>/.agents/skills --apply
```

Danach jede neu erzeugte `description` lesen und schärfen. Skills, die laut `audit.py` auf nicht vorhandene Pfade zeigen, einzeln lesen und korrigieren.

## 5. Gedächtnis

- `<ws>/.claude/settings.json`: `"autoMemoryEnabled": false`
- `~/.codex/config.toml`: `[features]` → `memories = false` (prüfen mit `codex features list | grep memories`)
- Vorhandene Claude-Memories sichten (`~/.claude/projects/*/memory/*.md`): Dauerhaftes nach "Gemerkt", Projektstände in den Vault, Rest verwerfen

## 6. Frontmatter im Vault

- Kernnotizen auflisten (ohne Ausschlüsse), **jede anlesen** (Überschrift und erste Zeilen reichen meist) und `thema` plus `beschreibung` setzen
- Zuordnung als Tabelle dem Inhaber zeigen, bevor geschrieben wird, wenn Kunden, Leads und eigene Projekte gemischt sind
- Schreiben per Skript: Frontmatter nur voranstellen, nichts im Inhalt ändern, abbrechen wenn Zeile 1 schon `---` ist
- Prüfen: `git diff --numstat` zeigt pro Datei nur hinzugefügte Zeilen

## 7. vault-index einrichten

```bash
cp -R <skill>/assets/vault-index <ws>/.agents/skills/vault-index
# config.json anpassen: vault, agents_md, ausschluss, hinweise
```

- In der Workspace-`AGENTS.md` den Vault-Abschnitt mit Router-Markierungen und Suchreihenfolge einsetzen (Vorlage in `assets/agents-md-bausteine.md`)
- `python3 check_frontmatter.py && python3 build_index.py`, zweimal laufen lassen: gleiches Ergebnis (idempotent), `git diff AGENTS.md` nur zwischen den Markierungen
- Einbinden: Session-Ende-Skill (vor dem Git-Schritt), Projekt-Skill (nach dem Anlegen), Notiz-Skill (nach dem Schreiben). Der Session-Ende-Skill sichert zusätzlich `~/.agents`
- Vault-Konventionen um die Frontmatter-Regel ergänzen, Notiz-Skills auf das Schema umstellen (`thema`, `beschreibung`, kein `title`/`tags`/`created`)

## 8. Obsidian

Erst `references/suche-und-obsidian.md` lesen, dort stehen die vier Suchschritte, warum die CLI zuerst kommt und die Bedingungen (App läuft, bei mehreren Vaults `vault=` mitgeben).

- kepano-Skills: `git clone --depth 1 https://github.com/kepano/obsidian-skills` in einen Temp-Ordner, **jede `SKILL.md` lesen**, dann `obsidian-markdown`, `obsidian-bases`, `obsidian-cli` nach `~/.agents/skills/` kopieren und für Claude verlinken
- CLI: Inhaber schaltet in Obsidian ein (Einstellungen → Allgemein → Erweitert → Command line interface → Registrieren). Test:
  ```bash
  obsidian vault="<name>-brain" backlinks file="<bekannte-notiz>"
  ```
  Ergebnis mit `rg -l -F "[[<bekannte-notiz>" <vault> | wc -l` vergleichen
- `rg` für Codex: `which rg` außerhalb von Claude prüfen, sonst `brew install ripgrep`

## 9. Kunden (nur wenn beauftragt)

- Kundenmuster aus `assets/agents-md-bausteine.md`: Kunden-Brain mit eigener `AGENTS.md` plus `CLAUDE.md` mit `@AGENTS.md`, Kundenworkspace mit Pflichtzeile, Start-Skill des Kunden liest die Brain-`AGENTS.md`
- Den ganzen Skill im Kunden-Brain wiederholen: Frontmatter, `vault-index` mit eigener `config.json`, Router in der Kunden-`AGENTS.md`
- Sicherheits-Setup: `references/sicherheit-kunden.md`

## 10. Test

- Testfragen aus `assets/testfragen-vorlage.md` auf den Vault zuschneiden: 10 Fragen, jede trifft ein anderes Thema, mindestens eine auf eine ausgelagerte Regel, eine auf eine Info, die nur in einer Sammeldatei steht
- `bash <skill>/scripts/agenten_test.sh <ws> <fragen.md> <ausgabe> [codex-modell]`
- Bewerten: stimmt die Antwort, stehen die richtigen Dateien unter "Gelesen:". Ziel 10/10 für beide
- `codex-skill-fehler.txt` muss leer sein, sonst Schritt 4 wiederholen
- Wachstumstest: Testnotiz mit neuem Thema und einem Geheimwort anlegen, `build_index.py`, **frische** Sessions fragen nach dem Geheimwort und wie sie die Datei gefunden haben. Erwartet: über den Router. Testnotiz löschen, `build_index.py`
- Kunden-Test (Schritt 9): in Codex im Kundenworkspace eine Regel aus der Brain-`AGENTS.md` abfragen

## 11. Abschluss

- `audit.py` erneut, alle FEHLT behoben oder bewusst begründet
- Commits in Workspace, Vault und `~/.agents`, gezielt gestagt, auf Deutsch
- Umbau im Vault dokumentieren (Notiz mit Frontmatter, dann `build_index.py`), Tages-Log
- Dem Inhaber: was sich geändert hat, Testergebnis, was bei ihm liegt (Obsidian-CLI, Codex `/hooks`)
