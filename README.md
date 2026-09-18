# Tesla FSD i Norge

Uoffisiell statushub om godkjenning av Tesla FSD Supervised (SAE nivå 2) i Norge. Primært for norske Tesla-eiere som vil ha klare fakta — ikke spekulasjon uten kilde.

**Canonical URL:** [https://fsdnorge.no/](https://fsdnorge.no/)

Speil på GitHub Pages: [https://OleBee.github.io/tesla-fsd-norge/](https://OleBee.github.io/tesla-fsd-norge/) (custom domain `fsdnorge.no` via `CNAME`).

## Sider

- [`index.html`](index.html) — norsk godkjennings-hub (status, L2-disclaimer, kilder, tidslinje)
- [`tcmv.html`](tcmv.html) — estimert TCMV-stemme per EU-land (bokmål)
- [`europa.html`](europa.html) — live-feed for EU artikkel 39 / TCMV (bokmål UI + `data/europa-feed.json`)

## Data

- [`data/status.json`](data/status.json) — strukturert snapshot (EU-land, TCMV, norsk månedssjanse, tidsserie)
- [`data/svv-siste.json`](data/svv-siste.json) — siste sjekk av Statens vegvesens FSD-side
- [`data/europa-feed.json`](data/europa-feed.json) — feed-elementer for Europa-siden (behold nøkler/form)

## Sideinnhold (Norge)

Huben skal være faktabasert. Behold:

- statusbanner med sjansemåler (fra `data/status.json` når tilgjengelig)
- tydelig SAE nivå 2 / Supervised-disclaimer
- faktaboks for norsk status + SVV-lenke
- hero-nedtelling til neste TCMV-vindu
- én miniklokke: UN R171 Series 02
- landtabell **Land som påvirkes av avstemningen**
- tidslinje
- kilder/lenker
- kort uoffisiell-disclaimer

Måler styres av `data-prosent` på `#sjanse-kort` / `#tcmv-sjanse-kort`. Behold automasjonsvennlige IDer.

Hele den offentlige UI-en er bokmål (nav, aria-labels, tomtilstander, title, meta).

## Automatiseringer

- **FSD-status til GitHub** — daglig kl. 08.30 Europe/Oslo. Oppdaterer `index.html` og `data/status.json`. Skal respektere hub-layouten. Rører ikke `tcmv.html`.
- **LAZARUS** (internt navn) — daglig kl. 07.00 Europe/Oslo. Eier `tcmv.html`. Navnet skal ikke vises offentlig.
- **SVV FSD-side endring** — hverdager 08–16. Skriver til repoet ved materiell endring. Rører `data/svv-siste.json`.

Ved skriving til `index.html`: ingress med «Sist oppdatert D. måned ÅÅÅÅ kl. TT.MM» (Europe/Oslo). Samme tidspunkt i `data/status.json` som `sist_oppdatert_iso` og `sist_oppdatert_nb`. Skriv aldri «Oppdateres daglig».

## Kilderegel

Offisiell status bygger på Statens vegvesen, RDW, nasjonale typegodkjenningsmyndigheter, Europakommisjonen/TCMV/komitologiregisteret, EUR-Lex (2018/858), UNECE/UN R171/WP.29, ETSC og Tesla Europe.

Rykter fra troverdige kontoer på X kan tas med i hero og tidslinje, men må merkes som rykte. De får ikke erstatte offisiell status. Ikke finn på godkjenninger.
