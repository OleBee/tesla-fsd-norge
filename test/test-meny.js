/* Testside /test/: meny øverst på mobil og «Nedtelling per land (estimat)»
   fra data/nedtelling.json. Kortene bruker samme oppsett som /nedtelling/.
   Fra 768 px og opp er menyen og nedtellingsdelen skjult med CSS. */
(function () {
  "use strict";

  var mq = window.matchMedia("(max-width: 767px)");
  var nav = document.getElementById("tm-nav");
  if (!nav) return;
  var links = Array.prototype.slice.call(nav.querySelectorAll("a[data-tm]"));
  var head = document.getElementById("tm-head") || nav;

  /* Høyden på den faste toppen styrer scroll-margin-top i CSS */
  function measure() {
    if (!mq.matches) return;
    document.documentElement.style.setProperty("--tm-head-h", Math.round(head.getBoundingClientRect().height) + "px");
  }
  measure();
  window.addEventListener("resize", measure);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(measure);

  /* —— Aktivt valg —— */
  var row = nav.querySelector("ul");

  /* Myk kant til høyre bare når det finnes flere faner utenfor skjermen */
  function edge() {
    var more = row.scrollLeft + row.clientWidth < row.scrollWidth - 2;
    nav.classList.toggle("tm-mer", more);
  }
  row.addEventListener("scroll", edge, { passive: true });
  window.addEventListener("resize", edge);

  /* Rull fanerekka slik at valgt fane er synlig */
  function showTab(a) {
    var pad = parseFloat(getComputedStyle(row).paddingLeft) || 0;
    var left = a.offsetLeft - row.offsetLeft;
    var right = left + a.offsetWidth;
    var target = null;
    if (left - pad < row.scrollLeft) target = left - pad;
    else if (right + pad > row.scrollLeft + row.clientWidth) target = right + pad - row.clientWidth;
    if (target !== null) row.scrollTo({ left: Math.max(0, target), behavior: "smooth" });
  }

  function setActive(id) {
    links.forEach(function (a) {
      if (a.getAttribute("data-tm") === id) {
        if (a.getAttribute("aria-current") !== "true") { a.setAttribute("aria-current", "true"); showTab(a); }
      } else a.removeAttribute("aria-current");
    });
  }

  var lock = 0, userMoved = false;
  ["touchstart", "wheel", "keydown"].forEach(function (ev) {
    window.addEventListener(ev, function () { userMoved = true; }, { passive: true });
  });

  /* Bilder i feeden lastes først når de nærmer seg, og kan skyve målet nedover
     mens siden ruller. Derfor retter vi opp posisjonen et par ganger etterpå. */
  function jump(id) {
    var sec = document.getElementById(id);
    if (!sec) return;
    userMoved = false;
    sec.scrollIntoView({ block: "start" });
    [700, 1400, 2200].forEach(function (ms) {
      setTimeout(function () {
        if (userMoved) return;
        var want = parseFloat(getComputedStyle(sec).scrollMarginTop) || 0;
        if (Math.abs(sec.getBoundingClientRect().top - want) > 4) sec.scrollIntoView({ block: "start", behavior: "instant" });
      }, ms);
    });
  }

  links.forEach(function (a) {
    a.addEventListener("click", function (e) {
      var id = a.getAttribute("data-tm");
      e.preventDefault();
      setActive(id);
      lock = Date.now() + 2400; /* la rullingen bli ferdig før rullesporingen tar over */
      if (location.hash !== "#" + id) history.pushState(null, "", "#" + id);
      jump(id);
    });
  });

  function onScroll() {
    if (!mq.matches || Date.now() < lock) return;
    var navH = head.getBoundingClientRect().height + 16;
    var current = links[0].getAttribute("data-tm");
    var best = -Infinity;
    links.forEach(function (a) {
      var sec = document.getElementById(a.getAttribute("data-tm"));
      if (!sec) return;
      var top = sec.getBoundingClientRect().top - navH;
      if (top <= 1 && top > best) { best = top; current = a.getAttribute("data-tm"); }
    });
    /* Nederst på siden: siste del som er synlig */
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) {
      var last = document.getElementById("nedtelling-land");
      if (last && last.getBoundingClientRect().top < window.innerHeight) current = "nedtelling-land";
    }
    setActive(current);
  }
  var queued = false;
  window.addEventListener("scroll", function () {
    if (queued) return;
    queued = true;
    window.requestAnimationFrame(function () { queued = false; onScroll(); });
  }, { passive: true });

  /* —— Nedtelling per land (estimat) —— */
  var STATUS = {
    "lansert": { label: "Lansert", cls: "s-lansert" },
    "godkjent, utrulling snart": { label: "Godkjent, utrulling snart", cls: "s-godkjent" },
    "venter på anerkjennelse": { label: "Venter på anerkjennelse", cls: "s-anerkj" },
    "venter på EU-vedtak": { label: "Venter på EU-vedtak", cls: "s-eu" },
    "ukjent": { label: "Ukjent", cls: "s-ukjent" }
  };
  var EOS = 470;
  var cards = [];

  function pad(n) { return String(n).padStart(2, "0"); }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return "&#" + c.charCodeAt(0) + ";"; });
  }
  function fmtDate(ymd) {
    if (!ymd) return "";
    try {
      return new Date(ymd + "T12:00:00Z").toLocaleDateString("nb-NO", { day: "numeric", month: "long", year: "numeric", timeZone: "Europe/Oslo" });
    } catch (e) { return ymd; }
  }
  function fmtMonth(ymd) {
    if (!ymd) return "";
    try {
      return new Date(ymd + "T12:00:00Z").toLocaleDateString("nb-NO", { month: "long", year: "numeric", timeZone: "Europe/Oslo" });
    } catch (e) { return ymd; }
  }
  function cap(t) { return t ? t.charAt(0).toUpperCase() + t.slice(1) : t; }
  function target(ymd) {
    var p = ymd.split("-");
    return new Date(Number(p[0]), Number(p[1]) - 1, Number(p[2]), 0, 0, 0);
  }
  function host(u) {
    try { return new URL(u).hostname.replace(/^www\./, ""); } catch (e) { return "kilde"; }
  }
  function sourcesHtml(list) {
    var out = [];
    (list || []).forEach(function (u, i) {
      if (!/^https:\/\//.test(u)) return;
      out.push('<a href="' + esc(u) + '" rel="noopener" target="_blank">[' + (i + 1) + "] " + esc(host(u)) + "</a>");
    });
    return out.join(" ");
  }

  /* Samme kortinnhold som cardHtml() i /nedtelling/ */
  function cardHtml(c, isNorge) {
    var st = STATUS[c.status] || STATUS.ukjent;
    var h = '<div class="nt-head"><span class="nt-iso">' + esc(c.iso) + "</span>" +
      '<span class="nt-land">' + esc(c.land) + "</span>" +
      '<span class="badge ' + st.cls + '"><i></i> ' + esc(st.label) + "</span></div>";

    if (c.status === "lansert") {
      if (c.lansert_dato) {
        h += '<div class="nt-big">Lansert ' + esc(fmtDate(c.lansert_dato)) + "</div>";
        if (c.godkjent_dato) h += '<div class="nt-when">Godkjent ' + esc(fmtDate(c.godkjent_dato)) + "</div>";
      } else {
        h += '<div class="nt-big">Lansert</div>' +
          '<div class="nt-when">Godkjent ' + esc(fmtDate(c.godkjent_dato)) + " · utrullingsdato ikke bekreftet</div>";
      }
    } else if (c.estimert_dato) {
      var tag = c.metode === "modell"
        ? '<span class="badge mod-tag">modellert estimat</span> '
        : '<span class="badge est-tag">estimat</span> ';
      var steg = c.metode === "modell" && c.modell_steg ? '<span class="nt-steg">· modellsteg ' + esc(c.modell_steg) + "</span>" : "";
      var spenn = !!(c.estimert_tidligst && c.estimert_senest);
      if (spenn) {
        h += '<div class="nt-big nt-spenn">' + esc(cap(fmtMonth(c.estimert_tidligst))) + " – " + esc(fmtMonth(c.estimert_senest)) + "</div>" +
          '<div class="nt-when">' + tag + "tidligst " + esc(fmtDate(c.estimert_tidligst)) + " · senest " + esc(fmtDate(c.estimert_senest)) + steg + "</div>";
      } else {
        h += '<div class="nt-when">' + tag + esc(fmtDate(c.estimert_dato)) + steg + "</div>";
      }
      h += (spenn ? '<div class="nt-when nt-cd-lbl">Nedtelling til tidligste dato</div>' : "") +
        '<div class="units" data-target="' + esc(c.estimert_dato) + '" aria-live="polite">' +
        '<div class="unit"><span class="n" data-part="days">––</span><span class="u">dager</span></div>' +
        '<div class="unit"><span class="n" data-part="hours">––</span><span class="u">timer</span></div>' +
        '<div class="unit"><span class="n" data-part="mins">––</span><span class="u">min</span></div>' +
        "</div>" +
        '<p class="cd-done" hidden>Estimatet er passert – vi venter på bekreftet utrulling</p>';
      if (c.godkjent_dato) h += '<div class="nt-when">Godkjent ' + esc(fmtDate(c.godkjent_dato)) + "</div>";
    } else if (c.status === "godkjent, utrulling snart" && c.godkjent_dato) {
      h += '<div class="nt-big">Godkjent ' + esc(fmtDate(c.godkjent_dato)) + "</div>" +
        '<div class="nt-when">Tesla har ikke oppgitt noen dato for utrullingen</div>';
    } else {
      h += '<div class="nt-when">Dato mangler i datagrunnlaget</div>';
    }

    if (isNorge) {
      h += '<p class="nt-norge-lede">Danske eiere har kjørt med FSD Supervised siden juni. Norske eiere venter på Brussel. ' +
        (c.estimert_tidligst && c.estimert_senest
          ? "Følger Norge EU raskt, kan systemet komme i " + esc(fmtMonth(c.estimert_tidligst)) + ". Går det like tregt som med BlueCruise, der Statens vegvesen brukte " + esc(EOS) + " dager, blir det " + esc(fmtMonth(c.estimert_senest)) + "."
          : "Deretter venter de på Statens vegvesen, som brukte " + esc(EOS) + " dager på BlueCruise.") + "</p>";
    }
    h += '<p class="nt-why">' + esc(c.begrunnelse) + "</p>";
    h += '<div class="nt-foot"><span>Sikkerhet: ' + esc(c.sikkerhet) + "</span><span>Sjekket " + esc(fmtDate(c.sist_oppdatert)) + "</span></div>";
    h += '<div class="nt-foot">Kilder: ' + sourcesHtml(c.kilder) + "</div>";
    return h;
  }

  function makeCard(c, isNorge) {
    var st = STATUS[c.status] || STATUS.ukjent;
    var el = document.createElement("article");
    el.className = "nt-card " + st.cls + (isNorge ? " is-norge" : "");
    el.innerHTML = cardHtml(c, isNorge);
    cards.push(el);
    return el;
  }

  function tick() {
    var now = new Date();
    cards.forEach(function (el) {
      var u = el.querySelector(".units[data-target]");
      if (!u) return;
      var ms = target(u.getAttribute("data-target")).getTime() - now.getTime();
      var done = el.querySelector(".cd-done");
      if (ms <= 0) {
        u.hidden = true;
        if (done) done.hidden = false;
        return;
      }
      var m = Math.floor(ms / 60000);
      u.querySelector('[data-part="days"]').textContent = pad(Math.floor(m / 1440));
      u.querySelector('[data-part="hours"]').textContent = pad(Math.floor((m % 1440) / 60));
      u.querySelector('[data-part="mins"]').textContent = pad(m % 60);
    });
  }

  function render(data) {
    var land = (data && data.land) || [];
    if (data.modell && data.modell.eos_etterslep_dager != null) EOS = data.modell.eos_etterslep_dager;
    var no = null, est = [], mod = [], lansert = [];
    land.forEach(function (c) {
      if (c.iso === "NO") no = c;
      else if (c.status === "lansert") lansert.push(c);
      else if (c.metode === "modell") mod.push(c);
      else est.push(c);
    });
    function byDate(a, b) {
      var da = a.estimert_tidligst || a.estimert_dato || a.godkjent_dato || "9999";
      var db = b.estimert_tidligst || b.estimert_dato || b.godkjent_dato || "9999";
      var d = da.localeCompare(db);
      return d !== 0 ? d : a.land.localeCompare(b.land, "nb");
    }
    est.sort(byDate);
    mod.sort(byDate);
    lansert.sort(function (a, b) {
      return (a.lansert_dato || a.godkjent_dato || "").localeCompare(b.lansert_dato || b.godkjent_dato || "");
    });
    if (no) document.getElementById("tm-nt-norge").appendChild(makeCard(no, true));
    [["tm-nt-est", est], ["tm-nt-mod", mod], ["tm-nt-lansert", lansert]].forEach(function (g) {
      var box = document.getElementById(g[0]);
      g[1].forEach(function (c) { box.appendChild(makeCard(c, false)); });
      if (!g[1].length) box.previousElementSibling.hidden = true;
    });
    tick();
    setInterval(tick, 30000);
  }

  var loaded = false;
  function load() {
    if (loaded || !mq.matches) return;
    loaded = true;
    var empty = document.getElementById("tm-nt-empty");
    fetch("/data/nedtelling.json", { cache: "no-store" })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        if (d) { render(d); empty.hidden = true; }
        else empty.textContent = "Kunne ikke laste data/nedtelling.json.";
      })
      .catch(function () { empty.textContent = "Kunne ikke laste data/nedtelling.json."; });
  }
  load();
  if (mq.addEventListener) mq.addEventListener("change", load);
  else if (mq.addListener) mq.addListener(load);

  if (location.hash === "#nedtelling-land") setTimeout(function () { jump("nedtelling-land"); }, 400);
  onScroll();
  edge();
})();
