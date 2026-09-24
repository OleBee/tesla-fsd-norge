# Utkast: Historie — Autopilot og FSD
Arne Breistrand · 19. september 2026 · markdown til `historie.html` · **ikke pushet**

**Redaksjonell linje (Kåre):** Autopilot og FSD er to separate Level 2-pakker. Ikke skriv at «AP ble til FSD». HW og versjonsnavn kun med kilde. Norge/SVV/EØS som egne punkter.

**Foreslått URL:** `https://fsdnorge.no/historie.html` · nav: Historie

---

## Forslag til side-struktur

1. Ingress + «hva denne siden er»
2. Faktaboks: tre (fire) pakker
3. Hardware HW1–HW4 (kort, illustrerbart — Petter)
4. Tidslinje 2014→nå (kronologisk)
5. Blokk: EU og Norge (skilt fra US-historikk)
6. Kilder

---

## 1) Ingress (utkast)

**H1:** Autopilot og FSD — historien fram til nå

**Kicker:** Tesla · Level 2 · pakker · hardware · EU/Norge

**Lede:**
Tesla selger førerstøtte i flere pakker. Autopilot og Full Self-Driving (Supervised) er begge SAE nivå 2: føreren er alltid ansvarlig. De er **ikke** det samme produktet, og Autopilot er ikke «grunnlaget som ble til FSD» i produktspråket. Denne siden er en faktabasert tidslinje for hardware, pakkenavn og viktige milepæler — med særskilt plass til EU og Norge.

Sist oppdatert: [dato ved push]

---

## 2) Faktaboks — pakkene (skill tydelig)

| Pakke | Hva det typisk dekker (marked/år avgjør) | Merk |
|-------|------------------------------------------|------|
| **Autopilot** | Traffic-Aware Cruise Control + Autosteer (filholder / hastighetstilpasning) | Standard eller basispakke i mange markeder. Level 2. |
| **Enhanced Autopilot (EAP)** | Utvidet motorvei-pakke: bl.a. Navigate on Autopilot, automatiske filskift, Autopark, Summon (der tilgjengelig) | Egen betalt midtpakke fra 2016; senere trukket inn/erstattet av FSD i flere markeder. |
| **Full Self-Driving / FSD Capability** | Tidligere produktnavn for den øverste pakken (bykjøring, lys/skilt, osv.) | Pakkenavn før «Supervised»-etiketten ble standard. |
| **FSD (Supervised)** | Dagens navn på den øverste Level 2-pakken: rute, by, lys/skilt, parkering m.m. under aktiv overvåkning | Krever fører. Ikke autonomt. Regional godkjenning avgjør hva som er live. |

**Kort skille-setning til layout:**
> Samme kameraer og datamaskin kan kjøre flere pakker. Pakken du har betalt for — og hva myndighetene tillater i landet ditt — avgjør hva som er påskrudd. Hardware alene er ikke det samme som FSD-godkjenning.

Kilder til pakkeskill: Tesla FSD-produktside (tesla.com/fsd); Tesla eierhåndbok FSD Supervised; Not a Tesla App-oversikt AP/EAP/FSD (sekundær, merket).

---

## 3) Hardware HW1–HW4 (Petter: diagram)

| Gen | Ca. produksjon | Sensor/compute (kort) | Merknad |
|-----|----------------|----------------------|---------|
| **HW1** | ~sep 2014 – okt 2016 | Mobileye EyeQ3, 1 fremre kamera + radar + ultrasonikk | Første Autopilot-hardware. Kan ikke kjøre moderne FSD. |
| **HW2** | okt 2016 – ~2017 | 8 kameraer, Nvidia Drive PX 2 | «Autopilot 2.0» / Tesla Vision. Start på egen multi-kamera-stack. |
| **HW2.5** | ~2017 – 2019 | Forbedret/redundant compute, samme 8-kamera-layout | Ofte oppgraderbar til HW3-datamaskin for FSD-kunder (historikk om pris/vilkår varierer — ikke lov nå). |
| **HW3** | fra ~apr 2019 | Tesla «FSD Computer» (egen SoC) | Bærebjelke for FSD Beta / FSD Supervised på millioner av biler. Radar/ultrasonikk senere fjernet på mange biler (vision-only). |
| **HW4 / AI4** | fra jan 2023 | Nyere kameraer + kraftigere SoC | Start Model S/Y refresh; FSD på HW4 kom gradvis. Senere versjoner bruker native HW4-oppløsning (rapportert fra v13-familien). |

Kilder: Wikipedia *Tesla Autopilot hardware* (samlet oversikt — bruk som sekundær); Electrek HW2-annonsering 19. okt 2016; Tesla support «Full Self-Driving Computer» (sjekk bil); Carnex/Find My Electric som sekundære HW-guider.

**Advarsel i brødtekst:** Oppgraderingsrettigheter HW2/HW2.5→HW3 har endret seg over tid. Ikke lov leseren gratis oppgradering uten å sjekke egen ordre/Tesla.

---

## 4) Tidslinje (kronologisk — hovedstoff)

