---
name: betriebssystem-multi-agent
description: "Baut ein bestehendes Claude-Code-Betriebssystem (Workspace plus Obsidian-Vault) so um, dass Codex und Hermes denselben vollständigen Kontext haben: Audit, Sicherungspunkt, Grill-Runden, Plan mit Codex-Gegenprüfung, Themen-Router, Regeln nach Auslöser, Skills zentral, Obsidian-CLI, Sicherheits-Setup für Kunden, Test mit beiden Agenten."
disable-model-invocation: true
---

# Betriebssystem multi-agent machen

Nimmt ein Betriebssystem, das nur Claude Code wirklich versteht, und macht es **agent-native**: Claude Code, Codex und Hermes lesen dieselben Regeln, dieselben Skills und finden zu jedem Thema alle Dateien im Vault. Für das eigene System und als Leistung für Kunden.

- **Rein:** Pfad zum Workspace, Pfad zum Vault (Brain), ob eigenes System oder Kunde
- **Raus:** umgebautes System, ein freigegebener Plan unter `<ws>/projekte/multi-agent-umbau/plan.md`, Testergebnis beider Agenten, Commits in Workspace, Vault und `~/.agents`

## Das Prinzip in einem Satz

Die `AGENTS.md` ist die **Landkarte, nicht das Handbuch**: Was in jeder Antwort gilt, steht drin. Alles andere steht in eigenen Dateien, und die `AGENTS.md` sagt in normaler Sprache, wann welche Datei zu lesen ist. `@`-Importe versteht nur Claude, deshalb trägt nie ein `@` Inhalt, den ein anderer Agent braucht. Einzige Ausnahme ist die `CLAUDE.md` neben jeder `AGENTS.md`: Sie enthält nur `@AGENTS.md`. Claude könnte die `AGENTS.md` inzwischen auch allein lesen, aber nicht in jeder Version und jeder Umgebung. Der Zwischenverweis stellt sicher, dass Claude sie immer liest, und lädt nichts doppelt.

Damit ein Agent zu einem Thema **alles** findet, gilt eine feste Suche in vier Schritten: Router, Index, Verweise im Graph, Stichwort. Schritt 3 und 4 laufen zuerst über die **Obsidian-CLI**, weil sie Obsidians eigenen Link-Index abfragt. Die CLI muss der Inhaber einmal in Obsidian freischalten, und die App muss dabei laufen. Alles dazu in `references/suche-und-obsidian.md`.

## Startprotokoll

1. Pfade klären: Workspace, Vault, eigenes System oder Kunde. Fehlt etwas, einmal nachfragen
2. `references/fallen.md` lesen. Jede Zeile dort ist im ersten Echtumbau passiert
3. Audit laufen lassen und lesen:
   ```bash
   python3 <skill>/scripts/audit.py --workspace <ws> --vault <vault>
   ```
4. Werkzeuge prüfen: `claude`, `codex`, `jq`, `rg` (für Codex außerhalb von Claude), `gh`. Fehlendes installieren (`brew install ...`), Login nur einmal beim Inhaber anfordern

## Kontext-Mapping

| Wofür | Datei |
|---|---|
| Entscheidungen mit Empfehlungen | `references/grill-fragen.md` |
| Umsetzung Schritt für Schritt | `references/bausteine.md` |
| Stolperfallen | `references/fallen.md` |
| Suche in vier Schritten, Obsidian-CLI einrichten | `references/suche-und-obsidian.md` |
| Sicherheits-Setup für Kunden | `references/sicherheit-kunden.md` |
| Texte für die `AGENTS.md`-Dateien | `assets/agents-md-bausteine.md` |
| Plan | `assets/plan-vorlage.md` |
| Testfragen | `assets/testfragen-vorlage.md` |
| Router-Skript für den Workspace | `assets/vault-index/` (wird kopiert) |
| Secret-Sperren | `assets/hooks/` |

## Arbeitsanweisung

