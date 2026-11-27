/* Språk på tadnorge.no: norsk (/ og /nedtelling/) og engelsk (/en/ og /en/countdown/).
   1) window.TADSPRAK: språket på siden, henting av data og fletting av engelsk tekst
      (data/en/*.json) inn i de norske datafilene. Samme regler som scripts/validate_engelsk.py.
   2) Språkknappen NO/EN i toppen: går til tilsvarende side og fane, og til samme sak
      når en sak er åpnet (#saks-id) eller ligger øverst på skjermen.
   Versjonen (?v=) settes av scripts/bump_versions.py. */
(function () {
  "use strict";

  var lang = (document.documentElement.getAttribute("lang") || "nb").slice(0, 2) === "en" ? "en" : "nb";

  /* —— Fletting —— */
  var FEED_FELT = ["title", "summary", "why_it_matters"];
  var BILDE_FELT = ["alt", "caption", "source_label"];
  var STATUS_BLOKKER = {
    norge_status: null,
    tcmv: ["siste_utfall", "neste_sikkerhet", "etikett", "sannsynlig_utfall", "kommentar", "neste_dato_nb", "anslag_begrunnelse"],
    norge_denne_maneden: ["etikett", "kommentar"],
    series_02: ["merknad", "dato_nb"]
  };
  var TL_FELT = ["tekst", "etikett", "dato_visning"];

  function kopi(o) { return o == null ? o : JSON.parse(JSON.stringify(o)); }

  function tidslinjeNokler(tl) {
    var sett = {};
    return (tl || []).map(function (it) {
      var d = it.dato || "?";
      sett[d] = (sett[d] || 0) + 1;
      return d + "#" + sett[d];
    });
  }

  function flettFeed(no, en) {
    var ut = kopi(no);
    var ov = (en && en.items) || {};
    ((ut && ut.items) || []).forEach(function (it) {
      var e = ov[it.id];
      it._en = !!e;
      if (!e) return;
      FEED_FELT.forEach(function (f) { if (e[f]) it[f] = e[f]; });
      (it.images || []).forEach(function (im, i) {
        var ei = (e.images || [])[i];
        if (im && ei) BILDE_FELT.forEach(function (f) { if (ei[f]) im[f] = ei[f]; });
      });
    });
    return ut;
  }

  function flettStatus(no, en) {
    var ut = kopi(no);
    if (!ut) return ut;
    en = en || {};
    Object.keys(STATUS_BLOKKER).forEach(function (b) {
      if (!(b in en)) return;
      var felt = STATUS_BLOKKER[b];
      if (!felt) { ut[b] = en[b]; return; }
      ut[b] = ut[b] || {};
      felt.forEach(function (f) { if (en[b] && en[b][f]) ut[b][f] = en[b][f]; });
    });
    var tl = {};
    (en.timeline || []).forEach(function (e) { tl[e.nokkel] = e; });
    var nok = tidslinjeNokler(ut.timeline);
    (ut.timeline || []).forEach(function (it, i) {
      var e = tl[nok[i]];
      it._en = !!e;
      if (e) TL_FELT.forEach(function (f) { if (e[f]) it[f] = e[f]; });
    });
    return ut;
  }

  function flettNedtelling(no, en) {
    var ut = kopi(no);
    if (!ut) return ut;
    en = en || {};
    var navn = en.navn || {}, land = en.land || {};
    (ut.land || []).forEach(function (c) {
      if (navn[c.iso]) c.land = navn[c.iso];
      var e = land[c.iso] || {};
      c._en = !!e.begrunnelse;
      if (e.begrunnelse) c.begrunnelse = e.begrunnelse;
      if (e.fakta) c.fakta = e.fakta;
    });
    return ut;
  }

  var FLETT = { "europa-feed.json": flettFeed, "status.json": flettStatus, "nedtelling.json": flettNedtelling };

  function hentJson(url) {
    return fetch(url, { cache: "no-store" })
      .then(function (r) { return r.ok ? r.json() : null; })
      .catch(function () { return null; });
  }

  /* Norsk side: /data/<navn>. Engelsk side: /data/<navn> flettet med /data/en/<navn>.
     Mangler den engelske fila, vises den norske teksten (validatoren hindrer det i en PR). */
  function hentData(navn) {
    var no = hentJson("/data/" + navn);
    if (lang !== "en" || !FLETT[navn]) return no;
    return Promise.all([no, hentJson("/data/en/" + navn)]).then(function (p) {
      return p[0] ? FLETT[navn](p[0], p[1]) : null;
    });
  }

  window.TADSPRAK = {
    lang: lang,
    hentData: hentData,
    flett: { feed: flettFeed, status: flettStatus, nedtelling: flettNedtelling },
    tidslinjeNokler: tidslinjeNokler
  };

  /* —— Språkknappen —— */
  var sw = document.querySelector(".lang-sw");
  if (!sw) return;
  var other = sw.querySelector("a:not([aria-current])");
  if (!other) return;
  var base = other.getAttribute("href").split("#")[0];

  /* Faner og ankre med ulike navn på norsk og engelsk. Saks-id-ene er like på begge språk. */
  var TIL_EN = {
    "siste-nytt": "latest-news", "tidslinje": "timeline", "status": "status",
    "nedtelling-land": "countdown-by-country", "nedtelling": "countdown-by-country",
    "metode": "method", "top": "top"
  };
  var TIL_NO = {
    "latest-news": "siste-nytt", "timeline": "tidslinje", "status": "status",
    "countdown-by-country": "nedtelling-land", "countdown": "nedtelling-land",
    "method": "metode", "top": "top"
  };
  var MAP = lang === "en" ? TIL_NO : TIL_EN;

  function mapHash(id) {
    if (!id) return "";
    return MAP[id] || id;   /* saks-id og ukjente ankre beholdes */
  }

  function headH() {
    var h = document.getElementById("tm-head");
    var r = h && h.getBoundingClientRect();
    return r && getComputedStyle(h).position === "sticky" ? r.height : 0;
  }

  /* Saken som ligger øverst på skjermen, hvis leseren har rullet ned i feeden */
  function sakISyne() {
    var items = document.querySelectorAll(".feed-item[id]");
    if (!items.length || window.scrollY < 120) return null;
    var top = headH() + 8;
    for (var i = 0; i < items.length; i++) {
      var el = items[i];
      if (!el.offsetParent) return null;   /* feeden er skjult (annen fane på mobil) */
      var r = el.getBoundingClientRect();
      if (r.bottom > top + 40 && r.top < window.innerHeight * 0.6) return i === 0 && r.top > top - 4 ? null : el.id;
    }
    return null;
  }

  function aktivFane() {
    if (!document.documentElement.classList.contains("tm-tabs")) return "";
    var a = document.querySelector('.tm-nav a[aria-current="true"]');
    return a ? a.getAttribute("data-tm") : "";
  }

  function maal() {
    var hash = decodeURIComponent((location.hash || "").replace(/^#/, ""));
    /* 1) saken øverst på skjermen, 2) valgt fane på mobil, 3) adressen slik den er */
    var id = sakISyne() || aktivFane() || hash;
    var forste = document.querySelector(".tm-nav a[data-tm]");
    /* Første fane (Siste nytt / Latest news) er forsiden: ingen hash */
    if (id && forste && (id === forste.getAttribute("data-tm") || MAP[id] === MAP[forste.getAttribute("data-tm")])) id = "";
    var m = mapHash(id);
    return base + (m ? "#" + encodeURIComponent(m) : "");
  }

  function oppdater() { other.setAttribute("href", maal()); }
  ["pointerdown", "focus", "mouseenter"].forEach(function (ev) { other.addEventListener(ev, oppdater, { passive: true }); });
  other.addEventListener("click", oppdater);
  window.addEventListener("hashchange", oppdater);
  oppdater();
})();