### 2014–2015 · Autopilot starter
- **Sep/okt 2014:** Model S får HW1 (Mobileye). Autopilot som hardware-forberedelse.
- **Okt 2015:** Autopilot software v7.0 ruller ut — første bredde aktivering av Autosteer / TACC på HW1.
  - Kilde: samtidige rapporter / Wikipedia Autopilot (sekundær); bekreft mot Tesla blog/release notes der mulig.

### 2016 · Brudd med Mobileye, HW2, nye pakker
- **2016:** Partnerskapet med Mobileye avsluttes; Tesla går over til egen vision-stack.
- **19. okt 2016:** Tesla kunngjør at alle nye biler får hardware for «full self-driving capability»; introduserer **Enhanced Autopilot** og **Full Self-Driving**-pakke som separate kjøpsvalg ved siden av basis-Autopilot.
  - Kilde: Electrek 19.10.2016 (Tesla-kunngjøring).
- **Merk:** Her skilles pakkene eksplisitt i Teslas eget produktspråk — ikke «AP ble FSD».

### 2017 · Enhanced Autopilot fase 1
- **Des 2016 / jan 2017:** Første fase av Enhanced Autopilot på HW2 (målt/forsiktig utrulling; ikke feature-komplett mot gammel HW1 med én gang).
  - Kilde: Electrek 1.1.2017 (release notes).

### 2018 · Navigate on Autopilot
- **Okt 2018:** Navigate on Autopilot ruller ut i USA for EAP/FSD-kjøpere (på-ramp til avkjøring med filforslag; tidlig versjon krevde bekreftelse med blinklys).
  - Kilde: Electrek 27.10.2018 (Tesla-sitat i artikkel).

### 2019 · HW3 / FSD Computer
- **Fra april 2019:** HW3 (Tesla FSD Chip) i produksjon.
  - Kilde: Wikipedia Autopilot hardware (dato); Tesla support om FSD Computer.

### 2020 · FSD Beta (USA)
- **20. okt 2020:** FSD Beta begynner begrenset utrulling i USA (bykjøring under overvåkning — fortsatt Level 2).
  - Kilde: Electrek 20.10.2020 (Musk/Tesla-kunngjøring samme kveld).
- **Merk for Norge/EU:** Dette er **ikke** europeisk typegodkjenning. US- og EU-software er ikke én-til-én (RDW understreker dette senere).

### 2021–2023 · Vision-only, HW4, bredere FSD Beta
- **2021+:** Radar fjernes gradvis på nye biler; stack går mot vision.
- **2022:** Ultrasonikk fases ut på mange nye biler (Tesla Vision / parkering via kamera).
- **Nov 2022:** FSD Beta åpnes for alle nordamerikanske eiere som har kjøpt opsjonen (rapportert).
- **Jan 2023:** HW4 begynner å skips i refreshed Model S/Y; FSD på HW4 kommer etter hvert, ikke day-one feature-komplett.
  - Kilder: Wikipedia Autopilot hardware; samtidige Electrek/Teslarati — merk sekundær der primær mangler.

### 2024 · «Beta» ut, «Supervised» inn
- **Mars/april 2024:** Tesla dropper «FSD Beta»-navnet i release notes; systemet omtales som **FSD (Supervised)** (bl.a. 2024.3.10 / v12.3.3-familien).
  - Kilde: Teslarati 31.3.2024; Drive Tesla Canada 1.4.2024 (release notes sitert).
- **Merk:** Navneendring ≠ SAE-nivåendring. Fortsatt førerstøtte Level 2.

### 2025–2026 · Europa: artikkel 39, RDW, TCMV, Norge
*(Egen seksjon under — ikke bland inn i US-hype-linjen uten tydelig geografi-merke.)*

---

## 5) EU og Norge (egen blokk)

