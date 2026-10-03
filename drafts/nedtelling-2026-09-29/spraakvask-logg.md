# Nedtelling per land (29.09.2026) – mølle-logg

Omfang: ny side `/nedtelling/index.html`, `data/nedtelling.json` (32 land), én lenke i bunnteksten på forsiden, `sitemap.xml`.
Skills lest før vask: fsd-redaksjon, bie-stil, norsk-bokm-l, norsk-bokmaal-rettskrivning (inkl. references/llm-typiske-feil.md og tall-dato-tegn.md).

## Redaksjonelt avvik (meldt til CoS)
«FSD redaksjon» sier «ingen nye undersider». Ole ba uttrykkelig om `/nedtelling/` 29.09.2026. Forsidens toppnav er ikke gjeninnført; siden har bare én diskré lenke i bunnteksten.

## Hard redigering
- Nyheten først i ingressen: «FSD Supervised er godkjent i 8 av 27 EU-land. I Norge venter eierne fortsatt.»
- Vinkling: kritikk rettes mot ventetiden, ikke teknologien («Norske eiere venter fortsatt på Brussel – og deretter på Statens vegvesen»).
- Ingen norsk godkjenning og ingen norsk dato. Norge = «venter på EU-vedtak», estimat null.
- «Estimat» står på merkelappen over nedtellingen, i banneret øverst og i metoden. Lanserte land har ikke noe estimat, bare dokumentert dato.
- Kroatia: godkjenningen merket «Tesla Europe meldte …»; kroatisk vedtak ikke publisert (står i teksten).
- Slovenia: utrullingsdatoen hviler på eierinnlegg (står i teksten, sikkerhet middels).
- Belgia: 11.06 er Teslas kunngjøring; TeslaNorth skrev at bilene skulle få oppdateringen «i ukene som kommer». Sikkerheten er derfor satt ned til middels, og metoden sier «kunngjort av Tesla eller observert hos eiere».
- Estland: utrullingsdatoen er ikke bekreftet → `lansert_dato` null, og siden viser «utrullingsdato ikke bekreftet».

## Språkvask (rettskrivning)
- Setning som startet med tall («8 av 27 EU-land har …») er skrevet om: «FSD Supervised er godkjent i 8 av 27 EU-land.»
- Klokkeslett: nb-NO gir «23:30» → rettet i JS til «kl. 23.30» (Språkrådet).
- Forkortelser forklart første gang: RDW (nederlandsk typegodkjenningsmyndighet), TCMV (EUs tekniske komité for motorkjøretøy), KBA, AVP, CSDD, Traficom, Transpordiamet, ASTRA.
- «om CSDD ikke finner …» → «hvis CSDD ikke finner …» (tydeligere betingelse).
- «meldte utrulling» → «meldte at utrullingen startet» / «kunngjorde utrulling» (mer presist verb).
- «Tesla sier selskapet» → «Tesla sier at selskapet» (tydeligere leddsetning).
- «ikke godkjenner på egen hånd og venter» → «ikke vil godkjenne på egen hånd, men venter» (komma foran «men»).
- «under polske forhold» → «på polske veier»; «Tidspunktet for en nasjonal avgjørelse avhenger av» → «Når en nasjonal avgjørelse kommer, avhenger av» (klart språk).
- Hellas: «en lov for å anerkjenne» → «at det vil legge fram et lovforslag som anerkjenner» (mer presist; «fram» er brukt konsekvent).
- Tankestrek (–) i innskudd og i tittel, bindestrek bare i sammensetninger (EU-vedtak, EØS-avtalen, EU-befolkningen, nivå 2-førerstøtte).
- Desimalkomma (12,7 %, 1,5 dager), mellomrom foran %.
- Datoer i prosa: «29. september 2026»; ISO bare i JSON.

## Klart språk / anti-maskin
- Korte kort-tekster, varierte åpninger (ikke tre «Det …» på rad), aktive verb.
- Ingen tomme forsterkere, ingen «hen», ingen videotidskoder (validatoren sjekker «hen» og `[mm:ss`).
- Anglisismer: «rollout» → utrulling; «estimate» → estimat. Produktnavn uoversatt (FSD Supervised, Tesla Europe).

## Bevisst urørt
- Egennavn og organnavn: RDW, TCMV, KBA, AVP, CSDD, Traficom, Transpordiamet, ASTRA, Færdselsstyrelsen, Statens vegvesen.
- URL-er og kildetitler.
- JS-logikk: `esc()` bruker numeriske tegnkoder (`"&#" + charCode + ";"`), ingen navngitte HTML-entiteter.

