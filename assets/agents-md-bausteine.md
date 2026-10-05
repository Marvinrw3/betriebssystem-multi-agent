# Textbausteine für die AGENTS.md-Dateien

Zum Einsetzen beim Umbau. `<...>` ersetzen. Sprache und Ton an den Inhaber anpassen.

## Global: `~/.agents/AGENTS.md`, Kopf

```markdown
# Globale Anweisungen (gelten für alle Projekte)

Gilt für jeden Agenten auf diesem Rechner: Claude Code, Codex, Hermes. Claude lädt diese Datei über `~/.claude/CLAUDE.md`, Codex über `~/.codex/AGENTS.md`, Hermes über `~/.hermes/SOUL.md`, alle drei sind Verweise auf diese eine Datei.
```

Verknüpfen:

```bash
printf '@~/.agents/AGENTS.md\n' > ~/.claude/CLAUDE.md
ln -sf ~/.agents/AGENTS.md ~/.codex/AGENTS.md
mkdir -p ~/.hermes && ln -sf ~/.agents/AGENTS.md ~/.hermes/SOUL.md
```

## Global: Regeln nach Auslöser

```markdown
## Regeln nach Auslöser

Diese Regeln gelten genauso verbindlich wie alles hier, stehen aber in eigenen Dateien, weil sie nur in bestimmten Momenten gebraucht werden. **Greift der Auslöser, zuerst die Datei lesen, dann handeln.**

| Auslöser | Datei |
|---|---|
| Commit, Push, irgendein Git-Vorgang | `~/.agents/regeln/git.md` |
| In einen Vault schreiben, Notiz anlegen, Dateinamen wählen, entscheiden wo Kundenwissen hingehört | `~/.agents/regeln/vault-konventionen.md` |
| Code schreiben oder ändern | `~/.agents/regeln/code.md` |
| Frage zu einer Library, einem Framework, SDK, CLI oder Cloud-Dienst | `~/.agents/regeln/context7.md` |
| Ein Lernprotokoll-Eintrag ist unklar, oder ein neuer kommt dazu | `~/.agents/regeln/lernprotokoll-faelle.md` |
```

## Global: Lernprotokoll

```markdown
## Lernprotokoll

Korrekturen aus der echten Arbeit, gelten in jedem Projekt. Pro Eintrag die Regel, der Fall dahinter steht in `~/.agents/regeln/lernprotokoll-faelle.md`. **Neuer Eintrag:** Fall dort, Einzeiler hier, ohne zu fragen.

- [YYYY-MM-DD] **<Thema>.** <Regel in einem Satz>
```

`lernprotokoll-faelle.md` beginnt mit der Pflegeanweisung: zwei Stellen ergänzen, Bestehendes nie löschen oder umschreiben außer auf ausdrückliche Ansage, bei parallelen Agenten vorher frisch lesen.

## Global: Freigabe bei Außenkontakt

```markdown
## Freigabe bei Außenkontakt

Alles, was nach außen geht oder im Werbekonto wirkt, läuft in eine **zweite Schleife**: erst Entwurf plus kurze Erklärung (was passiert, an wen, warum, was es auslöst), dann auf Freigabe warten, erst danach ausführen.

- **Mails und Nachrichten jeder Art:** Mail, DM, WhatsApp, SMS, LinkedIn, Kommentare, Posts
- **Maßgebliche Änderungen im Werbekonto:** live schalten, pausieren, löschen, Budget, Gebot, Zielgruppe, Zahlungsdaten. Lesen, auswerten und pausiert angelegte Entwürfe brauchen keine Freigabe
```

## Global: Vault-Konventionen, Zusatz Frontmatter (in `regeln/vault-konventionen.md`)

````markdown
### Frontmatter: Thema und Beschreibung
Jede Notiz außerhalb von Logs, Archiv und Rohdaten beginnt in Zeile 1 mit:

```yaml
---
thema:
  - akquise
  - mueller-gmbh
beschreibung: "Ein Satz, was drinsteht"
---
```

Daraus baut der Skill `vault-index` den Router in der Workspace-`AGENTS.md` und `vault-index.md`. Themen aus dem Index wiederverwenden, ein neues nur, wenn keins passt. Kunden und Leads zusätzlich mit Firmennamen. Keine weiteren Felder wie `title`, `tags` oder `status`, auch wenn `obsidian-markdown` sie vorschlägt.

