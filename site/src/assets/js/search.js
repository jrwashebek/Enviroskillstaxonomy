// EMST local search. The index is embedded in the page and loaded before the user types, so no request depends on
// the query (ADR-0012: no user input in URLs or requests). No network or storage API. Licence: Apache-2.0.
(function () {
  "use strict";
  var idxEl = document.getElementById("emst-search-index");
  var input = document.getElementById("emst-q");
  var out = document.querySelector("[data-results]");
  var status = document.querySelector("[data-status]");
  var form = document.querySelector("[data-search-form]");
  if (!idxEl || !input || !out) return;
  var base = (document.querySelector('link[rel="stylesheet"][href*="/assets/css/emst.css"]') || {}).getAttribute
    ? document.querySelector('link[rel="stylesheet"][href*="/assets/css/emst.css"]').getAttribute("href").replace(/assets\/css\/emst\.css$/, "")
    : "/";
  var items = JSON.parse(idxEl.textContent).map(function (x) { return { t: x.t, k: x.k, u: x.u, hay: (x.t + " " + (x.a || "")).toLowerCase() }; });
  function norm(s) { return s.toLowerCase().replace(/[^a-z0-9 ]+/g, " ").trim(); }
  var timer = null;
  function run() {
    var q = norm(input.value);
    out.textContent = "";
    if (q.length < 2) { status.textContent = ""; return; }
    var terms = q.split(/\s+/);
    var hits = [];
    for (var i = 0; i < items.length; i++) {
      var it = items[i], ok = true, score = 0;
      for (var j = 0; j < terms.length; j++) {
        var p = it.hay.indexOf(terms[j]);
        if (p < 0) { ok = false; break; }
        score += p === 0 ? 3 : (it.hay.charAt(p - 1) === " " ? 2 : 1);
      }
      if (ok) hits.push({ it: it, score: score });
    }
    hits.sort(function (a, b) { return (b.score - a.score) || a.it.t.length - b.it.t.length; });
    hits.slice(0, 50).forEach(function (h) {
      var li = document.createElement("li"), a = document.createElement("a");
      var url = base.replace(/\/$/, "") + h.it.u;
      if (base.charAt(0) !== "/") url = base + h.it.u.slice(1).replace(/\/(#.*)?$/, "/index.html$1");
      a.href = url; a.textContent = h.it.t;
      li.appendChild(a); li.appendChild(document.createTextNode(" (" + h.it.k + ")"));
      out.appendChild(li);
    });
    status.textContent = hits.length ? (hits.length > 50 ? "Showing 50 of " + hits.length + " results." : hits.length + " results.") : "No results.";
  }
  input.addEventListener("input", function () { window.clearTimeout(timer); timer = window.setTimeout(run, 150); });
  if (form) form.addEventListener("submit", function (e) { e.preventDefault(); run(); });
})();
