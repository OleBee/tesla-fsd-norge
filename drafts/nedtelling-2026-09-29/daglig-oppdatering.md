# Daglig oppdatering av data/nedtelling.json (fsdnorge.no/nedtelling/)

Kjøres én gang i døgnet, etter den vanlige sjekken av `data/status.json`, `data/europa-feed.json` og `data/svv-siste.json`. Siden leser bare `data/nedtelling.json`. HTML skal ikke endres i den daglige jobben.

## 1. Hent og les
1. `git pull` i `/workspace/tesla-fsd-norge`.
2. Les `data/status.json` (`eu_land`, `eu_andel_befolkning_prosent`) og `data/svv-siste.json` (`norge_kundegodkjent`). De er fasit for hvilke EU-land som er godkjent.
3. Les `data/nedtelling.json`.

## 2. Sjekk kilder (fast rekkefølge)
- **Tesla Europe på X** (@teslaeurope): «approved in …» og «now rolling out in …».
- **Trackere som stikkprøve, ikke fasit:** https://fsd-eu-tracker.de/en/ · https://finebutwhy.com/fsd/ · https://fsdlive.eu/
- **EU-sporet:** Komitologiregisteret/CIRCABC for TCMV (agenda, votum, dato for desember-møtet), Electrek/Reuters.
- **Norge:** Statens vegvesens ADAS-side (samme sjekk som `svv-siste.json`).
- **Land med åpen sak:** Latvia (TAP-portalen, prosjekt 26-TA-2030, og regjeringsvedtak), Finland (Traficom), Hellas, Irland, Italia, Tyskland (KBA/BMV), Frankrike (UTAC-tester), Sverige.
- Søk: `"FSD Supervised" approved <land> <måned år>` og `"FSD Supervised" rolling out <land>`.

## 3. Oppdater per land (bare ved nye, kildebelagte fakta)
Sett `sist_oppdatert` til dagens dato (YYYY-MM-DD) på alle land du har sjekket. Endre ellers bare det som har endret seg:

| Hendelse | Endring |
|---|---|
| Nytt land godkjent (Tesla Europe eller myndighet) | `status` = «godkjent, utrulling snart», `godkjent_dato` = vedtaksdato, `estimert_dato` = `godkjent_dato` + `metode.utrullingsforsinkelse_brukt_dager`, `sikkerhet` = «middels», kilder. **Oppdater samtidig `status.json`** (eu_land, befolkningsandel) – validatoren krever samsvar. |
| Utrulling bekreftet (Tesla-kunngjøring eller dokumentert kundeinstallasjon) | `status` = «lansert», `lansert_dato` = første dokumenterte dato, `estimert_dato` = null. Legg landet inn i `metode.grunnlag` og regn ut median på nytt (se punkt 4). |
| Formelt steg med kjent dato/frist (f.eks. latvisk regjeringsvedtak → CSDD har 10 virkedager) | Estimat = dato for steget + fristen (virkedager, uten helg) + `utrullingsforsinkelse_brukt_dager`, `sikkerhet` = «lav» eller «middels». Skriv regnestykket i `begrunnelse`. |
| TCMV setter FSD opp til **votum** med dato | Sett `eu_spor.dato_for_votum_kjent` = true og `eu_spor.neste_tcmv` = datoen. Ikke gi EU-land estimat før metoden er utvidet og godkjent av Ole (et ja krever også kommisjonsvedtak). |
| Ingen endring | Bare `sist_oppdatert`. |

Aldri: finn på en dato, gi Norge estimat uten SVV-grunnlag, eller sett Norge til godkjent/lansert uten at `svv-siste.json` har `norge_kundegodkjent: true`.

## 4. Metode (median)
`metode.grunnlag` = alle lanserte land med både `godkjent_dato` og `lansert_dato`, med `dager` = differansen. `utrullingsforsinkelse_median_dager` = medianen, `utrullingsforsinkelse_brukt_dager` = medianen rundet opp. Endres den brukte verdien, må alle estimater for «godkjent, utrulling snart» regnes om. Validatoren kontrollerer dette.

## 5. Toppnivå
- `sist_oppdatert_iso` = nå, med tidssone (`+02:00` sommertid, `+01:00` fra 25. oktober). `sist_oppdatert_nb` = f.eks. «30. september 2026 kl. 09.15».
- `oppsummering` = samme tall som `status.json`.

## 6. Valider – push bare ved grønt
```
python3 scripts/validate_nedtelling.py
```
Exit 0 = grønt. ADVARSEL om passert estimat betyr: sjekk om utrullingen er bekreftet. Er den ikke det, la estimatet stå (siden viser «Estimatet er passert – vi venter på bekreftet utrulling»), eller flytt det én gang med begrunnelse.

Ny eller endret leserprosa (`begrunnelse`, `tidligst`) skal gjennom språkmølla (fsd-redaksjon, bie-stil, norsk-bokmål, rettskrivning). Rene dato- og statusendringer trenger ikke egen logg.

## 7. Push og kontroll
- Commit-melding: `nedtelling: <kort endring> (<dato>)`.
- Push: `git -c credential.helper='!gh auth git-credential' push origin HEAD`. Hvis gh ikke er logget inn: GitHub-connectoren (`user-GitHub-xai`, `push_files`).
- Etter push: hent `https://raw.githubusercontent.com/OleBee/tesla-fsd-norge/main/data/nedtelling.json` og kjør `python3 -m json.tool` på den. Endres HTML: trekk ut `<script>` og kjør `node --check`.
