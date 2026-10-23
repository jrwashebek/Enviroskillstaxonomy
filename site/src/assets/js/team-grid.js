// EMST team grid (View 2, team). Reads gap-check files the user selects, in the browser only, and shows counts per
// level for each competency when at least `min_cell` (5) compatible files are loaded. Notes and supervisor views are
// never read into the grid; no names exist in the files. No network or storage API is used. Licence: Apache-2.0.
(function () {
  "use strict";
  var input = document.getElementById("emst-team-files");
  var metaEl = document.getElementById("emst-team-meta");
  if (!input || !metaEl) return;
  var meta = JSON.parse(metaEl.textContent);
  var MIN = meta.min_cell || 5;
  var status = document.querySelector("[data-status]");
  var grid = document.querySelector("[data-grid]");
  var csvBtn = document.querySelector('[data-action="team-csv"]');
  var LEVELS = ["none", "L1", "L2", "L3", "L4", "L5", "unsure"];
  var LABEL = { none: "Not yet", unsure: "Not sure" };
  var last = null;

  function say(m) { status.textContent = ""; window.setTimeout(function () { status.textContent = m; }, 30); }
  function readAll(files) {
    return Promise.all(Array.prototype.map.call(files, function (f) {
      return new Promise(function (res) {
        if (f.size > 2 * 1024 * 1024) return res(null);
        var r = new FileReader();
        r.onload = function () { try { res(JSON.parse(String(r.result))); } catch (e) { res(null); } };
        r.onerror = function () { res(null); };
        r.readAsText(f);
      });
    }));
  }
  function el(tag, text, attrs) {
    var e = document.createElement(tag);
    if (text != null) e.textContent = text;
    if (attrs) Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    return e;
  }
  input.addEventListener("change", function () {
    grid.textContent = ""; if (csvBtn) csvBtn.hidden = true; last = null;
    readAll(input.files).then(function (docs) {
      var ok = docs.filter(function (d) { return d && d.schema_version === "emst-gap-check@1" && Array.isArray(d.ratings); });
      var bad = docs.length - ok.length;
      var groups = {};
      ok.forEach(function (d) {
        var key = d.mode === "role" ? (d.role_variant_id + " · " + d.level) : "chosen competencies";
        (groups[key] = groups[key] || []).push(d);
      });
      var keys = Object.keys(groups).sort(function (a, b) { return groups[b].length - groups[a].length; });
      if (!keys.length) { say("No gap-check files found among the " + docs.length + " files chosen."); return; }
      var key = keys[0], set = groups[key];
      var extra = (bad ? " " + bad + " files were not gap-check files." : "") + (keys.length > 1 ? " Files for other roles or levels were set aside." : "");
      if (set.length < MIN) {
        say("Fewer than " + MIN + " compatible files (" + set.length + " for " + key + "), so no grid is shown. Looking at individual files is up to the people who shared them." + extra);
        return;
      }
      var counts = {};
      set.forEach(function (d) {
        d.ratings.forEach(function (r) {
          if (!r.self) return;
          var c = counts[r.competency] = counts[r.competency] || {};
          c[r.self] = (c[r.self] || 0) + 1;
        });
      });
      var table = el("table", null, { "class": "usa-table usa-table--compact" });
      table.appendChild(el("caption", "Counts of people at each level, " + set.length + " files, " + key + ". Release " + meta.release_id + "."));
      var thead = el("thead"), hr = el("tr");
      hr.appendChild(el("th", "Competency", { scope: "col" }));
      LEVELS.forEach(function (l) { hr.appendChild(el("th", LABEL[l] || l, { scope: "col", "class": "emst-num" })); });
      thead.appendChild(hr); table.appendChild(thead);
      var tb = el("tbody"); var rowsOut = [];
      Object.keys(counts).sort(function (a, b) { return (meta.titles[a] || a).localeCompare(meta.titles[b] || b); }).forEach(function (id) {
        var tr = el("tr");
        tr.appendChild(el("th", meta.titles[id] || id, { scope: "row" }));
        var out = [id, meta.titles[id] || id];
        LEVELS.forEach(function (l) { var n = counts[id][l] || 0; tr.appendChild(el("td", String(n), { "class": "emst-num" })); out.push(n); });
        tb.appendChild(tr); rowsOut.push(out);
      });
      table.appendChild(tb);
      var wrap = el("div", null, { "class": "emst-table-wrap", tabindex: "0", role: "region", "aria-label": "Team grid" });
      wrap.appendChild(table); grid.appendChild(wrap);
      grid.appendChild(el("p", "Self-ratings only; supervisor views and notes in the files are ignored. Counts describe this group for development planning and must not be used to rate, rank or select anyone."));
      last = { key: key, rows: rowsOut };
      if (csvBtn) csvBtn.hidden = false;
      say("Grid built from " + set.length + " files." + extra);
    });
  });
  if (csvBtn) csvBtn.addEventListener("click", function () {
    if (!last) return;
    var lines = [["competency_id", "competency"].concat(LEVELS).concat(["group", "release_id"]).join(",")];
    last.rows.forEach(function (r) { lines.push(r.concat([last.key, meta.release_id]).map(function (s) { s = String(s); return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; }).join(",")); });
    var blob = new Blob([lines.join("\n") + "\n"], { type: "text/csv" });
    var url = URL.createObjectURL(blob), a = document.createElement("a");
    a.href = url; a.download = "emst-team-grid.csv"; document.body.appendChild(a); a.click(); document.body.removeChild(a);
    window.setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  });
})();
