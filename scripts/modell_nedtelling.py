#!/usr/bin/env python3
"""Scenariomodell for data/nedtelling.json (fsdnorge.no/nedtelling/).

Regner ut estimert_dato, modell_steg og begrunnelse for alle land med
metode = "modell", ut fra parameterne i toppnivå-blokken «modell».

Bruk (fra repo-roten):
  python3 scripts/modell_nedtelling.py [--today YYYY-MM-DD]          # skriver fila
  python3 scripts/modell_nedtelling.py --check [--today YYYY-MM-DD]  # bare sammenlign
Endre aldri modellerte datoer for hånd: endre inndata og kjør skriptet.

Engelsk versjon (/en/countdown/): skriptet skriver også «begrunnelse» for de
modellerte landene i data/en/nedtelling.json, ut fra den engelske «fakta»
(skrives for hånd) og den engelske modellteksten under. --check feiler hvis
den engelske begrunnelsen er utdatert eller den engelske «fakta» mangler.

Inndata per land (metode = "modell"):
  modell_type  signal | eu | eos | ukjent | ikke_eu
  signal_dato  (bare for signal) dato for første offentlige signal om nasjonal sak
  fakta        kildebelagt faktatekst; modellteksten legges etter

EØS-land (modell_type = "eos") får et spenn i stedet for én dato:
  estimert_tidligst  EU-scenariet pluss utrullingsmedianen (antagelse: Norge
                     følger EU kort tid etter vedtaket; vi har ingen kilde for
                     hvor kort etterslepet blir)
  estimert_senest    EU-scenariet pluss BlueCruise-etterslepet (eos_presedens)
  estimert_dato      = estimert_tidligst (sortering og bakoverkompatibilitet)
"""
import json, math, statistics, sys
from datetime import date, timedelta

MND = ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august",
       "september", "oktober", "november", "desember"]
SPENN_FELT = ("estimert_tidligst", "estimert_senest")
ORD = ["null", "én", "to", "tre", "fire", "fem", "seks", "sju", "åtte", "ni", "ti", "elleve", "tolv"]


def nb(d):
    return f"{d.day}. {MND[d.month - 1]} {d.year}"


def antall(n, ental="dag", flertall="dager"):
    tall = ORD[n] if 0 <= n <= 12 else str(n)
    return f"{tall} {ental if n == 1 else flertall}"


MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]
WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]
EN_PATH = "data/en/nedtelling.json"


def en_dato(d):
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def en_antall(n, one="day", many="days"):
    tall = WORDS[n] if 0 <= n <= 12 else str(n)
    return f"{tall} {one if n == 1 else many}"


def D(s):
    return date.fromisoformat(s)


