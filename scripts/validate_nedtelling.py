#!/usr/bin/env python3
"""Validerer data/nedtelling.json (fsdnorge.no/nedtelling/).

Bruk:  python3 scripts/validate_nedtelling.py [--today YYYY-MM-DD]
Avslutter med kode 1 ved feil (FEIL), 0 ellers. ADVARSEL stopper ikke.
Kjøres fra repo-roten. Sjekker skjema, datoer, metodekonsistens og at
godkjente land stemmer med data/status.json.
"""
import json, math, re, statistics, sys
from datetime import date, datetime

STATUSER = {"lansert", "godkjent, utrulling snart", "venter på anerkjennelse",
            "venter på EU-vedtak", "ukjent"}
SIKKERHET = {"lav", "middels", "høy"}
EU27 = set("AT BE BG CY CZ DE DK EE ES FI FR GR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK".split())
PAAKREVD_ANDRE = {"NO", "IS", "LI", "CH", "GB"}
FELT = ["land", "iso", "status", "estimert_dato", "sikkerhet", "begrunnelse", "kilder", "sist_oppdatert"]
FORBUDT = [r"\bhen\b", r"\[\d{1,2}:\d{2}", r"&(amp|lt|gt|quot|#\d+);"]

feil, adv = [], []
def F(m): feil.append(m)
def A(m): adv.append(m)

