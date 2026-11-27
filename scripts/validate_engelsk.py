#!/usr/bin/env python3
"""Engelsk versjon av tadnorge.no (/en/): felles hjelpefunksjoner og validator.

Den engelske teksten ligger i egne filer ved siden av de norske:

  data/en/europa-feed.json   saker:      items.<id> = {title, summary, why_it_matters, images[]}
  data/en/status.json        statuskort: norge_status, tcmv, norge_denne_maneden, series_02
                             tidslinje:  timeline[] med nøkkel «dato#n»
  data/en/nedtelling.json    land:       navn.<ISO>, land.<ISO> = {begrunnelse | fakta}

Alt som ikke er tekst (datoer, tall, kilder, bilder, status) hentes fra de norske
filene, så det finnes bare én kilde for fakta. Hver engelsk oppføring har et
«norsk_sha»: de 12 første tegnene av SHA-256 for den norske teksten den er
oversatt fra. Endres den norske teksten, stemmer ikke lenger hashen, og
validatoren feiler til den engelske teksten er oppdatert.

Arbeidsflyt for redaksjonen (norsk -> engelsk -> valider):
  1. Skriv eller endre den norske saken i data/*.json.
  2. python3 scripts/validate_engelsk.py --mangler
       viser hva som mangler eller er utdatert, med den norske teksten og en
       ferdig mal (JSON) du kan lime inn i data/en/*.json.
  3. Skriv den engelske teksten i data/en/*.json.
  4. python3 scripts/validate_engelsk.py --stamp feed:<id> [status:tcmv ...]
       setter norsk_sha for oppføringene du har oversatt (ingen andre).
     For modellerte land i nedtellingen: python3 scripts/modell_nedtelling.py
       skriver den engelske begrunnelsen selv ut fra «fakta».
  5. python3 scripts/validate_engelsk.py   (må gi «0 feil»)
     python3 scripts/build_seo.py           (bygger /en/ sin statiske blokk og en/feed.xml)

Bruk:
  python3 scripts/validate_engelsk.py            valider, kode 1 ved FEIL
  python3 scripts/validate_engelsk.py --mangler  liste over manglende/utdaterte, med mal
  python3 scripts/validate_engelsk.py --stamp NØKKEL [NØKKEL ...]
  python3 scripts/validate_engelsk.py --stamp-alle   (bare ved første oppsett)

Nøkler: feed:<id>, status:norge_status, status:tcmv, status:norge_denne_maneden,
status:series_02, tidslinje:<YYYY-MM-DD>#<n>, nedtelling:<ISO>.

Feiler (FEIL) hvis en sak, en statusblokk, en tidslinjeoppføring eller et land
mangler engelsk tekst, hvis teksten er utdatert (norsk_sha stemmer ikke), hvis
avsnitt eller bilder ikke stemmer overens, hvis det finnes engelske oppføringer
uten norsk motpart, eller hvis teksten bryter husreglene (ITavisen, tidskoder
fra video, HTML-entiteter). ADVARSEL stopper ikke.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
EN = DATA / "en"

FEED_FELT = ("title", "summary", "why_it_matters")
BILDE_FELT = ("alt", "caption", "source_label")
STATUS_BLOKKER = {
    "norge_status": None,   # ren tekst
    "tcmv": ("siste_utfall", "neste_sikkerhet", "etikett", "sannsynlig_utfall", "kommentar",
             "neste_dato_nb", "anslag_begrunnelse"),
    "norge_denne_maneden": ("etikett", "kommentar"),
    "series_02": ("merknad", "dato_nb"),
}
TIDSLINJE_FELT = ("tekst", "etikett", "dato_visning")
# Husregler for engelsk tekst (samme ånd som FORBUDT i validate_nedtelling.py)
FORBUDT = [
    (r"\bIT-avisen\b|\bItavisen\b|\bIT avisen\b|\bITAvisen\b", "skriv «ITavisen»"),
    (r"\[\d{1,2}:\d{2}", "tidskode fra video"),
    (r"&(amp|lt|gt|quot|#\d+);", "HTML-entitet i rå tekst"),
    (r"«|»", "norske anførselstegn – bruk “ ” på engelsk"),
]
# Ord som tyder på at norsk tekst har lekket inn (bare advarsel: navn og titler kan inneholde dem)
NORSK_ORD = re.compile(r"\b(ikke|og|det|som|på|eiere|godkjent|Hvorfor|betyr|ennå|fortsatt)\b")


def les(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def skriv(p: Path, d) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(obj) -> str:
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()[:12]


# —— Hva som er norsk kildetekst for hver oppføring ——

def kilde_feed(it: dict) -> dict:
    k = {f: it.get(f) or "" for f in FEED_FELT}
    k["images"] = [{f: (im or {}).get(f) or "" for f in BILDE_FELT} for im in it.get("images") or []]
    return k


def kilde_status(st: dict, blokk: str):
    felt = STATUS_BLOKKER[blokk]
    if felt is None:
        return st.get(blokk) or ""
    b = st.get(blokk) or {}
    return {f: b.get(f) or "" for f in felt}


def tidslinje_nokler(timeline: list) -> list[str]:
    """«dato#n»: n teller oppføringer med samme dato i norsk rekkefølge (1, 2, ...)."""
    sett: dict[str, int] = {}
    ut = []
    for it in timeline or []:
        d = it.get("dato") or "?"
        sett[d] = sett.get(d, 0) + 1
        ut.append(f"{d}#{sett[d]}")
    return ut


