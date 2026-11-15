# Heizungsdashboard mit Bildentität

Das Dashboard verwendet ausschließlich Home-Assistant-Standardkarten. Es benötigt weder HACS noch zusätzliche Karten. Es zeigt eine Bildentitätskarte mit aktuellem Sensorwert, sämtliche ausgewählten ETA-Sensoren und einen 24-Stunden-Verlauf der Temperatursensoren.

## 1. Bild ablegen

Das bereitgestellte Logo `eta-logo.png` nach `/config/www/eta-logo.png` auf Home Assistant kopieren. Den Ordner `www` bei Bedarf anlegen; falls er neu angelegt wurde, Home Assistant neu starten. Das Bild muss anschließend unter `http://DEIN-HOME-ASSISTANT:8123/local/eta-logo.png` erreichbar sein (bei HTTPS dessen Adresse verwenden).

Die Bildentitätskarte zeigt das ETA-Logo anstelle der Heizungszeichnung. Der aktuelle Sensorwert erscheint in der eingeblendeten Leiste. Das Logo wird ohne Beschnitt angezeigt. Die frühere schematische Zeichnung liegt optional weiterhin im Paket.

## 2. Konfiguration passend zu deinen Sensoren erzeugen

Zuerst die Integration „ETA Heizung (Lesend)“ einrichten, den automatischen Scan abwarten und die vorausgewählten Datenpunkte bestätigen.

1. `dashboard-erzeugen.jinja` als Text öffnen und den vollständigen Inhalt kopieren.
2. In Home Assistant **Entwicklerwerkzeuge → Template** öffnen und dort einfügen.
3. Die gerenderte Ausgabe rechts kopieren, beginnend mit `title: ETA Heizung`. Den Jinja-Quelltext nicht direkt in ein Dashboard einfügen.

Die Vorlage ermittelt die tatsächlichen Entitäts-IDs über `integration_entities('eta_readonly')`. Bei mehreren Heizungen kannst du dort stattdessen den genauen Titel der gewünschten Integration eintragen. Als Bildentität wird der erste Temperatursensor verwendet, ersatzweise der erste Sensor. Nachträglich lässt sich die gewünschte Entität im Karteneditor wählen.

## 3. Dashboard anlegen

1. **Einstellungen → Dashboards → Dashboard hinzufügen**: ein neues, leeres Dashboard erstellen, z. B. „ETA Heizung“. Falls eine Auswahl erscheint, ein selbst verwaltetes Dashboard wählen.
2. Dieses Dashboard öffnen, **Bearbeiten → Drei-Punkte-Menü → Rohkonfigurationseditor** öffnen. Falls angeboten, zuerst die Kontrolle über das Dashboard übernehmen.
3. Die Konfiguration des neuen Dashboards durch die gerenderte Ausgabe aus Schritt 2 ersetzen und speichern.

Nur in ein neues Dashboard einfügen: Das Ersetzen würde die bisherigen Karten eines bestehenden Dashboards überschreiben. Falls deine Version andere Menübezeichnungen verwendet, den YAML-/Rohkonfigurationseditor des Dashboards verwenden.

## Anpassen

- Bildentitätskarte bearbeiten → **Entität**: gewünschten Sensor festlegen, etwa Kesseltemperatur oder Betriebszustand. Der Wert und sein tatsächlicher Sensorname werden unten im Bild eingeblendet. Antippen öffnet Details und Verlauf.
- Eigenes Foto: Foto nach `/config/www/heizung.jpg` kopieren und in der Karte `image: /local/heizung.jpg` setzen.
- Weitere Sensoren: zuerst in der Integration bereitstellen, anschließend die Vorlage erneut ausführen oder Karten manuell ergänzen. Die Entitätsliste wird einmalig beim Erzeugen zusammengestellt.
- Der Temperaturverlauf benötigt aufgezeichnete Daten des Home-Assistant-Recorders. Bei neuen Sensoren baut er sich erst nach und nach auf. Nicht verfügbare Werte weisen auf Verbindungsprobleme oder nicht lesbare Datenpunkte hin.
- Eine zusätzliche `image.*`-Entität ist für diese Bildentitätskarte nicht erforderlich.

## Prüfung und Quellen

SVG-Datei und Vorlagenstruktur wurden lokal geprüft. Ein Ausführen der Jinja-Vorlage und ein Test in deiner laufenden Home-Assistant-Instanz stehen noch aus.

- https://www.home-assistant.io/dashboards/picture-entity/
- https://www.home-assistant.io/template-functions/integration_entities/

## Logo und Bildrechte

Das von dir bereitgestellte ETA-Logo wird unverändert als lokale Datei eingebunden. Es wird nicht von der ETA-Website nachgeladen. Der kurze Hinweis im Dashboard kennzeichnet die Integration als unabhängig und inoffiziell.

Das Bereitstellen des Bildes belegt keine Nutzungserlaubnis. Ein Quellen- oder Markenhinweis ersetzt eine gegebenenfalls erforderliche Erlaubnis nicht. ETA erklärt im [Impressum](https://www.eta.co.at/impressum/), dass die Nutzung von Dateien seiner Website eine ausdrückliche Zustimmung erfordert; genannt werden auch Logos und Bilder. Eine Freigabe für dieses Logo wurde nicht geprüft. Vor Veröffentlichung oder Weitergabe des Pakets mit Logo die erforderlichen Rechte klären. Ohne passende Berechtigung das Logo entfernen: die Bildzeile im Markdown-Kopf löschen und `eta-logo.png` nicht verwenden.

Die schematische Heizungszeichnung wurde für dieses Dashboard erstellt. Weitere externe Bilder sind nicht enthalten. Wenn du später ein fremdes Foto verwendest, dessen konkrete Lizenzbedingungen prüfen und erforderliche Bildnachweise ergänzen. Das Dashboard selbst lädt die mitgelieferten Bilder ausschließlich vom eigenen Home-Assistant-Server.

Quelle für die Herstellerangabe: https://www.eta.co.at/impressum/ (abgerufen am 25.10.2026).
