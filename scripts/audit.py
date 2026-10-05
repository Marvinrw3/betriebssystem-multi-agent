#!/usr/bin/env python3
"""Bestandsaufnahme eines Claude-Code-Betriebssystems: Was sieht Codex, was nur Claude?
Nur lesend. Aufruf: python3 audit.py --workspace ~/Desktop/<workspace> [--vault ~/Desktop/<name>-brain]
Ausgabe: Markdown-Bericht auf stdout, pro Befund OK / PRÜFEN / FEHLT."""
import argparse, json, os, re, shutil, subprocess
from pathlib import Path

HOME = Path.home()
zeilen = []
def out(status, text): zeilen.append(f"- **{status}** {text}")
def kopf(t): zeilen.append(f"\n## {t}\n")
def kurz(p): return str(p).replace(str(HOME), "~")

def lies(p):
    try: return Path(p).read_text(encoding="utf-8", errors="replace")
    except Exception: return None

def importe(p):
    t = lies(p) or ""
    return re.findall(r"(?m)^\s*@(\S+)", t)

def frontmatter(p):
    t = lies(p) or ""
    if not t.startswith("---\n"): return None
    ende = t.find("\n---", 4)
    return t[4:ende] if ende > 0 else None

def cmd(*a):
    try: return subprocess.run(a, capture_output=True, text=True, timeout=20, stdin=subprocess.DEVNULL).stdout
    except Exception: return ""

ap = argparse.ArgumentParser()
ap.add_argument("--workspace", required=True)
ap.add_argument("--vault")
ap.add_argument("--global-dir", default="~/.agents")
a = ap.parse_args()
WS = Path(a.workspace).expanduser()
G = Path(a.global_dir).expanduser()
V = Path(a.vault).expanduser() if a.vault else None
zeilen.append(f"# Audit: {kurz(WS)}")

kopf("1. Anweisungsdateien")
ws_agents, ws_claude = WS / "AGENTS.md", WS / "CLAUDE.md"
out("OK" if ws_agents.exists() else "FEHLT", f"`{kurz(ws_agents)}` ({ws_agents.stat().st_size if ws_agents.exists() else 0} Byte). Codex liest nur diese Datei")
if ws_claude.exists():
    imp = importe(ws_claude)
    rest = [l for l in (lies(ws_claude) or "").splitlines() if l.strip() and not l.strip().startswith("@AGENTS.md")]
    out("OK" if imp == ["AGENTS.md"] and not rest else "PRÜFEN", f"`CLAUDE.md` Importe: {imp or 'keine'}, weitere Zeilen: {len(rest)}. Ziel: nur `@AGENTS.md`, alles andere sieht Codex nicht")
for datei in [ws_agents, ws_claude, HOME / ".claude/CLAUDE.md", G / "AGENTS.md"]:
    for i in importe(datei):
        if i not in ("AGENTS.md", "~/.agents/AGENTS.md", str(G / "AGENTS.md")):
            out("FEHLT", f"`@{i}` in `{kurz(datei)}`: Inhalt fehlt Codex und Hermes. Ausschreiben oder als Pfad mit Auslöser verweisen")
gl = G / "AGENTS.md"
out("OK" if gl.exists() else "FEHLT", f"globale Datei `{kurz(gl)}`")
for link, soll in [(HOME / ".codex/AGENTS.md", gl), (HOME / ".hermes/SOUL.md", gl)]:
    if link.is_symlink(): out("OK" if link.resolve() == soll.resolve() else "PRÜFEN", f"`{kurz(link)}` → `{kurz(os.readlink(link))}`")
    else: out("FEHLT" if link.parent.exists() else "INFO", f"`{kurz(link)}` ist kein Symlink auf die globale Datei")
