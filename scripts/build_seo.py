#!/usr/bin/env python3
"""Bygger SEO-filer for tadnorge.no fra data/*.json.

Genererer:
  - feed.xml          RSS 2.0 fra data/europa-feed.json
  - sitemap.xml       levende sider med lastmod
  - index.html        statisk forhåndsvisning av feed og tidslinje mellom
                      SEO:FEED- og SEO:TIDSLINJE-markørene (JS erstatter
                      innholdet ved lasting, så dette er bare for søkemotorer
                      og lesere uten JavaScript)
  - en/index.html     det samme på engelsk: norske data flettet med data/en/*.json
                      (se scripts/validate_engelsk.py)
  - en/feed.xml       engelsk RSS
  - sitemap.xml har også /en/ og /en/countdown/, med hreflang-alternativer.

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
SOURCE_LABEL_EN = {"svv": "SVV", "circabc": "CIRCABC", "tcmv-vote": "TCMV estimate",
                   "norway": "Norway status", "news": "News"}
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"]
STATIC_FEED_MAX = 20
# Faste tekster per språk (samme som T i /forside.js)
TXT = {
    "nb": {"labels": SOURCE_LABEL, "oppdatering": "Oppdatering", "hvorfor": "Hvorfor det betyr noe:",
           "kilde": "Kilde", "feed": "#siste-nytt", "tl": "#tidslinje", "status": "#status"},
    "en": {"labels": SOURCE_LABEL_EN, "oppdatering": "Update", "hvorfor": "Why it matters:",
           "kilde": "Source", "feed": "#latest-news", "tl": "#timeline", "status": "#status"},
}


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


def en_datetime(iso: str) -> str:
    """«27 November 2026, 13.45 CET», som fmtDateTime() i /forside.js på /en/."""
    d = parse_iso(iso).astimezone(OSLO)
    tz = "CEST" if d.utcoffset().total_seconds() == 7200 else "CET"
    return f"{d.day} {MONTHS_EN[d.month - 1]} {d.year}, {d:%H.%M} {tz}"


def en_date(ymd: str) -> str:
    d = parse_iso(ymd + "T12:00:00+02:00") if len(ymd) <= 10 else parse_iso(ymd)
    d = d.astimezone(OSLO)
    return f"{d.day} {MONTHS_EN[d.month - 1]} {d.year}"


def esc(s) -> str:
    # Samme escaping som esc() i index.html
    return re.sub(r"[&<>\"']", lambda m: f"&#{ord(m.group(0))};", "" if s is None else str(s))


def summary_paragraphs(text: str) -> str:
    """Del summary på tom linje i flere <p class="feed-summary">. Ett avsnitt om det ikke er skift."""
    parts = [para.strip() for para in re.split(r"\n\s*\n", text or "") if para.strip()]
    return "".join(f'<p class="feed-summary">{esc(para)}</p>' for para in parts)


def feed_href(it: dict, lang: str = "nb") -> str:
    """Samme lenkelogikk som renderFeed() i /forside.js."""
    t = TXT[lang]
    href = it.get("url") or ""
    if (not href or re.search(r"(?:fsd|tad)norge\.no/nyheter/", href)
            or re.match(r"^nyheter/", href) or href.startswith("/nyheter/")):
        return t["feed"]
    if (re.search(r"(?:fsd|tad)norge\.no/(tcmv|europa|historie)\.html", href)
            or re.match(r"^(tcmv|europa|historie)\.html$", href)):
        if "tcmv.html" in href:
            return t["status"]
        if "historie.html" in href:
            return t["tl"]
        return t["feed"]
    return href


def is_internal(href: str) -> bool:
    return href.startswith("#") or re.match(r"^https?://(www\.)?(tad|fsd)norge\.no(/|$)", href) is not None


def static_figures(images, lang: str = "nb") -> str:
    """Samme markup som renderFigures() i index.html."""
    out = []
    for im in images or []:
        if not im or not im.get("src"):
            continue
        cap = esc(im["caption"]) if im.get("caption") else ""
        if im.get("source_url"):
            cap += (" " if cap else "") + f'<a href="{esc(im["source_url"])}" rel="noopener">{esc(im.get("source_label") or TXT[lang]["kilde"])}</a>'
        src = im["src"]
        if lang == "en" and not re.match(r"^(https?:)?/|^data:", src):
            src = "/" + src   # /en/ ligger én mappe ned
        size = (f' width="{esc(im["width"])}"' if im.get("width") else "") + (f' height="{esc(im["height"])}"' if im.get("height") else "")
        out.append(f'<figure class="feed-fig"><a href="{esc(src)}"><img src="{esc(src)}" alt="{esc(im.get("alt") or "")}" '
                   f'loading="lazy" decoding="async"{size}></a>' + (f"<figcaption>{cap}</figcaption>" if cap else "") + "</figure>")
    return "".join(out)


def static_feed(items: list[dict], indent: str, lang: str = "nb") -> str:
    t = TXT[lang]
    when_fn = en_datetime if lang == "en" else nb_datetime
    out = []
    for it in items[:STATIC_FEED_MAX]:
        src = it.get("source") or "news"
        label = t["labels"].get(src, src)
        cls = "badge " + ("tcmv-vote" if src == "tcmv-vote" else src)
        title = esc(it.get("title") or t["oppdatering"])
        href = feed_href(it, lang)
        if href and href != t["feed"]:
            rel = ' rel="noopener"' if href.startswith("http") else ""
            title_html = f'<a href="{esc(href)}"{rel}>{title}</a>'
        else:
            title_html = f"<span>{title}</span>"
        idattr = f' id="{esc(it["id"])}"' if it.get("id") else ""
        langattr = ' lang="nb"' if lang == "en" and it.get("_en") is False else ""
        parts = [
            f'<li class="feed-item"{idattr}{langattr}>',
            f'<div class="feed-meta"><span class="{cls}"><i></i> {esc(label)}</span>'
            f'<span class="feed-when"><time datetime="{esc(it.get("iso", ""))}">{esc(when_fn(it["iso"]) if it.get("iso") else "—")}</time></span></div>',
            f'<div class="feed-title">{title_html}</div>',
        ]
        if it.get("summary"):
            parts.append(summary_paragraphs(it["summary"]))
        parts.append(static_figures(it.get("images"), lang))
        if it.get("why_it_matters"):
            parts.append(f'<p class="feed-why"><strong>{t["hvorfor"]}</strong> {esc(it["why_it_matters"])}</p>')
        parts.append("</li>")
        out.append(indent + "".join(parts))
    return "\n".join(out)


def static_timeline(status: dict, indent: str, lang: str = "nb") -> str:
    date_fn = en_date if lang == "en" else nb_date
    out = []
    for it in status.get("timeline") or []:
        fase = it.get("fase") or "passert"
        cls = ' class="neste"' if fase in ("neste", "next") else (' class="langsiktig"' if fase == "langsiktig" else "")
        when = it.get("dato_visning") or (date_fn(it["dato"]) if it.get("dato") else "—")
        if it.get("etikett"):
            when += " · " + it["etikett"]
        if lang == "en" and it.get("_en") is False:
            cls += ' lang="nb"'
        out.append(f'{indent}<li{cls}><div class="when">{esc(when)}</div><div class="what">{esc(it.get("tekst", ""))}</div></li>')
    return "\n".join(out)


def replace_block(text: str, name: str, body: str) -> str:
    pat = re.compile(rf"([ \t]*)<!-- SEO:{name}:START[^>]*-->\n.*?\n?([ \t]*)<!-- SEO:{name}:END -->", re.S)
    m = pat.search(text)
    if not m:
        raise SystemExit(f"Fant ikke SEO:{name}-markørene")
    indent = m.group(1)
    start = m.group(0).splitlines()[0]
    block = f"{start}\n{body}\n{indent}<!-- SEO:{name}:END -->" if body else f"{start}\n{indent}<!-- SEO:{name}:END -->"
    return text[:m.start()] + block + text[m.end():]


def build_index(feed: dict, status: dict, lang: str = "nb") -> str:
    p = ROOT / ("en/index.html" if lang == "en" else "index.html")
    text = p.read_text(encoding="utf-8")
    indent = "            "
    text = replace_block(text, "FEED", static_feed(feed.get("items") or [], indent, lang))
    text = replace_block(text, "TIDSLINJE", static_timeline(status, indent, lang))
    return text


def rfc822(iso: str) -> str:
    return format_datetime(parse_iso(iso).astimezone(timezone.utc), usegmt=True)


RSS = {
    "nb": {"title": "TAD Norge – siste nytt om Tesla FSD i Norge og EU", "path": "/", "feed": "/feed.xml",
           "desc": "Uoffisiell statusside som følger godkjenningen av Tesla FSD Supervised "
                   "(Tesla Assisted Driving) i Norge og EU. Nyheter med kilder fra Statens vegvesen, RDW, TCMV og EU.",
           "language": "nb-NO", "kilde": "Kilde"},
    "en": {"title": "TAD Norge – latest news on Tesla FSD in Norway and the EU", "path": "/en/", "feed": "/en/feed.xml",
           "desc": "Unofficial status site following the approval of Tesla FSD Supervised "
                   "(Tesla Assisted Driving) in Norway and the EU. News sourced from the Norwegian Public Roads "
                   "Administration (Statens vegvesen), RDW, TCMV and the EU.",
           "language": "en", "kilde": "Source"},
}


def build_rss(feed: dict, lang: str = "nb") -> str:
    r = RSS[lang]
    t = TXT[lang]
    items = sorted(feed.get("items") or [], key=lambda i: parse_iso(i["iso"]), reverse=True)
    last = feed.get("updated_iso") or (items[0]["iso"] if items else "2026-01-01T00:00:00+01:00")
    x = html.escape
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        "  <channel>",
        f"    <title>{r['title']}</title>",
        f"    <link>{SITE}{r['path']}</link>",
        f'    <atom:link href="{SITE}{r["feed"]}" rel="self" type="application/rss+xml"/>',
        f"    <description>{x(r['desc'], quote=False)}</description>",
        f"    <language>{r['language']}</language>",
        f"    <lastBuildDate>{rfc822(last)}</lastBuildDate>",
        "    <image>",
        f"      <url>{SITE}/favicon-192.png</url>",
        f"      <title>{r['title']}</title>",
        f"      <link>{SITE}{r['path']}</link>",
        "    </image>",
    ]
    for it in items:
        link = f"{SITE}{r['path']}#{it['id']}" if it.get("id") else f"{SITE}{r['path']}{t['feed']}"
        desc = []
        if it.get("summary"):
            for para in re.split(r"\n\s*\n", it["summary"]):
                para = para.strip()
                if para:
                    desc.append(f"<p>{x(para, quote=False)}</p>")
        for im in it.get("images") or []:
            if im and im.get("src"):
                src_abs = im["src"] if im["src"].startswith("http") else f"{SITE}/{im['src'].lstrip('/')}"
                desc.append(f'<p><img src="{x(src_abs)}" alt="{x(im.get("alt") or "")}"></p>')
                if im.get("caption"):
                    desc.append(f"<p><em>{x(im['caption'], quote=False)}</em></p>")
        if it.get("why_it_matters"):
            desc.append(f"<p><strong>{t['hvorfor']}</strong> {x(it['why_it_matters'], quote=False)}</p>")
        src = it.get("url") or ""
        if src and not is_internal(src):
            desc.append(f'<p>{r["kilde"]}: <a href="{x(src)}">{x(src, quote=False)}</a></p>')
        lines += [
            "    <item>",
            f"      <title>{x(it.get('title') or t['oppdatering'], quote=False)}</title>",
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
    # (sti, lastmod, changefreq, priority, (norsk sti, engelsk sti))
    front = ("/", "/en/")
    countdown = ("/nedtelling/", "/en/countdown/")
    pages = [
        ("/", home, "daily", "1.0", front),
        ("/nedtelling/", nedt.get("sist_oppdatert_iso"), "daily", "0.8", countdown),
        ("/en/", home, "daily", "0.9", front),
        ("/en/countdown/", nedt.get("sist_oppdatert_iso"), "daily", "0.7", countdown),
    ]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for path, lm, freq, prio, (no, en) in pages:
        lines.append("  <url>")
        lines.append(f"    <loc>{SITE}{path}</loc>")
        if lm:
            lines.append(f"    <lastmod>{w3c(lm)}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{prio}</priority>")
        lines.append(f'    <xhtml:link rel="alternate" hreflang="no" href="{SITE}{no}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}{en}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{no}"/>')
        lines.append("  </url>")
    lines += ["</urlset>", ""]
    return "\n".join(lines)


def main() -> int:
    check = "--check" in sys.argv
    feed, status, nedt = load("europa-feed.json"), load("status.json"), load("nedtelling.json")
    sys.path.insert(0, str(ROOT / "scripts"))
    import validate_engelsk as ve
    feed_en = ve.flett_feed(feed, ve.last_en("europa-feed.json"))
    status_en = ve.flett_status(status, ve.last_en("status.json"))
    outputs = {
        ROOT / "feed.xml": build_rss(feed),
        ROOT / "sitemap.xml": build_sitemap(feed, status, nedt),
        ROOT / "index.html": build_index(feed, status),
        ROOT / "en" / "feed.xml": build_rss(feed_en, "en"),
        ROOT / "en" / "index.html": build_index(feed_en, status_en, "en"),
    }
    changed = []
    for path, content in outputs.items():
        old = path.read_text(encoding="utf-8") if path.exists() else None
        if old != content:
            changed.append(str(path.relative_to(ROOT)))
            if not check:
                path.write_text(content, encoding="utf-8")
    print(("Ville endret: " if check else "Oppdatert: ") + (", ".join(changed) if changed else "ingenting"))
    return 1 if (check and changed) else 0


if __name__ == "__main__":
    sys.exit(main())