def beregn(d, today):
    """Returnerer (parametre, {iso: (estimert_dato, modell_steg, begrunnelse, spennfelt)}).

    spennfelt er {"estimert_tidligst": ..., "estimert_senest": ...} for EØS-land, ellers {}.
    """
    land = {c["iso"]: c for c in d["land"]}
    m = d["modell"]

    # Ventetid godkjenning -> utrulling (samme som metode-blokken)
    lag = []
    for c in d["land"]:
        if c.get("status") == "lansert" and c.get("godkjent_dato") and c.get("lansert_dato"):
            lag.append((D(c["lansert_dato"]) - D(c["godkjent_dato"])).days)
    r = math.ceil(statistics.median(lag))

    # Ventetid signal -> vedtak i godkjente land
    sg = []
    for g in m["signal_grunnlag"]:
        godkj = land[g["iso"]]["godkjent_dato"]
        sg.append({**g, "godkjent": godkj, "dager": (D(godkj) - D(g["signal"])).days})
    dager = [x["dager"] for x in sg]
    med_raa = statistics.median(dager)
    med = math.ceil(med_raa)
    maks = max(dager)

    tcmv = D(m["tcmv_dato"])
    eu_kraft = tcmv + timedelta(days=m["eu_ikrafttredelse_dager"])
    eu = eu_kraft + timedelta(days=r)
    eos = m["eos_etterslep_dager"]
    uk_m = m["ukjent_margin_dager"]
    ie_m = m["ikke_eu_margin_dager"]

    tcmv_txt = ((f"Tesla-saken står på agendaen til TCMV {nb(tcmv)}, med mulig avstemning. "
                 f"Vi antar et ja, men det er en antagelse.")
                if m.get("tcmv_dato_antatt", True) and m.get("votum_mulig") else
                f"Vi antar et ja i TCMV {nb(tcmv)}. Det er en antagelse; ingen avstemning er satt opp."
                if m.get("tcmv_dato_antatt", True) else
                f"TCMV skal stemme {nb(tcmv)}, og vi antar et ja.")
    eu_txt = (f"Modellsteg 2 (EU-scenariet): {tcmv_txt} For Fords BlueCruise gikk det "
              f"{m['eu_ikrafttredelse_dager']} dager fra ja i TCMV til EU-godkjenningen var på plass. "
              f"Med {antall(r)} til utrulling gir det {nb(eu)}.")

    ut = {}
    for c in d["land"]:
        if c.get("metode") != "modell":
            continue
        spenn = {}
        t = c["modell_type"]
        navn = c["land"]
        if t == "signal":
            s = D(c["signal_dato"])
            a = s + timedelta(days=med + r)
            b = s + timedelta(days=maks + r)
            if a > today:
                dato, steg = a, "1"
                txt = (f"Modellsteg 1: Første offentlige signal om en nasjonal sak kom {nb(s)}. I landene som har "
                       f"godkjent, gikk det i median {med} dager fra et slikt signal til vedtak. Med {antall(r)} "
                       f"til utrulling gir det {nb(dato)}.")
            elif b > today:
                dato, steg = b, "1 (lengste ventetid)"
                txt = (f"Modellsteg 1: Første offentlige signal om en nasjonal sak kom {nb(s)}. Medianen på {med} "
                       f"dager er passert uten vedtak, så vi bruker den lengste ventetiden vi har sett, {maks} dager. "
                       f"Med {antall(r)} til utrulling gir det {nb(dato)}.")
            else:
                dato, steg = eu, "1 → 2"
                txt = (f"Modellsteg 1 → 2: Første offentlige signal kom {nb(s)}, men selv den lengste ventetiden "
                       f"vi har sett, {maks} dager, er passert. Vi bruker derfor EU-scenariet: {nb(eu)}.")
        elif t == "eu":
            dato, steg, txt = eu, "2", eu_txt
        elif t == "eos":
            tidl, sen = eu + timedelta(days=r), eu + timedelta(days=eos)
            dato, steg = tidl, "3"
            spenn = {"estimert_tidligst": tidl.isoformat(), "estimert_senest": sen.isoformat()}
            if c["iso"] == "NO":
                txt = (f"Modellsteg 3 gir et spenn: {nb(tidl)} til {nb(sen)}. Tidligst hvis Norge følger EU kort tid "
                       f"etter vedtaket. Ingen kilde sier hvor kort, så vi legger {antall(r)} på EU-scenariet "
                       f"({nb(eu)}). Det er median ventetid til utrulling. Senest hvis det går like tregt som med Fords "
                       f"BlueCruise. Da tok den norske avklaringen {eos} dager.")
            else:
                txt = (f"Modellsteg 3 gir et spenn: {nb(tidl)} til {nb(sen)}. Tidligst: EU-scenariet ({nb(eu)}) pluss "
                       f"{antall(r)}. Senest: samme EØS-etterslep som Norge hadde med BlueCruise, {eos} dager. "
                       f"Begge datoene er antagelser for {navn}.")
        elif t == "ukjent":
            dato, steg = eu + timedelta(days=uk_m), "4"
            txt = (f"Modellsteg 4: Uten en kjent nasjonal sak bruker vi EU-scenariet ({nb(eu)}) og legger på "
                   f"{uk_m} dager. Påslaget er en antagelse, ikke en observasjon.")
        elif t == "ikke_eu":
            dato, steg = eu + timedelta(days=ie_m), "5"
            txt = (f"Modellsteg 5 (utenfor EU og EØS): Vi bruker EU-scenariet ({nb(eu)}) og legger på {ie_m} dager. "
                   f"Påslaget er en antagelse; vi har ingen observert presedens.")
        else:
            raise ValueError(f"{navn}: ukjent modell_type {t!r}")
        ut[c["iso"]] = (dato.isoformat(), steg, (c["fakta"].rstrip() + " " + txt).strip(), spenn)

    param = {
        "utrulling_dager": r,
        "signal_grunnlag": sg,
        "signal_median_dager": med_raa,
        "signal_brukt_dager": med,
        "signal_maks_dager": maks,
        "eu_vedtak_dato": eu_kraft.isoformat(),
        "eu_scenario_dato": eu.isoformat(),
        "eos_tidligst_dato": (eu + timedelta(days=r)).isoformat(),
        "eos_senest_dato": (eu + timedelta(days=eos)).isoformat(),
    }
    return param, ut


