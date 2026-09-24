# SEO-copy — fsdnorge.no
Arne Breistrand · 19. september 2026 · ikke pushet

Mål: unik title (~60) + description (~155) per side. Canonical forblir https://fsdnorge.no/…  
og:title / og:description = samme tekst (eller litt kortere og).

## Title + description

### index.html (Norge)
- **title** (48): `Er Tesla FSD godkjent i Norge? Status 2026`
- **description** (138): `Kort svar: nei. Faktabasert status for Tesla FSD Supervised (SAE nivå 2) i Norge — Statens vegvesen, TCMV og EØS. Ikke kundegodkjent.`
- **og:title**: samme som title  
- **og:description**: `Kort svar: nei. FSD Supervised er ikke kundegodkjent i Norge. SAE nivå 2 — føreren er alltid ansvarlig.`

### tcmv.html
- **title** (45): `TCMV-stemme per land — FSD Supervised`
- **description** (140): `Uoffisielt estimat av EU-landenes TCMV-stemme om Tesla FSD Supervised. Krever 15 av 27 stater og 65 % befolkning. Rykte merkes.`
- **og:description**: `Uoffisielt TCMV-estimat for FSD Supervised. 15/27 stater og 65 % befolkning. Ikke offisiell protokoll.`

### europa.html
- **title** (42): `FSD Supervised i Europa — live-feed`
- **description** (133): `Norsk live-feed for EU artikkel 39 og TCMV rundt Tesla FSD Supervised. Poster ved materiell endring. Rykte skilles fra vedtak.`
- **og:description**: `Live-feed for artikkel 39 / TCMV. Rykte merkes separat fra myndighetsvedtak.`

### historie.html
- **title** (46): `Autopilot og FSD — tidslinje og pakker`
- **description** (131): `Historien om Tesla Autopilot, EAP og FSD Supervised: HW1–HW4, pakkeskill (Level 2) og EU/Norge. Fakta med kilder.`
- **og:description**: `Tidslinje for Autopilot, EAP og FSD Supervised. Separate Level 2-pakker — ikke «AP ble til FSD».`

## FAQ JSON-LD (index) — 4 naturlige spørsmål

Kun fakta vi allerede står for på huben:

1. **Er Tesla FSD Supervised godkjent for vanlige eiere i Norge?**  
   Nei. Statens vegvesen har ikke godkjent FSD Supervised for vanlig kundekjøring. Det som finnes, er begrenset testing med Tesla-trente sikkerhetsførere.

2. **Er FSD Supervised selvkjøring?**  
   Nei. Det er et førerstøttesystem på SAE nivå 2. Føreren er alltid ansvarlig og må følge med.

3. **Når stemmer EU / TCMV om FSD Supervised?**  
   Statens vegvesen skriver at neste TCMV-møte er i oktober, og at avstemning *kan* komme da. En konkret dato 6. oktober er rykte (Tesla Europe / X), ikke bekreftet agenda i komitologiregisteret.

4. **Hva skjer for Norge hvis TCMV sier ja?**  
   Norge har ikke stemmerett i TCMV. Som EØS-land følger Norge normalt EU-unntak, men Statens vegvesen kan motsette seg innføring av sikkerhetshensyn. Et EU-ja er ikke det samme som norsk kundegodkjenning samme dag.

## Krysslenker i brødtekst (forslag)

**index**
- Etter statuskort / «Hva er godkjent»: lenke «Les historien om Autopilot og FSD» → `historie.html`
- Ved TCMV-blokken: «Se estimert stemme per land» → `tcmv.html` (finnes delvis) + «Europa-feed» → `europa.html`

**historie**
- I EU/Norge-blokken: «Siste norske status» → `index.html` · «TCMV-estimat» → `tcmv.html`
- Avslutning: «Tilbake til godkjenningsstatus» → `index.html`

**tcmv**
- Under totals / note: «Norsk status» → `index.html` · «Hvorfor artikkel 39?» kort pek → `historie.html#eu-norge` (hvis Petter setter id)

**europa**
- Note under feed: beholde lenke til norsk status; legg til «Historie» → `historie.html`

## Ikke gjør
- Ingen meta keywords  
- Ingen keyword-stuffing i FAQ  
- Ikke endre automasjons-IDer

## Til Petter / Kåre
Jeg leverer copy her. Petter/Kåre setter title/description/JSON-LD/robots/sitemap i markup. Jeg kan skrive inn HTML-meta selv hvis Kåre vil — si ifra.
