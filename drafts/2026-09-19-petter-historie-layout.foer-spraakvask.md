# Layout-skisse — historie.html
Petter Gulliksen · 19. september 2026 · ikke pushet

## Nav (forslag — venter Kåres grønt)
`Norge · Historie · TCMV · Europa`  
Historie mellom Norge og TCMV (kronologi nærmest huben).

## Sidestruktur ↔ UI
1. **Ingress** — standard header (kicker / H1 / lede)
2. **Pakkekort** — `.pack-grid` 3–4 kolonner → 1 på mobil; match `.facts`/`.fact`
3. **Callout** — «AP ≠ FSD» (`.callout-split`)
4. **HW-diagram** — bilde `assets/historie/diagram-hardware.png` + kort tabell under
5. **Tidslinje** — vertikal `.era` (år-gruppe) + `.timeline` (gjenbruk rail-stil, full bredde)
6. **EU/Norge-blokk** — `.panel` med egen kicker, ikke blandet i US-linjer
7. **Kilder** — `.sources`

## Mobil
- Pakkekort: 1 kolonne
- HW: horisontal scroll *eller* stablet kort (jeg foreslår stablet — mer lesbart)
- Tidslinje: allerede vertikal; år-etikett sticky valgfritt

## Illustrasjoner (originale, i `drafts/historie/`)
| Fil | Bruk |
|-----|------|
| `diagram-pakker.png` | AP / EAP / FSD Supervised |
| `diagram-hardware.png` | HW1–HW4 |
| `callout-ap-vs-fsd.png` | Skille-setning |

Ingen Tesla-pressbilder.

## CSS
Ny seksjon i `site.css` (ikke rør automasjons-IDer på andre sider). Utkast-klasser: `.pack-grid`, `.pack`, `.era`, `.era-label`, `.callout-split`, `.hw-figure`.

## Blokkere
Venter Kåre på nav-rekkefølge + dybde software-versjoner før HTML-bygging.
