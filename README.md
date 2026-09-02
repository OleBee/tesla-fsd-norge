# Tesla FSD i Norge

Uoffisiell, én-sides statusside om godkjenning av Tesla FSD Supervised i Norge.

**Publisert her:** [https://olebee.github.io/tesla-fsd-norge/](https://olebee.github.io/tesla-fsd-norge/)

GitHub Pages er på. Siden ligger på `/tesla-fsd-norge/`.

## Filer

- [`index.html`](index.html) — den offentlige siden
- [`data/status.json`](data/status.json) — strukturert snapshot (EU-land, TCMV-vurdering, norsk månedssjanse)
- [`data/svv-siste.json`](data/svv-siste.json) — siste sjekk av Statens vegvesens FSD-side

## Sideinnhold (slim-layout fra 2. september 2026)

Siden skal være kort. Behold bare:

- statusbanner («FSD er ikke godkjent for vanlige eiere i Norge»)
- hero-nedtelling til neste TCMV-vindu
- to miniklokker: UN R171 Series 02 og Norsk vurdering
- ett månedskort med uoffisiell sjanse
- landtabell med overskriften **Land som påvirkes av avstemningen**
- tidslinje i høyre kolonne
- kort uoffisiell-disclaimer og footer

Ikke gjeninnfør: kortene «EU-avstemning», «EU-kunder i dag» og «EU-programvare»; avsnittene «Hva må skje før FSD kan brukes i Norge?», «Kort forklart», «Rykter på X» og «Kilder». Oktoberdatoen merkes som rykte i hero og tidslinje, ikke som et eget «Utsatt»-kort.

## Automatiseringer

- **FSD-status til GitHub** — daglig. Research, ev. oppdatering av FSD-skillen, språkvask av synlig bokmål, deretter `index.html` og `data/status.json`. Oppdaterer også sin egen grunnlinje når fakta flytter seg. Skal respektere slim-layouten over.
- **SVV FSD-side endring** — hver time på hverdager 08–16. Skriver til repoet bare ved materiell endring eller nede side. Ingen e-post. Skal ikke gjeninnføre slettede avsnitt.

Ved hver skriving til `index.html` skal ingressen ha tidsstempel: «Sist oppdatert D. måned ÅÅÅÅ kl. TT.MM» i tidssonen Europe/Oslo. Samme tidspunkt skal ligge i `data/status.json` som `sist_oppdatert_iso` og `sist_oppdatert_nb`. Skriv aldri «Oppdateres daglig».

Synlig prosa på siden skal være vasket bokmål før publisering.

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