def beregn_en(d, en, today):
    """Engelsk begrunnelse for modellerte land: {iso: tekst}. Samme grener og datoer som beregn()."""
    param, ut = beregn(d, today)
    m = d["modell"]
    r, med, maks = param["utrulling_dager"], param["signal_brukt_dager"], param["signal_maks_dager"]
    eu, tcmv = D(param["eu_scenario_dato"]), D(m["tcmv_dato"])
    eos, uk_m, ie_m = m["eos_etterslep_dager"], m["ukjent_margin_dager"], m["ikke_eu_margin_dager"]
    tcmv_txt = ((f"The Tesla case is on the TCMV agenda for {en_dato(tcmv)}, with a possible vote. "
                 f"We assume a yes, but that is an assumption.")
                if m.get("tcmv_dato_antatt", True) and m.get("votum_mulig") else
                f"We assume a yes in TCMV on {en_dato(tcmv)}. That is an assumption; no vote has been scheduled."
                if m.get("tcmv_dato_antatt", True) else
                f"TCMV is due to vote on {en_dato(tcmv)}, and we assume a yes.")
    eu_txt = (f"Model step 2 (the EU scenario): {tcmv_txt} For Ford’s BlueCruise, {m['eu_ikrafttredelse_dager']} days "
              f"passed from a yes in TCMV until the EU approval was in place. Adding {en_antall(r)} until rollout "
              f"gives {en_dato(eu)}.")
    navn = (en or {}).get("navn") or {}
    fakta = {iso: (v or {}).get("fakta") or "" for iso, v in ((en or {}).get("land") or {}).items()}
    ut_en = {}
    for c in d["land"]:
        iso = c["iso"]
        if iso not in ut:
            continue
        dato, steg, _, sp = ut[iso]
        dato = D(dato)
        t = c["modell_type"]
        if t == "signal":
            s = D(c["signal_dato"])
            if steg == "1":
                txt = (f"Model step 1: The first public signal of a national case came on {en_dato(s)}. In the countries "
                       f"that have approved, a median of {med} days passed from such a signal to a decision. Adding "
                       f"{en_antall(r)} until rollout gives {en_dato(dato)}.")
            elif steg.startswith("1 ("):
                txt = (f"Model step 1: The first public signal of a national case came on {en_dato(s)}. The median of "
                       f"{med} days has passed without a decision, so we use the longest wait we have seen, {maks} days. "
                       f"Adding {en_antall(r)} until rollout gives {en_dato(dato)}.")
            else:
                txt = (f"Model step 1 → 2: The first public signal came on {en_dato(s)}, but even the longest wait we "
                       f"have seen, {maks} days, has passed. We therefore use the EU scenario: {en_dato(eu)}.")
        elif t == "eu":
            txt = eu_txt
        elif t == "eos":
            tidl, sen = D(sp["estimert_tidligst"]), D(sp["estimert_senest"])
            if iso == "NO":
                txt = (f"Model step 3 gives a range: {en_dato(tidl)} to {en_dato(sen)}. The earliest date applies if Norway "
                       f"follows the EU shortly after the decision. No source says how soon, so we add {en_antall(r)} "
                       f"to the EU scenario ({en_dato(eu)}). That is the median wait until rollout. The latest date applies "
                       f"if it goes as slowly as with Ford’s BlueCruise, when Norwegian clearance took {eos} days.")
            else:
                txt = (f"Model step 3 gives a range: {en_dato(tidl)} to {en_dato(sen)}. Earliest: the EU scenario "
                       f"({en_dato(eu)}) plus {en_antall(r)}. Latest: the same EEA lag Norway had with BlueCruise, {eos} days. "
                       f"Both dates are assumptions for {navn.get(iso) or c['land']}.")
        elif t == "ukjent":
            txt = (f"Model step 4: With no known national case, we use the EU scenario ({en_dato(eu)}) and add "
                   f"{uk_m} days. The margin is an assumption, not an observation.")
        else:
            txt = (f"Model step 5 (outside the EU and EEA): We use the EU scenario ({en_dato(eu)}) and add {ie_m} days. "
                   f"The margin is an assumption; we have no observed precedent.")
        ut_en[iso] = (fakta[iso].rstrip() + " " + txt).strip() if fakta.get(iso) else None
    return ut_en


