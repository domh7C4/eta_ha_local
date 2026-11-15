# ETA-Heizung steuern – Version 1.0.1

## Freigabe

Nach dem Update auf 1.2.0: Einstellungen → Geräte & Dienste → ETA Heizung Lokal → Konfigurieren → Schreibzugriff freigeben. Die Integration wird neu geladen. Zum Deaktivieren denselben Schalter ausschalten. Vorhandene Sensoren behalten ihre internen IDs; die Integration heißt intern weiterhin `eta_readonly`.

Freigabe allein schreibt keinen Heizungswert. Sie aktiviert zusätzliche Auswahlentitäten und die Möglichkeit, mit `eta_readonly.set_value` explizite Aufträge auszuführen.

## Automatische Auswahlfelder

Für ausgewählte Datenpunkte, deren aktuelle ETA-Metadaten `isWritable="1"`, Typ `TEXT` und eine Liste eindeutiger Zustandsbezeichnungen enthalten, erscheinen Auswahlfelder. Dazu können Kessel Ein/Aus und Heizkreis-Betriebsarten gehören; die tatsächliche Anlage entscheidet. Es werden keine Schalteradressen oder Zahlenwerte für Zustände geraten.

Die Auswahlfelder können als normale Entitäten in einem Dashboard bedient werden. Nach geänderten Metadaten die Integration neu laden. Nicht eindeutig benannte Auswahllisten bekommen kein automatisch geratenes Bedienelement; sie bleiben per Rohwert-Aktion bedienbar, soweit von der API erlaubt.

## Zahlen / Sollwerte

Beispiel – nur mit dem tatsächlich passenden, schreibbaren Sensor verwenden:

```yaml
action: eta_readonly.set_value
target:
  entity_id: sensor.DEIN_TATSAECHLICHER_ETA_SOLLWERT
data:
  value: "40.5"
```

Die Beispiele enthalten absichtlich keine erfundenen echten Entitäts-IDs. Im Aktionseditor einen eigenen ETA-Sensor auswählen. Bei `scaleFactor=10` wird aus `40.5` der CAN-Rohwert `405`. Es wird nicht gerundet. Herstellerspezifische Minima/Maxima werden nicht geraten; die API muss den Auftrag annehmen. Bei Textvariablen stattdessen die exakt gemeldete Auswahlbezeichnung als `value` verwenden.

## Rohwerte

Für technische Bedienung ist `raw: true` möglich. Dann erwartet `value` einen ganzzahligen CAN-Rohwert ohne Skalierung. Bei Auswahlwerten wird auch ein Rohwert gegen die vom Gerät gemeldete Liste geprüft. Ein beliebiger Label-Text wird nicht als RAW-Zahl interpretiert.

```yaml
action: eta_readonly.set_value
target:
  entity_id: sensor.DEIN_TATSAECHLICHER_ETA_DATENPUNKT
data:
  value: "405"
  raw: true
```

## Zeitfenster

Die ETA-API unterstützt Zeitfenster mit den zusätzlichen Parametern `begin` und `end`: ganze Viertelstunden seit Mitternacht, also 0 = 00:00, 48 = 12:00, 96 = 24:00. Beide müssen gemeinsam angegeben werden, mit `begin <= end`. Das Beispiel gilt nur für eine tatsächlich schreibbare Zeitfenster-Variable; es ist keine generische Heizkreisadresse.

```yaml
action: eta_readonly.set_value
target:
  entity_id: sensor.DEIN_TATSAECHLICHER_ETA_ZEITFENSTER_DATENPUNKT
data:
  value: "40"
  begin: 0
  end: 48
```

Bei einer Temperaturvariablen mit Faktor 10 wird hier `value=400&begin=0&end=48` übertragen. Die Bedeutung des Werts und die Zuordnung von Tag/Zeitfenster muss zur gewählten Variable passen. Die Version enthält keinen grafischen Wochenplan-Editor.

## Technischer Ablauf

- Nur tatsächlich ausgewählte, bekannte Sensoradressen können beschrieben werden.
- Vor jedem Schreiben: aktuelles GET auf `/user/varinfo/{Adresse}`. URI und `isWritable` werden geprüft.
- Dann genau ein POST auf `/user/var/{Adresse}` mit Formularparametern, ohne Redirects und ohne automatische Wiederholung.
- Nur eine passende `<success uri="/user/var/..."/>`-Antwort gilt als Bestätigung.
- Anschließend werden die Sensoren erneut abgefragt. Der Hersteller kann Werte begrenzen oder später durch seine Regelung wieder verändern.
- Bei Timeout nach dem POST ist der tatsächliche Zustand unklar. Ein Auftrag wird nicht als sicher fehlgeschlagen ausgegeben und blind wiederholt.

Die Metadata-Abfrage benötigt API 1.2. Ohne bestätigte Metadaten wird auch im RAW-Modus nicht geschrieben. Nicht im Menü sichtbare oder außerhalb der REST-API liegende Servicefunktionen sind nicht freigeschaltet.

## Teststatus

Schreibaufträge wurden nur gegen In-Memory-Ersatzantworten und Testobjekte geprüft. Es wurde kein Auftrag an eine reale Heizung gesendet. Ein vollständiger Home-Assistant-Laufzeittest steht aus.

## Dashboard-Karte

Die Custom Card `custom:eta-heating-card` zeigt freigegebene Auswahlentitäten automatisch an. Die Karte wird in einem vorhandenen Dashboard platziert und erzeugt keine eigene Seitenleistenansicht. Beim Laden der Karte werden keine Schreibaufträge gesendet.
