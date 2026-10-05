# Grill-Fragen: die Entscheidungen vor dem Umbau

Diese Fragen stellt der Skill in Runden (Frontier-Prinzip: nur Fragen, deren Voraussetzungen schon geklärt sind). Jede Frage mit Empfehlung. Die Empfehlungen sind der Stand, der sich im ersten Echtumbau bewährt hat. Weicht der Kunde ab, ist das seine Entscheidung, nur die Folgen benennen.

Format pro Frage:

```
❓ **Q1 - <Titel>**: <Frage, Optionen>

➡️ <Empfehlung mit einem Satz Begründung>
```

## Runde 1: Grundsatz

**Q1 - Wo steht der Themen-Router?** (a) direkt in der Workspace-`AGENTS.md` (b) eigene Datei, `AGENTS.md` zeigt darauf.
➡️ (a). Die `AGENTS.md` wird immer geladen, so weiß jeder Agent sicher, wo was liegt. Details stehen im Index.

**Q2 - Was kommt in den Vault-Index?** (a) alles (b) alles außer Logs, Archiv und Rohdaten großer Wissenssammlungen.
➡️ (b). Logs findet der Agent über das Datumsmuster, Rohdaten über den Skill der Sammlung. Sonst geht das Wichtige unter.

**Q3 - Bekommt jede Kernnotiz Frontmatter?** Zwei Felder oben in der Notiz, `thema` und `beschreibung`.
➡️ Ja. Daraus entsteht der Router automatisch, in Obsidian als Tabelle nutzbar.

**Q4 - Lernprotokoll global oder pro Workspace?**
➡️ Global. Korrekturen gelten in jedem Workspace, auch bei Kunden. Einzeiler in `~/.agents/AGENTS.md`, Fälle in einer eigenen Datei.

**Q5 - Regeln mit klarem Auslöser auslagern?** Git, Vault-Schreiben, Code, Library-Doku.
➡️ Ja, nach `~/.agents/regeln/`. Was in jeder Antwort gilt (Ton, Schreibregeln, Rolle, Security, Freigaben), bleibt in der `AGENTS.md`, sonst wendet es der Agent nicht an, weil er die Datei nie öffnet.

**Q6 - Kunden-Brains in diesem Umbau?**
➡️ Muster jetzt festlegen, Umsetzung pro Kunde danach. Erst ein System sauber, dann kopieren.

**Q7 - Hermes?**
➡️ Mitdenken, nicht testen. Hermes liest `AGENTS.md` ohnehin (`.hermes.md` → `AGENTS.md` → `CLAUDE.md`, die erste gewinnt).

**Q8 - obsidian-skills von kepano installieren?** (`obsidian-markdown`, `obsidian-bases`, `obsidian-cli`)
➡️ Ja, nach `~/.agents/skills/`. Offizielle Skills vom Obsidian-Gründer, laufen in Claude und Codex.

**Q9 - Wann ist der Umbau bestanden?**
➡️ 10 Themenfragen an Claude und Codex in frischen Sessions, beide öffnen die richtigen Dateien, 10 von 10. Dazu der Wachstumstest.

## Runde 2: Aufbau

**Q10 - Welche Start-Themen?** Aus den Ordnern und Inhalten des Vaults ableiten, typisch: `kontext`, `marke`, `angebot`, `akquise`, `content`, `kunden`, `projekte`, `finanzen-behoerden`, `tools-ki`, `kurse`.
➡️ Die Liste ist nur der Start. Neue Themen entstehen von selbst, sobald eine Notiz sie trägt. Kunden und Leads zusätzlich mit Firmennamen als Thema.

**Q11 - Welche Frontmatter-Felder?** (a) nur `thema` und `beschreibung` (b) zusätzlich `status`.
➡️ (a). Status wird in Prioritäten-Dateien gepflegt, doppelt gepflegt veraltet er.

**Q12 - Wie bleibt der Index aktuell?**
➡️ Skript `vault-index` in den Abschluss-Skills (Session-Ende, Projekt anlegen, Notiz anlegen). Nichts von Hand.

