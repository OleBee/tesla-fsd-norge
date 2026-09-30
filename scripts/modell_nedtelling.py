#!/usr/bin/env python3
"""Scenariomodell for data/nedtelling.json (fsdnorge.no/nedtelling/).

Regner ut estimert_dato, modell_steg og begrunnelse for alle land med
metode = "modell", ut fra parameterne i toppnivå-blokken «modell».

Bruk (fra repo-roten):
  python3 scripts/modell_nedtelling.py [--today YYYY-MM-DD]          # skriver fila
  python3 scripts/modell_nedtelling.py --check [--today YYYY-MM-DD]  # bare sammenlign
Endre aldri modellerte datoer for hånd: endre inndata og kjør skriptet.

Inndata per land (metode = "modell"):
  modell_type  signal | eu | eos | ukjent | ikke_eu
  signal_dato  (bare for signal) dato for første offentlige signal om nasjonal sak
  fakta        kildebelagt faktatekst; modellteksten legges etter
"""
import json, math, statistics, sys
from datetime import date, timedelta

MND = ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august",
       "september", "oktober", "november", "desember"]
ORD = ["null", "én", "to", "tre", "fire", "fem", "seks", "sju", "åtte", "ni", "ti", "elleve", "tolv"]


def nb(d):
    return f"{d.day}. {MND[d.month - 1]} {d.year}"


def antall(n, ental="dag", flertall="dager"):
    tall = ORD[n] if 0 <= n <= 12 else str(n)
    return f"{tall} {ental if n == 1 else flertall}"


def D(s):
    return date.fromisoformat(s)


def beregn(d, today):
    """Returnerer (parametre, {iso: (estimert_dato, modell_steg, begrunnelse)})."""
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

    tcmv_txt = (f"Vi antar et ja i TCMV {nb(tcmv)}. Datoen er en antagelse; ingen avstemning er satt opp."
                if m.get("tcmv_dato_antatt", True) else
                f"TCMV skal stemme {nb(tcmv)}, og vi antar et ja.")
    eu_txt = (f"Modellsteg 2 (EU-scenariet): {tcmv_txt} For Fords BlueCruise gikk det "
              f"{m['eu_ikrafttredelse_dager']} dager fra ja i TCMV til EU-godkjenningen var på plass. "
              f"Med {antall(r)} til utrulling gir det {nb(eu)}.")

    ut = {}
    for c in d["land"]:
        if c.get("metode") != "modell":
            continue
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
            dato, steg = eu + timedelta(days=eos), "3"
            if c["iso"] == "NO":
                txt = (f"Modellsteg 3: EU-scenariet ({nb(eu)}) pluss norsk etterslep. Da EU hadde godkjent Fords "
                       f"BlueCruise, brukte Statens vegvesen og Samferdselsdepartementet {eos} dager på å slå fast at "
                       f"godkjenningen også gjelder i Norge. Gjentar det seg, får norske eiere FSD Supervised først "
                       f"{nb(dato)}" + (" – mer enn ett år etter EU-landene." if eos > 365 else "."))
            else:
                txt = (f"Modellsteg 3: EU-scenariet ({nb(eu)}) pluss samme EØS-etterslep som Norge hadde med "
                       f"BlueCruise, {eos} dager. At {navn} bruker like lang tid, er en antagelse.")
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
        ut[c["iso"]] = (dato.isoformat(), steg, (c["fakta"].rstrip() + " " + txt).strip())

    param = {
        "utrulling_dager": r,
        "signal_grunnlag": sg,
        "signal_median_dager": med_raa,
        "signal_brukt_dager": med,
        "signal_maks_dager": maks,
        "eu_vedtak_dato": eu_kraft.isoformat(),
        "eu_scenario_dato": eu.isoformat(),
    }
    return param, ut


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
                e, s, b = ut[c["iso"]]
                if (c.get("estimert_dato"), c.get("modell_steg"), c.get("begrunnelse")) != (e, s, b):
                    print(f"AVVIK {c['land']}: fil={c.get('estimert_dato')}/{c.get('modell_steg')} beregnet={e}/{s} (eller begrunnelse)"); avvik += 1
        print(f"{len(ut)} modellerte land · {avvik} avvik")
        return 1 if avvik else 0
    d["modell"].update(param)
    for c in d["land"]:
        if c["iso"] in ut:
            c["estimert_dato"], c["modell_steg"], c["begrunnelse"] = ut[c["iso"]]
    with open(path, "w", encoding="utf-8") as f:
        dump(d, f)
    for c in sorted(d["land"], key=lambda c: c.get("estimert_dato") or ""):
        if c["iso"] in ut:
            print(f"{c['iso']}  {c['estimert_dato']}  steg {c['modell_steg']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
