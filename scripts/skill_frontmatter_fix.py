#!/usr/bin/env python3
"""Repariert Skills, die Codex nicht laden kann: fehlendes Frontmatter, fehlendes name.
Ergänzt bei disable-model-invocation: true die Datei agents/openai.yaml für Codex.
Standard ist Probelauf, --apply schreibt. Aufruf: python3 skill_frontmatter_fix.py <skills-ordner>... [--apply]"""
import argparse, re
from pathlib import Path

ap = argparse.ArgumentParser(); ap.add_argument("ordner", nargs="+"); ap.add_argument("--apply", action="store_true")
a = ap.parse_args()
for basis in a.ordner:
    for sk in sorted(Path(basis).expanduser().glob("*/SKILL.md")):
        t = sk.read_text(encoding="utf-8"); name = sk.parent.name; neu = None
        if not t.startswith("---\n"):
            zeilen = [l for l in t.splitlines() if l.strip()]
            titel = zeilen[0].lstrip("# ").strip() if zeilen else name
            satz = zeilen[1].strip() if len(zeilen) > 1 else ""
            desc = (titel.split(" - ", 1)[-1] + (": " + satz if satz else "")).replace('"', "'")
            neu = f'---\nname: {name}\ndescription: "{desc}"\n---\n\n' + t
            print(f"Frontmatter ergänzen: {sk}")
        else:
            ende = t.find("\n---", 4); fm = t[4:ende]
            if not re.search(r"(?m)^name:", fm):
                neu = f"---\nname: {name}\n" + t[4:]; print(f"name ergänzen: {sk}")
            if re.search(r"(?m)^disable-model-invocation:\s*true", fm) and not (sk.parent / "agents/openai.yaml").exists():
                print(f"agents/openai.yaml anlegen: {sk.parent}")
                if a.apply:
                    (sk.parent / "agents").mkdir(exist_ok=True)
                    (sk.parent / "agents/openai.yaml").write_text("policy:\n  allow_implicit_invocation: false\n")
        if neu and a.apply: sk.write_text(neu, encoding="utf-8")
if not a.apply: print("Probelauf. Mit --apply ausführen, danach die neuen description-Zeilen lesen und schärfen.")
