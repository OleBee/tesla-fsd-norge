#!/usr/bin/env python3
"""Bygger SEO-filer for tadnorge.no fra data/*.json.

Genererer:
  - feed.xml          RSS 2.0 fra data/europa-feed.json
  - sitemap.xml       levende sider med lastmod
  - index.html        statisk forhåndsvisning av feed og tidslinje mellom
                      SEO:FEED- og SEO:TIDSLINJE-markørene (JS erstatter
                      innholdet ved lasting, så dette er bare for søkemotorer
                      og lesere uten JavaScript)

Utdata er deterministisk: samme JSON gir samme filer. Kjør før push:
    python3 scripts/build_seo.py
Med --check avsluttes skriptet med kode 1 hvis noe ville blitt endret.
"""
from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://tadnorge.no"
OSLO = ZoneInfo("Europe/Oslo")
MONTHS = ["januar", "februar", "mars", "april", "mai", "juni", "juli",
          "august", "september", "oktober", "november", "desember"]
SOURCE_LABEL = {"svv": "SVV", "circabc": "CIRCABC", "tcmv-vote": "TCMV-estimat",
                "norway": "Norgesstatus", "news": "Nyheter"}
STATIC_FEED_MAX = 20


def load(name: str):
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


def parse_iso(s: str) -> datetime:
    d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    if d.tzinfo is None:
        d = d.replace(tzinfo=OSLO)
    return d


def nb_datetime(iso: str) -> str:
    d = parse_iso(iso).astimezone(OSLO)
    return f"{d.day}. {MONTHS[d.month - 1]} {d.year} kl. {d:%H:%M}"


def nb_date(ymd: str) -> str:
    d = parse_iso(ymd + "T12:00:00+02:00") if len(ymd) <= 10 else parse_iso(ymd)
    d = d.astimezone(OSLO)
    return f"{d.day}. {MONTHS[d.month - 1]} {d.year}"


def esc(s) -> str:
    # Samme escaping som esc() i index.html
    return re.sub(r"[&<>\"']", lambda m: f"&#{ord(m.group(0))};", "" if s is None else str(s))


def feed_href(it: dict) -> str:
    """Samme lenkelogikk som renderFeed() i index.html."""
    href = it.get("url") or ""
    if (not href or re.search(r"(?:fsd|tad)norge\.no/nyheter/", href)
            or re.match(r"^nyheter/", href) or href.startswith("/nyheter/")):
        return "#siste-nytt"
    if (re.search(r"(?:fsd|tad)norge\.no/(tcmv|europa|historie)\.html", href)
            or re.match(r"^(tcmv|europa|historie)\.html$", href)):
        if "tcmv.html" in href:
            return "#status"
        if "historie.html" in href:
            return "#tidslinje"
        return "#siste-nytt"
    return href


def is_internal(href: str) -> bool:
    return href.startswith("#") or re.match(r"^https?://(www\.)?(tad|fsd)norge\.no(/|$)", href) is not None


def static_feed(items: list[dict], indent: str) -> str:
    out = []
    for it in items[:STATIC_FEED_MAX]:
        src = it.get("source") or "news"
        label = SOURCE_LABEL.get(src, src)
        cls = "badge " + ("tcmv-vote" if src == "tcmv-vote" else src)
        title = esc(it.get("title") or "Oppdatering")
        href = feed_href(it)
        if href and href != "#siste-nytt":
            rel = ' rel="noopener"' if href.startswith("http") else ""
            title_html = f'<a href="{esc(href)}"{rel}>{title}</a>'
        else:
            title_html = f"<span>{title}</span>"
        idattr = f' id="{esc(it["id"])}"' if it.get("id") else ""
        parts = [
            f'<li class="feed-item"{idattr}>',
            f'<div class="feed-meta"><span class="{cls}"><i></i> {esc(label)}</span>'
            f'<span class="feed-when"><time datetime="{esc(it.get("iso", ""))}">{esc(nb_datetime(it["iso"]) if it.get("iso") else "—")}</time></span></div>',
            f'<div class="feed-title">{title_html}</div>',
        ]
        if it.get("summary"):
            parts.append(f'<p class="feed-summary">{esc(it["summary"])}</p>')
        if it.get("why_it_matters"):
            parts.append(f'<p class="feed-why"><strong>Hvorfor det betyr noe:</strong> {esc(it["why_it_matters"])}</p>')
        parts.append("</li>")
        out.append(indent + "".join(parts))
    return "\n".join(out)


def static_timeline(status: dict, indent: str) -> str:
    out = []
    for it in status.get("timeline") or []:
        fase = it.get("fase") or "passert"
        cls = ' class="neste"' if fase in ("neste", "next") else (' class="langsiktig"' if fase == "langsiktig" else "")
        when = nb_date(it["dato"]) if it.get("dato") else "—"
        if it.get("etikett"):
            when += " · " + it["etikett"]
        out.append(f'{indent}<li{cls}><div class="when">{esc(when)}</div><div class="what">{esc(it.get("tekst", ""))}</div></li>')
    return "\n".join(out)


