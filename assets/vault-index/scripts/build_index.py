#!/usr/bin/env python3
"""Schreibt vault-index.md im Vault und den Router-Block in der AGENTS.md (Pfade aus config.json)
aus dem Frontmatter aller Kernnotizen. Idempotent, ändert nur zwischen den Markierungen."""
import sys
from collections import defaultdict
from pathlib import Path
from vault_lib import AGENTS_MD, HINWEISE, INDEX, VAULT, kernnotizen, frontmatter

START = "<!-- router:start (automatisch, nicht von Hand ändern) -->"
ENDE = "<!-- router:end -->"

themen, ohne = defaultdict(list), []
for rel, p in kernnotizen():
    fm = frontmatter(p) or {}
    thema = fm.get("thema") or []
    if isinstance(thema, str):
        thema = [thema]
    if not thema:
        ohne.append(rel)
        continue
    for t in thema:
        themen[t].append((rel, Path(rel).stem, fm.get("beschreibung", "")))

# Index im Vault: Wiki-Links, damit er in Obsidian verlinkt ist
teile = ["> Automatisch erzeugt vom Skill `vault-index`. Nicht von Hand ändern, sondern das Frontmatter der Notizen.",
         "", "# Vault-Index", "",
         "Jede Kernnotiz nach Thema, mit einem Satz Inhalt. Ausgenommene Ordner stehen in `config.json` des Skills `vault-index`.", ""]
for t in sorted(themen):
    teile += [f"## {t}", ""]
    teile += [f"- [[{stem}]]: {b}" for _, stem, b in themen[t]]
    teile.append("")
if ohne:
    teile += ["## Ohne Thema", ""] + [f"- `{r}`" for r in ohne] + [""]
INDEX.write_text("\n".join(teile), encoding="utf-8")

# Router-Block in der AGENTS.md: Pfade, damit jeder Agent sie direkt öffnen kann
text = AGENTS_MD.read_text(encoding="utf-8")
if START not in text or ENDE not in text:
    sys.exit(f"Markierungen fehlen in {AGENTS_MD}, nichts geändert")
vault_kurz = str(VAULT).replace(str(Path.home()), "~")
zeilen = [START, f"| Thema | Dateien (ab `{vault_kurz}/`) |", "|---|---|"]
for t in sorted(themen):
    pfade = ", ".join(f"`{r}`" for r, _, _ in themen[t])
    hinweis = f" · {HINWEISE[t]}" if t in HINWEISE else ""
    zeilen.append(f"| **{t}** | {pfade}{hinweis} |")
zeilen.append(ENDE)
vorher, rest = text.split(START, 1)
_, nachher = rest.split(ENDE, 1)
AGENTS_MD.write_text(vorher + "\n".join(zeilen) + nachher, encoding="utf-8")

print(f"{sum(len(v) for v in themen.values())} Einträge in {len(themen)} Themen, {len(ohne)} ohne Thema")
