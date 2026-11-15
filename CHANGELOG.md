# Änderungen

## 1.0.1 – 15.11.2026

- Integrationseigene Dashboard-Seite und Seitenleisteneintrag aus Version 1.3.0 entfernt.
- Normale Custom Card `custom:eta-heating-card`, wie eine Flow Card platzierbar.
- Automatische Registrierung der Kartenressource im Storage-Modus.
- Erscheint als „ETA Heizung Lokal“ in der Kartenauswahl.
- Konfigurationseditor für Titel, Anlagenfilter, Bild-Sensor, Verlauf und Steuerung.
- Automatische Erkennung der ETA-Entitäten innerhalb der Karte.
- 34 Python-Tests und sechs JavaScript-Prüfungen bestanden. Kein realer HA-Browsertest.

## Frühere lokale Entwicklungsstände

Die nachfolgenden Versionsbezeichnungen gehören zu lokalen Entwürfen, nicht zur aktuellen Veröffentlichungsnummer. Der hier bereitgestellte Stand ist v1.0.1.

## 1.3.0 – 15.11.2026

- Automatisches, integrationseigenes Dashboard pro eingerichteter Anlage.
- Logo direkt aus der Integration: kein Kopieren nach `www` erforderlich.
- Keine manuelle Ausführung der Jinja-Vorlage mehr nötig.
- Sensoren, Temperaturen und freigegebene Auswahlentitäten aus der aktuellen Entity Registry.
- Dashboard in den Integrationsoptionen aktivierbar/deaktivierbar; Standard an.
- Keine Überschreibung bestehender Dashboard-URLs oder Benutzer-Dashboards.
- Eigene Registrierung beim Entladen der Integration entfernen.
- 39 lokale Tests bestanden; vollständiger HA-/UI-Test steht aus.

## 1.2.0 – 15.11.2026

- Optionaler API-Schreibzugriff bei Einrichtung und in nachträglichen Optionen.
- Aktuelle Berechtigungsprüfung via `/user/varinfo` vor jedem Schreibauftrag.
- Auswahlentitäten für schreibbare TEXT-Variablen mit gemeldeten Auswahlwerten.
- Aktion `eta_readonly.set_value` für Anzeigewerte, RAW-Werte und Zeitfenster.
- Prüfung von Skalierung, Enum-Werten, Zieladresse und passender Schreibbestätigung.
- Keine automatische Wiederholung eines Schreibauftrags.
- Brand-Ordner mit Original-Logo und quadratischer Thumbnail-Variante.
- Anzeigename „ETA Heizung Lokal“, interne Domain bleibt `eta_readonly`.
- Technische Mindestversion Home Assistant 2026.11.0 hinterlegt.
- 31 lokale Tests; kein Auftrag an eine reale Heizung gesendet.

## 1.1.1 – 15.11.2026

- Fehlende `hacs.json` im Repository-Stamm ergänzt.
- `documentation`, `issue_tracker` und `codeowners` im Integrationsmanifest ergänzt.
- Installation über Marketplace/HACS und manuelle Einrichtung in README beschrieben.
- Hinweis zur separaten Dashboard-Installation und zu älteren Releases ohne `hacs.json`.
- Keine Änderungen an Abfragen, Sensoren oder gespeicherten Konfigurationen.

## 1.1.0 – 15.11.2026

- Automatischer Erstscan des echten Menübaums mit Fortschrittsanzeige.
- Prüfung aller gefundenen Adressen; lesbare Werte vorausgewählt, nicht lesbare gezählt.
- Keine feste Begrenzung auf 50 Datenpunkte mehr.
- Höchstens zwei gleichzeitige GET-Anfragen bei Scan und Polling.
- Abbruch der Einrichtung beendet auch die laufenden Scan-Worker.
- Bei langsamen Durchläufen automatisch längeres effektives Abfrageintervall.
- Vorhandene Konfigurationseinträge bleiben lesbar und behalten ihre Auswahl.
- 15 lokale Tests, Dokumentation und deutsche/englische Einrichtungstexte.
- GPL-3.0-only, Sponsoring und Dashboard mit ETA-Logo bleiben enthalten.

Kein Test an realer Heizung oder in einer laufenden Home-Assistant-Instanz. Kein Code aus dorsch95/ha-eta-webservices übernommen; eigenständige Implementierung anhand der ETA-API und des eigenen vorhandenen Codes.
