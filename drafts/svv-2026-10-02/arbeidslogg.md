# SVV 2. okt – ingen votum i TCMV 6. okt (arbeidslogg)

Kilde hentet med curl 2.10.2026: vegvesen.no/.../forerstottesystemer/ (HTTP 200). Seksjon «Oppdatering 2. oktober om TCMV-møte» funnet. «Sist oppdatert: 3. juli 2026».

## Runde 1 utkast (forkastet)
Tittel: «Statens vegvesen bekrefter: Ingen avstemning 6. oktober» – lede «Det blir ingen … Det skriver …» (to Det-åpninger).
## Runde 2 hard redigering
- SVV i første setning, nyheten først.
- «Avstemming» bare i SVV-sitat; egen prosa bruker «avstemning» (som resten av siden). Ingen sitat med «avstemming» brukt.
- Fjernet «kan påvirke» (ikke i kilden) → «kan sende spørsmål og kommentarer».
- Juni-fakta (Norge et av få land med skriftlige spørsmål) fra samme SVV-side.
## Runde 3 rettskrivning
- Kolon + ikke-setning → liten bokstav (tittel). Kolon + helsetning → stor bokstav ikke brukt.
- Komma etter innskutt leddsetning «så lenge …, og har …».
- «ikke engang» (Bokmålsordboka: engang adv.). «junimøtet», «artikkel 39-sak», «EU-votum», «TCMV-ja».
- Tankestrek (–) i ny prosa.
## Runde 4 klar-språk / anti-maskin
- Varierte setningslengder (4–30 ord). Kort punchlinje: «Denne gangen sendte Norge ingenting.»
- Ingen tomme intensiver. Ingen anglicismer.
- Forkortelser forklart: SVV, TCMV (EUs tekniske komité for motorvogner), FN Reg. 171 (FN-regelverket for førerstøttesystemer, DCAS).
## Runde 5 UI/JSON-synk
- status.json tcmv.*, norge_denne_maneden.kommentar, timeline 2.10 + 6.10, sjanse_historikk 2.10.
- europa-feed standings + nytt item øverst.
- svv-siste.json.
- index.html: kun statisk fallback-prosa (FAQ JSON-LD, cd-note, etikett) + fallback-tall 30→0 i span/data-prosent. JS urørt.
