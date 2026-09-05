# Tesla FSD i Norge

Uoffisiell, én-sides statusside om godkjenning av Tesla FSD Supervised i Norge.

**Publisert her:** [https://olebee.github.io/tesla-fsd-norge/](https://olebee.github.io/tesla-fsd-norge/)

**TCMV-stemme per land (engelsk):** [https://olebee.github.io/tesla-fsd-norge/tcmv.html](https://olebee.github.io/tesla-fsd-norge/tcmv.html)

GitHub Pages er på. Siden ligger på `/tesla-fsd-norge/`.

## Filer

- [`index.html`](index.html) — den offentlige Norgesiden
- [`tcmv.html`](tcmv.html) — engelsk oversikt over estimert TCMV-stemme per land
- [`data/status.json`](data/status.json) — strukturert snapshot (EU-land, TCMV, norsk månedssjanse, tidsserie)
- [`data/svv-siste.json`](data/svv-siste.json) — siste sjekk av Statens vegvesens FSD-side (eies av SVV-jobben)

## Sideinnhold (slim-layout fra 2. september 2026)

Siden skal være kort. Behold bare:

- statusbanner med sjansemåler og tidsserie i samme boks
- hero-nedtelling til neste TCMV-vindu
- én miniklokke: UN R171 Series 02
- landtabell med overskriften **Land som påvirkes av avstemningen**
- tidslinje i høyre kolonne
- kort uoffisiell-disclaimer under tabellen

Ikke gjeninnfør: kortet **Norsk vurdering**; footer-linjen nederst; kortene «EU-avstemning», «EU-kunder i dag» og «EU-programvare»; avsnittene «Hva må skje før FSD kan brukes i Norge?», «Kort forklart», «Rykter på X» og «Kilder». Oktoberdatoen merkes som rykte i hero og tidslinje, ikke som et eget «Utsatt»-kort.

Måler og graf styres av `data-prosent` på `#sjanse-kort` og JSON i `#sjanse-historikk`. Ikke erstatt SVG eller script. Siste punkt i grafen merkes **I dag**.

## Automatiseringer

- **FSD-status til GitHub** — daglig kl. 08.30 Europe/Oslo. Research, ev. oppdatering av FSD-skillen, språkvask, deretter `index.html` og `data/status.json`. Oppdaterer også sin egen grunnlinje når fakta flytter seg. Skal respektere slim-layouten over. Rører ikke `tcmv.html` med mindre estimatene der er oppdatert bevisst.
- **SVV FSD-side endring** — hver time på hverdager 08–16. Skriver til repoet bare ved materiell endring eller nede side. Ingen e-post. Skal ikke gjeninnføre slettede avsnitt. Rører `data/svv-siste.json`.

Ved hver skriving til `index.html` skal ingressen ha tidsstempel: «Sist oppdatert D. måned ÅÅÅÅ kl. TT.MM» i tidssonen Europe/Oslo. Samme tidspunkt skal ligge i `data/status.json` som `sist_oppdatert_iso` og `sist_oppdatert_nb`. Skriv aldri «Oppdateres daglig».

Synlig prosa på Norgesiden skal være vasket bokmål før publisering. `tcmv.html` er engelsk.

## Kilderegel

Offisiell status bygger på:

- Statens vegvesen
- RDW
- Nasjonale typegodkjenningsmyndigheter (for eksempel Færdselsstyrelsen)
- Europakommisjonen / TCMV / komitologiregisteret
- EUR-Lex (EU 2018/858)
- UNECE / UN R171 / WP.29
- ETSC når det gjelder uavhengig trafikksikkerhetsvurdering
- Tesla Europe / offisiell brukermanual

Rykter fra troverdige kontoer på X kan tas med i hero og tidslinje, men må merkes som rykte. De får ikke erstatte offisiell status. Trackere og forum brukes ikke som primærkilde.