**Q13 - Wer setzt Frontmatter bei neuen Notizen?**
➡️ Die Skills, die Notizen anlegen, plus eine Regel in den Vault-Konventionen. `check_frontmatter.py` ist das Netz.

**Q14 - `~/.agents` in Git?**
➡️ Ja, privates Repo. Dort liegen Regeln, Lernprotokoll und alle Skills. Ohne Repo ist bei einem Defekt alles weg.

**Q15 - Wohin kommen ausgelagerte Workspace-Teile?** (a) `<workspace>/regeln/` sichtbar (b) versteckt.
➡️ (a). Der Inhaber soll sehen, was drin ist.

**Q16 - Wie bekommt Codex beim Kunden die Regeln des Kunden-Brains?** (a) erste Zeile der Kunden-`AGENTS.md`: "Pflicht vor allem anderen: `~/Desktop/<kunde>-brain/AGENTS.md` lesen", plus der Start-Skill liest sie (b) Skript kopiert die Regeln in die Workspace-`AGENTS.md`.
➡️ (a), eine Quelle. Risiko: Es ist eine Anweisung, kein automatisches Laden, weil das Brain ein Nachbarordner ist. Der Test prüft es, fällt er durch, auf (b) umstellen.

**Q17 - Obsidian-CLI einschalten?**
➡️ Ja, wenn Obsidian beim Arbeiten läuft (Punkt unter dem Dock-Symbol). Liefert Backlinks aus dem Obsidian-Index. Sonst reicht die Dateisuche.

## Runde 3: Feinheiten

**Q18 - Suchreihenfolge als Regel oder Skill?**
➡️ Regel in der `AGENTS.md`. Ein Skill springt nur an, wenn der Agent ihn für passend hält, eine Regel gilt immer.

**Q19 - Router-Block vom Skript schreiben lassen?**
➡️ Ja, zwischen zwei Markierungen. Vorteil: neue Themen sofort drin. Einzige Regel für den Menschen: diesen Block nicht von Hand ändern, sondern das Frontmatter.

**Q20 - `CLAUDE.md` behalten oder löschen?**
➡️ Behalten, nur mit `@AGENTS.md`. Claude liest `AGENTS.md` allein nur, wenn keine `CLAUDE.md` existiert und die Version passt, der Einzeiler wirkt immer und lädt nichts doppelt.

**Q21 - Gedächtnis der Agenten?**
➡️ Beide aus (Claude `autoMemoryEnabled: false` im Workspace, Codex `[features] memories = false`). Dauerhafte Fakten in einen Abschnitt "Gemerkt" der `AGENTS.md`, Projektstände in den Vault. Sonst wissen die Agenten nach Wochen Unterschiedliches, und Codex trägt Kundenwissen in andere Projekte.

**Q22 - Sicherheits-Setup (nur bei Kunden)?** Die vier Bausteine aus `references/sicherheit-kunden.md`.
➡️ Kommt drauf an, **wessen Rechner**: Läuft das System auf dem Rechner des Kunden, alle vier Bausteine global. Arbeitet der Dienstleister auf seinem eigenen Rechner für den Kunden, nur die Deny-Regeln im Kunden-Workspace (Baustein 3), weil die Hooks global wirken und sonst auch sein eigenes System sperren. Lücke dann: Codex bleibt im Kunden-Workspace ungesperrt, die Regel steht nur als Text.

**Q24 - Unter-Repos im Workspace (Apps, Website)?**
➡️ Nicht im selben Durchgang. Jedes bekommt später eine eigene `AGENTS.md` mit Pflichtzeile, eigener Test. Code-Projekte mit eigenem Framework (z. B. AI Engineering Kit) haben eigene Regeln, die nicht nebenbei angefasst werden.

**Q25 - Schreibrecht für Codex?**
➡️ Kunden-Workspace als `trusted`, Kunden-Brain in `writable_roots` der `~/.codex/config.toml`. Sonst kann Codex dort keinen Log und keinen Index schreiben. Das Schreibrecht gilt global in Codex.

**Q23 - Wenn ein Lead Kunde wird?**
➡️ Briefing und Gesprächsfragen ziehen ins neue Kunden-Brain, im eigenen Brain bleibt nur eine Stand-Datei.