def kilde_tidslinje(it: dict) -> dict:
    return {f: it.get(f) or "" for f in TIDSLINJE_FELT}


def kilde_land(c: dict) -> str:
    """Modellerte land oversettes fra «fakta» (begrunnelsen lages av modellen), andre fra «begrunnelse»."""
    return c.get("fakta") or "" if c.get("metode") == "modell" else c.get("begrunnelse") or ""


# —— Lasting og fletting (samme regler som window.TADSPRAK.flett i /sprak.js) ——

def last_en(navn: str) -> dict:
    p = EN / navn
    return les(p) if p.exists() else {}


def flett_feed(no: dict, en: dict) -> dict:
    ut = json.loads(json.dumps(no))
    oversatt = (en or {}).get("items") or {}
    for it in ut.get("items") or []:
        e = oversatt.get(it.get("id"))
        it["_en"] = bool(e)
        if not e:
            continue
        for f in FEED_FELT:
            if e.get(f):
                it[f] = e[f]
        for im, eim in zip(it.get("images") or [], e.get("images") or []):
            for f in BILDE_FELT:
                if im is not None and eim and eim.get(f):
                    im[f] = eim[f]
    return ut


def flett_status(no: dict, en: dict) -> dict:
    ut = json.loads(json.dumps(no))
    en = en or {}
    for blokk, felt in STATUS_BLOKKER.items():
        if blokk not in en:
            continue
        if felt is None:
            ut[blokk] = en[blokk]
        else:
            ut.setdefault(blokk, {})
            for f in felt:
                if (en[blokk] or {}).get(f):
                    ut[blokk][f] = en[blokk][f]
    tl = {e.get("nokkel"): e for e in en.get("timeline") or []}
    for it, k in zip(ut.get("timeline") or [], tidslinje_nokler(ut.get("timeline") or [])):
        e = tl.get(k)
        it["_en"] = bool(e)
        if e:
            for f in TIDSLINJE_FELT:
                if e.get(f):
                    it[f] = e[f]
    return ut


def flett_nedtelling(no: dict, en: dict) -> dict:
    ut = json.loads(json.dumps(no))
    en = en or {}
    navn = en.get("navn") or {}
    land = en.get("land") or {}
    for c in ut.get("land") or []:
        iso = c.get("iso")
        if navn.get(iso):
            c["land"] = navn[iso]
        e = land.get(iso) or {}
        c["_en"] = bool(e.get("begrunnelse"))
        if e.get("begrunnelse"):
            c["begrunnelse"] = e["begrunnelse"]
        if e.get("fakta"):
            c["fakta"] = e["fakta"]
    return ut


# —— Validering ——

def avsnitt(t: str) -> int:
    return len([p for p in re.split(r"\n\s*\n", t or "") if p.strip()])


def tekstsjekk(hvor: str, tekst: str, feil: list, adv: list) -> None:
    if not isinstance(tekst, str):
        return
    for pat, hva in FORBUDT:
        if re.search(pat, tekst):
            feil.append(f"{hvor}: {hva} ({pat})")
    treff = NORSK_ORD.findall(tekst)
    if len(treff) >= 3:
        adv.append(f"{hvor}: ser norsk ut? ({', '.join(sorted(set(treff)))})")


