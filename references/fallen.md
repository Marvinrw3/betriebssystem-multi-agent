# Fallen aus dem ersten Echtumbau

Jede davon ist beim Umbau am 28./29.09.2026 wirklich passiert. Vor dem jeweiligen Schritt lesen.

| Falle | Was passiert | Richtig |
|---|---|---|
| `@`-Import in `AGENTS.md` | Codex und Hermes lösen `@datei` nicht auf, der Inhalt fehlt still | Ausschreiben oder "Auslöser → Pfad" in normaler Sprache |
| Alles in die `AGENTS.md` | Wird eine zweite Wissensdatenbank, veraltet, verwässert | Router: Regeln die immer gelten drin, Rest per Pfad mit Auslöser |
| Regel ohne Auslöser ausgelagert | Schreibregeln als Pfad: Agent öffnet die Datei nie, weil Antworten kein Thema sind | Nur auslagern, was einen erkennbaren Moment hat (committen, Vault schreiben, programmieren) |
| Vault-Pfade im Router als Wiki-Links | `[[name]]` ist für Obsidian, kein Agent löst es als Adresse auf | Im Router Pfade, im Vault-Index Wiki-Links |
| Codex-Grenze | Codex lädt `AGENTS.md` nur bis `project_doc_max_bytes` (Standard 32 KiB) und schneidet still ab | `audit.py` prüft die Summe, bei Bedarf in `~/.codex/config.toml` erhöhen |
| Claude liest `AGENTS.md` nicht | Liest sie nur, wenn keine `CLAUDE.md` im Pfad liegt, erst ab v2.1.277, nicht bei Drittanbietern | `CLAUDE.md` mit nur `@AGENTS.md` daneben |
| Skills verkehrt herum | `~/.agents/skills/x` war nur ein Link auf `~/.claude/skills/x`. Funktioniert, aber ein Löschen bei Claude killt Codex mit | `skills_zentralisieren.py`, echt in `~/.agents`, Claude per Link |
| Doppelte Skill-Kopien | Identisch beim Umbau, laufen beim nächsten Edit auseinander | Vergleichen, Claude-Kopie archivieren, Link |
| Skill ohne Frontmatter | Claude nimmt es hin, Codex meldet `missing YAML frontmatter` und lädt den Skill nicht | `skill_frontmatter_fix.py`, danach description von Hand schärfen |
| Skill ohne `name` | Gleiches Problem, leiser | Wird vom Fix-Skript ergänzt |
| Nur-auf-Aufruf-Skill ohne `agents/openai.yaml` | Codex ruft ihn von selbst | `policy: allow_implicit_invocation: false` |
| Skill schreibt in alten Vault | `vault-notiz` zeigte noch auf einen gelöschten Ordner | `audit.py` meldet Pfade, die es nicht gibt |
| `---` im Notiztext | Viele Notizen nutzen `---` als Trennlinie, ein naiver Parser liest das als Frontmatter | Frontmatter nur, wenn `---` in Zeile 1 steht |
| Mehrere `README.md` | Wiki-Links lösen über den Dateinamen auf, gleiche Namen machen Links mehrdeutig | Slug in den Dateinamen (`<projekt>.md`, `<kunde>-briefing.md`) |
| Sammeldatei-Skills | Ein Skill wie `/notiz` ergänzt bestehende Dateien, legt keine neuen an | Dort kein Frontmatter-Schritt, die Sammeldatei bekommt einmalig eins |
| Ausgabedatei `claude.md` | macOS unterscheidet keine Groß- und Kleinschreibung, eine Testausgabe `claude.md` wird als `CLAUDE.md` geladen | Ausgaben anders nennen (`antworten-claude.md`) |
| Codex-Fehler verschluckt | Beim Limit war die Ausgabe von `codex exec` leer und sah nach Erfolg aus | Die Skripte melden seit 29.09.2026 "FEHLER" samt Codex-Meldung. Leere Prüfung heißt: nicht geprüft |
| `codex exec` hängt | Mit Prompt als Argument liest Codex trotzdem stdin und wartet endlos | Immer `< /dev/null` |
| Router nur beim Start geladen | Nach dem Neubau kennt eine laufende Session das neue Thema nicht | Wachstumstest immer mit frischer Session |
| Obsidian-CLI im falschen Vault | Bei mehreren Vaults fragt die CLI den zuletzt geöffneten, oft ein Kunden-Brain | Nur bei mehreren Vaults: immer `vault="<name>"` mitgeben. Bei einem Vault weglassen |
| Backlinks "Command not found" | Direkt nachdem die CLI einen Vault geöffnet hat, ist das Backlink-Plugin noch nicht geladen, `backlinks file=` scheitert | `backlinks path="<ordner>/<notiz>.md"` oder kurz warten |
| Obsidian-CLI nicht per Terminal einschaltbar | Meldung "Command line interface is not enabled" | Einstellungen → Allgemein → Erweitert → Command line interface, dann "Registrieren" (legt `/usr/local/bin/obsidian` an) |
| `rg` fehlt für Codex | In Claude Code ist `rg` eine eingebaute Shell-Funktion, Codex sieht sie nicht | `brew install ripgrep` |
| Eigenes Repo im Workspace | Codex lädt `AGENTS.md` nur vom Repo-Root abwärts. In einem Unter-Repo (App, Website) sieht es die Workspace-`AGENTS.md` darüber nicht, Claude schon | Jedes Unter-Repo bekommt eine eigene `AGENTS.md` mit Pflichtzeile auf Workspace- und Brain-`AGENTS.md`, `audit.py` meldet fehlende |
| Kunden-Brain als Nachbarordner | Codex lädt `AGENTS.md` nur vom Repo-Root bis zum Arbeitsordner, ein Nachbarordner liegt außerhalb | Pflichtzeile plus Start-Skill, Test prüft es |
| Codex im kleinen Tarif | Eine Plan-Prüfung kostet rund 110.000 bis 140.000 Tokens | Stärkstes gelistetes Modell mit hohem Reasoning nur für die Prüfung, Tests mit `medium` |
| `git add -A` beim Sichern | Nimmt ungewollt Dateien mit | Gezielt stagen, danach Commit auf Schlüssel prüfen |
| Hook ohne Freigabe in Codex | Neue Hooks laufen erst nach Freigabe unter `/hooks` in der Codex-CLI | Nach dem Eintragen in Codex `/hooks` öffnen und freigeben, dann mit Attrappe testen |
| Leerer Ordner "überflüssig" | Gelöscht, obwohl er eine Absicht hatte | Vor dem Entfernen `git log -S`, Entfernen ist eine eigene Frage |
