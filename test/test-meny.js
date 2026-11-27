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

  /* —— Faner og glidende strek —— */
  var row = nav.querySelector("ul");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");

  function easeOut(t) { return 1 - Math.pow(1 - t, 3); }
  function idOf(a) { return a.getAttribute("data-tm"); }
  function linkFor(id) { return links.filter(function (a) { return idOf(a) === id; })[0]; }

  /* Én felles strek som glir mellom fanene (posisjon, bredde og farge) */
  nav.classList.add("tm-js");
  var ind = document.createElement("span");
  ind.className = "tm-ind";
  ind.setAttribute("aria-hidden", "true");
  row.appendChild(ind);

  function placeInd(a, instant) {
    if (!a) return;
    if (instant) ind.classList.add("tm-ind-fast");
    ind.style.width = a.offsetWidth + "px";
    ind.style.transform = "translateX(" + a.offsetLeft + "px)";
    ind.setAttribute("data-tm", idOf(a));
    if (instant) { void ind.offsetWidth; ind.classList.remove("tm-ind-fast"); }
  }

  /* Myk kant til høyre bare når det finnes flere faner utenfor skjermen */
  function edge() {
    nav.classList.toggle("tm-mer", row.scrollLeft + row.clientWidth < row.scrollWidth - 2);
  }
  row.addEventListener("scroll", edge, { passive: true });

  /* Fanerekka ruller sidelengs med samme kurve og varighet */
  var rowAnim = 0;
  function showTab(a, dur) {
    var pad = parseFloat(getComputedStyle(row).paddingLeft) || 0;
    var left = a.offsetLeft, right = left + a.offsetWidth, to = null;
    if (left - pad < row.scrollLeft) to = left - pad;
    else if (right + pad > row.scrollLeft + row.clientWidth) to = right + pad - row.clientWidth;
    if (to === null) return;
    to = Math.max(0, Math.min(to, row.scrollWidth - row.clientWidth));
    cancelAnimationFrame(rowAnim);
    if (!dur || reduce.matches) { row.scrollLeft = to; return; }
    var from = row.scrollLeft, t0 = null;
    row.style.scrollSnapType = "none";
    rowAnim = requestAnimationFrame(function step(now) {
      if (t0 === null) t0 = now;
      var t = Math.min(1, (now - t0) / dur);
      row.scrollLeft = from + (to - from) * easeOut(t);
      if (t < 1) rowAnim = requestAnimationFrame(step);
      else row.style.scrollSnapType = "";
    });
  }

  var current = null;
  function setActive(id, dur) {
    if (id === current) return;
    current = id;
    links.forEach(function (a) {
      if (idOf(a) === id) a.setAttribute("aria-current", "true");
      else a.removeAttribute("aria-current");
    });
    var a = linkFor(id);
    placeInd(a, !dur || reduce.matches);
    showTab(a, dur);
  }

  /* —— Hver fane er en egen side på mobil (Ole 27.11 kl. 18.30) ——
     Bare valgt del vises. Adressen bruker de faste id-ene: #siste-nytt, #tidslinje,
     #status og #nedtelling-land (#nedtelling godtas også). Fra 768 px er alt som før:
     ingen del skjules, og adressen styrer ingenting. */
  var PANELS = ["siste-nytt", "tidslinje", "status", "nedtelling-land"];
  var ALIAS = { "nedtelling": "nedtelling-land" };
  var root = document.documentElement;
  var pos = {};      /* rulleposisjon per fane i denne økten */
  var seen = {};     /* faner som er åpnet før i økten */
  try { pos = JSON.parse(sessionStorage.getItem("tm-pos") || "{}") || {}; } catch (e) { pos = {}; }
  function savePos() { try { sessionStorage.setItem("tm-pos", JSON.stringify(pos)); } catch (e) {} }

  function panel(id) { return document.getElementById(id); }
  function panelOf(el) {
    for (var i = 0; i < PANELS.length; i++) { var p = panel(PANELS[i]); if (p && p.contains(el)) return PANELS[i]; }
    return null;
  }

  /* Hva adressen peker på: { tab, el } der el er et anker inne i en fane */
  function resolve(hash) {
    var id = decodeURIComponent((hash || "").replace(/^#/, ""));
    if (!id) return { tab: "siste-nytt", el: null };
    if (ALIAS[id]) return { tab: ALIAS[id], el: null, alias: true };
    if (PANELS.indexOf(id) >= 0) return { tab: id, el: null };
    var el = document.getElementById(id);
    var tab = el && panelOf(el);
    return tab ? { tab: tab, el: el } : { tab: "siste-nytt", el: null };
  }

  function headerOffset() { return head.getBoundingClientRect().height + 16; }
  function topOf(id) {
    var p = panel(id);
    return p ? Math.max(0, p.getBoundingClientRect().top + window.scrollY - headerOffset()) : 0;
  }
  function jumpTo(y) { window.scrollTo({ top: y, left: 0, behavior: "instant" }); }

  function fadeIn(p) {
    if (reduce.matches) return;
    p.classList.add("tm-enter");
    void p.offsetWidth;
    requestAnimationFrame(function () { p.classList.remove("tm-enter"); });
  }

  /* Fokus til delen (ikke overskriften), uten ring og uten at siden hopper */
  function focusPanel(id) {
    var p = panel(id);
    if (!p) return;
    if (!p.hasAttribute("tabindex")) p.setAttribute("tabindex", "-1");
    try { p.focus({ preventScroll: true }); } catch (e) { p.focus(); }
  }

  /* Bytt fane. how: "top" | "restore" | element (anker inne i fanen) */
  function show(id, how, opts) {
    opts = opts || {};
    if (current && current !== id) pos[current] = window.scrollY;
    var same = current === id;
    PANELS.forEach(function (pid) {
      var p = panel(pid);
      if (p) p.classList.toggle("tm-on", pid === id);
    });
    setActive(id, opts.instant ? 0 : 350);
    var y;
    if (how && how.nodeType === 1) {
      var m = parseFloat(getComputedStyle(how).scrollMarginTop) || headerOffset();
      y = how.getBoundingClientRect().top + window.scrollY - m;
    } else if (how === "restore" && seen[id] && pos[id] != null && !same) y = pos[id];
    else y = topOf(id);
    seen[id] = true;
    jumpTo(Math.max(0, y));
    if (!same && !opts.instant) fadeIn(panel(id));
    if (opts.focus) focusPanel(id);
    savePos();
  }

  var tabsOn = false;
  function enableTabs() {
    if (tabsOn || !mq.matches) return;
    tabsOn = true;
    root.classList.add("tm-tabs");
    if ("scrollRestoration" in history) history.scrollRestoration = "manual";
    var r = resolve(location.hash);
    if (r.alias) history.replaceState(history.state, "", "#" + r.tab);
    show(r.tab, r.el || "top", { instant: true });
    /* Direktelenke til en sak: feeden tegnes på nytt når dataene kommer, så vi retter opp
       posisjonen et par ganger hvis leseren ikke har begynt å rulle selv */
    if (r.el) {
      var anchorId = r.el.id, touched = false;
      ["touchstart", "wheel", "keydown"].forEach(function (ev) {
        window.addEventListener(ev, function () { touched = true; }, { passive: true, once: true });
      });
      [400, 1200, 2500].forEach(function (ms) {
        setTimeout(function () {
          var el = document.getElementById(anchorId);
          if (touched || !tabsOn || !el || location.hash !== "#" + anchorId) return;
          var m = parseFloat(getComputedStyle(el).scrollMarginTop) || headerOffset();
          var d = el.getBoundingClientRect().top - m;
          if (Math.abs(d) > 2) jumpTo(window.scrollY + d);
        }, ms);
      });
    }
  }
  function disableTabs() {
    if (!tabsOn) return;
    tabsOn = false;
    root.classList.remove("tm-tabs");
    PANELS.forEach(function (pid) { var p = panel(pid); if (p) { p.classList.remove("tm-on", "tm-enter"); p.removeAttribute("tabindex"); } });
    if ("scrollRestoration" in history) history.scrollRestoration = "auto";
  }
  function onMq() { if (mq.matches) enableTabs(); else disableTabs(); }
  if (mq.addEventListener) mq.addEventListener("change", onMq);
  else if (mq.addListener) mq.addListener(onMq);

  /* Logoen «tadnorge» (lenke til /) går til Siste nytt på mobil (Ole 27.11 kl. 19.01).
     Uten JavaScript eller fra 768 px er den en vanlig lenke til forsiden. */
  var logoAnim = 0;
  function smoothTop(y) {
    cancelAnimationFrame(logoAnim);
    var from = window.scrollY;
    if (reduce.matches || Math.abs(from - y) < 2) { jumpTo(y); return; }
    var dur = Math.min(450, 300 + Math.abs(from - y) / 40), t0 = null, stop = false;
    function halt() { stop = true; }
    ["touchstart", "wheel", "keydown"].forEach(function (ev) { window.addEventListener(ev, halt, { passive: true, once: true }); });
    logoAnim = requestAnimationFrame(function step(now) {
      if (stop) return;
      if (t0 === null) t0 = now;
      var t = Math.min(1, (now - t0) / dur);
      jumpTo(from + (y - from) * easeOut(t));
      if (t < 1) logoAnim = requestAnimationFrame(step);
    });
  }
  var logo = head.querySelector(".brand-mark");
  if (logo) logo.addEventListener("click", function (e) {
    if (!tabsOn || e.button > 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    e.preventDefault();
    delete pos["siste-nytt"];
    if (current === "siste-nytt") {
      if (location.hash !== "#siste-nytt") history.replaceState(history.state, "", "#siste-nytt");
      smoothTop(topOf("siste-nytt"));
      focusPanel("siste-nytt");
      savePos();
      return;
    }
    if (location.hash !== "#siste-nytt") history.pushState(null, "", "#siste-nytt");
    show("siste-nytt", "top", { focus: true });
  });

  /* Fanene */
  links.forEach(function (a) {
    a.addEventListener("click", function (e) {
      if (!tabsOn) return;
      e.preventDefault();
      var id = idOf(a);
      if (id === current) { show(id, "top", { focus: true }); return; }
      if (location.hash !== "#" + id) history.pushState(null, "", "#" + id);
      show(id, "restore", { focus: true });
    });
  });

  /* Andre lenker til #anker på siden: bytt til riktig fane og rull til ankeret.
     Lenker til andre sider, for eksempel /nedtelling/, går som før. */
  document.addEventListener("click", function (e) {
    if (!tabsOn || e.defaultPrevented || e.button > 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest && e.target.closest("a[href]");
    if (!a || nav.contains(a)) return;
    var href = a.getAttribute("href");
    if (!href || href.charAt(0) !== "#" || href.length < 2) return;
    var r = resolve(href);
    e.preventDefault();
    if (location.hash !== href) history.pushState(null, "", href);
    show(r.tab, r.el || "top", { focus: !r.el });
  });

  /* Tilbake/fram i nettleseren */
  window.addEventListener("popstate", function () {
    if (!tabsOn) return;
    var r = resolve(location.hash);
    show(r.tab, r.el || "restore", { focus: true });
  });
  window.addEventListener("hashchange", function () {
    if (!tabsOn) return;
    var r = resolve(location.hash);
    if (r.tab !== current || r.el) show(r.tab, r.el || "restore");
  });

  function relayout() { if (current) placeInd(linkFor(current), true); edge(); }
  window.addEventListener("resize", relayout);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(relayout);

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

  enableTabs();
  if (!current) setActive(resolve(location.hash).tab, 0);
  edge();
})();
