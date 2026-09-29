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