def replace_block(text: str, name: str, body: str) -> str:
    pat = re.compile(rf"([ \t]*)<!-- SEO:{name}:START[^>]*-->\n.*?\n?([ \t]*)<!-- SEO:{name}:END -->", re.S)
    m = pat.search(text)
    if not m:
        raise SystemExit(f"Fant ikke SEO:{name}-markørene i index.html")
    indent = m.group(1)
    start = m.group(0).splitlines()[0]
    block = f"{start}\n{body}\n{indent}<!-- SEO:{name}:END -->" if body else f"{start}\n{indent}<!-- SEO:{name}:END -->"
    return text[:m.start()] + block + text[m.end():]


def build_index(feed: dict, status: dict) -> str:
    p = ROOT / "index.html"
    text = p.read_text(encoding="utf-8")
    indent = "            "
    text = replace_block(text, "FEED", static_feed(feed.get("items") or [], indent))
    text = replace_block(text, "TIDSLINJE", static_timeline(status, indent))
    return text


def rfc822(iso: str) -> str:
    return format_datetime(parse_iso(iso).astimezone(timezone.utc), usegmt=True)


def build_rss(feed: dict) -> str:
    items = sorted(feed.get("items") or [], key=lambda i: parse_iso(i["iso"]), reverse=True)
    last = feed.get("updated_iso") or (items[0]["iso"] if items else "2026-01-01T00:00:00+01:00")
    x = html.escape
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        "  <channel>",
        "    <title>TAD Norge – siste nytt om Tesla FSD i Norge og EU</title>",
        f"    <link>{SITE}/</link>",
        f'    <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>',
        "    <description>Uoffisiell statusside som følger godkjenningen av Tesla FSD Supervised "
        "(Tesla Assisted Driving) i Norge og EU. Nyheter med kilder fra Statens vegvesen, RDW, TCMV og EU.</description>",
        "    <language>nb-NO</language>",
        f"    <lastBuildDate>{rfc822(last)}</lastBuildDate>",
        "    <image>",
        f"      <url>{SITE}/favicon-192.png</url>",
        "      <title>TAD Norge – siste nytt om Tesla FSD i Norge og EU</title>",
        f"      <link>{SITE}/</link>",
        "    </image>",
    ]
    for it in items:
        link = f"{SITE}/#{it['id']}" if it.get("id") else f"{SITE}/#siste-nytt"
        desc = []
        if it.get("summary"):
            desc.append(f"<p>{x(it['summary'], quote=False)}</p>")
        if it.get("why_it_matters"):
            desc.append(f"<p><strong>Hvorfor det betyr noe:</strong> {x(it['why_it_matters'], quote=False)}</p>")
        src = it.get("url") or ""
        if src and not is_internal(src):
            desc.append(f'<p>Kilde: <a href="{x(src)}">{x(src, quote=False)}</a></p>')
        lines += [
            "    <item>",
            f"      <title>{x(it.get('title') or 'Oppdatering', quote=False)}</title>",
            f"      <link>{x(link)}</link>",
            f'      <guid isPermaLink="false">{x(it.get("id") or link)}</guid>',
            f"      <pubDate>{rfc822(it['iso'])}</pubDate>",
            f"      <description>{x(''.join(desc), quote=False)}</description>",
            "    </item>",
        ]
    lines += ["  </channel>", "</rss>", ""]
    return "\n".join(lines)


def w3c(iso: str) -> str:
    return parse_iso(iso).astimezone(OSLO).isoformat(timespec="seconds")


def build_sitemap(feed: dict, status: dict, nedt: dict) -> str:
    cands = [c for c in (feed.get("updated_iso"), status.get("sist_oppdatert_iso")) if c]
    home = max(cands, key=parse_iso) if cands else None
    pages = [
        ("/", home, "daily", "1.0"),
        ("/nedtelling/", nedt.get("sist_oppdatert_iso"), "daily", "0.8"),
    ]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, lm, freq, prio in pages:
        lines.append("  <url>")
        lines.append(f"    <loc>{SITE}{path}</loc>")
        if lm:
            lines.append(f"    <lastmod>{w3c(lm)}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{prio}</priority>")
        lines.append("  </url>")
    lines += ["</urlset>", ""]
    return "\n".join(lines)


def main() -> int:
    check = "--check" in sys.argv
    feed, status, nedt = load("europa-feed.json"), load("status.json"), load("nedtelling.json")
    outputs = {
        ROOT / "feed.xml": build_rss(feed),
        ROOT / "sitemap.xml": build_sitemap(feed, status, nedt),
        ROOT / "index.html": build_index(feed, status),
    }
    changed = []
    for path, content in outputs.items():
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old != content:
            changed.append(path.name)
            if not check:
                path.write_text(content, encoding="utf-8")
    print(("Ville endret: " if check else "Oppdatert: ") + (", ".join(changed) if changed else "ingenting"))
    return 1 if (check and changed) else 0


if __name__ == "__main__":
    sys.exit(main())