### Hva som er vedtak / offisielt
- **10. april 2026 — RDW (Nederland):** Typegodkjenning for **FSD Supervised** med midlertidig/nasjonal gyldighet i Nederland under artikkel 39-sporet. RDW understreker: ikke selvkjørende; føreren ansvarlig; EU-bred adgang krever senere avstemning blant medlemsland.
  - Primærkilde: [RDW 10.04.2026](https://www.rdw.nl/en/news/2026/rdw-explanation-of-european-type-approval-tesla-with-provisional-validity-in-the-netherlands)
- **Mai–juni 2026:** Flere EU-land anerkjenner den nederlandske saken nasjonalt (Litauen, Estland, Danmark, Belgia — datoer som på fsdnorge index/TCMV).
- **5. mai 2026:** RDW presenterer saken i TCMV; Norge deltar uten stemmerett (SVV).
- **30. juni 2026:** TCMV-diskusjon uten avstemning (SVV).
- **3. juli 2026:** SVV oppdaterer infosiden: kritisk til deler av RDW-unntakene; kundedemoer ikke godkjent før Tesla endrer villedende materiell; neste TCMV-møte i **oktober**, avstemning *kan* komme.
  - Primærkilde: [Statens vegvesen — førerstøttesystemer](https://www.vegvesen.no/fag/trafikk/its-portalen/its-i-statens-vegvesen/metr/forerstottesystemer/)
- **7. september 2026:** Slovenia rapportert som sjette land med nasjonal kundegodkjenning (Tesla Europe / huben).

### Hva som er rykte / sekundært
- **6. oktober 2026** som konkret avstemningsdato: Tesla Europe / presse / trackere — **ikke** bekreftet i komitologiregisteret som agenda per hubens siste sjekk. SVV sier bare «oktober».
- Sjansetall på fsdnorge er uoffisielle skjønnstall.

### Norge — statuslinje (skal matche index)
- **Ikke kundegodkjent.** Begrenset testing med Tesla-trente sikkerhetsførere.
- EØS: Norge har ikke TCMV-stemme; følger normalt EU-unntak, men kan motsette seg av sikkerhetshensyn.
- Autopilot/TACC som allerede er tillatt under egne godkjenninger er **ikke** det samme som FSD Supervised-kundegodkjenning.

---

## 6) Forslag til brødtekst-bokser (pull quotes / callouts)

**Callout A — pakkeskill**
> Autopilot holder deg i filen og tilpasser fart. FSD Supervised kan i tillegg håndtere by, kryss og rute — der det er godkjent. Begge krever at du følger med.

**Callout B — hardware ≠ godkjenning**
> HW3 eller HW4 i bilen betyr ikke at FSD Supervised er lovlig å aktivere der du bor.

**Callout C — USA ≠ EU**
> RDW: FSD Supervised i USA er ikke den samme software-versjonen som i EU. Sammenlign ikke milepæler én-til-én.

---

## 7) Nav / teknisk (til Kåre + Petter)

- Ny fil: `historie.html`
- Nav på alle sider: `Historie` mellom Europa og (eller etter) Norge — Kåre velger rekkefølge. Forslag: Norge · Historie · TCMV · Europa
- Canonical: `https://fsdnorge.no/historie.html`
- Behold `site.css`, badge-språk, L2-disclaimer i footer
- Petter: tidslinje mobil (vertikal), HW-diagram, AP-vs-FSD-illustrasjon — ingen Tesla-pressbilder
- Ingen endring av automasjons-IDer på index/tcmv/europa

---

## 8) Kildeliste (synlig på siden)

### Primære / myndighet
1. RDW — type approval FSD Supervised (10.04.2026): https://www.rdw.nl/en/news/2026/rdw-explanation-of-european-type-approval-tesla-with-provisional-validity-in-the-netherlands
2. Statens vegvesen — ADAS / Tesla FSD: https://www.vegvesen.no/fag/trafikk/its-portalen/its-i-statens-vegvesen/metr/forerstottesystemer/
3. EUR-Lex — forordning (EU) 2018/858 (art. 39-kontekst): https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32018R0858

### Tesla / produkt
4. Tesla — Full Self-Driving (Supervised): https://www.tesla.com/fsd
5. Tesla eierhåndbok — FSD (Supervised) (region/modellavhengig URL)
6. Tesla support — Full Self-Driving Computer (HW-sjekk)

### Samtidig journalistikk (dato-festede milepæler)
7. Electrek — HW2 / FSD-hardware-kunngjøring 19.10.2016: https://electrek.co/2016/10/19/tesla-fully-autonomous-self-driving-car/
8. Electrek — Enhanced Autopilot fase 1, 01.01.2017: https://electrek.co/2017/01/01/tesla-enhanced-autopilot-release-notes/
9. Electrek — Navigate on Autopilot, 27.10.2018: https://electrek.co/2018/10/27/tesla-navigate-on-autopilot-demo-rollout/
10. Electrek — FSD Beta rollout, 20.10.2020: https://electrek.co/2020/10/20/tesla-full-self-driving-beta-rollout-elon-musk-slow-cautious/
11. Teslarati — FSD (Supervised) erstatter Beta, 31.03.2024: https://www.teslarati.com/tesla-formally-drops-fsd-beta-moniker/
12. Reuters — EU-vei for FSD, 30.06.2026: https://www.reuters.com/business/finance/teslas-road-full-self-driving-approval-europe-2026-06-30/

### Sekundære (bruk sparsomt, merk)
13. Wikipedia — Tesla Autopilot / Autopilot hardware (oversikt HW-datoer)
14. Not a Tesla App — AP vs EAP vs FSD
15. fsdnorge index/TCMV (egne datoer for EU-land 2026 — kryssjekk mot primær)

---

## 9) Åpne punkter til Kåre

1. Nav-rekkefølge: Historie før eller etter TCMV?
2. Skal Speed Offset / svensk nei (2026) inn som eget tidslinjepunkt, eller kun under EU-blokken?
3. Hvor dypt på software-versjoner (v9, v10, v11, v12, v13)? Forslag: bare navngitte milepæler med kilde (Beta 2020, Supervised 2024, HW4-native v13) — ikke full versjonstabell.
4. Grønt på struktur → jeg skriver HTML; Petter illustrasjoner parallelt.

