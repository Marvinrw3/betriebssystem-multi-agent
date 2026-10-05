#!/usr/bin/env python3
"""Listet Kernnotizen ohne thema oder beschreibung (Exitcode 1) und warnt bei zu knappen Beschreibungen."""
import sys
from vault_lib import kernnotizen, frontmatter

MIN_ZEICHEN = 40  # darunter fehlen fast immer die Stichworte, über die ein Agent die Notiz findet

fehlend, knapp = [], []
for rel, p in kernnotizen():
    fm = frontmatter(p) or {}
    if not fm.get("thema") or not fm.get("beschreibung"):
        fehlend.append(rel)
    elif len(fm["beschreibung"]) < MIN_ZEICHEN:
        knapp.append(rel)

for rel in fehlend:
    print(f"ohne thema/beschreibung: {rel}")
for rel in knapp:
    print(f"Beschreibung zu knapp (unter {MIN_ZEICHEN} Zeichen): {rel}")
print(f"{len(fehlend)} Notizen ohne vollständiges Frontmatter, {len(knapp)} mit zu knapper Beschreibung")
sys.exit(1 if fehlend else 0)
