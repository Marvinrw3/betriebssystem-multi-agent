#!/usr/bin/env bash
#
# Codex-Adapter für ~/.claude/hooks/block-env-access.sh (Secret-Sperre).
#
# Codex liefert bei Dateiänderungen tool_name "apply_patch" und den ganzen Patch
# in tool_input.command, also auch den Dateiinhalt. Damit Dateien, die den
# Namen der Secret-Datei nur erwähnen, nicht fälschlich blockiert werden,
# bleiben hier nur die Kopfzeilen des Patches (welche Datei wird angefasst).
# Alles andere (Bash, MCP-Tools) geht unverändert an das Claude-Skript, das
# Format passt: tool_name, tool_input, Antwort mit permissionDecision "deny".

input=$(cat)
tool=$(printf '%s' "$input" | jq -r '.tool_name // ""' 2>/dev/null)

if [ "$tool" = "apply_patch" ]; then
  input=$(printf '%s' "$input" | jq '.tool_input.command |= ([splits("\n")] | map(select(test("^\\*\\*\\* (Add|Update|Delete) File: |^\\*\\*\\* Move to: "))) | join("\n"))' 2>/dev/null)
fi

printf '%s' "$input" | "$HOME/.claude/hooks/block-env-access.sh"
