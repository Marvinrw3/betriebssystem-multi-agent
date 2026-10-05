#!/usr/bin/env bash
# Stellt Claude und Codex dieselben Testfragen in frischen Sessions, nur lesend.
# Aufruf: agenten_test.sh <arbeitsordner> <fragen.md> <ausgabeordner> [codex-modell]
# Ergebnis: <ausgabeordner>/antworten-claude.md und antworten-codex.md. Nie "claude.md" nennen:
# macOS unterscheidet keine Groß- und Kleinschreibung, Claude würde die Datei als CLAUDE.md laden. Pro Frage muss eine Zeile "Gelesen:" stehen.
set -uo pipefail
ORDNER="$1"; FRAGEN="$2"; AUS="$3"; MODELL="${4:-}"
mkdir -p "$AUS"; cd "$ORDNER"
PROMPT="$(cat "$FRAGEN")"
ARG=(); [ -n "$MODELL" ] && ARG=(-m "$MODELL")
claude -p "$PROMPT" --allowedTools "Read,Grep,Glob,Bash(rg:*),Bash(ls:*),Bash(cat:*),Bash(obsidian:*),Skill" < /dev/null > "$AUS/antworten-claude.md" 2>&1 &
codex exec "${ARG[@]}" -c model_reasoning_effort="medium" --sandbox read-only --skip-git-repo-check "$PROMPT" < /dev/null > "$AUS/codex-roh.txt" 2>&1 &
wait
awk '/^tokens used/{f=1;next} f' "$AUS/codex-roh.txt" > "$AUS/antworten-codex.md"
grep "failed to load skill" "$AUS/codex-roh.txt" | sed 's/.*failed to load skill/Skill nicht geladen:/' | sort -u > "$AUS/codex-skill-fehler.txt"
echo "Claude: $(grep -c 'Gelesen:' "$AUS/antworten-claude.md") Antworten mit Quellen, Codex: $(grep -c 'Gelesen:' "$AUS/antworten-codex.md")"
if [ ! -s "$AUS/antworten-codex.md" ]; then echo "FEHLER: Codex hat nicht geantwortet:" >&2; grep -iE "error|limit|quota|usage|unauthorized" "$AUS/codex-roh.txt" | tail -5 >&2; fi
echo "Codex-Skillfehler: $(wc -l < "$AUS/codex-skill-fehler.txt") (Details in codex-skill-fehler.txt)"