def ymd(v, hva):
    if not isinstance(v, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
        F(f"{hva}: ikke ISO-dato (YYYY-MM-DD): {v!r}"); return None
    try: return date.fromisoformat(v)
    except ValueError: F(f"{hva}: ugyldig dato {v!r}"); return None

def main():
    today = date.today()
    if "--today" in sys.argv:
        today = date.fromisoformat(sys.argv[sys.argv.index("--today") + 1])
    try:
        d = json.load(open("data/nedtelling.json", encoding="utf-8"))
    except Exception as e:
        print(f"FEIL: data/nedtelling.json kan ikke leses som JSON: {e}"); return 1

    for k in ["sist_oppdatert_iso", "oppsummering", "metode", "land"]:
        if k not in d: F(f"toppnivå mangler «{k}»")
    try:
        su = datetime.fromisoformat(d.get("sist_oppdatert_iso", ""))
        if su.tzinfo is None: F("sist_oppdatert_iso mangler tidssone")
        elif su.date() > today: F(f"sist_oppdatert_iso ligger i fremtiden: {su}")
        elif (today - su.date()).days > 2: A(f"sist_oppdatert_iso er {(today - su.date()).days} dager gammel")
    except ValueError:
        F("sist_oppdatert_iso er ikke ISO 8601 med tid")

    land = d.get("land", [])
    isos = [c.get("iso") for c in land]
    dup = {i for i in isos if isos.count(i) > 1}
    if dup: F(f"dupliserte iso-koder: {sorted(dup)}")
    mangler = (EU27 | PAAKREVD_ANDRE) - set(isos)
    if mangler: F(f"mangler land: {sorted(mangler)}")

    lag = []
    for c in land:
        n = f"{c.get('land', '?')} ({c.get('iso', '?')})"
        for k in FELT:
            if k not in c: F(f"{n}: mangler felt «{k}»")
        st = c.get("status")
        if st not in STATUSER: F(f"{n}: ugyldig status {st!r}")
        if c.get("sikkerhet") not in SIKKERHET: F(f"{n}: ugyldig sikkerhet {c.get('sikkerhet')!r}")
        if not isinstance(c.get("iso"), str) or not re.fullmatch(r"[A-Z]{2}", c.get("iso", "")):
            F(f"{n}: iso må være to store bokstaver")
        b = c.get("begrunnelse", "")
        if not isinstance(b, str) or len(b) < 20: F(f"{n}: begrunnelse mangler eller er for kort")
        elif len(b) > 320: A(f"{n}: begrunnelse er lang ({len(b)} tegn)")
        for txt in [b, c.get("tidligst", "") or ""]:
            for pat in FORBUDT:
                if re.search(pat, txt): F(f"{n}: forbudt mønster {pat} i tekst")
        k = c.get("kilder")
        if not isinstance(k, list) or not k: F(f"{n}: kilder må være en ikke-tom liste")
        else:
            for u in k:
                if not isinstance(u, str) or not u.startswith("https://"): F(f"{n}: kilde er ikke https-URL: {u!r}")
        so = ymd(c.get("sist_oppdatert"), f"{n} sist_oppdatert")
        if so and so > today: F(f"{n}: sist_oppdatert i fremtiden")
        e = c.get("estimert_dato")
        ed = None
        if e is not None:
            ed = ymd(e, f"{n} estimert_dato")
        g = ymd(c["godkjent_dato"], f"{n} godkjent_dato") if c.get("godkjent_dato") else None
        if st == "lansert":
            if e is not None: F(f"{n}: lansert land skal ha estimert_dato null (bruk lansert_dato)")
            if "lansert_dato" not in c: F(f"{n}: lansert land mangler lansert_dato (kan være null)")
            if not g: F(f"{n}: lansert land mangler godkjent_dato")
            ld = ymd(c["lansert_dato"], f"{n} lansert_dato") if c.get("lansert_dato") else None
            if ld and g:
                if ld < g: F(f"{n}: lansert_dato før godkjent_dato")
                lag.append({"iso": c["iso"], "dager": (ld - g).days})
            if ld and ld > today: F(f"{n}: lansert_dato i fremtiden")
        if st == "godkjent, utrulling snart":
            if not g: F(f"{n}: godkjent land mangler godkjent_dato")
            if ed is None: A(f"{n}: godkjent land uten estimat (metoden gir normalt et estimat)")
        if st in ("ukjent",) and e is not None:
            F(f"{n}: status «ukjent» kan ikke ha estimat (metoden krever grunnlag)")
        if st == "venter på EU-vedtak" and e is not None and not d.get("eu_spor", {}).get("dato_for_votum_kjent"):
            F(f"{n}: EU-estimat uten kjent dato for votum (eu_spor.dato_for_votum_kjent=false)")
        if e is None and c.get("sikkerhet") == "høy" and st != "lansert":
            A(f"{n}: sikkerhet «høy» uten estimat")
        if ed and ed < today and st != "lansert":
            A(f"{n}: estimatet {e} er passert – sjekk om utrullingen er bekreftet, og oppdater status/estimat")
        if c.get("iso") == "NO" and st in ("lansert", "godkjent, utrulling snart"):
            try:
                svv = json.load(open("data/svv-siste.json", encoding="utf-8"))
                if not svv.get("norge_kundegodkjent"):
                    F("NO: status sier godkjent/lansert, men data/svv-siste.json har norge_kundegodkjent=false")
            except Exception:
                F("NO: godkjent/lansert, men data/svv-siste.json kan ikke leses")

    # Metode: median ventetid må stemme med grunnlaget og brukes i estimater
    m = d.get("metode", {})
    if lag:
        med = statistics.median([x["dager"] for x in lag])
        brukt = math.ceil(med)
        if m.get("utrullingsforsinkelse_median_dager") != med:
            F(f"metode: median i fila ({m.get('utrullingsforsinkelse_median_dager')}) ≠ beregnet ({med})")
        if m.get("utrullingsforsinkelse_brukt_dager") != brukt:
            F(f"metode: brukt forsinkelse ({m.get('utrullingsforsinkelse_brukt_dager')}) ≠ opprundet median ({brukt})")
        gr = sorted((x["iso"], x["dager"]) for x in m.get("grunnlag", []))
        if gr != sorted((x["iso"], x["dager"]) for x in lag):
            F("metode.grunnlag stemmer ikke med lanserte land (godkjent_dato/lansert_dato)")
        for c in land:
            if c.get("status") == "godkjent, utrulling snart" and c.get("godkjent_dato") and c.get("estimert_dato"):
                forvent = date.fromordinal(date.fromisoformat(c["godkjent_dato"]).toordinal() + brukt)
                if c["estimert_dato"] != forvent.isoformat():
                    F(f"{c['land']}: estimert_dato {c['estimert_dato']} ≠ godkjent + {brukt} dager ({forvent})")

    # Kryss mot status.json
    try:
        s = json.load(open("data/status.json", encoding="utf-8"))
        navn = {c["land"]: c for c in land}
        godkj_nt = {c["land"] for c in land if c.get("gruppe") == "EU" and c.get("status") in ("lansert", "godkjent, utrulling snart")}
        godkj_s = {x["land"] for x in s.get("eu_land", [])}
        if godkj_nt != godkj_s:
            F(f"godkjente EU-land avviker fra status.json: bare nedtelling={sorted(godkj_nt - godkj_s)}, bare status={sorted(godkj_s - godkj_nt)}")
        for x in s.get("eu_land", []):
            c = navn.get(x["land"])
            if c and c.get("godkjent_dato") != x.get("dato"):
                F(f"{x['land']}: godkjent_dato {c.get('godkjent_dato')} ≠ status.json {x.get('dato')}")
        o = d.get("oppsummering", {})
        if o.get("eu_godkjent") != len(godkj_s): F("oppsummering.eu_godkjent ≠ antall i status.json")
        if o.get("eu_befolkning_prosent") != s.get("eu_andel_befolkning_prosent"):
            F("oppsummering.eu_befolkning_prosent ≠ status.json")
    except FileNotFoundError:
        A("data/status.json finnes ikke – hopper over kryssjekk")

    for a in adv: print("ADVARSEL:", a)
    for f in feil: print("FEIL:", f)
    print(f"{len(land)} land sjekket · {len(feil)} feil · {len(adv)} advarsler")
    return 1 if feil else 0

if __name__ == "__main__":
    sys.exit(main())