def sjekk(feil: list, adv: list, mangler: list) -> None:
    """Fyller feil/adv. mangler får (nøkkel, norsk kilde, mal) for --mangler."""
    feed, status, nedt = les(DATA / "europa-feed.json"), les(DATA / "status.json"), les(DATA / "nedtelling.json")
    efeed, estatus, enedt = last_en("europa-feed.json"), last_en("status.json"), last_en("nedtelling.json")

    if status.get("norge_kundegodkjent") is not False:
        feil.append("status.json: norge_kundegodkjent må være false til Norge faktisk har sagt ja (og da skal mandatet endres først)")

    # Saker
    items = (efeed.get("items") or {})
    ids = []
    for it in feed.get("items") or []:
        iid = it.get("id")
        if not iid:
            feil.append(f"feed: sak uten id ({it.get('title')!r})")
            continue
        ids.append(iid)
        k = kilde_feed(it)
        e = items.get(iid)
        n = f"feed:{iid}"
        mal = {f: "" for f in FEED_FELT}
        if k["images"]:
            mal["images"] = [{f: "" for f in BILDE_FELT if im[f]} for im in k["images"]]
        if not e:
            feil.append(f"{n}: mangler engelsk versjon i data/en/europa-feed.json")
            mangler.append((n, "mangler", k, mal))
            continue
        for f in FEED_FELT:
            if k[f] and not (e.get(f) or "").strip():
                feil.append(f"{n}: mangler engelsk «{f}»")
            tekstsjekk(f"{n}.{f}", e.get(f), feil, adv)
        if avsnitt(k["summary"]) != avsnitt(e.get("summary")):
            feil.append(f"{n}: summary har {avsnitt(e.get('summary'))} avsnitt på engelsk, {avsnitt(k['summary'])} på norsk")
        eim = e.get("images") or []
        if len(eim) != len(k["images"]):
            feil.append(f"{n}: {len(eim)} bildetekster på engelsk, {len(k['images'])} bilder på norsk")
        for i, (nim, ei) in enumerate(zip(k["images"], eim)):
            for f in BILDE_FELT:
                if nim[f] and not (ei or {}).get(f):
                    feil.append(f"{n}: bilde {i + 1} mangler engelsk «{f}»")
                tekstsjekk(f"{n}.images[{i}].{f}", (ei or {}).get(f), feil, adv)
        if e.get("norsk_sha") != sha(k):
            feil.append(f"{n}: utdatert – den norske teksten er endret etter oversettelsen (oppdater engelsk, så --stamp {n})")
            mangler.append((n, "utdatert", k, {f: e.get(f) for f in FEED_FELT}))
    for iid in items:
        if iid not in ids:
            feil.append(f"feed:{iid}: engelsk sak uten norsk motpart (slett den eller gi den riktig id)")

    # Statusblokker
    for blokk, felt in STATUS_BLOKKER.items():
        n = f"status:{blokk}"
        k = kilde_status(status, blokk)
        e = estatus.get(blokk)
        mal = "" if felt is None else {f: "" for f in felt if k.get(f)}
        if not e:
            feil.append(f"{n}: mangler engelsk versjon i data/en/status.json")
            mangler.append((n, "mangler", k, mal))
            continue
        if felt is None:
            if not str(e).strip():
                feil.append(f"{n}: tom engelsk tekst")
            tekstsjekk(n, e, feil, adv)
        else:
            for f in felt:
                if k.get(f) and not (e.get(f) or "").strip():
                    feil.append(f"{n}: mangler engelsk «{f}»")
                tekstsjekk(f"{n}.{f}", e.get(f), feil, adv)
        if (estatus.get("norsk_sha") or {}).get(blokk) != sha(k):
            feil.append(f"{n}: utdatert – den norske teksten er endret (oppdater engelsk, så --stamp {n})")
            mangler.append((n, "utdatert", k, e))

    # Tidslinje
    etl = {x.get("nokkel"): x for x in estatus.get("timeline") or []}
    nokler = tidslinje_nokler(status.get("timeline") or [])
    for it, key in zip(status.get("timeline") or [], nokler):
        n = f"tidslinje:{key}"
        k = kilde_tidslinje(it)
        e = etl.get(key)
        mal = {"nokkel": key, **{f: "" for f in TIDSLINJE_FELT if k[f]}}
        if not e:
            feil.append(f"{n}: mangler engelsk versjon i data/en/status.json (timeline)")
            mangler.append((n, "mangler", k, mal))
            continue
        for f in TIDSLINJE_FELT:
            if k[f] and not (e.get(f) or "").strip():
                feil.append(f"{n}: mangler engelsk «{f}»")
            tekstsjekk(f"{n}.{f}", e.get(f), feil, adv)
        if e.get("norsk_sha") != sha(k):
            feil.append(f"{n}: utdatert – den norske teksten er endret (oppdater engelsk, så --stamp {n})")
            mangler.append((n, "utdatert", k, e))
    for key in etl:
        if key not in nokler:
            feil.append(f"tidslinje:{key}: engelsk oppføring uten norsk motpart")

    # Nedtelling
    navn = enedt.get("navn") or {}
    eland = enedt.get("land") or {}
    isos = []
    for c in nedt.get("land") or []:
        iso = c.get("iso")
        isos.append(iso)
        n = f"nedtelling:{iso}"
        if not navn.get(iso):
            feil.append(f"{n}: mangler engelsk landnavn i data/en/nedtelling.json (navn.{iso})")
        k = kilde_land(c)
        e = eland.get(iso) or {}
        modell = c.get("metode") == "modell"
        felt = "fakta" if modell else "begrunnelse"
        if not (e.get(felt) or "").strip():
            feil.append(f"{n}: mangler engelsk «{felt}»" + (" (begrunnelsen skrives av scripts/modell_nedtelling.py)" if modell else ""))
            mangler.append((n, "mangler", k, {felt: ""}))
            continue
        if modell and not (e.get("begrunnelse") or "").strip():
            feil.append(f"{n}: mangler engelsk begrunnelse – kjør python3 scripts/modell_nedtelling.py")
        for f in ("fakta", "begrunnelse"):
            tekstsjekk(f"{n}.{f}", e.get(f), feil, adv)
        if e.get("norsk_sha") != sha(k):
            feil.append(f"{n}: utdatert – den norske «{'fakta' if modell else 'begrunnelse'}» er endret (oppdater engelsk, så --stamp {n})")
            mangler.append((n, "utdatert", k, {felt: e.get(felt)}))
    for iso in eland:
        if iso not in isos:
            feil.append(f"nedtelling:{iso}: engelsk land uten norsk motpart")


