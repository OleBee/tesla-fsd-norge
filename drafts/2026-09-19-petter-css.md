# CSS-skisse — hierarki / badges / mobil
Petter Gulliksen · 19. september 2026 · ikke pushet

## Gjort i working copy
- Page-layout (layout, timeline, table, clocks, rail) flyttet fra inline `index.html` → `site.css`
- H1: font-weight 600
- Soft-badge nøytralisert (ikke «aktiv status»-blå flate); warn beholdt amber
- `clock-head` gap 8px + margin under badges før H2
- **Norge-meter primær** (`#sjanse-kort`): store tall
- **TCMV-meter sekundær** (`#tcmv-sjanse-kort`): mindre tall (clamp 40–56), tynnere bar
- Landtabell: klasse `countries-table`, stablet under 720px
- IDer og `data-prosent` urørt

## Ikke gjort
- Push (venter Kåre)
- Brand/favicon i produksjon (eget spor)
- Full flytting av tcmv/europa inline CSS (tcmv har allerede stablet tabell)

## Klar for
Samlet gjennomgang med Arnes HTML.
