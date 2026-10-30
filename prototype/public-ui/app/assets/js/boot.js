// Runs before first paint, before the app bundle: index.html lists it last in <head>, after every file the page fetches
// (with a CSP <meta>, Chrome does not fetch ahead of a parser-blocking script). No storage, no fetch, no inline code.
// Licence: Apache-2.0.
// 1. Marks that scripts are on (the menu collapses on small screens).
// 2. On a deep link, marks the page so app.css hides the home page that index.html carries prerendered; it never flashes.
// 3. Starts the route's data file now, beside the app bundle, from the map tools/build-app.mjs writes into
//    <meta name="emst-early-data">. Data still loads as <script src>; lib/data.js waits for a data script that is in
//    flight instead of adding a second one, and this file marks each data script when it has loaded or failed.
// 4. Fonts: index.html links the @font-face rules as their own stylesheet with media="print", so they fetch nothing at
//    first. On the home page they apply at once. On a deep link they apply once the route's H1 has rendered, because on a
//    slow connection the three font files would share the bandwidth the bundle and data need for that first view. Text
//    shows in the fallback font until then (font-display: swap); fonts never block a paint.
// 5. Until main.js replaces the prerendered chrome and home page (marked data-prerender) with live, identical markup, it
//    keeps them usable: the menu button works, and a search sent early is sent again once the app is ready. When the
//    markup is replaced, focus, typed text, an open menu and the scroll position on the home page carry over.
(function () {
  "use strict";
  var doc = document, root = doc.documentElement;
  root.classList.add("js");

  function routeOf(hash) { // as lib/router.js reads it: null for a plain anchor such as #main
    try {
      var s = decodeURIComponent(String(hash || "").replace(/^#/, ""));
      return s.charAt(0) === "/" ? s.split("@")[0] || "/" : null;
    } catch (e) { return "?"; }
  }
  var path = routeOf(location.hash);
  function markRoute(p) { root.classList.toggle("route-deep", p !== null && p !== "/"); }
  markRoute(path);

  // ---------------------------------------------------------------- fonts (index.html only)
  var fonts = doc.getElementById("emst-fonts");
  function fontsOn() { if (fonts) { fonts.media = "all"; fonts = null; } }
  function routeShown() { return !doc.querySelector("#main [data-prerender]") && !!doc.querySelector("#main h1"); }
  if (!root.classList.contains("route-deep")) fontsOn();
  else if (fonts) {
    doc.addEventListener("DOMContentLoaded", function () {
      var main = doc.getElementById("main");
      if (routeShown() || !main || !window.MutationObserver) return fontsOn();
      var mo = new MutationObserver(function () { if (routeShown()) { mo.disconnect(); fontsOn(); } });
      mo.observe(main, { childList: true });
    });
    window.addEventListener("load", fontsOn); // safety net
  }

  // ---------------------------------------------------------------- data scripts
  function markDone(e) { var t = e.target; if (t && t.tagName === "SCRIPT") t.setAttribute("data-done", e.type); }
  doc.addEventListener("load", markDone, true);
  doc.addEventListener("error", markDone, true);

  var meta = doc.querySelector('meta[name="emst-early-data"]');
  if (meta && path) {
    var entries = (meta.getAttribute("content") || "").split(/\s+/);
    for (var i = 0; i < entries.length; i++) {
      var eq = entries[i].indexOf("="), file = entries[i].slice(0, eq), routes = entries[i].slice(eq + 1).split(",");
      if (eq < 1 || !/^[a-z0-9-]+$/.test(file)) continue;
      for (var j = 0; j < routes.length; j++) {
        if (path === routes[j] || path.indexOf(routes[j] + "/") === 0) { loadEarly(file); break; }
      }
    }
  }
  function loadEarly(file) {
    var src = "data/" + file + ".js";
    if (doc.querySelector('script[src="' + src + '"]')) return;
    var el = doc.createElement("script");
    el.src = src;
    el.async = true;
    doc.head.appendChild(el);
  }

  // ---------------------------------------------------------------- prerendered markup (index.html only)
  var PRE = "[data-prerender]";
  var held = null, menuOpen = false, homeY = 0, observer = null;
  function pre(el) { return el && el.closest ? el.closest(PRE) : null; }
  function locate(el) { // where an element sits, so the same element can be found in the replacement markup
    var box = el.closest("#site-top, #site-bottom, #main");
    if (!box) return null;
    var steps = [];
    for (var n = el; n !== box; n = n.parentElement) steps.unshift(Array.prototype.indexOf.call(n.parentElement.children, n));
    return { box: box.id, steps: steps, el: el, submit: false };
  }
  function find(loc) {
    var n = doc.getElementById(loc.box);
    for (var i = 0; n && i < loc.steps.length; i++) n = n.children[loc.steps[i]];
    if (!n || pre(n) || n.tagName !== loc.el.tagName || n.id !== loc.el.id || n.getAttribute("class") !== loc.el.getAttribute("class")) return null;
    return n;
  }
  function watch() {
    if (observer || !window.MutationObserver) return;
    observer = new MutationObserver(restore);
    ["site-top", "main", "site-bottom"].forEach(function (id) { var b = doc.getElementById(id); if (b) observer.observe(b, { childList: true }); });
  }
  function restore() {
    if (held && !held.el.isConnected) {
      var n = find(held);
      if (n) {
        var old = held.el, submit = held.submit, active = doc.activeElement;
        held = null;
        var typed = n.tagName === "INPUT" && old.value;
        if (typed) { n.value = old.value; try { n.setSelectionRange(old.selectionStart, old.selectionEnd); } catch (e) { /* not a text field */ } }
        if (!active || active === doc.body) n.focus({ preventScroll: true });
        if (submit && n.form) n.form.requestSubmit();
        else if (typed) n.dispatchEvent(new Event("input", { bubbles: true })); // the combobox offers suggestions
      }
    }
    if (menuOpen) {
      var toggle = doc.querySelector(".site-nav__toggle");
      if (toggle && !pre(toggle)) { menuOpen = false; if (toggle.getAttribute("aria-expanded") !== "true") toggle.click(); }
    }
    if (homeY && !doc.querySelector('[data-prerender="home"]')) {
      var y = homeY;
      homeY = 0;
      if (routeOf(location.hash) === "/" && window.scrollY === 0) window.scrollTo(0, y);
    }
    if (!doc.querySelector(PRE)) { observer.disconnect(); held = null; menuOpen = false; homeY = 0; }
  }
  doc.addEventListener("focusin", function (e) {
    if (pre(e.target)) { held = locate(e.target); watch(); }
    else if (held && !held.submit) held = null;
  }, true);
  doc.addEventListener("focusout", function (e) { // focus left for empty page space, not because the markup was replaced
    var h = held;
    if (h && e.target === h.el && !e.relatedTarget) setTimeout(function () { if (held === h && h.el.isConnected && doc.activeElement !== h.el && !h.submit) held = null; }, 0);
  }, true);
  doc.addEventListener("submit", function (e) {
    if (!pre(e.target)) return;
    e.preventDefault(); // the app is not ready; send it again when it is (and CSP form-action 'none' would block it)
    var field = e.target.querySelector("input");
    held = field ? locate(field) : null;
    if (held) { held.submit = true; watch(); }
  }, true);
  doc.addEventListener("click", function (e) {
    var t = e.target;
    if (!t || !t.closest) return;
    var toggle = t.closest(".site-nav__toggle"), link = t.closest(".site-nav__list a");
    if (toggle && pre(toggle)) { // the same behaviour main.js gives the live button
      var list = doc.getElementById(toggle.getAttribute("aria-controls"));
      if (!list) return;
      menuOpen = list.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(menuOpen));
      watch();
    } else if (link && pre(link)) {
      link.closest(".site-nav__list").classList.remove("is-open");
      var tg = doc.querySelector(PRE + " .site-nav__toggle");
      if (tg) tg.setAttribute("aria-expanded", "false");
      menuOpen = false;
    }
  });
  window.addEventListener("hashchange", function () { // a prerendered link followed before the app is ready
    var p = routeOf(location.hash);
    if (p !== null && doc.querySelector('[data-prerender="home"]')) { markRoute(p); if (p === "/") fontsOn(); }
  });
  window.addEventListener("scroll", function () {
    if (!root.classList.contains("route-deep") && doc.querySelector('[data-prerender="home"]')) { homeY = window.scrollY; watch(); }
  }, { passive: true });
})();
