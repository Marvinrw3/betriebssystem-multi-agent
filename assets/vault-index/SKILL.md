---
name: vault-index
description: "Baut den Vault-Index und den Router-Block in der AGENTS.md neu aus dem Frontmatter der Notizen und meldet Notizen ohne Thema. Läuft automatisch am Session-Ende und beim Anlegen von Projekten."
disable-model-invocation: true
---

# Vault-Index

Hält den Themen-Router aktuell, damit Claude und Codex zu jedem Thema alle Dateien finden.

- **Rein:** das Frontmatter (`thema`, `beschreibung`) aller Kernnotizen in dem Vault aus `config.json`
- **Raus:** `vault-index.md` im Vault (nach Thema, mit Wiki-Links für Obsidian) und der Block zwischen `<!-- router:start … -->` und `<!-- router:end -->` in der `AGENTS.md` aus `config.json` (Pfade für die Agenten)

## Startprotokoll

1. Prüfen, dass beide Markierungen in der `AGENTS.md` aus `config.json` stehen. Fehlen sie, bricht das Skript ab und ändert nichts
2. Kernnotizen sind alle `.md` im Vault außer die Ordner unter `ausschluss` in `config.json`

## Arbeitsanweisung

1. `python3 scripts/check_frontmatter.py` ausführen (aus dem Skill-Ordner)
2. Meldet es Notizen ohne Thema oder mit zu knapper Beschreibung: jede lesen und Frontmatter nach der Vorlage unten ergänzen. Themen aus dem Index wiederverwenden, ein neues Thema nur, wenn keins passt
3. `python3 scripts/build_index.py` ausführen
4. Ausgabe nennen: Anzahl Einträge und Themen, neue Themen gesondert

## Vorlage Frontmatter

Steht in Zeile 1 der Notiz, vor allem anderen:

```yaml
---
thema:
  - akquise
  - mueller-gmbh
beschreibung: "Lead Müller GmbH: Firmenanalyse und Ansatzpunkte"
---
```

- `thema`: ein bis drei Einträge, Kleinbuchstaben mit Bindestrich. Kunden und Leads zusätzlich mit Firmennamen
- `beschreibung`: ein bis zwei Sätze, was drinsteht, **mit den Stichworten, nach denen gefragt wird**: Namen von Personen und Firmen, Zahlen, Preise, Entscheidungen, Fachbegriffe. Agenten wählen bei großen Themen nur über diese Beschreibung aus, welche Dateien sie öffnen. Fehlt ein Name hier, wird die Notiz bei einer Frage nach diesem Namen übersehen. Gut: "Leads aus dem Netzwerk: Firma A (über Kontakt X), Firma B (über Kontakt Y), mit Stand und nächstem Schritt". Zu dünn: "Leads aus dem eigenen Netzwerk"

## Definition of Done

- [ ] `check_frontmatter.py` meldet 0 Notizen
- [ ] `vault-index.md` ist neu geschrieben
- [ ] Router-Block in der `AGENTS.md` enthält jedes Thema aus dem Index, außerhalb der Markierungen ist nichts verändert (`git diff AGENTS.md` prüfen)
- [ ] Neue Themen sind dem Inhaber genannt
