#!/usr/bin/env bash
#
# Blockiert jeden Zugriff auf .env und .env.* in jedem Workspace.
#
# Läuft als PreToolUse-Hook ohne Matcher, greift also vor JEDEM Tool-Aufruf:
# Read, Edit, Write, Bash, Grep, Glob und auch MCP-Tools.
#
# Arbeitsweise: liest das Hook-JSON von stdin, zieht die Zielangaben aus
# tool_input heraus (Dateipfade, Shell-Befehle, Grep-Pfade, Glob-Patterns) und
# prüft sie gegen zwei Muster. Trifft eines zu, wird der Tool-Aufruf mit
# permissionDecision "deny" abgebrochen, bevor er ausgeführt wird.
#
# Eingebunden in ~/.claude/settings.json, gilt damit global für alle Workspaces.

input=$(cat)

tool=$(printf '%s' "$input" | jq -r '.tool_name // ""' 2>/dev/null)

# Zielangaben aus tool_input flach einsammeln, eine pro Zeile.
# Die Inhaltsfelder werden bewusst ausgenommen: Sonst würde jeder Text, in dem
# .env nur erwähnt wird, blockiert, also auch secrets-workflow.md, .gitignore
# oder dieses Skript selbst. Geprüft wird, wohin ein Aufruf zielt, nicht was
# er schreibt.
targets=$(printf '%s' "$input" | jq -r '[.tool_input | del(.content, .new_string, .old_string, .new_source, .description) | .. | strings] | join("\n")' 2>/dev/null)

deny() {
  printf '%s' "$1" | jq -R -s '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: .
    }
  }'
  exit 0
}

# --- Regel 1: .env selbst, für alle Tools ---------------------------------
# Trifft .env, .env.local, /pfad/zu/.env usw.
# Trifft bewusst NICHT: environment, NODE_ENV, config.environment.json
if printf '%s' "$targets" | grep -qE '(^|[^[:alnum:]_])\.env([^[:alnum:]]|$)'; then
  deny "Gesperrt: Zugriff auf .env ist global technisch blockiert (~/.claude/hooks/block-env-access.sh). Secrets nie direkt lesen, sondern über Environment-Variablen oder einen Wrapper nutzen. Ablauf für neue Keys steht in der AGENTS.md des Workspace."
fi

# --- Regel 2: den Wrapper nicht über die Shell starten --------------------
# scripts/mcp-wrapper.sh lädt .env in die Umgebung und führt danach einen
# beliebigen Befehl aus. Über das Bash-Tool aufgerufen wäre er ein Umweg an
# Regel 1 vorbei, weil im Befehl selbst kein .env steht.
# Claude Code startet den Wrapper beim MCP-Verbinden als eigenen Prozess und
# nicht als Tool-Aufruf, dieser Weg bleibt davon unberührt.
# Absichtlich nur für Bash: Die Datei lesen und bearbeiten bleibt erlaubt.
if [ "$tool" = "Bash" ] && printf '%s' "$targets" | grep -qE 'mcp-wrapper\.sh'; then
  deny "Gesperrt: mcp-wrapper.sh darf nicht über die Shell gestartet werden (~/.claude/hooks/block-env-access.sh). Der Wrapper lädt .env in die Umgebung, ein Aufruf hier wäre ein Umweg um die .env-Sperre. Claude Code startet ihn beim MCP-Verbinden selbst, das funktioniert weiterhin. Die Datei lesen oder bearbeiten ist erlaubt."
fi

exit 0
