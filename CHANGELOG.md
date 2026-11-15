# Änderungen

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
