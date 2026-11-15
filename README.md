# ETA Heizung für Home Assistant

![ETA-Logo](dashboard/eta-logo.png)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
![Version](https://img.shields.io/badge/Version-1.0.1-blue)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Custom%20Integration-41BDF5)
[![Sponsor via PayPal](https://img.shields.io/badge/PayPal-Projekt%20unterst%C3%BCtzen-00457C?logo=paypal&logoColor=white)](https://www.paypal.me/domh7C4)

**Repository:** [domh7C4/eta_ha_local](https://github.com/domh7C4/eta_ha_local)

Unabhängige, inoffizielle Custom Integration für die lokale ETAtouch REST-API. Standardmäßig lesend, optional mit freischaltbarem API-Schreibzugriff. Projektstand: **15. November 2026**, Version **1.0.1**.

## Aktueller Funktionsumfang

- Einrichtung in der Home-Assistant-Oberfläche mit Host, Port und Abfrageintervall.
- Automatische Erkennung aller im Menübaum enthaltenen und beim Scan erfolgreich lesbaren Datenpunkte. Keine feste 50-Werte-Grenze; alle gefundenen Werte sind vorausgewählt.
- Sensoren für Temperaturen, Druck, Leistung, Zähler und Textzustände; verfügbare Werte hängen von der konkreten Anlage ab.
- Abfrage standardmäßig alle 60 Sekunden, einstellbar zwischen 30 und 3600 Sekunden.
- Dashboard mit **ETA-Logo als Bildentitätskarte anstelle der Heizungszeichnung**, darunter aktueller Sensorwert, Sensorliste und Temperaturverlauf.
- Eigene Dashboard-Karte **ETA Heizung Lokal**, wie eine Flow Card im vorhandenen Dashboard platzierbar. Automatische Erkennung der ETA-Entitäten innerhalb der Karte; keine zusätzliche Seite und kein Seitenleisteneintrag.
- Optionaler API-Schreibzugriff: automatische Auswahlelemente und eine Aktion für Werte/Zeitfenster.
- Lokale Logo-Dateien im `brand`-Ordner für die Integrationsdarstellung.
- Die Demo aus dem Chat verwendet simulierte Werte; die Integration verwendet echte Werte nach Verbindung mit der Heizung.

## Automatische Erkennung beim ersten Einrichten

Die Integration lädt `/user/menu` von der angegebenen Heizung, übernimmt die tatsächlichen Adressen und Namen aus dem XML-Menü und prüft jeden Kandidaten mit `GET /user/var/{Adresse}`. Auch lesbare Einträge mit Unterobjekten werden geprüft. Es gibt keine feste Liste von Kesselmodellen oder vorgegebenen Sensoradressen. Die Heizung selbst muss weiterhin per IP-Adresse oder Hostname angegeben werden; dies ist keine Netzwerksuche nach Heizungen.

Während der Suche zeigt Home Assistant den Fortschritt. Alle erfolgreich gelesenen Werte sind anschließend vorausgewählt. Du musst keine Adressen oder Sensoren einzeln heraussuchen. Nicht lesbare Einträge (z. B. Menügruppen) und Verbindungsfehler werden übersprungen und im Ergebnis gezählt. Ein vorübergehend ausgefallener Wert lässt sich dabei nicht sicher von einem dauerhaft nicht lesbaren unterscheiden: bei unerwartet wenigen Funden mit stabiler Verbindung erneut einrichten.

Die bestätigte Auswahl wird lokal im Home-Assistant-Konfigurationseintrag gespeichert und nach einem Neustart wiederverwendet. Bereits eingerichtete Anlagen behalten ihre bisherigen Datenpunkte; zum vollständigen Erstscan mit dieser Version die alte Integration entfernen und neu hinzufügen. Dabei können sich Entitäts-IDs ändern, anschließend das Dashboard aktualisieren. Neu hinzugefügte Anlagenkomponenten werden nicht während jedes Polling-Durchlaufs erneut gesucht.

Der Scan verwendet ausschließlich GET. Schreibzugriff erfolgt nur nach ausdrücklicher Freigabe. Dann wird `/user/varinfo/{Adresse}` für Berechtigungen und Auswahlwerte verwendet und auf ausdrücklichen Bedienauftrag per POST geschrieben. `/user/errors` wird weiterhin nicht abgefragt. Es werden keine Variablensätze angelegt.

## Voraussetzungen

Home Assistant mit Zugriff auf sein Konfigurationsverzeichnis und Netzwerkzugriff auf die Heizung. Für Version 1.0.1 ist Home Assistant ab **2026.11.0** als technische Mindestversion hinterlegt. Ein vollständiger Laufzeittest in dieser Version steht noch aus. Schreibzugriff benötigt ETA-API **1.2** mit `/user/varinfo` (laut ETA-Handbuch ab Systemsoftware x.49.0). Ohne passende Metadaten bleibt der betreffende Datenpunkt nicht steuerbar; lesende Sensoren funktionieren weiterhin.

Laut bereitgestelltem ETA-Handbuch: ETAtouch-Systemsoftware ab 1.20.0; Gerät auf meineta.at registrieren, LAN-Zugriff dort beantragen und anschließend am Touchdisplay in den Systemeinstellungen aktivieren.

Verbindung prüfen: `http://HEIZUNGS-IP:8080/user/menu` muss ETA-XML liefern. Keine meinETA-Zugangsdaten in der Integration erforderlich.

## Integration installieren

### Über den Home-Assistant-Marketplace

1. **Einstellungen → Marketplace** öffnen.
2. Oben rechts **Über Link hinzufügen / Add from link** wählen.
3. `https://github.com/domh7C4/eta_ha_local` eintragen und hinzufügen. Falls nach dem Typ gefragt wird, **Integration** wählen.
4. **ETA Heizung Lokal** öffnen und installieren. Falls eine GitHub-Verbindung angefordert wird, diese zuerst einrichten.
5. Anschließend Home Assistant neu starten und mit **Einrichtung** unten fortfahren.

Das Repository muss öffentlich erreichbar sein. Die erforderliche `hacs.json` liegt im Repository-Stamm. Die Aufnahme in den allgemeinen Katalog wird damit nicht behauptet; das Repository wird über seinen Link hinzugefügt.

### Über HACS, sofern in deiner Home-Assistant-Version vorhanden

1. **HACS → Drei-Punkte-Menü → Benutzerdefinierte Repositories** öffnen.
2. `https://github.com/domh7C4/eta_ha_local` eintragen, Kategorie **Integration** wählen und hinzufügen.
3. **ETA Heizung Lokal** herunterladen.
4. Home Assistant vollständig neu starten und mit **Einrichtung** fortfahren.

### Manuelle Installation

1. Repository als ZIP herunterladen und entpacken.
2. Den Ordner `custom_components/eta_readonly` vollständig nach **`/config/custom_components/eta_readonly`** kopieren. `manifest.json` muss unmittelbar in diesem Zielordner liegen.
3. Home Assistant vollständig neu starten.

### Einrichtung

1. **Einstellungen → Geräte & Dienste → Integration hinzufügen → ETA Heizung Lokal** öffnen.
2. IP-Adresse oder Hostname ohne `http://`, Port **8080**, Intervall zunächst **60 Sekunden** eingeben.
3. Den automatischen Scan abwarten: Menübaum laden, jede gefundene Adresse lesen und alle erfolgreich geprüften Werte vorauswählen. Im Ergebnis die Zahl der gefundenen und übersprungenen Einträge prüfen. Einfach bestätigen oder die Auswahl reduzieren.
4. Sensoren beim Gerät **ETA Heizung** prüfen. Übersprungene Menügruppen werden nicht als Sensoren angelegt; später ausfallende Werte werden als nicht verfügbar angezeigt.

Kein Eintrag in `configuration.yaml` nötig. Karten-JavaScript und Logo liegen vollständig in `custom_components/eta_readonly` und werden von Marketplace/HACS mit installiert. Bei normalen Storage-Ressourcen registriert die Integration die JavaScript-Ressource automatisch. Die Platzierung der Karte im gewünschten Dashboard erfolgt durch dich.

## Heizungssteuerung / API-Schreibzugriff

1. **Einstellungen → Geräte & Dienste → ETA Heizung Lokal → Konfigurieren** öffnen.
2. **Schreibzugriff freigeben** aktivieren und speichern. Bei neuen Installationen ist die Freigabe auch im ersten Einrichtungsformular möglich; Standard bleibt aus.
3. Nach dem Neuladen werden die Metadaten der ausgewählten Werte abgefragt. Für schreibbare `TEXT`-Werte mit eindeutiger Auswahlliste erscheinen automatisch `select`-Entitäten, zum Beispiel für Ein/Aus oder Betriebsarten, sofern die Anlage sie bereitstellt.
4. Andere schreibbare Werte über **Entwicklerwerkzeuge → Aktionen → `eta_readonly.set_value`** setzen. Als Ziel den zugehörigen ETA-Sensor auswählen. Zahlen werden standardmäßig in dessen Anzeigeeinheit eingegeben; gültige Textzustände exakt wie vom Gerät gemeldet.

Vor jedem Auftrag prüft die Integration die aktuelle Schreibberechtigung erneut. Ohne Freigabe, bei fehlenden Metadaten oder bei `isWritable=0` wird kein Schreibauftrag gesendet. Die ETA-API muss den konkreten Auftrag bestätigen; bei unklarer Antwort/Timeout wird er nicht automatisch wiederholt. Die Heizung kann ihn trotzdem bereits ausgeführt haben; dann zuerst den tatsächlichen Zustand prüfen.

„Vollzugriff“ bedeutet hier Zugriff auf die über die ETA-Webservices freigegebenen Variablen. Er umfasst keinen Zugriff außerhalb der API, keine Freischaltung gesperrter Servicefunktionen, keinen Firmwarezugriff und keine vollständige Nachbildung des Touchdisplays. Nicht jede Anlage meldet jede Funktion als schreibbar. Numerische Eingabefelder/Slider werden ohne verlässlich bekannte Grenzen nicht erfunden; solche Werte sind über die beschriebene Aktion bedienbar. Das Gerät entscheidet über herstellerspezifische Wertebereiche.

[Bedienung, Rohwerte und Zeitfenster mit Beispielen](docs/STEUERUNG.md).

## Logo im Marketplace und in der Integration

`custom_components/eta_readonly/brand/icon.png` enthält eine quadratische Thumbnail-Variante des bereitgestellten ETA-Logos, `brand/logo.png` das unveränderte Original. Die quadratische Variante wurde mit ImageGen aus dem Original für diesen Zweck aufbereitet; sie ist keine vom Hersteller gelieferte neue Bilddatei. Beide Dateien sind vom GPL-Lizenzumfang ausgenommen.

Home Assistant kann die lokalen Brand-Bilder nach Installation nutzen. Für die Marketplace-Vorschau vor der Installation können Katalog-/Brand-Abgleich und Cache maßgeblich sein; ein lokales ZIP allein ändert die bereits angezeigte Kachel nicht. Die Dateien müssen im veröffentlichten Repository und verwendeten Release **v1.0.1** enthalten sein. Für alte HACS-Versionen wird durch lokale Brand-Dateien keine automatische Vorab-Anzeige zugesichert.

[Hintergrund zur Logo-Anzeige und den Bilddateien](docs/BRANDING.md).

## ETA-Karte zum Dashboard hinzufügen – wie eine Flow Card

1. Integration installieren/aktualisieren und Home Assistant vollständig neu starten.
2. Die Heizung unter **ETA Heizung Lokal** einrichten und den Scan bestätigen, falls noch nicht erfolgt.
3. Browser vollständig neu laden, damit die neue Kartenressource geladen wird.
4. Dein gewünschtes Dashboard öffnen → **Bearbeiten → Karte hinzufügen** → **ETA Heizung Lokal** suchen.
5. Karte hinzufügen und speichern. Logo, erkannte Sensoren, Temperaturverlauf und freigegebene Auswahlfelder erscheinen innerhalb dieser Karte.

**Es wird keine Dashboard-Seite angelegt und kein Eintrag in der Seitenleiste erzeugt.** Das Verhalten entspricht einer normalen Custom Card: Die Integration liefert die Karte und das Bild mit, du platzierst sie im bestehenden Dashboard.

Die Karte besitzt einen Konfigurationseditor für Titel, optionalen Bild-Sensor sowie das Ein-/Ausblenden von Verlauf und Steuerung. Ohne Anlagenfilter zeigt sie alle ETA-Entitäten dieser Integration. Bei mehreren Anlagen kann `config_entry_id` gesetzt werden; die passende ID steht im Sensorattribut `eta_config_entry_id`.

Alternativ eine **manuelle Karte** mit folgender Konfiguration hinzufügen (kein komplettes Dashboard-YAML):

```yaml
type: custom:eta-heating-card
title: ETA Heizung
show_history: true
show_controls: true
```

Optional:

```yaml
type: custom:eta-heating-card
title: Heizraum
config_entry_id: DEINE_ETA_ANLAGEN_ID
picture_entity: sensor.DEIN_ETA_SENSOR
show_history: true
show_controls: true
```

Die Platzhalter durch eigene Werte ersetzen oder die optionalen Zeilen weglassen. Das Logo wird von `/eta_readonly/eta-logo.png` geladen; kein Kopieren nach `www` und keine Jinja-Ausführung erforderlich.

### Falls die Karte nicht in der Auswahl erscheint

Die Integration muss eingerichtet/geladen sein. Nach dem Neustart den Browser-Cache durch vollständiges Neuladen aktualisieren. Unter den Dashboard-Ressourcen muss folgende JavaScript-Modulressource vorhanden sein:

```text
/eta_readonly/eta-heating-card.js?v=1.0.1
```

Typ: **JavaScript-Modul / module**. Bei Storage-Ressourcen wird dieser Eintrag automatisch erstellt bzw. aktualisiert. Werden Ressourcen ausdrücklich in YAML verwaltet, diesen Eintrag selbst ergänzen:

```yaml
lovelace:
  resources:
    - url: /eta_readonly/eta-heating-card.js?v=1.0.1
      type: module
```

In einen vorhandenen `lovelace`-/`resources`-Abschnitt integrieren, keine doppelten Hauptschlüssel anlegen.

### Umstieg von Version 1.3.0

Nach Update auf 1.0.1 und Neustart wird die frühere integrationseigene Seitenleistenansicht nicht mehr registriert. Die frühere Option `create_dashboard` wird nicht mehr angeboten und alte gespeicherte Werte dafür werden ignoriert. Danach die Karte im gewünschten Dashboard hinzufügen. Eigene, manuell angelegte Dashboards werden nicht verändert.

Die Karte ergänzt neue ETA-Entitäten automatisch, sobald sie von der Integration bereitgestellt werden; die Integration selbst führt nach wie vor keinen ständigen neuen Menüscan durch. Der Temperaturverlauf benötigt Recorder-Daten. Ein grafischer Wochenplan-Editor ist nicht enthalten. Zahlen-/Zeitfenster-Schreibaufträge bleiben über `eta_readonly.set_value` verfügbar.

[Weitere Hinweise und optionale ältere manuelle Vorlage](dashboard/ANLEITUNG.md).

## Updates und Grenzen

Vor Updates ein Backup erstellen. Bei Installation über Marketplace/HACS dort das Update ausführen; bei manueller Installation die Dateien im vorhandenen Integrationsordner ersetzen. Anschließend Home Assistant neu starten. Ein reines Update auf 1.0.1 erfordert keine erneute Einrichtung und keinen neuen Scan. Die bisherige interne Domain `eta_readonly` bleibt für bestehende Geräte und Sensor-IDs erhalten. Schreibzugriff kann über **Konfigurieren** nachträglich freigeschaltet werden; dabei wird die Integration neu geladen. Eine Änderung von Host, Port, Intervall oder Datenpunktauswahl erfordert derzeit Entfernen und erneutes Einrichten der Integration; dabei können sich Entitäts-IDs ändern. Dashboard anschließend prüfen.

API-Schreibzugriff ist optional und auf ausgewählte Datenpunkte mit aktueller Schreibfreigabe durch die ETA-API beschränkt. Keine Abfrage aktiver Störungsmeldungen über `/user/errors`. Pro Datenpunkt eine GET-Anfrage, mit höchstens zwei gleichzeitigen Abfragen. Bei langen Durchläufen wird das effektive Intervall auf mindestens das 1,5-Fache der letzten Durchlaufdauer angehoben (auf volle Sekunden aufgerundet), bleibt aber mindestens beim konfigurierten Intervall. Einzelne Ausfälle machen den jeweiligen Sensor nicht verfügbar. Es wird keine Rücksetzlogik für Energie-/Betriebsstundenzähler angenommen.

## Verifizierter Stand

34 Python-Tests für Parser, Erkennung, Schreibzugriff, HTTP-Bestätigungen und die Kartenressourcen sowie sechs JavaScript-Prüfungen für Kartenaufbau, Entitätsfilterung, Einstellungen, leere Zustände, Aktualisierung und Kartenauswahl bestanden. Python-Syntax und JSON-Dateien wurden ebenfalls geprüft. Die Laufzeittests verwenden kleine Home-Assistant-/DOM-Ersatzobjekte; sie sind keine vollständigen HA-Integrationstests. Auf diesem eingeschränkten Windows-Host liefen die reinen Coroutine-Tests über eine In-Memory-Ereignisschleife ohne Netzwerk-I/O. Die Integration wurde noch **nicht in einer laufenden Home-Assistant-Instanz oder an der realen Heizung getestet**. Die Dashboard-Vorlage wurde strukturell geprüft; ihre Ausführung in Home Assistant steht ebenfalls aus. Keine Behauptung einer umfassenden Kompatibilitätsprüfung.

Tests ohne Home Assistant oder Zusatzpakete ausführen:

```sh
python -m unittest discover -s tests -v
python -m compileall -q custom_components
node tests/test_card.cjs
```

GitHub Actions führt Parser- und Syntaxprüfungen aus, sobald das Repository hochgeladen ist.

## Logo, Rechte und Weitergabe

Das Logo wurde vom Nutzer bereitgestellt und unverändert übernommen. Für dieses Logo liegt hier kein Nachweis einer Nutzungserlaubnis vor. Es ist ausdrücklich von der GPL-3.0-Lizenz dieses Projekts ausgenommen. Der Hinweis im Dashboard ersetzt keine erforderliche Berechtigung. Vor öffentlicher Weitergabe die Rechte klären; ohne Berechtigung die Logo-Datei und ihre Verweise entfernen oder durch ein eigenes Bild ersetzen. Einzelheiten und Herstellerquelle stehen in der Dashboard-Anleitung. Keine weiteren fremden Bilder werden nachgeladen.

[Technische Details und Quellen](docs/TECHNIK.md).

## Repository-Struktur und Veröffentlichung

```text
eta_ha_local/
├── hacs.json
├── README.md
├── LICENSE
├── THIRD_PARTY_NOTICES.md
├── custom_components/
│   └── eta_readonly/
│       ├── manifest.json
│       ├── __init__.py
│       ├── api.py
│       ├── config_flow.py
│       ├── frontend.py
│       ├── www/eta-heating-card.js
│       ├── scan.py
│       ├── sensor.py
│       └── ...
├── dashboard/
├── docs/
├── tests/
└── .github/
```

Beim GitHub-Upload den **Inhalt** der entpackten ZIP direkt in den Repository-Stamm hochladen, keinen zusätzlichen äußeren Ordner. `hacs.json` muss neben `README.md` liegen, nicht unter `custom_components`.

Für diese Korrektur einen neuen Release **`v1.0.1`** aus dem aktualisierten Commit erstellen. Auch die installierte bzw. gewählte Release-Version muss `hacs.json` enthalten. Eine alte Version ohne diese Datei wird durch einen Upload nur auf den Hauptbranch nicht nachträglich repariert. Es ist kein separater ZIP-Release-Download konfiguriert; der Installer liest die Dateien aus dem gewählten Git-Stand.

[Anleitung zum manuellen Upload](docs/GITHUB.md).

## Unterstützung / Sponsor

Wenn dir dieses Projekt hilft, kannst du die Weiterentwicklung freiwillig unterstützen:

[![PayPal](https://img.shields.io/badge/PayPal-Spenden-00457C?logo=paypal&logoColor=white)](https://www.paypal.me/domh7C4)

## Lizenz

Der eigene Projektcode, die eigenen Dashboard-Vorlagen, Dokumentation und die eigens erstellte schematische Zeichnung stehen unter der **GNU General Public License Version 3, ausschließlich diese Version (`GPL-3.0-only`)**. Der vollständige Lizenztext liegt in [LICENSE](LICENSE).

Das Projekt wird ohne Gewährleistung bereitgestellt; die vollständigen Bedingungen ergeben sich aus der Lizenz. Fremde Marken, Logos und andere fremde Materialien werden nicht unter diese Lizenz gestellt. Das betrifft insbesondere `dashboard/eta-logo.png`. Einzelheiten stehen in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
## Fehlerbehebung: „Keine hacs.json im Stammverzeichnis“

- Prüfen, ob `hacs.json` direkt unter `https://github.com/domh7C4/eta_ha_local/blob/main/hacs.json` liegt. Bei einem anderen Standardbranch dessen Namen verwenden.
- Die Datei muss als Datei hochgeladen sein, nicht nur innerhalb eines ZIP-Anhangs oder in einem Unterordner.
- Wenn ein älterer Release ausgewählt ist, eine korrigierte Version wie `v1.0.1` wählen bzw. neu veröffentlichen.
- Anschließend das Repository im Marketplace/HACS aktualisieren und die Installation erneut versuchen.

## Dokumentation zu Marketplace/HACS

- [Marketplace: benutzerdefinierte Repositories](https://www.home-assistant.io/integrations/marketplace/#custom-repositories)
- [hacs.json: Aufbau und Felder](https://contributors.home-assistant.io/marketplace/reference/hacs-json/)
- [Repository-Struktur für Integrationen](https://contributors.home-assistant.io/marketplace/reference/repository-structure/)