def stamp(nokler: list[str], alle: bool = False) -> list[str]:
    feed, status, nedt = les(DATA / "europa-feed.json"), les(DATA / "status.json"), les(DATA / "nedtelling.json")
    efeed, estatus, enedt = last_en("europa-feed.json"), last_en("status.json"), last_en("nedtelling.json")
    gjort, ukjent = [], set(nokler)
    for it in feed.get("items") or []:
        n = f"feed:{it.get('id')}"
        e = (efeed.get("items") or {}).get(it.get("id"))
        if e is not None and (alle or n in ukjent):
            e["norsk_sha"] = sha(kilde_feed(it)); gjort.append(n); ukjent.discard(n)
    for blokk in STATUS_BLOKKER:
        n = f"status:{blokk}"
        if blokk in estatus and (alle or n in ukjent):
            estatus.setdefault("norsk_sha", {})[blokk] = sha(kilde_status(status, blokk)); gjort.append(n); ukjent.discard(n)
    etl = {x.get("nokkel"): x for x in estatus.get("timeline") or []}
    for it, key in zip(status.get("timeline") or [], tidslinje_nokler(status.get("timeline") or [])):
        n = f"tidslinje:{key}"
        if key in etl and (alle or n in ukjent):
            etl[key]["norsk_sha"] = sha(kilde_tidslinje(it)); gjort.append(n); ukjent.discard(n)
    for c in nedt.get("land") or []:
        n = f"nedtelling:{c.get('iso')}"
        e = (enedt.get("land") or {}).get(c.get("iso"))
        if e is not None and (alle or n in ukjent):
            e["norsk_sha"] = sha(kilde_land(c)); gjort.append(n); ukjent.discard(n)
    if ukjent:
        raise SystemExit("Fant ikke (eller mangler engelsk oppføring for): " + ", ".join(sorted(ukjent)))
    skriv(EN / "europa-feed.json", efeed)
    skriv(EN / "status.json", estatus)
    skriv(EN / "nedtelling.json", enedt)
    return gjort


def main() -> int:
    args = sys.argv[1:]
    if args and args[0] in ("--stamp", "--stamp-alle"):
        gjort = stamp(args[1:], alle=args[0] == "--stamp-alle")
        print(f"norsk_sha satt for {len(gjort)} oppføring(er)" + (": " + ", ".join(gjort) if len(gjort) <= 12 else ""))
        print("Kjør python3 scripts/validate_engelsk.py for å validere.")
        return 0
    feil, adv, mangler = [], [], []
    sjekk(feil, adv, mangler)
    if "--mangler" in args:
        if not mangler:
            print("Ingenting mangler: alle saker, statusblokker, tidslinjeoppføringer og land har oppdatert engelsk tekst.")
        for n, hva, k, mal in mangler:
            print(f"\n=== {n} ({hva}) ===")
            print("Norsk:", json.dumps(k, ensure_ascii=False, indent=2))
            print("Engelsk mal:", json.dumps(mal, ensure_ascii=False, indent=2))
        print(f"\n{len(mangler)} oppføring(er) trenger engelsk. Etter oversettelse: --stamp <nøkkel>.")
        return 1 if mangler else 0
    for m in adv:
        print("ADVARSEL:", m)
    for m in feil:
        print("FEIL:", m)
    print(f"Engelsk versjon: {len(feil)} feil, {len(adv)} advarsler")
    return 1 if feil else 0


if __name__ == "__main__":
    sys.exit(main())
