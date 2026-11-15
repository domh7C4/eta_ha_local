# Logo / Marketplace-Thumbnail

## Enthaltene Dateien

- `custom_components/eta_readonly/brand/icon.png`: quadratische, mit ImageGen aus dem bereitgestellten Logo erstellte Thumbnail-Variante.
- `custom_components/eta_readonly/brand/logo.png`: unverändertes Original des bereitgestellten Logos.
- `dashboard/eta-logo.png`: unveränderte Logo-Datei für die Bildentitätskarte.

Die Dateien sind Bestandteil des Integrationsordners und werden bei der Installation mit übertragen. Es sind fremde Markenbilder bzw. daraus abgeleitete Darstellungen, keine GPL-lizenzierten Projektgrafiken. Die quadratische Variante stellt keine Herstellerfreigabe dar.

## Anzeige

Home Assistant unterstützt lokale Brand-Bilder für Custom Integrations seit 2026.3. Der `brand`-Ordner gehört deshalb in den Integrationsordner, nicht allein in den Repository-Stamm und auch nicht nur in `dashboard`.

Die Marketplace-Vorschau vor der Installation verwendet teilweise den externen Brand-Abgleich des Katalogs. Laut Brands-Projekt werden die Brand-Bilder der im Marketplace erfassten Integrationen regelmäßig aus dem neuesten Release abgeglichen. Deshalb die Dateien auf GitHub hochladen, Release `v1.0.1` aus diesem Commit veröffentlichen und gegebenenfalls den Cache-/Abgleichzeitraum abwarten. Bei einem nur per Link hinzugefügten, noch nicht abgeglichenen Repository kann vor der Installation weiterhin ein Platzhalter erscheinen. Diese lokale Änderung ist keine Bestätigung einer Aufnahme in den Katalog.

Das Logo in einer GitHub-README ist ein anderer Anzeigeort. Auch GitHubs „Social preview“ ist eine separate Repository-Einstellung und wird durch das `brand`-Verzeichnis nicht gesetzt.

Quellen:
- https://contributors.home-assistant.io/blog/2026/02/24/brands-proxy-api/
- https://contributors.home-assistant.io/core/integrations/brands/
- https://github.com/home-assistant/brands#marketplace-icons

## Aufbereitung des quadratischen Icons

Built-in ImageGen mit dem bereitgestellten Logo als Referenz. Prompt: „Prepare this exact provided ETA logo as a square application thumbnail on an opaque pure white background. Preserve the logo's letters, gray shape and yellow circular eta mark exactly, without redrawing or inventing any text or graphics. Keep its full original horizontal aspect ratio, centered on the square canvas with ample white space above and below. No extra text, no shadows, no gradients, no decorative additions. This is only a square thumbnail layout of the existing supplied logo. Output a square image.“

Die Thumbnail-Variante ist eine generierte Ableitung, keine Garantie pixelidentischer Reproduktion. Das unveränderte Original liegt separat bei.
