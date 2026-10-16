# Tekstutkast — index / tcmv / europa
Arne Breistrand · 19. september 2026 · ikke pushet

Kilder sjekket i dag:
- SVV FSD-side (vegvesen.no …/forerstottesystemer/) — «sist» offentlig: 3. juli 2026. Bekrefter: ikke kundegodkjent; begrenset testing; kundedemoer stanset; TCMV-møte i oktober «kan» bli første avstemningsmulighet.
- Komitologiregister / EUR-Lex 2018/858 (lenket på siden)
- Reuters (FR UTAC 3. sep), Tesla Europe / sekundære trackere for 6. okt-dato

## 1) Index — ingress (strammet)

**Nå:**
> Kort svar for vanlige eiere: **nei**. Faktabasert status fra Statens vegvesen, TCMV og EØS — ingen oppdiktede godkjenninger. Sist oppdatert …

**Forslag:**
> Kort svar: **nei**. Vanlige norske eiere kan ikke aktivere FSD Supervised. Status bygger på Statens vegvesen, TCMV og EØS — ikke på rykter. Sist oppdatert …

## 2) Index — faktabokser

Behold tre bokser. Små stramninger:

| Boks | Forslag verdi | Forslag undertekst |
|------|---------------|--------------------|
| Kundegodkjenning | Ikke godkjent | Vanlige eiere kan ikke aktivere FSD Supervised. |
| SVV-infoside | Sist oppdatert 3. juli 2026 | Offisiell linje uendret siden da. Ingen ny kundegodkjenning. |
| Systemnivå | Nivå 2 · Supervised | Førerstøtte. Føreren er alltid ansvarlig. |

Statuskort-ingress (strammet):
> Statens vegvesen har ikke godkjent FSD Supervised for vanlig kundekjøring. Det som finnes, er begrenset testing med Tesla-trente sikkerhetsførere — ikke kundegodkjenning.

## 3) Rykte vs. vedtak — TCMV-dato (viktigste rettelse)

**SVV (vedtak/offisiell):** Neste TCMV-møte er i **oktober**. Det **kan** bli første mulighet for avstemning, avhengig av svar på medlemslandenes spørsmål.

**Rykte / sekundær:** Konkret dato **6. oktober 2026** og «vote expected» — Tesla Europe / X / trackere. Agendaen er ikke i komitologiregisteret (sjekk ved push).

**Forslag badge-par på index + tcmv:**
- `TCMV-møte i oktober` (soft/nøytral) — SVV
- `6. okt · rykte` (warn) — ikke agenda-bekreftet

**Forslag H2:** «TCMV møtes i oktober — avstemning er mulig, ikke bekreftet»
**Forslag undertekst:** «Datoen 6. oktober er rykte (Tesla Europe / X). SVV skriver bare «oktober» og at avstemning avhenger av svarene. Seks godkjente land dekker ca. 9,4 % av EU-befolkningen.»

## 4) Sjansemålere

Behold IDer og `data-prosent`. Stram etikett september → måned:
- «Sjanse for FSD til norske eiere denne måneden» (ikke låst til «september» når kalenderen snur)
- Undertekst behold: «Uoffisielt skjønnstall, ikke et tall fra Vegvesenet.»

## 5) Tallfeil å fikse

- Index landtabell / tidslinje: **9,4 %**
- tcmv.html totals: **9,3 %**
- europa-feed standings: **9,4 %**

→ Harmoniser til **9,4 %** (seks land) overalt, eller hent fra `status.json` én gang.

## 6) tcmv.html — ingress

**Forslag:**
> Uoffisielt estimat av hvordan de 27 EU-landene kan stemme om anerkjennelse av den nederlandske artikkel 39-saken. Kvalifisert flertall: minst 15 av 27 stater og 65 % av befolkningen. «Ja» i tabellen er estimat, ikke offentlig stemmeprotokoll. Sist oppdatert …

Merknad på «Nei»-land med «Ingen offentlig prosess»: bytt til «Ingen offentlig anerkjennelse kjent» der vi mangler primærkilde — unngår å oversette stillhet til formelt nei.

## 7) europa.html — ingress

**Forslag:**
> Live-feed for EU artikkel 39 / TCMV. Poster merkes etter kilde. Rykte får egen badge og erstatter ikke SVV- eller Kommisjonsvedtak. Sist oppdatert …

Feed: ingen tekstendring i HTML nødvendig utover ingress; sjekk at nye items i `europa-feed.json` alltid har `source` som skiller `svv` / `news` / `tcmv-vote`.

## 8) Anbefalt neste steg (Kåre)

1. Godkjenn rykte/vedtak-skillet for 6. okt vs «oktober».
2. Godkjenn harmonisering 9,4 %.
3. Petter: behold sjansemålere + IDer; visuell retning kan følge etter tekst-OK.
