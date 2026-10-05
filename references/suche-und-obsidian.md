# Suche im Vault: die vier Schritte und die Obsidian-CLI

Das ist der Teil, der dafür sorgt, dass ein Agent zu einem Thema **alles** findet und nicht nur die erste passende Datei. Er steht als Regel in der Workspace-`AGENTS.md` (Textbaustein in `assets/agents-md-bausteine.md`), nicht als Skill: Ein Skill springt nur an, wenn der Agent ihn für passend hält, eine Regel gilt bei jedem Thema.

## Die vier Schritte

Bei jedem Thema in dieser Reihenfolge, **bis nichts mehr fehlt**. Nicht jedes Mal alle vier: Meist reicht Schritt 1, die weiteren greifen, wenn das Thema unklar ist, mehrere Themen berührt oder eine gelesene Notiz auf Wichtiges verweist.

1. **Router:** In der `AGENTS.md` steht pro Thema eine Zeile mit allen Dateien. Alle Dateien der passenden Zeilen lesen, nicht nur eine
2. **Index:** `vault-index.md` im Vault listet jede Notiz nach Thema mit einem Satz Inhalt. Dort nach weiteren Notizen zum selben oder einem Nachbarthema schauen
3. **Verweise im Graph:** den `[[Wiki-Links]]` der gelesenen Notizen folgen und die **Backlinks** prüfen, also welche Notizen auf diese Notiz verweisen:
   ```bash
   obsidian vault="<name>-brain" backlinks file="<notiz>"
   ```
   Meldet die CLI `Error: Command "backlinks" not found. It may require a plugin to be enabled.`, ist der Vault gerade erst geöffnet worden (die CLI öffnet einen genannten Vault selbst) und das Backlink-Plugin noch nicht geladen. Am 29.09.2026 hielt das in zwei Vaults eine Weile an. Dann denselben Befehl mit vollem Pfad ab Vault-Wurzel nehmen, `backlinks path="<ordner>/<notiz>.md"`, oder kurz warten. Beide liefern dieselben Treffer
4. **Stichwort:** für alles, was 1 bis 3 nicht gefunden haben:
   ```bash
   obsidian vault="<name>-brain" search query="<stichwort>" limit=20
   ```

Bei nur einem Vault fällt `vault="<name>-brain"` in den Befehlen weg, siehe unten.

Router und Index entstehen automatisch aus dem Frontmatter (`thema`, `beschreibung`), Schritt 3 und 4 nutzen den Graph, den Obsidian ohnehin pflegt.

## Warum die Obsidian-CLI zuerst

Die CLI fragt Obsidians **eigenen Index** ab. Obsidian kennt jede Verbindung im Vault, auch Links mit Anzeigetext (`[[name|Text]]`), Links auf Überschriften und Verbindungen, die nach einem Umbenennen nachgezogen wurden. Eine Textsuche in den Dateien muss das erraten. Deshalb ist die CLI in Schritt 3 und 4 immer der erste Weg, die Dateisuche nur der Ersatz.

**Ersatz, wenn die CLI nicht antwortet:**

```bash
rg -l -F "[[<notiz>" ~/Desktop/<name>-brain        # Backlinks
rg -l -i "<stichwort>" ~/Desktop/<name>-brain      # Stichwort
```

`rg` (ripgrep) muss dafür auch außerhalb von Claude installiert sein, sonst hat Codex es nicht: `which rg`, sonst `brew install ripgrep`.

## Einrichten, einmalig beim Inhaber

Per Terminal geht es nicht, Obsidian meldet sonst "Command line interface is not enabled".

1. Obsidian öffnen, unten links das **Zahnrad** (Einstellungen)
2. **Allgemein** → nach unten zu **Erweitert**
3. **Befehlszeilenschnittstelle** (Command line interface) einschalten
4. Im Dialog **"Registrieren"** klicken. Das legt den Befehl `obsidian` im Terminal an (`/usr/local/bin/obsidian`), eventuell fragt der Mac nach dem Passwort

Test:

```bash
which obsidian
obsidian vault="<name>-brain" backlinks file="<bekannte-notiz>"
rg -l -F "[[<bekannte-notiz>" ~/Desktop/<name>-brain | wc -l   # gleiche Anzahl erwartet
```

## Zwei Punkte, die man kennen muss

- **Die App muss laufen.** Die CLI ist eine Fernbedienung für die laufende Obsidian-App. Das Symbol im Dock heißt nicht, dass sie offen ist: offen ist sie nur, wenn unter dem Symbol der **Punkt** leuchtet. Läuft sie nicht, antwortet die CLI nicht, und der Agent nutzt den Ersatz. Wer Obsidian nie offen hat, lässt die CLI weg, die Suche funktioniert trotzdem
- **Bei mehreren Vaults `vault="<name>"` mitgeben.** Die meisten arbeiten mit einem einzigen Vault, dann fällt der Teil weg (`obsidian backlinks file="<notiz>"`). Wer mehrere hat, etwa ein eigenes Brain plus Kunden-Brains, muss ihn immer setzen: Ohne fragt die CLI den zuletzt geöffneten Vault, und das ist oft ein Kunden-Brain. Dann sucht der Agent im falschen Gedächtnis. Welcher Vault gerade im Vordergrund offen ist, spielt dabei keine Rolle: Die CLI öffnet den genannten Vault bei Bedarf selbst, eventuell in einem zweiten Obsidian-Fenster (am 29.09.2026 getestet)

## Dazu gehören die kepano-Skills

`obsidian-markdown` (sauberes Obsidian-Format beim Schreiben), `obsidian-bases` (Tabellen-Ansichten), `obsidian-cli` (Befehlsreferenz). Installation in `references/bausteine.md`, Schritt 8. Beim Frontmatter gilt das eigene Schema (`thema`, `beschreibung`), auch wenn `obsidian-markdown` `title` und `tags` vorschlägt.
