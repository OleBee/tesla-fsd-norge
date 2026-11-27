#!/usr/bin/env python3
"""Setter versjon (?v=) på CSS- og JS-filene som forsiden og testsiden lenker til.

Versjonen er de 8 første tegnene av SHA-256 for filinnholdet. Da får
nettleseren en ny adresse hver gang en fil endres, selv om GitHub Pages
sender Cache-Control: max-age=600.

Kjør etter endringer i site.css, mobil-meny.css eller mobil-meny.js:
    python3 scripts/bump_versions.py
Med --check endres ingenting, og skriptet avslutter med kode 1 hvis en versjon er utdatert.

Rører bare lenkene i sidene under PAGES. Annet innhold, også SEO-markørene
som scripts/build_seo.py skriver mellom, blir stående.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = ["/site.css", "/mobil-meny.css", "/mobil-meny.js"]
PAGES = ["index.html", "test/index.html"]


def version(url: str) -> str:
    return hashlib.sha256((ROOT / url.lstrip("/")).read_bytes()).hexdigest()[:8]


def main() -> int:
    check = "--check" in sys.argv
    stale = []
    for url in FILES:
        print(f"{url}?v={version(url)}")
    for rel in PAGES:
        page = ROOT / rel
        text = page.read_text(encoding="utf-8")
        new = text
        for url in FILES:
            pat = re.compile(r'((?:href|src)=")' + re.escape(url) + r'(?:\?v=[^"]*)?(")')
            if len(pat.findall(new)) != 1:
                raise SystemExit(f"Fant ikke nøyaktig én lenke til {url} i {rel}")
            new = pat.sub(lambda m: f"{m.group(1)}{url}?v={version(url)}{m.group(2)}", new)
        if new == text:
            continue
        stale.append(rel)
        if not check:
            page.write_text(new, encoding="utf-8")
    if not stale:
        print("Versjonene er oppdatert.")
        return 0
    if check:
        print("Utdatert i " + ", ".join(stale) + ": kjør python3 scripts/bump_versions.py")
        return 1
    print("Oppdatert: " + ", ".join(stale))
    return 0


if __name__ == "__main__":
    sys.exit(main())
