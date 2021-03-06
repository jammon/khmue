# Website für den Bedarf der Intensivmedizin in KHMue

## Geräteeinweisungen
Hier sollen alle Geräteeinweisungen dokumentiert werden.

### Models
- Gerätekategorie
- Gerät
- Mitarbeiter
- Berufsgruppe ("Pflege ITS", "Ärzte", "Ärzte ITS", "Firmenvertreter")
	+ bestimmt die einzuweisenden Geräte
- Einweiser (beauftragte Mitarbeiter mit Ersteinweisung)
- Einweisung (ggf. Ersteinweisung)

### Views
- index: ?
- Mitarbeiter
- Geräte
- Neue Einweisung
- Gerätepass für Mitarbeiter
- Fehlende Einweisungen

### Usecases
- Mitarbeiter eingeben √
- Mitarbeiter bearbeiten √
- Gerätekategorie eingeben (Admin √)
- Geräte eingeben √
- Geräte bearbeiten (?)
- Berufsgruppe mit einzuweisenden Geräten eingeben √
- Berufsgruppe mit einzuweisenden Geräten bearbeiten √
- Ersteinweisung dokumentieren √
- Folgeeinweisung dokumentieren √
- Abfragen, in welche Geräte eine Person einweisen kann (√)
- Fehlende Einweisungen
	+ Liste der Mitarbeiter mit Zahl der fehlenden Einweisungen √
	+ Liste fehlender Einweisungen pro einzelnem Mitarbeiter √
- Liste der Einweisungen jedes MA
	+ Gerätepass zum Ausdrucken