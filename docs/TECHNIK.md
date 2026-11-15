# ETA-Heizung für Home Assistant

Benutzerdefinierte, standardmäßig lesende, optional steuernde Integration für die ETAtouch REST-API gemäß ETA-RESTful-v1.2. Keine offizielle ETA- oder Home-Assistant-Integration.

## Installation

1. ZIP entpacken und den gesamten Ordner `custom_components/eta_readonly` nach `/config/custom_components/eta_readonly` deiner Home-Assistant-Installation kopieren. Nicht den äußeren Ordner kopieren.
2. Home Assistant vollständig neu starten.
3. **Einstellungen → Geräte & Dienste → Integration hinzufügen → ETA Heizung Lokal** öffnen.
4. IP-Adresse der Heizung, Port **8080** und Abfrageintervall (Standard 60 Sekunden) eingeben.
5. Die automatische Suche abwarten. Sie prüft die im Menü enthaltenen Datenpunkte, zählt nicht lesbare Einträge und wählt alle lesbaren Werte vor. Auswahl bestätigen oder bei Bedarf reduzieren.
6. Die Sensoren beim Gerät „ETA Heizung“ öffnen und bei Bedarf zum Dashboard hinzufügen.

Keine YAML-Konfiguration erforderlich. Zum Ändern der Datenpunktauswahl die Integration entfernen und erneut einrichten; dabei kann die Entitätsidentität wechseln. Änderungen an Host/Port/Intervall erfolgen ebenfalls durch erneute Einrichtung. Installation als benutzerdefiniertes Marketplace-/HACS-Repository ist ab 1.1.1 vorbereitet; siehe README.

## Voraussetzungen laut mitgelieferter ETA-Dokumentation

- ETAtouch-Systemsoftware ab 1.20.0.
- Gerät auf meineta.at registriert, LAN-Zugriff dort beantragt und anschließend am Touchdisplay in den Systemeinstellungen aktiviert (diese Reihenfolge nennt das Handbuch).
- Home Assistant erreicht die lokale IP-Adresse auf TCP-Port 8080.
- Im Browser prüfen: `http://DEINE-HEIZUNGS-IP:8080/user/menu`. Erwartet wird ETA-XML mit einem Menübaum. Die Integration benötigt keine meinETA-Zugangsdaten.

## Verhalten und Grenzen

Lesende Abfragen verwenden GET auf `/user/menu` und `/user/var/{Adresse}`. Mit aktivem Schreibzugriff werden zusätzlich `/user/varinfo/{Adresse}` gelesen und explizite Schreibaufträge per POST an `/user/var/{Adresse}` gesendet. Pro Aktualisierung wird jeder gespeicherte Datenpunkt einzeln gelesen, mit höchstens zwei gleichzeitigen Anfragen. Es werden keine Variablensätze auf der Heizung angelegt ; Heizungsparameter werden nur bei freigegebenem Schreibzugriff und einem expliziten Bedienauftrag geschrieben.

Numerische Werte werden als Rohwert geteilt durch `scaleFactor` übernommen, Textzustände als `strValue`. XML-Namensräume werden berücksichtigt. Zustände mit `advTextOffset` bleiben Text. Einheiten kommen vom Gerät; Temperatur, Druck und Leistung erhalten passende Sensorklassen. Zähler bekommen bewusst keine automatisch angenommene Statistikklasse, weil Rücksetzverhalten und Bedeutung nicht aus dem Menü hervorgehen.

Einzelne fehlerhafte Werte werden „nicht verfügbar“; gültige Werte werden weiter aktualisiert. Bei vollständigem Ausfall versucht Home Assistant die Verbindung erneut. Bei vielen Datenpunkten oder langsamer Steuerung ein längeres Intervall wählen. Pro Anfrage gilt ein Timeout von 10 Sekunden. Viele nicht erreichbare Datenpunkte können den Scan und Aktualisierungen deutlich verlängern. Das effektive Intervall wird bei langsamen Durchläufen automatisch vergrößert.

Die API wird lokal per HTTP angesprochen. Für Fernzugriff den bestehenden Zugang zu Home Assistant verwenden. Störungsmeldungen unter `/user/errors` und automatische Erkennung neu hinzugefügter Datenpunkte sind nicht Bestandteil dieser Version. API-Schreibzugriff und Grenzen sind in `STEUERUNG.md` dokumentiert.

## Prüfung

34 Python-Tests und sechs JavaScript-Prüfungen: XML-Auswertung, mehr als 50 Werte, Teilfehler, Abbruch, Parallelitätsgrenze, Einrichtungslogik, Schreibberechtigung, Wertkodierung, HTTP-Transport und Bestätigungen mit Ersatzobjekten. Python-Syntaxprüfung aller Integrationsdateien. Keine vollständigen HA-Integrationstests. Ein Test in einer laufenden Home-Assistant-Instanz und mit deiner realen Heizung steht noch aus.

## Quellen

- Bereitgestellte ETA-RESTful-v1.2.pdf, insbesondere Seiten 4 und 8–10.
- https://developers.home-assistant.io/docs/config_entries_config_flow_handler/
- https://developers.home-assistant.io/docs/integration_fetching_data/
- https://developers.home-assistant.io/docs/core/entity/sensor/

## Dashboard mit Bildentität

Im Ordner `dashboard` liegen Heizungsbild, Dashboard-Generator und eine Schritt-für-Schritt-Anleitung (`ANLEITUNG.md`). Der Generator verwendet deine tatsächlichen Sensor-IDs.

## Custom Card ab 1.0.1

`frontend.py` registriert ausschließlich eine JavaScript-Modulressource über die bestehende Lovelace-Ressourcensammlung. `www/eta-heating-card.js` ist eine normale Custom Card, die mit `window.loadCardHelpers` Standardkarten als vertikalen Stapel anzeigt. ETA-Entitäten werden über die Attribute `eta_integration` und `eta_config_entry_id` erkannt. Die Karte ist über `window.customCards` in der Kartenauswahl registriert und besitzt einen Konfigurationseditor.

Keine Änderung der Lovelace-Dashboard-Sammlung, keine Registrierung eines Panels, keine neue Dashboard-Seite und kein Seitenleisteneintrag. Logo und JavaScript werden über feste lokale HTTP-Pfade aus dem Integrationsordner bereitgestellt. YAML-verwaltete Ressourcen werden nicht verändert.
