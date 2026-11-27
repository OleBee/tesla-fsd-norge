# Tesla FSD i Norge

Uoffisiell statusside om godkjenning av Tesla FSD Supervised (SAE nivå 2) i Norge. Primært for norske Tesla-eiere som vil ha klare fakta — ikke spekulasjon uten kilde.

**Canonical URL:** [https://tadnorge.no/](https://tadnorge.no/) (tidligere fsdnorge.no; videresending og DNS tar Chief of Staff)

Speil på GitHub Pages: [https://OleBee.github.io/tesla-fsd-norge/](https://OleBee.github.io/tesla-fsd-norge/) (custom domain `tadnorge.no` via `CNAME`).

## Én side (singleside dashboard)

- [`index.html`](index.html) — Siste nytt (feed) · Historikk/Tidslinje · Forklaring (statuskort)
- [`en/index.html`](en/index.html) — engelsk versjon på `/en/`, samme oppsett og samme kode (se «Engelsk versjon» under)
- [`nedtelling/index.html`](nedtelling/index.html) og [`en/countdown/index.html`](en/countdown/index.html) — nedtelling per land
- Gamle URL-er (`europa.html`, `tcmv.html`, `historie.html`, `nyheter/*`) er tynne redirects til `/` (noindex)

## Data (JSON-only publish)

- [`data/status.json`](data/status.json) — tall, sjanser, countdown, `timeline[]`
- [`data/europa-feed.json`](data/europa-feed.json) — feed-elementer (title, summary, why_it_matters, iso, source/tags)
- [`data/svv-siste.json`](data/svv-siste.json) — siste sjekk av Statens vegvesens FSD-side

Ikke lag nye HTML-artikkelsider. Publiser via JSON; Chief of Staff pusher.

## Layout

Tre kolonner: feed | tidslinje | statuskort (countdown TCMV + Series 02, sjanser, landtall). Hydrering fra `data/*.json`. Behold automasjonsvennlige IDer i `index.html`.

Den norske UI-en er bokmål. `/en/` og `/en/countdown/` er engelsk (britisk rettskriving).

## Engelsk versjon (/en/)

Språkknappen NO/EN øverst til høyre går til tilsvarende side, fane og sak (`/sprak.js`). Faner på engelsk: `#latest-news`, `#timeline`, `#status`, `#countdown-by-country`; de norske hashene godtas også.

Felles kode for begge språk: `/forside.js` (feed, tidslinje, statuskort), `/mobil-meny.js` og `/mobil-meny.css` (mobilmeny), `/sprak.js` (språk, fletting av engelsk tekst, språkknapp). Språket styres av `<html lang>`.

**Lagring:** Den engelske teksten ligger i egne filer, `data/en/europa-feed.json`, `data/en/status.json` og `data/en/nedtelling.json`. De har bare tekst. Datoer, tall, kilder, bilder og status hentes alltid fra de norske filene, så fakta finnes ett sted. Hver engelsk oppføring har `norsk_sha` (hash av den norske teksten den er oversatt fra). Endres den norske teksten, feiler validatoren til den engelske er oppdatert.

**Flyten for hver ny eller endret sak (norsk → engelsk → valider):**

1. Skriv eller endre den norske teksten i `data/*.json` som før.
2. `python3 scripts/validate_engelsk.py --mangler` viser hva som mangler engelsk tekst eller er utdatert, med den norske teksten og en ferdig JSON-mal.
3. Skriv den engelske teksten i `data/en/*.json`: samme fakta og forbehold, navn, datoer og kilder uendret, Teslas og Musks påstander tilskrevet dem, ingen norsk godkjenning som ikke finnes, ingen tidskoder fra video, «ITavisen».
4. `python3 scripts/validate_engelsk.py --stamp feed:<id>` (eller `status:tcmv`, `tidslinje:<dato>#<n>`, `nedtelling:<ISO>`) setter `norsk_sha` for det du har oversatt.
5. Modellerte land i nedtellingen: skriv engelsk `fakta` i `data/en/nedtelling.json`; `python3 scripts/modell_nedtelling.py` skriver den engelske begrunnelsen selv.
6. `python3 scripts/validate_engelsk.py` (må gi «0 feil»), deretter `python3 scripts/build_seo.py` (bygger også `en/index.html` og `en/feed.xml`).

`validate_engelsk.py` feiler på manglende eller utdatert engelsk tekst, ulikt antall avsnitt eller bilder, engelske oppføringer uten norsk motpart, manglende landnavn, `norge_kundegodkjent` som ikke er `false`, og brudd på husreglene (IT-avisen-skrivemåte, video-tidskoder, HTML-entiteter, «»). Workflowen `seo.yml` kjører validatorene på pull requests og ved push til main.

## Automatiseringer (CoS eier)

Rutiner og push ligger hos Chief of Staff. Redaksjonsbot: `fsdnorge`. Etter TCMV-møte: oppdater singleside-JSON (`status.json` / `europa-feed.json`), ikke gamle `tcmv.html`.

## SEO og deling

- `scripts/build_seo.py` bygger `feed.xml` (RSS), `sitemap.xml` (med `lastmod` og hreflang-alternativer for `/`, `/en/`, `/nedtelling/` og `/en/countdown/`) og den statiske feed- og tidslinjeblokken i `index.html` (mellom `SEO:FEED`- og `SEO:TIDSLINJE`-markørene) fra `data/*.json`, og det samme på engelsk i `en/index.html` og `en/feed.xml`. Kjør `python3 scripts/build_seo.py` før push når JSON er endret. `--check` gir kode 1 hvis noe er utdatert.
- `.github/workflows/seo.yml` kjører det samme skriptet ved push til main og committer bare hvis noe er endret. Kjør `git pull --rebase` før push hvis du ikke har kjørt skriptet selv.
- Delingsbilde: `assets/og/tadnorge-og.png` (1200×630), kilde `scripts/og/og-image.html`, render med `bash scripts/og/render.sh`. `og-default.png` beholdes for gamle delinger.
- Logo for strukturerte data: `assets/brand/tadnorge-logo-512.png`.
- `robots.txt` stenger `/drafts/` og `/scripts/` for søkemotorer.

## Kilderegel

Offisiell status bygger på Statens vegvesen, RDW, nasjonale typegodkjenningsmyndigheter, Europakommisjonen/TCMV/komitologiregisteret, EUR-Lex (2018/858), UNECE/UN R171/WP.29, ETSC og Tesla Europe.

Rykter fra troverdige kontoer på X kan tas med, men må merkes som rykte. De får ikke erstatte offisiell status. Ikke finn på godkjenninger.
