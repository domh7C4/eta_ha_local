# Manuell auf GitHub hochladen

1. `eta-homeassistant-github.zip` lokal entpacken.
2. Auf GitHub ein neues Repository anlegen, beispielsweise `eta-homeassistant`. Zunächst private Sichtbarkeit wählen, solange die Berechtigung für die Weitergabe des ETA-Logos nicht geklärt ist.
3. Im neuen Repository „uploading an existing file“ bzw. „Add file → Upload files“ wählen.
4. Den **Inhalt** des entpackten Ordners hochladen: `hacs.json`, `README.md`, `custom_components`, `dashboard`, `docs`, `tests`, `.gitignore` und `.github` müssen direkt im Repository-Stamm liegen. Nicht bloß die ZIP-Datei hochladen. Versteckte Dateien gegebenenfalls im Explorer einblenden.
5. Den Upload mit einer Commit-Nachricht bestätigen.

Manche Konten erlauben das Hochladen von GitHub-Workflows erst nach einer zusätzlichen Berechtigungsfreigabe. Wenn GitHub `.github/workflows/check.yml` ablehnt, kann zunächst ohne diesen Ordner hochgeladen werden; die lokalen Tests bleiben nutzbar.

Die ZIP enthält Quellcode und Dokumentation, kein Git-Verzeichnis und keine Zugangsdaten. Es wurde kein Repository auf GitHub angelegt.

Für die Installation über Marketplace/HACS ist ein öffentliches Repository erforderlich. Nach Upload aller Dateien einen neuen Release `v1.0.1` aus dem korrigierten Commit erstellen. `hacs.json` muss auch im verwendeten Release vorhanden sein. Die Logo-Rechte vor öffentlicher Weitergabe klären.

Die Brand-Dateien unter `custom_components/eta_readonly/brand` ebenfalls hochladen. Die Logo-Anzeige vor Installation hängt gegebenenfalls vom Marketplace-Abgleich ab; Details in `BRANDING.md`.
