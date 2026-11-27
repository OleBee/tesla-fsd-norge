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

  /* —— Faner, glidende strek og myk rulling ——
     Egen animasjon med requestAnimationFrame i stedet for innebygd «smooth»:
     den hakker i Safari på iOS og bommer når bilder lastes underveis. */
  var row = nav.querySelector("ul");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  var DUR_MIN = 300, DUR_MAX = 450;

  function easeOut(t) { return 1 - Math.pow(1 - t, 3); }
  function duration(dist) { return reduce.matches ? 0 : Math.min(DUR_MAX, DUR_MIN + Math.abs(dist) / 40); }
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

  /* —— Rulling til en del —— */
  var anim = null;   /* { id, raf } mens siden ruller; rullesporingen står stille da */
  function stopAnim() {
    if (!anim) return;
    cancelAnimationFrame(anim.raf);
    anim = null;
    spy();
  }
  ["touchstart", "wheel", "keydown"].forEach(function (ev) {
    window.addEventListener(ev, function () { if (anim && anim.started) stopAnim(); }, { passive: true });
  });

  function targetY(sec) {
    var margin = parseFloat(getComputedStyle(sec).scrollMarginTop) || 0;
    var y = sec.getBoundingClientRect().top + window.scrollY - margin;
    var max = document.documentElement.scrollHeight - window.innerHeight;
    return Math.max(0, Math.min(y, max));
  }

  function scrollToSection(id) {
    var sec = document.getElementById(id);
    if (!sec) return;
    if (anim) cancelAnimationFrame(anim.raf);
    var from = window.scrollY, dur = duration(targetY(sec) - from);
    var t0 = null, settle = 0;
    anim = { id: id, raf: 0, started: false };
    setActive(id, dur);
    function frame(now) {
      if (!anim) return;
      anim.started = true;
      if (t0 === null) t0 = now;
      var to = targetY(sec);   /* målet leses på nytt hver ramme, så bilder som lastes ikke gir rykk */
      var t = dur ? Math.min(1, (now - t0) / dur) : 1;
      var y;
      if (t < 1) y = from + (to - from) * easeOut(t);
      else {
        /* Etterpå: følg målet mykt et lite øyeblikk hvis det flytter seg */
        var diff = to - window.scrollY;
        y = Math.abs(diff) < 1 || reduce.matches ? to : window.scrollY + diff * 0.35;
        settle += 1;
      }
      window.scrollTo({ top: y, left: 0, behavior: "instant" });
      if (t < 1 || (settle < 36 && Math.abs(targetY(sec) - window.scrollY) >= 1) || settle < 12) anim.raf = requestAnimationFrame(frame);
      else { anim = null; spy(); }
    }
    anim.raf = requestAnimationFrame(frame);
  }

  links.forEach(function (a) {
    a.addEventListener("click", function (e) {
      var id = idOf(a);
      e.preventDefault();
      if (location.hash !== "#" + id) history.pushState(null, "", "#" + id);
      scrollToSection(id);
    });
  });

  /* —— Rullesporing med hysterese ——
     Valgt del er den siste som har passert en linje rett under toppen.
     Bytte krever at den nye delen er minst 8 px forbi linjen, så fanene ikke blinker på grensene. */
  var HYST = 8;
  function spy() {
    if (!mq.matches || anim) return;
    var line = head.getBoundingClientRect().height + 24;
    var tops = links.map(function (a) {
      var sec = document.getElementById(idOf(a));
      return { id: idOf(a), top: sec ? sec.getBoundingClientRect().top : Infinity };
    });
    var cand = null;
    tops.forEach(function (o) { if (o.top <= line && (!cand || o.top > cand.top)) cand = o; });
    if (!cand) cand = tops.reduce(function (m, o) { return o.top < m.top ? o : m; });
    /* Nederst på siden: siste del vinner */
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) {
      var last = tops.reduce(function (m, o) { return o.top > m.top ? o : m; });
      if (last.top < window.innerHeight) cand = last;
    }
    if (!current) { setActive(cand.id, 0); return; }
    if (cand.id === current) return;
    var cur = tops.filter(function (o) { return o.id === current; })[0];
    var goingDown = cand.top > cur.top;
    if ((goingDown && cand.top <= line - HYST) || (!goingDown && cur.top > line + HYST) || cur.top === Infinity) setActive(cand.id, 250);
  }
  var queued = false;
  window.addEventListener("scroll", function () {
    if (queued || anim) return;
    queued = true;
    requestAnimationFrame(function () { queued = false; spy(); });
  }, { passive: true });

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

  if (location.hash === "#nedtelling-land") setTimeout(function () { scrollToSection("nedtelling-land"); }, 400);
  spy();
  if (!current) setActive("siste-nytt", 0);
  edge();
})();
