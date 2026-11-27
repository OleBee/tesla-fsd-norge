#!/usr/bin/env python3
"""Setter versjon (?v=) på CSS- og JS-filene som test/index.html lenker til.

Versjonen er de 8 første tegnene av SHA-256 for filinnholdet. Da får
nettleseren en ny adresse hver gang en fil endres, selv om GitHub Pages
sender Cache-Control: max-age=600.

Kjør etter endringer i site.css, test/test-meny.css eller test/test-meny.js:
    python3 scripts/bump_test_version.py
Med --check avsluttes skriptet med kode 1 hvis en versjon er utdatert.

Rører bare test/index.html. Forsiden (index.html) har ikke versjoner.
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "test" / "index.html"
FILES = ["/site.css", "/test/test-meny.css", "/test/test-meny.js"]


def version(url: str) -> str:
    return hashlib.sha256((ROOT / url.lstrip("/")).read_bytes()).hexdigest()[:8]


def main() -> int:
    check = "--check" in sys.argv
    text = PAGE.read_text(encoding="utf-8")
    new = text
    for url in FILES:
        pat = re.compile(r'((?:href|src)=")' + re.escape(url) + r'(?:\?v=[^"]*)?(")')
        if not pat.search(new):
            raise SystemExit(f"Fant ikke {url} i test/index.html")
        new = pat.sub(lambda m: f"{m.group(1)}{url}?v={version(url)}{m.group(2)}", new)
    for url in FILES:
        print(f"{url}?v={version(url)}")
    if new == text:
        print("Versjonene er oppdatert.")
        return 0
    if check:
        print("Utdatert: kjør python3 scripts/bump_test_version.py")
        return 1
    PAGE.write_text(new, encoding="utf-8")
    print("Oppdatert: test/index.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
