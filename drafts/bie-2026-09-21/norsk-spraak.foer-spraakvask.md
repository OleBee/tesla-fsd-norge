# Norsk språk — rettelser (fase 1)
Arne · 21.09.2026 · Bie + bokmål · ikke pushet

**Funn:** De tre nyeste postene i `data/europa-feed.json` er på engelsk. HTML-sider (index/tcmv/europa/historie) er i hovedsak bokmål. Unntak som kan stå: produktnavn, egennavn, URL, IDer. Kildelisten på historie har «type approval» (kan bli «typegodkjenning»).

---

## 1) `data/europa-feed.json` — tre poster

### A) `news-latvia-proposal-2026-09-21`

**title**  
Før: `Latvia’s economy ministry proposes Cabinet recognition of Dutch FSD Supervised approval`  
Etter: `Latvias økonomidepartement foreslår at regjeringen anerkjenner nederlandsk FSD Supervised-godkjenning`

**summary**  
Før: `On 21 September 2026 the Latvian Ministry of Economics published a proposal for the Cabinet of Ministers to recognise the Dutch RDW Article 39 provisional type approval. If Cabinet agrees, CSDD would have ten working days to finish Tesla’s application review. This is not yet a customer go-ahead — Latvia remains without national approval until that decision.`  
Etter: `21. september 2026 publiserte Latvias økonomidepartement et forslag om at regjeringen skal anerkjenne den nederlandske RDW artikkel 39-typegodkjenningen. Hvis regjeringen sier ja, får CSDD ti virkedager på å ferdigbehandle Teslas søknad. Dette er ikke kundegodkjenning ennå — Latvia mangler nasjonal godkjenning til beslutningen er tatt.`

**why_it_matters**  
Før: `Shows a formal Baltic follow-on path after EE/LT, but only a proposal. Does not change the Yes count for TCMV; map status is Uncertain until recognition.`  
Etter: `Viser en formell baltisk oppfølging etter Estland/Litauen, men bare et forslag. Endrer ikke «ja»-tellingen for TCMV; status er usikker til anerkjennelsen er vedtatt.`

---

### B) `tcmv-czechia-2026-09-21`

**title**  
Før: `Czechia flips to Yes on the TCMV map — 7/27 and 11.8% population`  
Etter: `Tsjekkia til «ja» på TCMV-kartet — 7 av 27 land og 11,8 % av befolkningen`

**summary**  
Før: `Czechia’s Ministry of Transport recognised the Dutch Article 39 file on 21 September 2026. Latvia’s economy ministry proposed Cabinet recognition the same day (still Uncertain — not a customer go-ahead). Unofficial October yes chance moved to 30%.`  
Etter: `Tsjekkias transportministerium anerkjente den nederlandske artikkel 39-saken 21. september 2026. Samme dag foreslo Latvias økonomidepartement regjeringsanerkjennelse (fortsatt usikkert — ikke kundegodkjenning). Uoffisiell sjanse for TCMV-ja i oktober er satt til 30 %.`

**why_it_matters**  
Før: `Vote math improved modestly, but the 15-state / 65% thresholds still need the large economies.`  
Etter: `Stemmetallene bedret seg noe, men tersklene 15 stater / 65 % befolkning krever fortsatt de store økonomiene.`

---

### C) `norway-czechia-2026-09-21`

**title**  
Før: `Czechia becomes seventh EU country with national FSD Supervised recognition`  
Etter: `Tsjekkia blir sjuende EU-land med nasjonal anerkjennelse av FSD Supervised`

**summary**  
Før: `Czech Ministry of Transport recognised the Dutch Article 39 provisional type approval for Tesla FSD Supervised on 21 September 2026. Tesla Europe confirms rollout soon. Seven member states now cover about 11.8% of the EU population. Norway remains without customer approval.`  
Etter: `Tsjekkias transportministerium anerkjente den nederlandske artikkel 39-typegodkjenningen for Tesla FSD Supervised 21. september 2026. Tesla Europe bekrefter utrulling snart. Sju medlemsland dekker nå om lag 11,8 % av EU-befolkningen. Norge er fortsatt uten kundegodkjenning.`

**why_it_matters**  
Før: `Adds population weight ahead of the rumoured 6 October TCMV window, but still far below the 15-state / 65% thresholds. No change to Norway’s SVV stance.`  
Etter: `Gir mer befolkningsvekt før det ryktede TCMV-vinduet 6. oktober, men fortsatt langt under tersklene 15 stater / 65 %. Ingen endring i Statens vegvesens linje for Norge.`

---

## 2) `historie.html` — kildeliste (valgfritt)

**Før:** `RDW (10.04.2026) — type approval FSD Supervised`  
**Etter:** `RDW (10.04.2026) — typegodkjenning FSD Supervised`

*(«Full Self-Driving (Supervised)» som produktnavn kan stå.)*

---

## 3) Øvrige sider

`index.html`, `tcmv.html`, `europa.html` (UI/lede/note): ingen vesentlig engelsk brødtekst funnet. Badge-tekst, tomtilstand («Ingen innlegg ennå»), feilmelding («Kunne ikke laste…») er bokmål.

Produktnavn som står: Autopilot, FSD Supervised, Enhanced Autopilot, Navigate on Autopilot, Hardware 1–4, TCMV, RDW, CSDD, UTAC — OK.

---

## Til Kåre / Petter

JSON-patch: erstatt de tre engelsk-postene som over. Deretter Petter synker feed (ingen HTML-strukturendring nødvendig utover valgfri kildelinje på historie).
