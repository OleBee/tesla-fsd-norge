#!/usr/bin/env python3
"""Sjekker delingsbildet (og:image / twitter:image / JSON-LD-bilde).

Husregel (Ole, 27.11.2026): delingsbildene skal ikke ha den runde måleren/ringen
til høyre. Skriptet feiler hvis
  - malen scripts/og/og-image.html har en måler (class="gauge", eller SVG/<circle>
    utenfor logoen i .brand),
  - en side peker til et annet bilde enn det render.sh lager, eller til det gamle
    tadnorge-og.png (med måler),
  - bildet mangler, ikke er 1200×630, eller sidene oppgir feil bredde/høyde,
  - (hvis Pillow finnes) området der måleren lå ikke er ren kortbakgrunn.
Bare standardbiblioteket trengs; pikselsjekken hoppes over uten Pillow.
"""
import json
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAL = ROOT / "scripts" / "og" / "og-image.html"
RENDER = ROOT / "scripts" / "og" / "render.sh"
SIDER = ("index.html", "nedtelling/index.html", "en/index.html", "en/countdown/index.html")
GAMMEL = "assets/og/tadnorge-og.png"  # gammel versjon med måler; ligger igjen for gamle cacher
MALER_OMRADE = (794, 162, 1094, 462)  # x0, y0, x1, y1 der måler-SVG-en lå
KORT = (14, 22, 36)  # #0e1624


def png_storrelse(p: Path):
    b = p.read_bytes()[:24]
    if b[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", b[16:24])


def main() -> int:
    feil = []
    mal = MAL.read_text(encoding="utf-8")
    if re.search(r'class="[^"]*\bgauge\b', mal) or ".gauge" in mal:
        feil.append("og-image.html: malen har en måler (gauge) – den skal ikke være med")
    uten_logo = re.sub(r'(?s)<div class="brand">.*?</div>\s*</div>', "", mal)
    uten_logo = re.sub(r'(?s)<div class="brand">.*?<div class="word">', "", uten_logo)
    if re.search(r"<svg\b|<circle\b", uten_logo):
        feil.append("og-image.html: SVG eller <circle> utenfor logoen – ingen måler/ring i delingsbildet")

    m = re.search(r'--screenshot="\$PWD/(assets/og/[^"]+\.png)"', RENDER.read_text(encoding="utf-8"))
    if not m:
        feil.append("render.sh: fant ikke filnavnet bildet skrives til")
        bilde = None
    else:
        bilde = m.group(1)
        p = ROOT / bilde
        if not p.exists():
            feil.append(f"{bilde} finnes ikke – kjør bash scripts/og/render.sh")
        elif png_storrelse(p) != (1200, 630):
            feil.append(f"{bilde}: er {png_storrelse(p)}, skal være (1200, 630)")
        else:
            try:
                from PIL import Image
                im = Image.open(p).convert("RGB").crop(MALER_OMRADE)
                farger = {c for _, c in im.getcolors(1 << 20)}
                if farger != {KORT}:
                    feil.append(f"{bilde}: området der måleren lå er ikke ren kortbakgrunn ({len(farger)} farger)")
            except ImportError:
                pass

    if bilde:
        url = f"https://tadnorge.no/{bilde}"
        for side in SIDER:
            h = (ROOT / side).read_text(encoding="utf-8")
            if GAMMEL in h:
                feil.append(f"{side}: peker fortsatt til {GAMMEL} (med måler)")
            for prop in ('property="og:image"', 'name="twitter:image"'):
                mm = re.search(r'<meta ' + re.escape(prop) + r' content="([^"]+)"', h)
                if not mm or mm.group(1) != url:
                    feil.append(f"{side}: {prop} er {mm.group(1) if mm else 'mangler'}, skal være {url}")
            for prop, verdi in (("og:image:width", "1200"), ("og:image:height", "630")):
                mm = re.search(r'<meta property="' + prop + r'" content="([^"]+)"', h)
                if not mm or mm.group(1) != verdi:
                    feil.append(f"{side}: {prop} skal være {verdi}")
            for blokk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
                for u in re.findall(r'https://tadnorge\.no/assets/og/[^"]+', json.dumps(json.loads(blokk))):
                    if u != url:
                        feil.append(f"{side}: JSON-LD peker til {u}, skal være {url}")

    for f in feil:
        print("FEIL:", f)
    print(f"Delingsbilde: {len(feil)} feil" + (f" ({bilde})" if bilde else ""))
    return 1 if feil else 0


if __name__ == "__main__":
    sys.exit(main())
