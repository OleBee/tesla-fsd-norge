# Tesla FSD i Norge

Uoffisiell, én-sides statusside om godkjenning av Tesla FSD Supervised i Norge.

**Publisert her:** [https://olebee.github.io/tesla-fsd-norge/](https://olebee.github.io/tesla-fsd-norge/)

GitHub Pages er på. Siden ligger på `/tesla-fsd-norge/`.

## Filer

- [`index.html`](index.html) — den offentlige siden
- [`data/status.json`](data/status.json) — strukturert snapshot (EU-land, TCMV-vurdering, norsk månedssjanse)
- [`data/svv-siste.json`](data/svv-siste.json) — siste sjekk av Statens vegvesens FSD-side

## Automatiseringer

- **FSD-status til GitHub** — daglig. Research, ev. oppdatering av FSD-skillen, språkvask av synlig bokmål, deretter `index.html` og `data/status.json`. Oppdaterer også sin egen grunnlinje når fakta flytter seg.
- **SVV FSD-side endring** — hver time på hverdager 08–16. Skriver til repoet bare ved materiell endring eller nede side. Ingen e-post.

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

Rykter fra troverdige kontoer på X kan tas med, men må merkes som rykte og oppgis bare med X som kilde. De får ikke erstatte offisiell status. Trackere og forum brukes ikke som primærkilde.
