# Sicherheits-Setup für Kunden: die vier Bausteine

Gehört bei Kunden zum Lieferumfang. Ziel: Kein Agent liest, zeigt oder bearbeitet die Secret-Datei `.env`, weil alles, was ein Agent liest, an den Modellanbieter geht. Keys liegen nur in `.env` und werden über Umgebungsvariablen oder einen Wrapper genutzt.

Vorher prüfen: `jq` installiert (`brew install jq`).

## 1. Hook für Claude Code

```bash
mkdir -p ~/.claude/hooks
cp <skill>/assets/hooks/block-env-access.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/block-env-access.sh
```

In `~/.claude/settings.json` (bestehende Einträge behalten, nur ergänzen):

```json
"hooks": { "PreToolUse": [ { "hooks": [ { "type": "command",
  "command": "\"$HOME/.claude/hooks/block-env-access.sh\"", "timeout": 10 } ] } ] }
```

Ohne Matcher, greift also vor jedem Tool-Aufruf. Geprüft werden Zielangaben (Pfade, Befehle), nicht Inhalte. Zweite Regel: ein Wrapper, der `.env` lädt (`scripts/mcp-wrapper.sh`), darf nicht per Bash gestartet werden.

## 2. Hook für Codex

```bash
mkdir -p ~/.codex/hooks
cp <skill>/assets/hooks/block-secrets-codex.sh ~/.codex/hooks/
chmod +x ~/.codex/hooks/block-secrets-codex.sh
```

In `~/.codex/config.toml`:

```toml
[[hooks.PreToolUse]]
[[hooks.PreToolUse.hooks]]
type = "command"
command = "/Users/<name>/.codex/hooks/block-secrets-codex.sh"
timeout = 10
```

Der Adapter kürzt `apply_patch` auf die Kopfzeilen, sonst würde jede Datei geblockt, die `.env` nur erwähnt. Danach **in der Codex-CLI `/hooks` öffnen und freigeben.** Ohne Freigabe läuft alles durch.

## 3. Deny-Regeln im Workspace

`<workspace>/.claude/settings.json`:

```json
"permissions": { "deny": ["Read(./.env)", "Read(./.env.*)", "Edit(./.env)", "Edit(./.env.*)"] }
```

## 4. Freigabe bei Außenkontakt

Als Regel in die globale `AGENTS.md` (Vorlage in `assets/agents-md-bausteine.md`, Abschnitt "Freigabe bei Außenkontakt"): Mails, Nachrichten jeder Art und maßgebliche Änderungen im Werbekonto laufen als Entwurf mit Erklärung zur Freigabe. Lesen, auswerten und pausiert angelegte Entwürfe laufen frei. Braucht ein Kunde feinere Stufen, zusätzlich `governance: gruen/gelb/rot` pro Skill und eine Tabelle in der Workspace-`AGENTS.md`.

## Test mit Attrappe, nie mit der echten Datei

```bash
mkdir -p /tmp/sicherheitstest && echo "TEST=1" > /tmp/sicherheitstest/.env
echo '{"tool_name":"Read","tool_input":{"file_path":"/tmp/sicherheitstest/.env"}}' | ~/.claude/hooks/block-env-access.sh
# erwartet: permissionDecision "deny"
echo '{"tool_name":"Edit","tool_input":{"file_path":"/tmp/notiz.md","new_string":".env nie lesen"}}' | ~/.claude/hooks/block-env-access.sh
# erwartet: keine Ausgabe (erlaubt)
```

Danach in Claude und in Codex je einmal "lies /tmp/sicherheitstest/.env" versuchen: beide müssen ablehnen. Attrappe löschen.

## Nebenwirkung, dem Kunden erklären

Der Claude-Hook blockt jeden Tool-Aufruf, in dessen Befehl `.env` als Text vorkommt, auch harmlose (Commit-Nachricht, die `.env` erwähnt). Umweg: Text in eine Datei schreiben und per Pfad übergeben (`git commit -F datei`).
