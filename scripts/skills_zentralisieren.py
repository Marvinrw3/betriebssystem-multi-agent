#!/usr/bin/env python3
"""Legt alle globalen Skills physisch nach ~/.agents/skills und gibt Claude Symlinks darauf.
Standard ist Probelauf. Erst mit --apply wird geändert. Doppelte Kopien werden verglichen:
gleich → Claude-Kopie ins Archiv, Symlink. Abweichend → nichts tun, melden.
Aufruf: python3 skills_zentralisieren.py [--apply] [--archiv ~/.claude/archive/skills-doppelt]"""
import argparse, filecmp, os, shutil
from pathlib import Path

HOME = Path.home()
G, C = HOME / ".agents/skills", HOME / ".claude/skills"
ap = argparse.ArgumentParser(); ap.add_argument("--apply", action="store_true")
ap.add_argument("--archiv", default=str(HOME / ".claude/archive/skills-doppelt"))
a = ap.parse_args(); ARCHIV = Path(a.archiv).expanduser()

def gleich(x, y):
    d = filecmp.dircmp(x, y)
    return not (d.left_only or d.right_only or d.diff_files or d.funny_files) and all(gleich(Path(x) / s, Path(y) / s) for s in d.common_dirs)

def tun(text, *schritte):
    print(("APPLY  " if a.apply else "PLAN   ") + text)
    if a.apply:
        for s in schritte: s()

G.mkdir(parents=True, exist_ok=True)
if C.is_symlink(): raise SystemExit(f"{C} ist selbst ein Symlink, hier ist nichts zu tun")
C.mkdir(parents=True, exist_ok=True)
abweichend = 0
# 1. Verkehrt herum: global nur Link nach ~/.claude → umdrehen
for g in sorted(G.iterdir()):
    if g.is_symlink() and Path(os.readlink(g)).expanduser().resolve().parent == C.resolve():
        c = C / g.name
        tun(f"umdrehen: {g.name}", lambda g=g: g.unlink(), lambda c=c, g=g: shutil.move(str(c), str(g)), lambda c=c, g=g: c.symlink_to(g))
# 2. Nur bei Claude oder doppelt
for c in sorted(C.iterdir()):
    if c.is_symlink() or not c.is_dir() or c.name.startswith("."): continue
    g = G / c.name
    if not g.exists():
        tun(f"verschieben: {c.name}", lambda c=c, g=g: shutil.move(str(c), str(g)), lambda c=c, g=g: c.symlink_to(g))
    elif g.is_dir() and not g.is_symlink():
        if gleich(c, g):
            tun(f"doppelt und gleich, Claude-Kopie ins Archiv: {c.name}", lambda: ARCHIV.mkdir(parents=True, exist_ok=True),
                lambda c=c: shutil.move(str(c), str(ARCHIV / c.name)), lambda c=c, g=g: c.symlink_to(g))
        else:
            abweichend += 1; print(f"STOPP  doppelt und ABWEICHEND, bitte vergleichen: {c.name}")
# 3. Global vorhanden, Claude fehlt
for g in sorted(G.iterdir()):
    if g.is_dir() and not g.name.startswith(".") and not (C / g.name).exists() and not (C / g.name).is_symlink():
        tun(f"Link für Claude anlegen: {g.name}", lambda g=g: (C / g.name).symlink_to(g))
tote = [c.name for c in C.iterdir() if c.is_symlink() and not c.exists()]
print(f"\nAbweichende Doppelte: {abweichend}. Tote Links bei Claude: {tote or 'keine'}")
if not a.apply: print("Probelauf. Mit --apply ausführen.")
