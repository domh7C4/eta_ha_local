# ETA Heizung für Home Assistant

![ETA-Logo](dashboard/eta-logo.png)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
![Version](https://img.shields.io/badge/Version-1.1.0-blue)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Custom%20Integration-41BDF5)
[![Sponsor via PayPal](https://img.shields.io/badge/PayPal-Projekt%20unterst%C3%BCtzen-00457C?logo=paypal&logoColor=white)](https://www.paypal.me/domh7C4)

Unabhängige, inoffizielle Custom Integration für die lokale ETAtouch REST-API. Ausschließlich lesend. Projektstand: **15. November 2026**, Version **1.1.0**.

## Aktueller Funktionsumfang

- Einrichtung in der Home-Assistant-Oberfläche mit Host, Port und Abfrageintervall.
- Automatische Erkennung aller im Menübaum enthaltenen und beim Scan erfolgreich lesbaren Datenpunkte. Keine feste 50-Werte-Grenze; alle gefundenen Werte sind vorausgewählt.
- Sensoren für Temperaturen, Druck, Leistung, Zähler und Textzustände; verfügbare Werte hängen von der konkreten Anlage ab.
- Abfrage standardmäßig alle 60 Sekunden, einstellbar zwischen 30 und 3600 Sekunden.
- Dashboard mit **ETA-Logo als Bildentitätskarte anstelle der Heizungszeichnung**, darunter aktueller Sensorwert, Sensorliste und Temperaturverlauf.
- Dashboard-Generator ermittelt die tatsächlichen Entitäts-IDs. Keine zusätzlichen Dashboard-Karten erforderlich.
- Die Demo aus dem Chat verwendet simulierte Werte; die Integration verwendet echte Werte nach Verbindung mit der Heizung.

## Automatische Erkennung beim ersten Einrichten

Die Integration lädt `/user/menu` von der angegebenen Heizung, übernimmt die tatsächlichen Adressen und Namen aus dem XML-Menü und prüft jeden Kandidaten mit `GET /user/var/{Adresse}`. Auch lesbare Einträge mit Unterobjekten werden geprüft. Es gibt keine feste Liste von Kesselmodellen oder vorgegebenen Sensoradressen. Die Heizung selbst muss weiterhin per IP-Adresse oder Hostname angegeben werden; dies ist keine Netzwerksuche nach Heizungen.

Während der Suche zeigt Home Assistant den Fortschritt. Alle erfolgreich gelesenen Werte sind anschließend vorausgewählt. Du musst keine Adressen oder Sensoren einzeln heraussuchen. Nicht lesbare Einträge (z. B. Menügruppen) und Verbindungsfehler werden übersprungen und im Ergebnis gezählt. Ein vorübergehend ausgefallener Wert lässt sich dabei nicht sicher von einem dauerhaft nicht lesbaren unterscheiden: bei unerwartet wenigen Funden mit stabiler Verbindung erneut einrichten.

Die bestätigte Auswahl wird lokal im Home-Assistant-Konfigurationseintrag gespeichert und nach einem Neustart wiederverwendet. Bereits eingerichtete Anlagen behalten ihre bisherigen Datenpunkte; zum vollständigen Erstscan mit dieser Version die alte Integration entfernen und neu hinzufügen. Dabei können sich Entitäts-IDs ändern, anschließend das Dashboard aktualisieren. Neu hinzugefügte Anlagenkomponenten werden nicht während jedes Polling-Durchlaufs erneut gesucht.

Der Scan verwendet ausschließlich GET. Weder werden Variablensätze angelegt noch Heizungsparameter verändert. `/user/errors` und `/user/varinfo` werden in dieser Version noch nicht abgefragt.

## Voraussetzungen

Home Assistant mit Zugriff auf sein Konfigurationsverzeichnis und Netzwerkzugriff auf die Heizung. Eine konkrete Mindestversion von Home Assistant wurde bislang nicht validiert.

Laut bereitgestelltem ETA-Handbuch: ETAtouch-Systemsoftware ab 1.20.0; Gerät auf meineta.at registrieren, LAN-Zugriff dort beantragen und anschließend am Touchdisplay in den Systemeinstellungen aktivieren.

Verbindung prüfen: `http://HEIZUNGS-IP:8080/user/menu` muss ETA-XML liefern. Keine meinETA-Zugangsdaten in der Integration erforderlich.

## Integration installieren

1. Repository als ZIP herunterladen und entpacken.
2. Den Ordner `custom_components/eta_readonly` vollständig nach **`/config/custom_components/eta_readonly`** kopieren. `manifest.json` muss unmittelbar in diesem Zielordner liegen.
3. Home Assistant vollständig neu starten.
4. **Einstellungen → Geräte & Dienste → Integration hinzufügen → ETA Heizung (Lesend)**.
5. IP-Adresse oder Hostname ohne `http://`, Port **8080**, Intervall zunächst **60 Sekunden** eingeben.
6. Den automatischen Scan abwarten: Menübaum laden, jede gefundene Adresse lesen und alle erfolgreich geprüften Werte vorauswählen. Im Ergebnis die Zahl der gefundenen und übersprungenen Einträge prüfen. Einfach bestätigen oder die Auswahl reduzieren.
7. Sensoren beim Gerät **ETA Heizung** prüfen. Nicht lesbare Menügruppen bleiben nicht verfügbar.

Kein Eintrag in `configuration.yaml` nötig. Eine Installation als HACS-Repository ist derzeit nicht eingerichtet.

## Dashboard installieren

1. `dashboard/eta-logo.png` nach **`/config/www/eta-logo.png`** kopieren. Wenn `www` neu angelegt wurde, Home Assistant neu starten.
2. Den Inhalt von `dashboard/dashboard-erzeugen.jinja` in **Entwicklerwerkzeuge → Template** einfügen.
3. Die **gerenderte Ausgabe**, beginnend mit `title: ETA Heizung`, kopieren.
4. Unter **Einstellungen → Dashboards** ein neues leeres Dashboard anlegen und öffnen.
5. **Bearbeiten → Rohkonfigurationseditor** öffnen, gegebenenfalls zuerst Kontrolle übernehmen, und die gerenderte Ausgabe einfügen. Nur die Konfiguration des neuen Dashboards ersetzen.
6. Speichern. In der Bildentitätskarte kann anschließend der gewünschte Sensor ausgewählt werden. Das Logo wird ohne Beschnitt angezeigt.

Die Vorlage selbst gehört nicht in den Rohkonfigurationseditor. Bei weiteren Sensoren die Vorlage erneut ausführen oder Karten manuell ergänzen. Der 24-Stunden-Verlauf baut sich erst mit der Aufzeichnung durch den Recorder auf.

[Ausführliche Dashboard-Anleitung einschließlich Bildrechten](dashboard/ANLEITUNG.md).

## Updates und Grenzen

Vor Updates den vorhandenen Integrationsordner sichern, Dateien ersetzen und Home Assistant neu starten. Eine Änderung von Host, Port, Intervall oder Datenpunktauswahl erfordert derzeit Entfernen und erneutes Einrichten der Integration; dabei können sich Entitäts-IDs ändern. Dashboard anschließend prüfen.

Keine Steuerung, keine Schalter, kein Schreiben von Heizungsparametern. Keine Abfrage aktiver Störungsmeldungen über `/user/errors`. Pro Datenpunkt eine GET-Anfrage, mit höchstens zwei gleichzeitigen Abfragen. Bei langen Durchläufen wird das effektive Intervall auf mindestens das 1,5-Fache der letzten Durchlaufdauer angehoben (auf volle Sekunden aufgerundet), bleibt aber mindestens beim konfigurierten Intervall. Einzelne Ausfälle machen den jeweiligen Sensor nicht verfügbar. Es wird keine Rücksetzlogik für Energie-/Betriebsstundenzähler angenommen.

## Verifizierter Stand

15 lokale Tests für Parser, Erkennung, Auswahlpersistenz, mehr als 50 Werte, begrenzte Parallelität und Abbruchverhalten sowie Python-Syntax und JSON-Dateien geprüft. Die Flow-Tests verwenden kleine Home-Assistant-Ersatzobjekte; sie sind keine vollständigen HA-Integrationstests. Auf diesem eingeschränkten Windows-Host liefen die reinen Coroutine-Tests über eine In-Memory-Ereignisschleife ohne Netzwerk-I/O. Die Integration wurde noch **nicht in einer laufenden Home-Assistant-Instanz oder an der realen Heizung getestet**. Die Dashboard-Vorlage wurde strukturell geprüft; ihre Ausführung in Home Assistant steht ebenfalls aus. Keine Behauptung einer umfassenden Kompatibilitätsprüfung.

Tests ohne Home Assistant oder Zusatzpakete ausführen:

```sh
python -m unittest discover -s tests -v
python -m compileall -q custom_components
```

GitHub Actions führt Parser- und Syntaxprüfungen aus, sobald das Repository hochgeladen ist.

## Logo, Rechte und Weitergabe

Das Logo wurde vom Nutzer bereitgestellt und unverändert übernommen. Für dieses Logo liegt hier kein Nachweis einer Nutzungserlaubnis vor. Es ist ausdrücklich von der GPL-3.0-Lizenz dieses Projekts ausgenommen. Der Hinweis im Dashboard ersetzt keine erforderliche Berechtigung. Vor öffentlicher Weitergabe die Rechte klären; ohne Berechtigung die Logo-Datei und ihre Verweise entfernen oder durch ein eigenes Bild ersetzen. Einzelheiten und Herstellerquelle stehen in der Dashboard-Anleitung. Keine weiteren fremden Bilder werden nachgeladen.

[Technische Details und Quellen](docs/TECHNIK.md).

## Eigenes GitHub-Repository

[Anleitung zum manuellen Upload](docs/GITHUB.md). Der Inhalt dieser ZIP gehört direkt in den Repository-Stamm.

## Unterstützung / Sponsor

Wenn dir dieses Projekt hilft, kannst du die Weiterentwicklung freiwillig unterstützen:

[![PayPal](https://img.shields.io/badge/PayPal-Spenden-00457C?logo=paypal&logoColor=white)](https://www.paypal.me/domh7C4)

## Lizenz

Der eigene Projektcode, die eigenen Dashboard-Vorlagen, Dokumentation und die eigens erstellte schematische Zeichnung stehen unter der **GNU General Public License Version 3, ausschließlich diese Version (`GPL-3.0-only`)**. Der vollständige Lizenztext liegt in [LICENSE](LICENSE).

Das Projekt wird ohne Gewährleistung bereitgestellt; die vollständigen Bedingungen ergeben sich aus der Lizenz. Fremde Marken, Logos und andere fremde Materialien werden nicht unter diese Lizenz gestellt. Das betrifft insbesondere `dashboard/eta-logo.png`. Einzelheiten stehen in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