## Faktagrunnlag for metoden
Ventetid fra godkjenning til første dokumenterte utrulling: NL 1 (10.→11.04), LT 0 (20.05), DK 2 (9.→11.06), BE 1 (10.→11.06), SI 3 (7.→10.09), CZ 2 (21.→23.09). Median 1,5 → 2 dager. Kroatia: 29.09 + 2 = 1. oktober 2026 (estimat).

## Resultat
Hard språksjekkliste: bestått. Validator: `python3 scripts/validate_nedtelling.py` → 0 feil, 0 advarsler.

---

# Runde 2 (30.09.2026): scenariomodell – alle land får dato

Omfang: `nedtelling/index.html` (ingress, meta/OG/Twitter, seksjoner, kortmerker, metodeboks, Norge-kort), `data/nedtelling.json` (versjon 2: `modell`-blokk, `metode`/`modell_steg`/`fakta` per land), maltekster i `scripts/modell_nedtelling.py`, `scripts/validate_nedtelling.py`, `daglig-oppdatering.md`.
Skills lest på nytt før vask: fsd-redaksjon, bie-stil, norsk-bokm-l, norsk-bokmaal-rettskrivning (komma.md, forvekslinger.md, llm-typiske-feil.md).

## Redaksjonelt
- Oles bestilling 30.09: ingen «Ingen estimat ennå». Seksjonen er fjernet. To nye seksjoner: «Estimat ut fra kildene» (observert) og «Modellert estimat».
- Skillet står på hvert kort: merkelappen «estimat» (oransje) eller «modellert estimat» (lilla) + «modellsteg N». Hver begrunnelse starter med «Modellsteg …».
- Antagelser er merket med ordet «antagelse» der de brukes: TCMV-dato 1. desember 2026, påslag 30 og 180 dager, EØS-etterslep for Island og Liechtenstein.
- Norge: aldri omtalt som godkjent. Datoen er betinget («Gjentar det seg, får norske eiere FSD Supervised først 27. juli 2028 – mer enn ett år etter EU-landene»). Kritikken rettes mot etterslepet (BlueCruise: 470 dager), ikke mot teknologien. Kortteksten: «… og deretter på Statens vegvesen, som brukte 470 dager på BlueCruise.»
- Meta: «Norge: ingen estimat ennå» → «Norge havner bakerst i modellen fordi Statens vegvesen venter på EU» / «Norge havner bakerst i køen» (stemmer: NO/IS/LI har seneste dato).

## Faktagrunnlag (sjekket 30.09)
- Signal → vedtak: BE 12.05 (VRT: De Ridder gir testlov) → 10.06 = 29 d; CZ 10.06 (Autohled: departementet uttaler seg første gang på X, onsdag 10. juni) → 21.09 = 103 d; SI 11.07 (Portal24: Vrtovec «v kratkem tudi pri nas») → 07.09 = 58 d; HR 10.09 (DZM til Autonet, via eletric-vehicles.com) → 29.09 = 19 d. Median 43,5 → 44, maks 103. LT/EE/DK utelatt (ingen datert myndighetssignal funnet), NL utelatt (ga selve godkjenningen).
- Signaldatoer for åpne saker: LV 21.09 (bb.lv), FI 23.06 (Traficom), GR 20.05 (evwire), IE 10.05 (RTÉ), IT 13.07 (teslers.it).
- TCMV → EU-godkjenning: ETSC 20.03.2024 («met … this week and approved» BlueCruise og BMW) → Ford 30.07.2024 («following approval by the European Commission») = 132 d.
- EU → Norge: Ford 30.07.2024 → Ford Motor Norge 12.11.2025 («Statens vegvesen og Samferdselsdepartementet har konkludert at EUs godkjenning av BlueCruise også er gjeldende i Norge») = 470 d.
- Kroatia 30.09: fortsatt ikke rapportert utrullet (Tesla: «Rollout will begin soon»). Estimat 1. oktober står.

## Språkvask (rettskrivning)
- Komma: fjernet komma foran etterstilt «fordi»-setning (3 steder: meta og metodeboks) – Språkrådet: normalt ikke komma foran etterstilt leddsetning.
- Komma etter innskutt nødvendig relativsetning beholdt: «I landene som har godkjent, gikk det …»; «At Island bruker like lang tid, er en antagelse.»
- «bruker vi lengste ventetid» → «bruker vi den lengste ventetiden» (bestemt form med adjektiv krever «den»).
- «Til slutt kommer ventetiden til utrulling» → «Til slutt legger vi på ventetiden til utrulling» (aktivt verb, samme verb som i resten av metoden).
- «Der ingen vedtak finnes» → «Der det ikke finnes noe vedtak» (mer naturlig ordstilling).
- «TCMV sa ja uka fram til 20. mars» → «i uka fram til»; komma mellom to helsetninger i parentes → semikolon.
- «Det er en antagelse: Ingen avstemning …» → «Datoen er en antagelse. Ingen avstemning …» (to korte setninger).
- Tall: «to dager» med bokstaver (≤ 12) i maltekstene via funksjon `antall()`; 30, 44, 103, 132, 180, 470 med sifre. Desimalkomma (43,5; 1,5).
- «antagelse» valgt (Bokmålsordboka har antagelse/antakelse som sidestilte former) og brukt konsekvent. «fram» konsekvent.
- Tankestrek (–) i «Steg 1 – åpen nasjonal sak» osv. og i Norge-teksten; pil (→) bare i merket «modellsteg 1 → 2».