1. **Sicherungspunkt.** Workspace und Vault committen, `~/.agents` als privates Repo anlegen (Schritt 0 in `references/bausteine.md`). Ab hier ist jeder Schritt umkehrbar
2. **Grillen.** Die Fragen aus `references/grill-fragen.md` in Runden stellen, jede mit Empfehlung, nur Fragen deren Voraussetzungen geklärt sind. Fakten selbst nachschlagen (Dateien, Versionen, Anzahl Notizen), nur Entscheidungen fragen. Was der Ist-Zustand laut Audit schon beantwortet, nicht fragen, sondern als "schon entschieden" nennen. Weiter erst, wenn der Fragenbaum leer ist
3. **Plan schreiben** nach `assets/plan-vorlage.md`, mit Zahlen aus dem Audit statt Annahmen
4. **Codex prüft den Plan**, neutral und nur lesend:
   ```bash
   bash <skill>/scripts/codex_pruefen.sh <ws>/projekte/multi-agent-umbau/plan.md "" <ws>
   ```
   Jeden Befund selbst gegen die Dateien prüfen, bevor er übernommen wird. Im Plan unter "Gegenprüfung" festhalten, was übernommen wurde und was nicht
5. **Freigabe einholen.** Plan kurz vorstellen, Befunde von Codex nennen, auf das Ja warten. Vorher wird nichts umgebaut außer dem Sicherungspunkt
6. **Umsetzen** nach `references/bausteine.md`, Schritte 1 bis 9, in dieser Reihenfolge. Nach jedem größeren Schritt eine Zeile Zwischenstand an den Inhaber
7. **Testen** (Schritt 10): 10 Themenfragen an Claude und Codex in frischen Sessions per `scripts/agenten_test.sh`, dazu Wachstumstest, bei Kunden Kunden-Test und Sicherheitstest mit Attrappe
8. **Abschließen** (Schritt 11): Audit erneut, Commits, Doku im Vault, Übergabe mit "Bei dir"-Liste

## Was nie passiert

- Inhalte löschen: Altes wandert nach `~/.claude/archive/<jahr-monat>/` oder ins Vault-Archiv
- Notizinhalte ändern beim Frontmatter-Setzen: nur voranstellen
- `git add -A` oder `.`: immer gezielt stagen, danach auf Schlüssel prüfen
- Die echte `.env` im Sicherheitstest: nur Attrappen

## Definition of Done

- [ ] `audit.py` zeigt kein FEHLT mehr, oder jedes verbleibende ist im Plan begründet
- [ ] Beide `AGENTS.md` enthalten keinen `@`-Import außer `CLAUDE.md` → `@AGENTS.md`
- [ ] `~/.codex/AGENTS.md` und `~/.hermes/SOUL.md` zeigen auf `~/.agents/AGENTS.md`
- [ ] Alle Skills liegen echt in `~/.agents/skills/` bzw. `<ws>/.agents/skills/`, Claude sieht sie per Symlink, Codex meldet keinen Ladefehler
- [ ] Jede Kernnotiz hat `thema` und `beschreibung`, `check_frontmatter.py` meldet 0
- [ ] Router-Block in der Workspace-`AGENTS.md` ist gebaut, `build_index.py` zweimal gelaufen ohne Unterschied
- [ ] `vault-index` ist in Session-Ende-, Projekt- und Notiz-Skill eingebunden
- [ ] Suche in vier Schritten steht als Regel in der Workspace-`AGENTS.md`, Schritt 3 und 4 mit `obsidian` zuerst (bei mehreren Vaults mit `vault="<name>"`), `rg` als Ersatz
- [ ] Obsidian-CLI vom Inhaber freigeschaltet und getestet (gleiche Backlink-Zahl wie `rg`), oder bewusst weggelassen, weil Obsidian nicht läuft
- [ ] Gedächtnis beider Agenten aus, "Gemerkt" angelegt
- [ ] Test: Claude 10/10, Codex 10/10, Wachstumstest bestanden
- [ ] Bei Kunden: Sicherheits-Setup mit Attrappe getestet, Codex-Hooks unter `/hooks` freigegeben
- [ ] Workspace, Vault und `~/.agents` committet und gepusht, Plan liegt unter `<ws>/projekte/multi-agent-umbau/plan.md`