- **Die Regeln eines Brains stehen in dessen eigener `AGENTS.md`**, daneben `CLAUDE.md` mit nur `@AGENTS.md`. Erste Zeile der `AGENTS.md` im Kundenworkspace: "Pflicht vor allem anderen: `~/Desktop/<kunde>-brain/AGENTS.md` lesen." Kein `@` auf das Brain
- **Wird ein Lead zum Kunden**, ziehen Briefing und Gesprächsfragen ins neue Kunden-Brain, im eigenen Brain bleibt nur `<kunde>-stand.md`
````

## Workspace: Vault-Abschnitt mit Router und Suchreihenfolge

Gibt es nur einen Vault, in Schritt 3 und 4 `vault="<name>-brain" ` streichen.

```markdown
## Vault (Single Source of Truth)
Alle Fakten liegen im Vault. Hier stehen **keine** Details, lies bei Bedarf direkt nach.

**Pfad:** `~/Desktop/<name>-brain/`

<Ordnertabelle des Vaults>

### Themen-Router

Zu jedem Thema die Dateien, die dazugehören. **Wird ein Thema angesprochen, alle Dateien der Zeile prüfen, nicht nur eine:** Bei bis zu fünf Dateien alle lesen. Bei mehr zuerst ihre Beschreibungen im Vault-Index lesen, dann jede Datei öffnen, die zur Frage passen könnte. Im Zweifel eine Datei mehr lesen, nicht eine weniger. Der Block wird vom Skill `vault-index` aus dem Frontmatter der Notizen gebaut, neue Themen erscheinen von selbst.

<!-- router:start (automatisch, nicht von Hand ändern) -->
<!-- router:end -->

**Immer, ohne Thema:** `<prioritäten-datei>` und `<offene-punkte-datei>` bei jedem Session-Start. Logs: `<log-muster>`.

### Suchreihenfolge

Bei jedem Thema in dieser Reihenfolge, bis nichts mehr fehlt:

1. **Router:** die Dateien der passenden Zeilen, nach der Regel oben (bis fünf alle, sonst über die Beschreibungen auswählen)
2. **Index:** `~/Desktop/<name>-brain/vault-index.md` nach weiteren Notizen zum selben oder einem Nachbarthema durchsehen
3. **Verweise:** den `[[Wiki-Links]]` der gelesenen Notizen folgen und Backlinks prüfen: `obsidian vault="<name>-brain" backlinks file="<name>"` (Obsidian läuft. `vault=` nur bei mehreren Vaults, dann Pflicht, sonst weglassen), nur falls das scheitert `rg -l -F "[[<name>" ~/Desktop/<name>-brain`
4. **Stichwort:** zuerst `obsidian vault="<name>-brain" search query="<stichwort>" limit=20`, nur falls das scheitert `rg -l -i "<stichwort>" ~/Desktop/<name>-brain`

Lies die gefundenen Dateien, statt aus dem Gedächtnis zu antworten. Der Vault ist die Wahrheit.
```

## Workspace: Regeln nach Auslöser

```markdown
## Regeln nach Auslöser

Die globalen Regeln in `~/.agents/AGENTS.md` gelten hier mit. Lokal kommt dazu, was nur diesen Workspace betrifft. **Greift der Auslöser, zuerst die Datei lesen, dann handeln.**

| Auslöser | Datei |
|---|---|
| <Auslöser> | `regeln/<datei>.md` |
```

## Workspace: Mehrere Agenten und Gemerkt

```markdown
## Mehrere Agenten
Dieser Workspace läuft in Claude Code und Codex, später auch in Hermes. Alle lesen diese Datei, dieselben Skills und denselben Vault.

- **Toolnamen:** Skills nennen Tools oft mit Claude-Namen (`mcp__server__tool`). In Codex das gleichnamige Tool des MCP-Servers oder Plugins nutzen
- **Sub-Agents:** Claude nutzt `.claude/agents/`, Codex `~/.codex/agents/<name>.toml`. Gleiche Aufgabe, gleicher Name
- **Laufen zwei Agenten parallel,** vor dem Schreiben in Lernprotokoll oder Logs die Datei frisch lesen und nur ergänzen

## Gemerkt
Einzelne Fakten und Präferenzen, die für jeden Agenten gelten. **Neue Merkpunkte kommen hierher**, nicht in ein Agenten-eigenes Gedächtnis. Projektstände gehören in den Vault.
```

## Kunden-Workspace: erste Zeile

```markdown
> **Pflicht vor allem anderen:** `~/Desktop/<kunde>-brain/AGENTS.md` lesen. Dort stehen die Regeln und der Router des Kunden-Brains.
```
