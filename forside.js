/* Forsiden på tadnorge.no, norsk (/) og engelsk (/en/): feed, tidslinje og statuskort
   fra data/*.json. Flyttet ut av index.html 27.11.2026 så begge språkversjonene bruker
   samme kode. Språket styres av <html lang> via window.TADSPRAK (/sprak.js), som også
   fletter inn engelsk tekst fra data/en/*.json på /en/.
   Versjonen (?v=) i index.html og en/index.html settes av scripts/bump_versions.py. */
(function () {
  "use strict";
  var S = window.TADSPRAK || { lang: "nb" };
  var EN = S.lang === "en";
  var LOCALE = EN ? "en-GB" : "nb-NO";

  /* Alle faste tekster på siden som skriptet setter selv, på begge språk */
  var T = EN ? {
    kilder: { svv: "SVV", circabc: "CIRCABC", "tcmv-vote": "TCMV estimate", norway: "Norway status", news: "News" },
    oppdatering: "Update",
    ingen: "No posts yet.",
    kunneIkke: "Could not load data/europa-feed.json.",
    hvorfor: "Why it matters:",
    kilde: "Source",
    tlRdw: "RDW Art. 39 type-approval",
    tlNasjonal: "national recognition of RDW Art. 39",
    tlVotum: "TCMV meeting with a vote on the Article 39 case.",
    tlMulig: "TCMV meeting. The Article 39 case is on the agenda with a possible vote.",
    tlIkke: "TCMV meeting. It is not confirmed that the committee will vote on the Article 39 case.",
    etAnslag: "Estimate, date not set",
    etVarslet: "Vote announced",
    etMulig: "Possible vote",
    etIkke: "Vote not confirmed",
    s02: "UN R171 Series 02 is expected to enter into force.",
    anslagPassert: "The estimated date has passed",
    anslagMot: "The countdown runs to our estimate, ",
    holdt: "The meeting has been held",
    s02Dato: "Late January 2027",
    desimal: "."
  } : {
    kilder: { svv: "SVV", circabc: "CIRCABC", "tcmv-vote": "TCMV-estimat", norway: "Norgesstatus", news: "Nyheter" },
    oppdatering: "Oppdatering",
    ingen: "Ingen innlegg ennå.",
    kunneIkke: "Kunne ikke laste data/europa-feed.json.",
    hvorfor: "Hvorfor det betyr noe:",
    kilde: "Kilde",
    tlRdw: "RDW Art. 39 typegodkjenning",
    tlNasjonal: "nasjonal anerkjennelse av RDW Art. 39",
    tlVotum: "TCMV-møte med avstemning om artikkel 39-saken.",
    tlMulig: "TCMV-møte. Artikkel 39-saken står på agendaen med mulig avstemning.",
    tlIkke: "TCMV-møte. Det er ikke bekreftet at komiteen stemmer over artikkel 39-saken.",
    etAnslag: "Anslag, dato ikke satt",
    etVarslet: "Avstemning varslet",
    etMulig: "Mulig avstemning",
    etIkke: "Avstemning ikke bekreftet",
    s02: "UN R171 Series 02 ventes i kraft.",
    anslagPassert: "Den anslåtte datoen er passert",
    anslagMot: "Nedtellingen går mot vårt anslag, ",
    holdt: "Møtet er holdt",
    s02Dato: "Sent i januar 2027",
    desimal: ","
  };
  var SOURCE_LABEL = T.kilder;
  /* Faneankre: interne lenker i feeden peker hit */
  var A = EN ? { feed: "#latest-news", tl: "#timeline", status: "#status" } : { feed: "#siste-nytt", tl: "#tidslinje", status: "#status" };

  var state = {
    tcmvIso: "2026-12-15T10:00:00+01:00",
    seriesIso: "2027-01-25T00:00:00+01:00"
  };

  function pad(n) { return String(n).padStart(2, "0"); }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return "&#" + c.charCodeAt(0) + ";";
    });
  }

  /* Norsk: «27. november 2026 kl. 13:45» (som før). Engelsk: «27 November 2026, 13:45 CET». */
  function fmtDateTime(iso) {
    if (!iso) return "—";
    try {
      if (!EN) {
        return new Date(iso).toLocaleString("nb-NO", {
          day: "numeric", month: "long", year: "numeric",
          hour: "2-digit", minute: "2-digit", timeZone: "Europe/Oslo"
        });
      }
      var p = {};
      new Intl.DateTimeFormat("en-GB", {
        day: "numeric", month: "long", year: "numeric", hour: "2-digit", minute: "2-digit",
        hourCycle: "h23", timeZone: "Europe/Oslo", timeZoneName: "short"
      }).formatToParts(new Date(iso)).forEach(function (x) { p[x.type] = x.value; });
      var tz = /^(CET|CEST)$/.test(p.timeZoneName) ? p.timeZoneName : (p.timeZoneName === "GMT+2" ? "CEST" : "CET");
      return p.day + " " + p.month + " " + p.year + ", " + p.hour + ":" + p.minute + " " + tz;
    } catch (e) { return iso; }
  }

  function fmtDate(isoOrYmd) {
    if (!isoOrYmd) return "—";
    try {
      var d = isoOrYmd.length <= 10
        ? new Date(isoOrYmd + "T12:00:00+02:00")
        : new Date(isoOrYmd);
      return d.toLocaleDateString(LOCALE, {
        day: "numeric", month: "long", year: "numeric", timeZone: "Europe/Oslo"
      });
    } catch (e) { return isoOrYmd; }
  }

  function remaining(iso, now) {
    if (!iso) return null;
    var ms = new Date(iso).getTime() - now.getTime();
    if (ms <= 0) return { done: true, days: 0, hours: 0, mins: 0, secs: 0 };
    var s = Math.floor(ms / 1000);
    return {
      done: false,
      days: Math.floor(s / 86400),
      hours: Math.floor((s % 86400) / 3600),
      mins: Math.floor((s % 3600) / 60),
      secs: s % 60
    };
  }

  function fillUnits(root, r) {
    if (!root) return;
    if (!r || r.done) return;
    var days = root.querySelector('[data-part="days"]');
    if (!days) return;
    days.textContent = String(r.days).padStart(2, "0");
    root.querySelector('[data-part="hours"]').textContent = pad(r.hours);
    root.querySelector('[data-part="mins"]').textContent = pad(r.mins);
    root.querySelector('[data-part="secs"]').textContent = pad(r.secs);
  }

  function setCountdown(unitsId, doneId, iso, now) {
    var units = document.getElementById(unitsId);
    var done = document.getElementById(doneId);
    var r = remaining(iso, now);
    if (!r || r.done) {
      if (units) units.hidden = true;
      if (done) done.hidden = false;
      return;
    }
    if (units) units.hidden = false;
    if (done) done.hidden = true;
    fillUnits(units, r);
  }

  function setBar(el, pct) {
    if (!el) return;
    el.style.width = Math.min(100, Math.max(0, pct)) + "%";
  }

  function setText(id, text) {
    var el = document.getElementById(id);
    if (el && text != null && text !== "") el.textContent = text;
  }

  /* —— Feed —— */
  // Valgfrie bilder per sak: images[] = { src, alt, caption, source_url, source_label }
  function renderSummary(text) {
    if (!text) return "";
    return String(text).split(/\n\s*\n/).map(function (p) {
      p = p.trim();
      return p ? '<p class="feed-summary">' + esc(p) + "</p>" : "";
    }).join("");
  }

  function renderFigures(images) {
    if (!images || !images.length) return "";
    return images.map(function (im) {
      if (!im || !im.src) return "";
      var cap = im.caption ? esc(im.caption) : "";
      if (im.source_url) {
        cap += (cap ? " " : "") + '<a href="' + esc(im.source_url) + '" rel="noopener">' + esc(im.source_label || T.kilde) + "</a>";
      }
      /* Bildestier i dataene er relative til roten; på /en/ må de gjøres absolutte */
      var src = EN && !/^(https?:)?\/|^data:/.test(im.src) ? "/" + im.src : im.src;
      return '<figure class="feed-fig"><a href="' + esc(src) + '"><img src="' + esc(src) + '" alt="' + esc(im.alt || "") + '" loading="lazy" decoding="async"' +
        (im.width ? ' width="' + esc(im.width) + '"' : "") + (im.height ? ' height="' + esc(im.height) + '"' : "") + "></a>" +
        (cap ? "<figcaption>" + cap + "</figcaption>" : "") + "</figure>";
    }).join("");
  }

  function renderFeed(data) {
    var feed = document.getElementById("feed");
    var empty = document.getElementById("feed-empty");
    var items = (data && data.items) || [];
    feed.innerHTML = "";
    if (!items.length) {
      empty.hidden = false;
      empty.textContent = T.ingen;
      return;
    }
    empty.hidden = true;
    items.forEach(function (it) {
      var src = it.source || "news";
      var label = SOURCE_LABEL[src] || src;
      var cls = "badge " + (src === "tcmv-vote" ? "tcmv-vote" : src);
      var title = esc(it.title || T.oppdatering);
      var href = it.url || "";
      // Interne URL-er er tynne redirects til forsiden — pek anker i stedet (unngå redirect-loop)
      if (!href || /(?:fsd|tad)norge\.no\/nyheter\//.test(href) || /^nyheter\//.test(href) || href.indexOf("/nyheter/") === 0) {
        href = A.feed;
      } else if (/(?:fsd|tad)norge\.no\/(tcmv|europa|historie)\.html/.test(href) || /^(tcmv|europa|historie)\.html$/.test(href)) {
        if (/tcmv\.html/.test(href)) href = A.status;
        else if (/historie\.html/.test(href)) href = A.tl;
        else href = A.feed;
      }
      var titleHtml = href && href !== A.feed
        ? ('<a href="' + esc(href) + '"' + (href.indexOf("http") === 0 ? ' rel="noopener"' : "") + ">" + title + "</a>")
        : ('<span>' + title + "</span>");
      var li = document.createElement("li");
      li.className = "feed-item";
      if (it.id) li.id = it.id;
      if (EN && it._en === false) li.lang = "nb";   /* mangler engelsk tekst: vis norsk, merket som norsk */
      li.innerHTML =
        '<div class="feed-meta"><span class="' + cls + '"><i></i> ' + esc(label) + "</span>" +
        '<span class="feed-when">' + esc(fmtDateTime(it.iso)) + "</span></div>" +
        '<div class="feed-title">' + titleHtml + "</div>" +
        renderSummary(it.summary) +
        renderFigures(it.images) +
        (it.why_it_matters
          ? '<p class="feed-why"><strong>' + T.hvorfor + "</strong> " + esc(it.why_it_matters) + "</p>"
          : "");
      feed.appendChild(li);
    });
  }

  /* —— Timeline —— */
  function buildFallbackTimeline(status) {
    var items = [];
    (status.eu_land || []).forEach(function (l) {
      items.push({
        dato: l.dato,
        tekst: l.land + " — " + (l.sti === "RDW Art. 39"
          ? T.tlRdw
          : T.tlNasjonal) + ".",
        fase: "passert"
      });
    });
    if (status.tcmv && status.tcmv.neste_dato) {
      items.push({
        dato: status.tcmv.neste_dato,
        tekst: status.tcmv.votum_bekreftet
          ? T.tlVotum
          : (status.tcmv.votum_mulig ? T.tlMulig : T.tlIkke),
        fase: "neste",
        etikett: status.tcmv.neste_dato_er_anslag
          ? T.etAnslag
          : (status.tcmv.votum_bekreftet ? T.etVarslet : (status.tcmv.votum_mulig ? T.etMulig : T.etIkke))
      });
    }
    if (status.series_02) {
      items.push({
        dato: status.series_02.iso ? status.series_02.iso.slice(0, 10) : "2027-01-25",
        tekst: status.series_02.merknad || T.s02,
        fase: "langsiktig",
        etikett: "Series 02"
      });
    }
    items.sort(function (a, b) { return (a.dato || "").localeCompare(b.dato || ""); });
    return items;
  }

  function renderTimeline(status) {
    var list = document.getElementById("tl-list") || document.getElementById("timeline");   /* /en/: id="timeline" er fanen */
    var items = (status && status.timeline && status.timeline.length)
      ? status.timeline
      : buildFallbackTimeline(status || {});
    list.innerHTML = "";
    items.forEach(function (it) {
      var li = document.createElement("li");
      var fase = it.fase || "passert";
      if (fase === "neste" || fase === "next") li.className = "neste";
      else if (fase === "langsiktig") li.className = "langsiktig";
      if (EN && it._en === false) li.lang = "nb";
      var when = it.dato_visning || fmtDate(it.dato);
      if (it.etikett) when += " · " + it.etikett;
      li.innerHTML =
        '<div class="when">' + esc(when) + "</div>" +
        '<div class="what">' + esc(it.tekst || "") +
        (it.kilde ? ' <a class="tl-kilde" href="' + esc(it.kilde) + '" rel="noopener" target="_blank">' + T.kilde + '</a>' : "") +
        "</div>";
      list.appendChild(li);
    });
  }

  /* —— Status cards —— */
  function applyStatus(data) {
    if (!data) return;

    var nm = data.norge_denne_maneden || {};
    if (nm.prosent != null) {
      setText("norge-tall", String(nm.prosent));
      document.getElementById("kort-norge").setAttribute("data-prosent", String(nm.prosent));
      setBar(document.getElementById("norge-fyll"), nm.prosent);
    }
    if (nm.etikett) setText("norge-etikett", nm.etikett);

    var tm = data.tcmv || {};
    if (tm.neste_iso) state.tcmvIso = tm.neste_iso;
    else if (tm.neste_dato) state.tcmvIso = tm.neste_dato + "T10:00:00+02:00";
    if (tm.neste_dato_nb) setText("tcmv-dato", tm.neste_dato_nb);
    else if (tm.neste_dato) setText("tcmv-dato", fmtDate(tm.neste_dato));
    if (tm.oktober_godkjenning_prosent != null) {
      setText("tcmv-tall", String(tm.oktober_godkjenning_prosent));
      document.getElementById("kort-tcmv").setAttribute("data-prosent", String(tm.oktober_godkjenning_prosent));
      setBar(document.getElementById("tcmv-fyll"), tm.oktober_godkjenning_prosent);
    }
    if (tm.etikett) setText("tcmv-etikett", tm.etikett);
    if (tm.kommentar) setText("tcmv-cd-note", tm.kommentar);
    if (tm.neste_dato_er_anslag) {
      document.getElementById("kort-tcmv-cd").classList.add("anslag");
      setText("tcmv-done", T.anslagPassert);
      setText("tcmv-cd-note", (tm.kommentar ? tm.kommentar + " " : "") + T.anslagMot + fmtDate(tm.neste_dato) + ".");
    } else {
      setText("tcmv-done", T.holdt);
    }

    var landN = (data.eu_land || []).length;
    setText("land-tall", String(landN));
    setBar(document.getElementById("land-fyll"), (landN / 27) * 100);

    var bef = data.eu_andel_befolkning_prosent;
    if (bef != null) {
      setText("bef-tall", String(bef).replace(".", T.desimal));
      setBar(document.getElementById("bef-fyll"), bef);
    }

    var s2 = data.series_02 || {};
    if (s2.iso) state.seriesIso = s2.iso;
    if (s2.dato_nb) setText("series-dato", s2.dato_nb);
    else if (s2.forventet) setText("series-dato", T.s02Dato);
    if (s2.merknad) setText("series-note", s2.merknad);

    renderTimeline(data);
  }

  /* Norge som spenn fra data/nedtelling.json (tidligst–senest) */
  function fmtMonth(ymd) {
    try {
      return new Date(ymd + "T12:00:00Z").toLocaleDateString(LOCALE, { month: "long", year: "numeric", timeZone: "Europe/Oslo" });
    } catch (e) { return ymd; }
  }
  function fmtDay(ymd) {
    try {
      return new Date(ymd + "T12:00:00Z").toLocaleDateString(LOCALE, { day: "numeric", month: "long", year: "numeric", timeZone: "Europe/Oslo" });
    } catch (e) { return ymd; }
  }
  function applyNedtelling(nt) {
    if (!nt || !nt.land) return;
    var no = nt.land.filter(function (c) { return c.iso === "NO"; })[0];
    if (!no || !no.estimert_tidligst || !no.estimert_senest) return;
    var fra = fmtMonth(no.estimert_tidligst);
    setText("norge-spenn", fra.charAt(0).toUpperCase() + fra.slice(1) + " – " + fmtMonth(no.estimert_senest));
    setText("norge-spenn-tidligst", fmtDay(no.estimert_tidligst));
    setText("norge-spenn-senest", fmtDay(no.estimert_senest));
    if (nt.modell && nt.modell.eos_etterslep_dager != null) setText("norge-spenn-dager", String(nt.modell.eos_etterslep_dager));
  }

  function applySvv(svv) {
    /* Soft enrichment only — main cards come from status.json */
    if (!svv) return;
  }

  function tick() {
    var now = new Date();
    setCountdown("tcmv-units", "tcmv-done", state.tcmvIso, now);
    setCountdown("series-units", "series-done", state.seriesIso, now);
  }

  /* Initial paint from embedded defaults, then hydrate */
  setBar(document.getElementById("norge-fyll"), 0);
  setBar(document.getElementById("tcmv-fyll"), 0);
  setBar(document.getElementById("land-fyll"), (12 / 27) * 100);
  setBar(document.getElementById("bef-fyll"), 28.6);
  tick();
  setInterval(tick, 1000);

  /* Data: på /en/ flettes engelsk tekst fra data/en/*.json inn (window.TADSPRAK i /sprak.js) */
  function hent(navn) {
    if (S.hentData) return S.hentData(navn);
    return fetch("/data/" + navn, { cache: "no-store" }).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
  }
  Promise.all([hent("status.json"), hent("europa-feed.json"), hent("svv-siste.json"), hent("nedtelling.json")]).then(function (triple) {
    applyStatus(triple[0]);
    if (triple[1]) renderFeed(triple[1]);
    else {
      document.getElementById("feed-empty").hidden = false;
      document.getElementById("feed-empty").textContent = T.kunneIkke;
    }
    applySvv(triple[2]);
    applyNedtelling(triple[3]);
    tick();
    /* Lenker fra RSS peker på #saks-id: rull dit etter at feeden er tegnet på nytt */
    if (location.hash.length > 1) {
      var target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if (target && target.scrollIntoView) target.scrollIntoView();
    }
  });
})();
