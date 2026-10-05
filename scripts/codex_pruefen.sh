#!/usr/bin/env bash
# Lässt Codex einen Plan neutral gegenprüfen, nur lesend.
# Aufruf: codex_pruefen.sh <plan.md> [modell] [arbeitsordner]
# Ohne Modell wird das stärkste Modell aus ~/.codex/models_cache.json mit "balanced" oder dem
# höchsten Reasoning genommen. Wichtig: stdin kommt aus /dev/null, sonst wartet codex exec endlos.
set -euo pipefail
PLAN="$1"; MODELL="${2:-}"; ORDNER="${3:-$(pwd)}"
if [ -z "$MODELL" ]; then
  MODELL=$(python3 -c "import json,os;d=json.load(open(os.path.expanduser('~/.codex/models_cache.json')));ms=[m for m in d['models'] if m.get('visibility')=='list'];ms.sort(key=lambda m:(-len(m.get('supported_reasoning_levels') or []),m.get('priority',99)));print(ms[0]['slug'])" 2>/dev/null || echo "")
fi
ARG=(); [ -n "$MODELL" ] && ARG=(-m "$MODELL")
cd "$ORDNER"
ROH=$(mktemp)
trap 'rm -f "$ROH"' EXIT
codex exec "${ARG[@]}" -c model_reasoning_effort="high" --sandbox read-only --skip-git-repo-check \
"Du bist neutraler Gegenprüfer. Lies $PLAN. Prüfe den Plan gegen die echten Dateien, auf die er sich bezieht (AGENTS.md, CLAUDE.md, ~/.agents/AGENTS.md, ~/.codex/config.toml, die genannten Skills und den Vault). Ändere nichts. Antworte auf Deutsch, knapp, als nummerierte Liste in drei Blöcken: 1) Fehler oder falsche Annahmen (mit Beleg: Datei und Zeile), 2) Lücken, also was fehlt, damit Claude Code UND Codex zu jedem Thema vollständigen Kontext finden, 3) was konkret in Codex anders funktioniert als geplant. Keine Lobeshymnen, nur Befunde." \
  < /dev/null > "$ROH" 2>&1 || true
ERGEBNIS=$(awk '/^tokens used/{f=1;next} f' "$ROH")
if [ -z "$ERGEBNIS" ]; then
  echo "FEHLER: Codex hat keine Prüfung geliefert. Letzte Meldungen:" >&2
  grep -iE "error|limit|quota|usage|unauthorized|login" "$ROH" | tail -5 >&2
  echo "Plan ist NICHT gegengeprüft. Im Plan unter Gegenprüfung vermerken und nachholen." >&2
  exit 1
fi
echo "$ERGEBNIS"