cc = lies(HOME / ".claude/CLAUDE.md") or ""
out("OK" if "@~/.agents/AGENTS.md" in cc or f"@{gl}" in cc else "FEHLT", "`~/.claude/CLAUDE.md` lädt die globale `AGENTS.md` per `@`")
cfg = lies(HOME / ".codex/config.toml") or ""
m = re.search(r"project_doc_max_bytes\s*=\s*(\d+)", cfg)
grenze = int(m.group(1)) if m else 32768
summe = sum(p.stat().st_size for p in [gl, ws_agents] if p.exists())
out("OK" if summe < grenze else "FEHLT", f"Codex-Grenze `project_doc_max_bytes` = {grenze}, beide AGENTS.md zusammen {summe} Byte. Darüber schneidet Codex still ab")

kopf("2. Commands, Rules, Gedächtnis")
for d in [HOME / ".claude/commands", WS / ".claude/commands", HOME / ".claude/rules", WS / ".claude/rules"]:
    n = len(list(d.glob("*.md"))) if d.exists() else 0
    out("OK" if n == 0 else "FEHLT", f"`{kurz(d)}`: {n} Dateien. Codex kennt weder Commands noch Rules, beides muss Skill oder AGENTS.md-Text werden")
st = lies(WS / ".claude/settings.json") or "{}"
try: mem = json.loads(st).get("autoMemoryEnabled")
except Exception: mem = None
out("OK" if mem is False else "PRÜFEN", f"Claude Auto-Memory im Workspace: `autoMemoryEnabled` = {mem}. Ziel: false, Dauerhaftes in den Abschnitt Gemerkt")
feat = cmd("codex", "features", "list")
m = re.search(r"(?m)^memories\s+\S+\s+(\w+)", feat)
out("OK" if m and m.group(1) == "false" else "PRÜFEN", f"Codex-Gedächtnis `memories` = {m.group(1) if m else 'unbekannt'}. Ziel: false, es gilt über alle Projekte hinweg")

kopf("3. Skills")
gs, cs = G / "skills", HOME / ".claude/skills"
if cs.is_symlink(): out("INFO", f"`{kurz(cs)}` ist selbst ein Symlink → `{kurz(os.readlink(cs))}`")
elif cs.exists():
    for e in sorted(cs.iterdir()):
        if e.name.startswith(".") or e.is_file(): continue
        if e.is_symlink():
            if not e.exists(): out("FEHLT", f"toter Link `{kurz(e)}`")
        elif (gs / e.name).exists() and not (gs / e.name).is_symlink():
            out("PRÜFEN", f"`{e.name}` liegt doppelt als Kopie (Claude und global). Vergleichen, Claude-Seite durch Symlink ersetzen")
        elif (gs / e.name).is_symlink():
            out("FEHLT", f"`{e.name}` liegt verkehrt herum: echt in `~/.claude/skills`, global nur als Link. Umdrehen mit `skills_zentralisieren.py`")
        else:
            out("FEHLT", f"`{e.name}` gibt es nur für Claude")
if gs.exists():
    for e in sorted(gs.iterdir()):
        if e.name.startswith(".") or not e.is_dir(): continue
        if not (cs / e.name).exists(): out("PRÜFEN", f"`{e.name}` fehlt für Claude (kein Link in `~/.claude/skills`)")
