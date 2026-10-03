# Daglig oppdatering av data/nedtelling.json (fsdnorge.no/nedtelling/)

Kjøres én gang i døgnet, etter den vanlige sjekken av `data/status.json`, `data/europa-feed.json` og `data/svv-siste.json`. Siden leser bare `data/nedtelling.json`; også tallene i metodeboksen fylles fra JSON. HTML skal ikke endres i den daglige jobben.

Kort rekkefølge: hent → sjekk kilder → oppdater fakta/inndata → `python3 scripts/modell_nedtelling.py` → `python3 scripts/validate_nedtelling.py` → push.

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
Alle land skal ha en dato og et `metode`-felt: `observert` (lansert eller godkjent + utrullingsmedian) eller `modell` (scenariomodellen, se punkt 4). Sett `sist_oppdatert` til dagens dato (YYYY-MM-DD) på alle land du har sjekket. Endre ellers bare det som har endret seg:

| Hendelse | Endring |
|---|---|
| Nytt land godkjent (Tesla Europe eller myndighet) | `status` = «godkjent, utrulling snart», `metode` = «observert», `godkjent_dato` = vedtaksdato, `estimert_dato` = `godkjent_dato` + `metode.utrullingsforsinkelse_brukt_dager`, `sikkerhet` = «middels», skriv ny `begrunnelse` med kilder. Fjern `modell_type`, `signal_dato` og `fakta`, og sett `modell_steg` = null. **Oppdater samtidig `status.json`** (eu_land, befolkningsandel). Har landet et datert offentlig signal før vedtaket, legg det inn i `modell.signal_grunnlag` (iso, signal, hva, kilde). |
| Utrulling bekreftet (Tesla-kunngjøring eller dokumentert kundeinstallasjon) | `status` = «lansert», `lansert_dato` = første dokumenterte dato, `estimert_dato` = null. Medianen i `metode.grunnlag` regnes om (punkt 5). |
| Nytt offentlig signal om nasjonal sak i et land uten sak | `modell_type` = «signal», `signal_dato` = datoen, kilden i `kilder`, `status` = «venter på anerkjennelse», oppdater `fakta`. |
| Formelt steg med kjent dato/frist (f.eks. latvisk regjeringsvedtak → CSDD har 10 virkedager) | Landet går fra modell til observert: `metode` = «observert», `estimert_dato` = dato for steget + fristen (virkedager, uten helg) + `utrullingsforsinkelse_brukt_dager`, `sikkerhet` = «middels», regnestykket i `begrunnelse`. Fjern modellfeltene. |
| TCMV setter FSD opp til **votum** med dato | `eu_spor.dato_for_votum_kjent` = true, `eu_spor.neste_tcmv` = datoen, `modell.tcmv_dato` = datoen, `modell.tcmv_dato_antatt` = false. Kjør modellen. Validatoren feiler til dette er gjort. |
| TCMV sier ja | `modell.tcmv_dato` = møtedatoen (ikke antatt). Kommer kommisjonsvedtaket med dato, kan EU-landene gå over til `observert` (vedtaksdato + utrullingsmedian) – spør Ole før metoden endres. |
| TCMV sier nei eller utsetter | Flytt `modell.tcmv_dato` til neste realistiske møte, behold `tcmv_dato_antatt` = true, oppdater `tcmv_begrunnelse`, kjør modellen. |
| Den antatte TCMV-datoen passerer uten votum | Validatoren gir FEIL. Flytt antagelsen som over. |
| Statens vegvesen endrer syn eller gir en egen frist | Oppdater `fakta` for NO. Ny frist med dato = NO går til `observert`. Aldri status godkjent/lansert uten `svv-siste.json` `norge_kundegodkjent: true`. |
| Ingen endring | Bare `sist_oppdatert`. Kjør likevel modellen (punkt 4): datoer kan flytte seg når tiden går. |

Aldri: finn på en dato, rediger en modellert dato for hånd, eller sett Norge til godkjent/lansert uten at `svv-siste.json` har `norge_kundegodkjent: true`.

## 4. Modellen – kjøres hver dag
```
python3 scripts/modell_nedtelling.py
```
Skriptet regner ut `estimert_dato`, `modell_steg` og `begrunnelse` (= `fakta` + modelltekst) for alle land med `metode` = «modell», og skriver avledede tall i `modell`-blokken. Inndata ligger i JSON:

