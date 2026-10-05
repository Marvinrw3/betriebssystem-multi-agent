"""Gemeinsame Teile für build_index.py und check_frontmatter.py.
Pfade und Ausschlüsse stehen in ../config.json, damit dieselben Skripte in jedem Workspace laufen."""
import json
from pathlib import Path

_cfg = json.loads((Path(__file__).resolve().parent.parent / "config.json").read_text(encoding="utf-8"))
VAULT = Path(_cfg["vault"]).expanduser()
AGENTS_MD = Path(_cfg["agents_md"]).expanduser()
INDEX = VAULT / _cfg.get("index_name", "vault-index.md")
AUSSCHLUSS = tuple(_cfg.get("ausschluss", []))
HINWEISE = _cfg.get("hinweise", {})


def kernnotizen():
    for p in sorted(VAULT.rglob("*.md")):
        rel = p.relative_to(VAULT).as_posix()
        if rel == INDEX.name or rel.startswith(AUSSCHLUSS) or "/." in "/" + rel:
            continue
        yield rel, p


def frontmatter(path):
    """Liest thema und beschreibung. Frontmatter zählt nur, wenn '---' in Zeile 1 steht,
    weil viele Notizen '---' als Trennlinie im Text nutzen."""
    zeilen = path.read_text(encoding="utf-8").split("\n")
    if not zeilen or zeilen[0].strip() != "---":
        return None
    daten, schluessel = {}, None
    for z in zeilen[1:]:
        if z.strip() == "---":
            return daten
        if z.startswith("  - ") and schluessel:
            daten.setdefault(schluessel, []).append(z[4:].strip().strip('"'))
        elif ":" in z and not z.startswith(" "):
            schluessel, wert = z.split(":", 1)
            schluessel, wert = schluessel.strip(), wert.strip()
            if wert.startswith("[") and wert.endswith("]"):
                daten[schluessel] = [w.strip().strip('"') for w in wert[1:-1].split(",") if w.strip()]
            elif wert:
                daten[schluessel] = wert.strip('"')
    return None
