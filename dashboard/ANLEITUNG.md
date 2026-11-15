# ETA-Karte im vorhandenen Dashboard – Version 1.0.1

## Wie eine Flow Card hinzufügen

1. Integration installieren bzw. auf 1.0.1 aktualisieren und Home Assistant neu starten.
2. ETA-Heizung einrichten bzw. bestehende Einrichtung laden lassen.
3. Browser vollständig neu laden.
4. Im gewünschten Dashboard **Bearbeiten → Karte hinzufügen → ETA Heizung Lokal** wählen und speichern.

Es wird keine eigene Dashboard-Seite angelegt und kein Seitenleisteneintrag erzeugt. Das Karten-JavaScript wird von der Integration mitgeliefert und bei Storage-Ressourcen automatisch registriert. Das Logo wird direkt aus der Integration geladen. Kein Bildkopieren und kein Template-Editor nötig.

## Manuelle Kartenkonfiguration

```yaml
type: custom:eta-heating-card
title: ETA Heizung
show_history: true
show_controls: true
```

Diese wenigen Zeilen gehören in eine **manuelle Karte**, nicht in den Rohkonfigurationseditor des gesamten Dashboards. Die Karte erkennt die tatsächlichen ETA-Entitäten automatisch. Optional lassen sich `config_entry_id` für eine einzelne Anlage und `picture_entity` für einen bestimmten Bild-Sensor setzen. Dieselben Einstellungen stehen im Karteneditor.

## Ressourcen

Erwartete Modulressource: `/eta_readonly/eta-heating-card.js?v=1.0.1`. Bei YAML-verwalteten Ressourcen muss sie selbst als `type: module` ergänzt werden; Details stehen in der README. Bei Storage-Ressourcen wird sie beim Laden der Integration eingetragen. Beim vollständigen Entfernen der Integration kann diese ausschließlich ihr gehörende Ressourcenzeile anschließend unter Dashboard-Ressourcen entfernt werden.

## Frühere Version 1.3.0

Die frühere automatisch registrierte Seitenleistenansicht entfällt nach Update und Neustart. Die Option dafür ist entfernt. Bestehende eigene Dashboards bleiben unverändert. Die Karte kann in einem beliebigen dieser Dashboards platziert werden.

## Optional: alte manuelle Vorlage

`dashboard-erzeugen.jinja` bleibt als Alternative für ein selbst gestaltetes, vollständiges Standardkarten-Dashboard erhalten. Nur bei Verwendung dieser alten Vorlage wird `eta-logo.png` nach `/config/www/eta-logo.png` kopiert und die Jinja-Vorlage in Entwicklerwerkzeuge → Template ausgeführt. Die gerenderte Ausgabe gehört dann in ein neues, leeres Dashboard. Für die neue Custom Card sind diese Schritte nicht erforderlich.

## Bildrechte und Grenzen

Das ETA-Logo wurde vom Nutzer bereitgestellt, eine Herstellerfreigabe wurde nicht nachgewiesen. Es ist nicht GPL-lizenziert; ein Hinweis ersetzt keine erforderliche Erlaubnis. Siehe `THIRD_PARTY_NOTICES.md`. Die Karte verändert keine Heizungseinstellung beim Laden; Auswahlfelder sind jedoch bei freigegebenem Schreibzugriff aktiv bedienbar. Ein realer Home-Assistant-Browsertest steht aus.
