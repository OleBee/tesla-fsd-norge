# Tesla FSD i Norge

Uoffisiell statusside om godkjenning av Tesla FSD Supervised (SAE nivå 2) i Norge. Primært for norske Tesla-eiere som vil ha klare fakta — ikke spekulasjon uten kilde.

**Canonical URL:** [https://tadnorge.no/](https://tadnorge.no/) (tidligere fsdnorge.no; videresending og DNS tar Chief of Staff)

Speil på GitHub Pages: [https://OleBee.github.io/tesla-fsd-norge/](https://OleBee.github.io/tesla-fsd-norge/) (custom domain `tadnorge.no` via `CNAME`).

## Én side (singleside dashboard)

- [`index.html`](index.html) — Siste nytt (feed) · Historikk/Tidslinje · Forklaring (statuskort)
- Gamle URL-er (`europa.html`, `tcmv.html`, `historie.html`, `nyheter/*`) er tynne redirects til `/` (noindex)

## Data (JSON-only publish)

- [`data/status.json`](data/status.json) — tall, sjanser, countdown, `timeline[]`
- [`data/europa-feed.json`](data/europa-feed.json) — feed-elementer (title, summary, why_it_matters, iso, source/tags)
- [`data/svv-siste.json`](data/svv-siste.json) — siste sjekk av Statens vegvesens FSD-side

Ikke lag nye HTML-artikkelsider. Publiser via JSON; Chief of Staff pusher.

## Layout

Tre kolonner: feed | tidslinje | statuskort (countdown TCMV + Series 02, sjanser, landtall). Hydrering fra `data/*.json`. Behold automasjonsvennlige IDer i `index.html`.

Hele den offentlige UI-en er bokmål.

## Automatiseringer (CoS eier)

Rutiner og push ligger hos Chief of Staff. Redaksjonsbot: `fsdnorge`. Etter TCMV-møte: oppdater singleside-JSON (`status.json` / `europa-feed.json`), ikke gamle `tcmv.html`.

## SEO og deling

- `scripts/build_seo.py` bygger `feed.xml` (RSS), `sitemap.xml` (med `lastmod`) og den statiske feed- og tidslinjeblokken i `index.html` (mellom `SEO:FEED`- og `SEO:TIDSLINJE`-markørene) fra `data/*.json`. Kjør `python3 scripts/build_seo.py` før push når JSON er endret. `--check` gir kode 1 hvis noe er utdatert.
- `.github/workflows/seo.yml` kjører det samme skriptet ved push til main og committer bare hvis noe er endret. Kjør `git pull --rebase` før push hvis du ikke har kjørt skriptet selv.
- Delingsbilde: `assets/og/tadnorge-og.png` (1200×630), kilde `scripts/og/og-image.html`, render med `bash scripts/og/render.sh`. `og-default.png` beholdes for gamle delinger.
- Logo for strukturerte data: `assets/brand/tadnorge-logo-512.png`.
- `robots.txt` stenger `/drafts/` og `/scripts/` for søkemotorer.

## Kilderegel

Offisiell status bygger på Statens vegvesen, RDW, nasjonale typegodkjenningsmyndigheter, Europakommisjonen/TCMV/komitologiregisteret, EUR-Lex (2018/858), UNECE/UN R171/WP.29, ETSC og Tesla Europe.

Rykter fra troverdige kontoer på X kan tas med, men må merkes som rykte. De får ikke erstatte offisiell status. Ikke finn på godkjenninger.
