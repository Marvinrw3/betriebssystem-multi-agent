# Plan: <Name des Systems> agent-native machen

> Stand: <Datum>. Ergebnis aus den Grill-Runden (Q1 bis Q<n>). Noch nicht freigegeben, nichts davon ist gebaut.

## Ziel

Claude Code und Codex haben vollständigen Kontext zu Workspace (`<ws>`) und Brain (`<vault>`). Jedes Thema führt zuverlässig zu allen passenden Dateien. Inhalte stehen ausgeschrieben oder per Pfad erreichbar, nie nur hinter einem `@`-Import. Das System wächst mit, wenn neue Notizen oder Themen entstehen.

## Ausgangslage

<Aus audit.py übernehmen: Zahlen und jede FEHLT-Zeile. Nur geprüfte Fakten, keine Vermutungen.>

## Entscheidungen

| # | Entscheidung |
|---|---|
| Q1 | <...> |

## Umsetzung in Schritten

<Schritte 0 bis 11 aus references/bausteine.md, auf dieses System zugeschnitten: konkrete Pfade, Anzahl Notizen, welche Skills angepasst werden, welche Regeln wohin wandern.>

## Test

<Die 10 Fragen, Wachstumstest, ggf. Kunden-Test und Sicherheitstest. Bestanden bei 10/10 für beide.>

## Nicht Teil dieses Plans

<Was bewusst später kommt.>

## Risiken

- Ausgelagerte Regeln liest ein Agent nur bei erkanntem Auslöser, deshalb bleiben Verhaltensregeln drin, ein Test prüft eine ausgelagerte Regel
- Das Skript schreibt in die `AGENTS.md`: nur zwischen Markierungen, Abbruch wenn sie fehlen, alles in Git
- <weitere, konkret für dieses System>

## Gegenprüfung

<Nach codex_pruefen.sh: welche Befunde übernommen, welche nicht und warum.>