## Klart språk / anti-maskin
- Maltekstene er kortet ned og variert: steg 4 åpner med «Uten en kjent nasjonal sak …» (unngår gjentakelse av «Vi har ikke funnet noen offentlig nasjonal sak» rett før), steg 5 bruker «(utenfor EU og EØS)» i stedet for å gjenta landnavnet.
- GB-fakta skrevet om for ikke å si «står utenfor» to ganger.
- Ingen tomme forsterkere, ingen «hen», ingen tidskoder (validatoren sjekker også `fakta`).

## Bevisst urørt
- Egennavn: BlueCruise, Ford, TCMV, RDW, CSDD, Traficom, Statens vegvesen, Samferdselsdepartementet. URL-er.
- JS-logikk utenom tekst. `esc()` bruker fortsatt numeriske tegnkoder.

## Resultat
Hard språksjekkliste: bestått. `python3 scripts/modell_nedtelling.py --check` → 0 avvik. `python3 scripts/validate_nedtelling.py` → 0 feil, 0 advarsler. `node --check` på skriptet i `nedtelling/index.html`: OK.

---

# Runde 3 – Kroatia lansert (03.10.2026)

## Faktagrunnlag (sjekket 03.10 med WebFetch)
- Slobodna Dalmacija, 1. oktober 2026 kl. 16:24: «Tesla je omogućila korištenje sustava Full Self-Driving (FSD) … i u Hrvatskoj». En eier kjører med systemet i sentrum av Šibenik. Tittelen «Do jučer nam se ovo činilo kao SF» betyr «fram til i går virket dette som science fiction». Den er retorisk og oppgir ingen dato for utrullingen.
- Moj Kraj, 1. oktober 2026 kl. 16:50: siterer Slobodna Dalmacija og har ingen egen dato.
- Søk (dnevno.hr, npscp.hr, portofon, notateslaapp, croatiaweek): Tesla meldte godkjenning 29.09 («Rollout will begin soon»). Ingen kilde oppgir en tidligere eierdato.
- Konklusjon: `lansert_dato` = 2026-10-01 (artikkeldatoen, første daterte eierrapport). Begrunnelsen sier at nøyaktig dato for utrullingen ikke er kjent. Samme nivå som Slovenia/Estland (eierrapporter), sikkerhet middels.
- Utrullingsmedian med HR (29.09 → 01.10 = 2 d): NL 1, LT 0, DK 2, BE 1, SI 3, CZ 2, HR 2 → median 2 (før 1,5). Brukt verdi er fortsatt 2, så ingen modellerte datoer flytter seg (`modell_nedtelling.py --today 2026-10-03`: 24 land, 0 avvik).

## Språkmølla (fire skills) på ny synlig tekst
Gjelder HR-begrunnelsen, tidslinjelinja i status.json og metodelinja «Medianen er 2 dager.»
- Rettskrivning: «Avisa Slobodna Dalmacija viste 1. oktober …» i stedet for å starte setningen med et tall. «datoen for artikkelen» → «artikkeldatoen». Stor bokstav etter kolon i tidslinja fordi en hel setning følger.
- Klart språk: korte setninger og én opplysning per setning. Usikkerheten står eksplisitt: «Nøyaktig dato for utrullingen er ikke kjent».
- Anti-maskin: ingen forsterkere og ingen gjentatte åpninger. Metodelinja viser ikke lenger «rundet opp til 2» når medianen allerede er 2 (JS-betingelse).
- Tall: sifre i målelista («NL 1, LT 0 … Medianen er 2 dager»), fordi tallene står i en rekke med andre måltall. Unntaket er bevisst.
- Statisk reservetekst for «Sist oppdatert» er endret fra 29. september til 3. oktober 2026. JS overskriver den fra JSON.

## Resultat
`validate_nedtelling.py` → exit 0. `node --check` OK. `esc()` er uendret og bruker numeriske tegnkoder.