def les_en():
    try:
        with open(EN_PATH, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def dump(d, f):
    """Skriver JSON med ett land per linje (lett å lese i diff, kompakt å pushe)."""
    f.write("{\n")
    keys = list(d.keys())
    for i, k in enumerate(keys):
        end = ",\n" if i < len(keys) - 1 else "\n"
        if k == "land":
            f.write('  "land": [\n')
            f.write(",\n".join("    " + json.dumps(c, ensure_ascii=False) for c in d["land"]))
            f.write("\n  ]" + end)
        else:
            f.write(f"  {json.dumps(k)}: {json.dumps(d[k], ensure_ascii=False)}{end}")
    f.write("}\n")


def main():
    today = date.today()
    if "--today" in sys.argv:
        today = D(sys.argv[sys.argv.index("--today") + 1])
    path = "data/nedtelling.json"
    d = json.load(open(path, encoding="utf-8"))
    param, ut = beregn(d, today)
    if "--check" in sys.argv:
        avvik = 0
        for k, v in param.items():
            if d["modell"].get(k) != v:
                print(f"AVVIK modell.{k}: fil={d['modell'].get(k)!r} beregnet={v!r}"); avvik += 1
        for c in d["land"]:
            if c["iso"] in ut:
                e, s, b, sp = ut[c["iso"]]
                if (c.get("estimert_dato"), c.get("modell_steg"), c.get("begrunnelse")) != (e, s, b):
                    print(f"AVVIK {c['land']}: fil={c.get('estimert_dato')}/{c.get('modell_steg')} beregnet={e}/{s} (eller begrunnelse)"); avvik += 1
                for k in SPENN_FELT:
                    if c.get(k) != sp.get(k):
                        print(f"AVVIK {c['land']}: {k} fil={c.get(k)!r} beregnet={sp.get(k)!r}"); avvik += 1
        en = les_en()
        if en is None:
            print(f"AVVIK: {EN_PATH} finnes ikke (engelsk versjon)"); avvik += 1
        else:
            for iso, b in beregn_en(d, en, today).items():
                e = (en.get("land") or {}).get(iso) or {}
                if b is None:
                    print(f"AVVIK {iso}: mangler engelsk «fakta» i {EN_PATH}"); avvik += 1
                elif e.get("begrunnelse") != b:
                    print(f"AVVIK {iso}: engelsk begrunnelse er utdatert – kjør python3 scripts/modell_nedtelling.py"); avvik += 1
        print(f"{len(ut)} modellerte land · {avvik} avvik")
        return 1 if avvik else 0
    d["modell"].update(param)
    for c in d["land"]:
        if c["iso"] in ut:
            c["estimert_dato"], c["modell_steg"], c["begrunnelse"], sp = ut[c["iso"]]
            for k in SPENN_FELT:
                if k in sp: c[k] = sp[k]
                else: c.pop(k, None)
    with open(path, "w", encoding="utf-8") as f:
        dump(d, f)
    en = les_en()
    if en is not None:
        mangler = []
        for iso, b in beregn_en(d, en, today).items():
            if b is None:
                mangler.append(iso)
                continue
            en.setdefault("land", {}).setdefault(iso, {})["begrunnelse"] = b
        with open(EN_PATH, "w", encoding="utf-8") as f:
            f.write(json.dumps(en, ensure_ascii=False, indent=2) + "\n")
        if mangler:
            print("Mangler engelsk «fakta» (data/en/nedtelling.json) for: " + ", ".join(mangler))
    for c in sorted(d["land"], key=lambda c: c.get("estimert_dato") or ""):
        if c["iso"] in ut:
            spenn = f"  ({c['estimert_tidligst']} – {c['estimert_senest']})" if c.get("estimert_senest") else ""
            print(f"{c['iso']}  {c['estimert_dato']}  steg {c['modell_steg']}{spenn}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