for basis in [gs, WS / ".agents/skills"]:
    if not basis.exists(): continue
    for sk in sorted(basis.glob("*/SKILL.md")):
        fm = frontmatter(sk)
        if fm is None: out("FEHLT", f"`{kurz(sk)}` ohne Frontmatter in Zeile 1. Codex lädt den Skill nicht"); continue
        name = re.search(r"(?m)^name:\s*(.+)$", fm); desc = re.search(r"(?m)^description:", fm)
        if not name or not desc: out("FEHLT", f"`{kurz(sk)}` ohne `name` oder `description`")
        elif name.group(1).strip().strip('"') != sk.parent.name: out("PRÜFEN", f"`{kurz(sk)}`: `name` weicht vom Ordnernamen ab")
        if re.search(r"(?m)^disable-model-invocation:\s*true", fm) and not (sk.parent / "agents/openai.yaml").exists():
            out("PRÜFEN", f"`{sk.parent.name}` nur auf Aufruf, aber ohne `agents/openai.yaml` (`allow_implicit_invocation: false`). Codex ruft ihn sonst von selbst")
        for pfad in set(re.findall(r"~/Desktop/([^/`\s\"')]+)", lies(sk) or "")):
            pfad = pfad.rstrip(".,;:")
            if "<" not in pfad and not (HOME / "Desktop" / pfad).exists():
                out("PRÜFEN", f"`{kurz(sk)}` verweist auf `~/Desktop/{pfad}`, das es nicht gibt (altes Ziel oder nur Beispiel?)")
for git in sorted(WS.glob("**/.git")):
    repo = git.parent
    if repo == WS or "node_modules" in repo.parts: continue
    teile = len(repo.relative_to(WS).parts)
    if teile > 3: continue
    hat = (repo / "AGENTS.md").exists()
    out("OK" if hat else "FEHLT", f"eigenes Repo `{kurz(repo)}`: " + ("hat eine eigene `AGENTS.md`" if hat else "ohne `AGENTS.md`. Codex liest nur innerhalb des Repos und sieht Workspace und Brain dort nicht. Lösung: `AGENTS.md` mit Pflichtzeile auf Workspace- und Brain-`AGENTS.md`, daneben `CLAUDE.md` mit `@AGENTS.md`"))
wl = WS / ".claude/skills"
out("OK" if not wl.exists() or wl.is_symlink() else "PRÜFEN", f"`{kurz(wl)}` sollte ein Symlink auf `.agents/skills` sein")

if V:
    kopf("4. Vault")
    notizen = [p for p in V.rglob("*.md") if "/." not in str(p)]
    mit = [p for p in notizen if (frontmatter(p) or "").find("thema") >= 0]
    out("INFO", f"{len(notizen)} Notizen, {len(mit)} mit `thema` im Frontmatter. Logs, Archiv und Rohdaten brauchen keins")
    t = lies(ws_agents) or ""
    out("OK" if "<!-- router:start" in t else "FEHLT", "Router-Markierungen in der Workspace-`AGENTS.md`")
    out("OK" if (V / "vault-index.md").exists() else "FEHLT", "`vault-index.md` im Vault")
    readmes = [p for p in notizen if p.name.lower() == "readme.md"]
    namen = {}
    for p in notizen: namen.setdefault(p.stem.lower(), []).append(p)
    doppelt = {k: v for k, v in namen.items() if len(v) > 1}
    out("OK" if not doppelt else "PRÜFEN", f"gleiche Dateinamen in mehreren Ordnern: {len(doppelt)} ({', '.join(list(doppelt)[:5])}). Wiki-Links werden dadurch mehrdeutig")
    out("OK" if shutil.which("obsidian") else "PRÜFEN", "Obsidian-CLI `obsidian` im PATH (Einstellungen → Allgemein → Erweitert → Command line interface, dann Registrieren)")

kopf("5. Sicherung und Werkzeuge")
for repo in [WS, V, G]:
    if not repo: continue
    if (repo / ".git").exists():
        offen = len([l for l in cmd("git", "-C", str(repo), "status", "--porcelain").splitlines() if l])
        remote = cmd("git", "-C", str(repo), "remote").strip()
        out("OK" if remote else "PRÜFEN", f"`{kurz(repo)}` ist Git-Repo, {offen} offene Änderungen, Remote: {remote or 'keins'}")
    else: out("FEHLT", f"`{kurz(repo)}` ist kein Git-Repo")
for tool in ["claude", "codex", "jq", "rg", "gh"]:
    out("OK" if shutil.which(tool) else "PRÜFEN", f"`{tool}` installiert")

print("\n".join(zeilen))