| Parameter | Nå | Type |
|---|---|---|
| `modell.signal_grunnlag` | BE 12.05→10.06 (29), CZ 10.06→21.09 (103), SI 11.07→07.09 (58), HR 10.09→29.09 (19). Median 43,5 → 44, maks 103 | observert |
| `metode.utrullingsforsinkelse_brukt_dager` | 2 (median av sju land: NL 1, LT 0, DK 2, BE 1, SI 3, CZ 2, HR 2; per 03.10) | observert |
| `modell.tcmv_dato` | 2026-12-01 | **antagelse** (`tcmv_dato_antatt` = true) |
| `modell.eu_ikrafttredelse_dager` | 132 (BlueCruise: TCMV 20.03.2024 → EU-godkjent 30.07.2024) | observert presedens |
| `modell.eos_etterslep_dager` | 470 (BlueCruise: EU 30.07.2024 → Norge 12.11.2025) | observert presedens for NO, antagelse for IS/LI |
| `modell.ukjent_margin_dager` | 30 | **antagelse** |
| `modell.ikke_eu_margin_dager` | 180 | **antagelse** |

Steg per `modell_type`:
1. `signal`: signal + median + utrulling. Passert → signal + maks + utrulling. Også passert → EU-scenariet («1 → 2»). Et land kan altså hoppe til 2027 den dagen fristen går ut – det er meningen; skriv det i feed hvis det gjelder et stort land.
2. `eu`: `tcmv_dato` + `eu_ikrafttredelse_dager` + utrulling = EU-scenariet.
3. `eos`: EU-scenariet + `eos_etterslep_dager` (NO, IS, LI).
4. `ukjent`: EU-scenariet + `ukjent_margin_dager`.
5. `ikke_eu`: EU-scenariet + `ikke_eu_margin_dager` (CH, GB).

Endres en parameter (ny presedens, nytt signal, ny TCMV-dato), skal ny `begrunnelse` gjennom språkmølla bare hvis malteksten i skriptet endres. Nye `fakta`-tekster skal alltid gjennom mølla. Parameterendringer som ikke er rene fakta (margin, antatt dato) krever ja fra Ole.

## 5. Metode (utrullingsmedian)
`metode.grunnlag` = alle lanserte land med både `godkjent_dato` og `lansert_dato`, med `dager` = differansen. `utrullingsforsinkelse_median_dager` = medianen, `utrullingsforsinkelse_brukt_dager` = medianen rundet opp. Endres den brukte verdien, må alle estimater for «godkjent, utrulling snart» regnes om for hånd, og modellen må kjøres på nytt (den bruker samme verdi). Validatoren kontrollerer begge.

## 6. Toppnivå
- `sist_oppdatert_iso` = nå, med tidssone (`+02:00` sommertid, `+01:00` fra 25. oktober). `sist_oppdatert_nb` = f.eks. «30. september 2026 kl. 09.15».
- `oppsummering` = samme tall som `status.json`.

## 7. Valider – push bare ved grønt
```
python3 scripts/validate_nedtelling.py
```
Exit 0 = grønt. Validatoren kjører modellen selv og feiler hvis en modellert dato, et modellsteg eller en begrunnelse i fila avviker fra det skriptet regner ut, hvis et land mangler dato eller `metode`, eller hvis den antatte TCMV-datoen er passert. ADVARSEL om passert estimat for et observert land betyr: sjekk om utrullingen er bekreftet. Er den ikke det, la estimatet stå (siden viser «Estimatet er passert – vi venter på bekreftet utrulling»), eller flytt det én gang med begrunnelse. For modellerte land skjer flyttingen automatisk neste dag modellen kjøres.

Ny eller endret leserprosa (`fakta`, `begrunnelse`, maltekster i `scripts/modell_nedtelling.py`) skal gjennom språkmølla (fsd-redaksjon, bie-stil, norsk-bokmål, rettskrivning). Rene dato- og statusendringer trenger ikke egen logg.

## 8. Push og kontroll
- Commit-melding: `nedtelling: <kort endring> (<dato>)`.
- Push: `git -c credential.helper='!gh auth git-credential' push origin HEAD`. Hvis gh ikke er logget inn: GitHub-connectoren (`user-GitHub-xai`, `push_files`).
- Etter push: hent `https://raw.githubusercontent.com/OleBee/tesla-fsd-norge/main/data/nedtelling.json` og kjør `python3 -m json.tool` på den. Endres HTML: trekk ut `<script>` og kjør `node --check`.
