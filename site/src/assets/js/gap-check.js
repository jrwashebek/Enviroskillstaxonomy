// EMST gap check (View 2). Runs only in the browser: ratings live in memory and leave the page only as a file the
// user saves (ADR-0012 I-1; Tier 1). This script uses no network API, no storage API and never writes the address bar.
// It ranks competencies for development, never people, and computes no score (ADR-0012 I-2). Licence: Apache-2.0.
(function () {
  "use strict";
  var form = document.querySelector("[data-gap-form]");
  var metaEl = document.getElementById("emst-gap-meta");
  if (!form || !metaEl) return;
  var meta = JSON.parse(metaEl.textContent);
  var SCHEMA = "emst-gap-check@1";
  var ORD = { none: 0, L1: 1, L2: 2, L3: 3, L4: 4, L5: 5 };
  var status = form.querySelector("[data-status]");
  var summary = document.querySelector("[data-summary]");
  var summaryBody = summary ? summary.querySelector("[data-summary-body]") : null;
  var dirty = false;

  function say(msg) { if (status) { status.textContent = ""; window.setTimeout(function () { status.textContent = msg; }, 30); } }
  function rows() { return Array.prototype.slice.call(form.querySelectorAll("fieldset.emst-rate[data-competency]")); }
  function radioValue(scope, role) {
    var g = scope.querySelector('[data-role="' + role + '"]');
    if (!g) return null;
    var c = g.querySelector("input[type=radio]:checked");
    return c ? c.value : null;
  }
  function setRadio(scope, role, value) {
    var g = scope.querySelector('[data-role="' + role + '"]');
    if (!g) return;
    Array.prototype.forEach.call(g.querySelectorAll("input[type=radio]"), function (r) { r.checked = (value != null && r.value === value); });
  }
  function roleLevel() {
    var c = form.querySelector('[data-role="level-choice"] input[type=radio]:checked');
    return c ? c.value : null;
  }
  function targetFor(fs) {
    if (meta.mode === "competencies") {
      var aim = fs.querySelector('[data-role="aim"]');
      return aim && aim.value ? aim.value : null;
    }
    var t = fs.getAttribute("data-targets");
    if (!t) return null;
    try { var m = JSON.parse(t); return m[roleLevel()] || null; } catch (e) { return null; }
  }
  function updateTargets() {
    if (meta.mode !== "role") return;
    rows().forEach(function (fs) {
      var p = fs.querySelector("[data-target-text]");
      var t = targetFor(fs);
      if (p) p.textContent = t ? "Target for the " + roleLevel() + " level of this role: " + t : "No target for the " + roleLevel() + " level of this role.";
    });
  }

  function collect() {
    var out = [];
    rows().forEach(function (fs) {
      var self = radioValue(fs, "self"), sup = radioValue(fs, "supervisor");
      var noteEl = fs.querySelector('[data-role="note"]');
      var aimEl = fs.querySelector('[data-role="aim"]');
      var note = noteEl ? noteEl.value.trim() : "";
      var aim = aimEl ? aimEl.value : "";
      if (!self && !sup && !note && !aim) return;
      var r = { competency: fs.getAttribute("data-competency"), self: self || null };
      if (sup) r.supervisor = sup;
      if (aim) r.aim = aim;
      if (note) r.note = note;
      out.push(r);
    });
    return out;
  }
  function payload() {
    return {
      schema_version: SCHEMA, release_id: meta.release_id, role_variant_id: meta.role_variant_id || null,
      level: meta.mode === "role" ? roleLevel() : null, mode: meta.mode, ratings: collect(),
    };
  }
  function download(name, text, type) {
    var blob = new Blob([text], { type: type });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url; a.download = name; a.rel = "noopener";
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    window.setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }

  function apply(data) {
    if (!data || data.schema_version !== SCHEMA || !Array.isArray(data.ratings)) throw new Error("This is not an EMST gap-check file (schema " + SCHEMA + ").");
    if (data.mode !== meta.mode) throw new Error("This file was saved from a different kind of gap check (" + data.mode + ").");
    if (meta.mode === "role" && data.role_variant_id !== meta.role_variant_id) throw new Error("This file is for a different role variant (" + data.role_variant_id + ").");
    clearAll(true);
    if (meta.mode === "role" && data.level) {
      var lv = form.querySelector('[data-role="level-choice"] input[value="' + cssEscape(data.level) + '"]');
      if (lv) lv.checked = true;
    }
    var byId = {};
    rows().forEach(function (fs) { byId[fs.getAttribute("data-competency")] = fs; });
    var missing = 0;
    data.ratings.forEach(function (r) {
      var fs = byId[r.competency];
      if (!fs) { missing++; return; }
      setRadio(fs, "self", r.self); setRadio(fs, "supervisor", r.supervisor || null);
      var n = fs.querySelector('[data-role="note"]'); if (n) n.value = typeof r.note === "string" ? r.note.slice(0, 500) : "";
      var a = fs.querySelector('[data-role="aim"]'); if (a) a.value = r.aim || "";
      var d = fs.closest("details"); if (d) d.open = true;
    });
    updateTargets();
    var note = data.release_id !== meta.release_id ? " It was saved from release " + data.release_id + "; this page is release " + meta.release_id + ", so some competencies may have changed." : "";
    say("Opened " + data.ratings.length + " ratings." + (missing ? " " + missing + " competencies in the file are not on this page." : "") + note);
    dirty = false;
  }
  function cssEscape(s) { return String(s).replace(/["\\]/g, "\\$&"); }
  function clearAll(silent) {
    rows().forEach(function (fs) {
      Array.prototype.forEach.call(fs.querySelectorAll("input[type=radio]"), function (r) { r.checked = false; });
      var n = fs.querySelector('[data-role="note"]'); if (n) n.value = "";
      var a = fs.querySelector('[data-role="aim"]'); if (a) a.value = "";
    });
    if (summary) { summary.hidden = true; if (summaryBody) summaryBody.textContent = ""; }
    dirty = false;
    if (!silent) say("Cleared. Nothing was stored anywhere, so there is nothing else to delete.");
  }

  function analyse() {
    var items = [];
    rows().forEach(function (fs) {
      var self = radioValue(fs, "self"), sup = radioValue(fs, "supervisor"), target = targetFor(fs);
      if (!self && !sup) return;
      items.push({
        id: fs.getAttribute("data-competency"), title: fs.getAttribute("data-title"), url: fs.getAttribute("data-url"),
        importance: Number(fs.getAttribute("data-importance")) || 0, self: self, sup: sup, target: target,
        gap: (target && self && self !== "unsure") ? (ORD[target] - ORD[self]) : null,
      });
    });
    var gaps = items.filter(function (i) { return i.gap != null && i.gap > 0; })
      .sort(function (a, b) { return (b.gap - a.gap) || (b.importance - a.importance) || a.title.localeCompare(b.title); });
    return {
      items: items, start: gaps.slice(0, 3), more: gaps.slice(3),
      strengths: items.filter(function (i) { return i.gap != null && i.gap <= 0; }),
      unsure: items.filter(function (i) { return i.self === "unsure"; }),
      noTarget: items.filter(function (i) { return !i.target && i.self && i.self !== "unsure"; }),
      differ: items.filter(function (i) { return i.sup && i.self && i.sup !== "unsure" && i.self !== "unsure" && i.sup !== i.self; }),
    };
  }
  function el(tag, text, attrs) {
    var e = document.createElement(tag);
    if (text != null) e.textContent = text;
    if (attrs) Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    return e;
  }
  function list(title, xs, fmt) {
    var sec = document.createElement("div");
    sec.appendChild(el("h3", title + " (" + xs.length + ")"));
    if (!xs.length) { sec.appendChild(el("p", "None.")); return sec; }
    var ul = el("ul", null, { "class": "usa-list" });
    xs.forEach(function (i) {
      var li = document.createElement("li");
      li.appendChild(el("a", i.title, { href: i.url }));
      li.appendChild(document.createTextNode(" " + fmt(i)));
      ul.appendChild(li);
    });
    sec.appendChild(ul);
    return sec;
  }
  function lv(x) { return x === "none" ? "not yet at the first level" : x === "unsure" ? "not sure" : x; }
  function renderSummary() {
    if (!summary || !summaryBody) return;
    var a = analyse();
    summaryBody.textContent = "";
    if (!a.items.length) {
      summaryBody.appendChild(el("p", "Rate at least one competency to see priorities."));
    } else {
      summaryBody.appendChild(list("Start with these", a.start, function (i) { return "now " + lv(i.self) + ", target " + i.target + "."; }));
      summaryBody.appendChild(list("Other gaps", a.more, function (i) { return "now " + lv(i.self) + ", target " + i.target + "."; }));
      summaryBody.appendChild(list("Where self and supervisor differ (talk about these)", a.differ, function (i) { return "self " + lv(i.self) + ", supervisor " + lv(i.sup) + "."; }));
      summaryBody.appendChild(list("Not sure yet", a.unsure, function () { return "look at the indicators with your supervisor."; }));
      summaryBody.appendChild(list("At or above the target", a.strengths, function (i) { return "now " + lv(i.self) + ", target " + i.target + "."; }));
      if (a.noTarget.length) summaryBody.appendChild(list("Rated without a target", a.noTarget, function (i) { return "now " + lv(i.self) + "."; }));
      summaryBody.appendChild(el("p", "Release " + meta.release_id + ". For development and planning; not a selection instrument. Targets and indicators are drafts that have not been validated."));
    }
    summary.hidden = false;
    var h = summary.querySelector("h2"); if (h) h.focus();
  }
  function csvCell(s) { s = String(s == null ? "" : s); return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; }
  function exportCsv() {
    var a = analyse();
    var lines = [["priority_group", "competency_id", "competency", "self", "supervisor", "target", "release_id", "notice"].join(",")];
    var notice = "For development and planning; not a selection instrument";
    function add(group, xs) { xs.forEach(function (i) { lines.push([group, i.id, i.title, i.self || "", i.sup || "", i.target || "", meta.release_id, notice].map(csvCell).join(",")); }); }
    add("start-with", a.start); add("other-gap", a.more); add("self-supervisor-differ", a.differ); add("not-sure", a.unsure); add("at-or-above-target", a.strengths);
    download((meta.file || "emst-gap-check").replace(/\.emst\.json$/, "") + "-priorities.csv", lines.join("\n") + "\n", "text/csv");
    say("Priorities downloaded as CSV.");
  }

  form.addEventListener("change", function (e) {
    dirty = true;
    if (e.target && (e.target.name === "role-level" || e.target.getAttribute("data-role") === "aim")) updateTargets();
  });
  form.addEventListener("input", function () { dirty = true; });
  form.addEventListener("submit", function (e) { e.preventDefault(); });
  document.addEventListener("click", function (e) {
    var b = e.target.closest ? e.target.closest("[data-action]") : null;
    if (!b) return;
    var act = b.getAttribute("data-action");
    if (act === "save") {
      var p = payload();
      download(meta.file || "emst-gap-check.emst.json", JSON.stringify(p, null, 1), "application/json");
      dirty = false;
      say("Saved " + p.ratings.length + " ratings to " + (meta.file || "a file") + " in your downloads. Nothing was sent anywhere.");
    } else if (act === "clear") { clearAll(false); }
    else if (act === "summary") { renderSummary(); }
    else if (act === "csv") { exportCsv(); }
    else if (act === "print") { window.print(); }
  });
  var opener = document.getElementById("emst-open-file");
  if (opener) opener.addEventListener("change", function () {
    var f = opener.files && opener.files[0];
    if (!f) return;
    if (f.size > 2 * 1024 * 1024) { say("That file is too large to be a gap-check file."); return; }
    var reader = new FileReader();
    reader.onload = function () {
      try { apply(JSON.parse(String(reader.result))); } catch (err) { say("Could not open the file: " + err.message); }
      opener.value = "";
    };
    reader.readAsText(f);
  });
  window.addEventListener("beforeunload", function (e) { if (dirty) { e.preventDefault(); e.returnValue = ""; } });
  updateTargets();
})();
