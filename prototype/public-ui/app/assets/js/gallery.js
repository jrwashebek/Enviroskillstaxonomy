/* EMST design-system gallery behaviour. Reference implementations of the interactive patterns
   (combobox, tabs, sortable table, copy, print) for the front-end developers. No network, no storage. */
(function () {
  "use strict";
  var doc = document, root = doc.documentElement;
  root.classList.add("js");

  function $(sel, ctx) { return (ctx || doc).querySelector(sel); }
  function $all(sel, ctx) { return Array.prototype.slice.call((ctx || doc).querySelectorAll(sel)); }

  /* ---------- Theme switch (gallery only; the site follows the device unless data-theme is set) ---------- */
  function paintSwatches() {
    var cs = getComputedStyle(root);
    $all("[data-token]").forEach(function (el) { el.style.background = "var(" + el.getAttribute("data-token") + ")"; });
    $all("[data-token-value]").forEach(function (el) { el.textContent = cs.getPropertyValue(el.getAttribute("data-token-value")).trim(); });
  }
  $all('#theme-switch input[name="theme"]').forEach(function (input) {
    input.addEventListener("change", function () {
      if (input.value === "system") root.removeAttribute("data-theme"); else root.setAttribute("data-theme", input.value);
      paintSwatches();
    });
  });
  var initial = root.getAttribute("data-theme");
  if (initial) { var r = $('#theme-switch input[value="' + initial + '"]'); if (r) r.checked = true; }
  paintSwatches();
  if (window.matchMedia) {
    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    if (mq.addEventListener) mq.addEventListener("change", paintSwatches);
  }

  /* ---------- Navigation toggle (small screens) ---------- */
  var toggle = $(".site-nav__toggle");
  if (toggle) {
    var list = doc.getElementById(toggle.getAttribute("aria-controls"));
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      list.classList.toggle("is-open", !open);
    });
  }

  /* ---------- Tabs: ARIA tabs with automatic activation and roving tabindex ---------- */
  $all("[data-tabs]").forEach(function (tabs) {
    var tabList = $all('[role="tab"]', tabs);
    function select(tab, focus) {
      tabList.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", String(on));
        t.tabIndex = on ? 0 : -1;
        doc.getElementById(t.getAttribute("aria-controls")).hidden = !on;
      });
      if (focus) tab.focus();
    }
    tabList.forEach(function (tab, i) {
      tab.addEventListener("click", function () { select(tab, false); });
      tab.addEventListener("keydown", function (e) {
        var n = tabList.length, next = null;
        if (e.key === "ArrowRight" || e.key === "ArrowDown") next = tabList[(i + 1) % n];
        else if (e.key === "ArrowLeft" || e.key === "ArrowUp") next = tabList[(i - 1 + n) % n];
        else if (e.key === "Home") next = tabList[0];
        else if (e.key === "End") next = tabList[n - 1];
        if (next) { e.preventDefault(); select(next, true); }
      });
    });
  });

  /* ---------- Search combobox (ARIA 1.2 combobox with listbox popup) ---------- */
  var SUGGEST = [
    { t: "Fuels and prescribed fire specialist", k: "Role", x: "Forest module", a: "rx burn fuels fire" },
    { t: "Wildland fire operations (crew to supervisor)", k: "Role", x: "Forest module", a: "firefighter crew 0462 fire" },
    { t: "Fire intelligence analyst (continuous operations)", k: "Role", x: "Watch: may be forming", a: "fire" },
    { t: "Plan smoke management for prescribed and managed fire within air quality requirements", k: "Competency", x: "Air module, levels L2 to L4", a: "rx burn smoke" },
    { t: "Field resource technician", k: "Role", x: "Core module", a: "tech 0462 0404 0455 0458 forestry technician" },
    { t: "Forestry Technician", k: "OPM series 0462", x: "4 linked roles", a: "0462 forestry tech" },
    { t: "Hydrologist", k: "Role", x: "Water quality module", a: "water hydrology" },
    { t: "Water and wastewater treatment operator", k: "Role", x: "Water module", a: "water wastewater" },
    { t: "Measure water quality and survey aquatic communities in the field", k: "Competency", x: "Levels L1 to L4", a: "wq water quality sampling" },
    { t: "Conservation corps member", k: "Role", x: "Core module", a: "corpsmember americorps crew" },
    { t: "Ground-truth remote-sensed, modelled and AI-generated outputs in the field", k: "Competency", x: "Watch, levels L1 to L4", a: "validation remote sensing ai" }
  ];
  var form = $("#site-search");
  if (form) {
    var input = $("#q"), lb = $("#q-list"), status = $("#q-status"), items = [], active = -1, announceTimer;
    function words(s) { return s.toLowerCase().split(/\s+/).filter(Boolean); }
    function matches(q) {
      var w = words(q);
      if (!w.length) return [];
      return SUGGEST.filter(function (s) {
        var hay = (s.t + " " + s.a + " " + s.k).toLowerCase();
        return w.every(function (x) { return hay.indexOf(x) !== -1; });
      }).slice(0, 6);
    }
    function highlight(el, text, q) {
      var w = words(q).filter(function (x) { return x.length > 1; });
      if (!w.length) { el.textContent = text; return; }
      var re = new RegExp("(" + w.map(function (x) { return x.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }).join("|") + ")", "gi");
      text.split(re).forEach(function (part, i) {
        if (i % 2) { var m = doc.createElement("mark"); m.textContent = part; el.appendChild(m); }
        else if (part) el.appendChild(doc.createTextNode(part));
      });
    }
    function setActive(i) {
      active = i;
      $all('[role="option"]', lb).forEach(function (o, j) { o.setAttribute("aria-selected", String(j === i)); });
      if (i >= 0) {
        var opt = lb.children[i];
        input.setAttribute("aria-activedescendant", opt.id);
        opt.scrollIntoView({ block: "nearest" });
      } else input.removeAttribute("aria-activedescendant");
    }
    function close() {
      lb.hidden = true; input.setAttribute("aria-expanded", "false"); setActive(-1);
    }
    function render() {
      var q = input.value.trim();
      items = matches(q);
      lb.textContent = "";
      items.forEach(function (s, i) {
        var li = doc.createElement("li");
        li.className = "listbox__option"; li.id = "q-opt-" + i; li.setAttribute("role", "option"); li.setAttribute("aria-selected", "false");
        var t = doc.createElement("span"); t.className = "listbox__title"; highlight(t, s.t, q);
        var k = doc.createElement("span"); k.className = "listbox__kind"; k.textContent = s.k;
        var x = doc.createElement("span"); x.className = "listbox__ctx"; x.textContent = s.x;
        li.appendChild(t); li.appendChild(k); li.appendChild(x);
        li.addEventListener("mousedown", function (e) { e.preventDefault(); });
        li.addEventListener("click", function () { choose(i); });
        lb.appendChild(li);
      });
      var open = items.length > 0;
      lb.hidden = !open; input.setAttribute("aria-expanded", String(open)); setActive(-1);
      clearTimeout(announceTimer);
      announceTimer = setTimeout(function () {
        status.textContent = !q ? "" : open ? items.length + (items.length === 1 ? " suggestion." : " suggestions.") : "No suggestions. Press Enter to search all records.";
      }, 500);
    }
    function choose(i) {
      var s = items[i];
      if (!s) return;
      input.value = s.t; close();
      status.textContent = s.k + ": " + s.t + ". In the site this opens the record page.";
    }
    input.addEventListener("input", render);
    input.addEventListener("keydown", function (e) {
      var open = !lb.hidden, n = items.length;
      if (e.key === "ArrowDown") { e.preventDefault(); if (!open) render(); if (items.length) setActive(active < items.length - 1 ? active + 1 : 0); }
      else if (e.key === "ArrowUp") { e.preventDefault(); if (open && n) setActive(active > 0 ? active - 1 : n - 1); }
      else if (e.key === "Enter" && open && active >= 0) { e.preventDefault(); choose(active); }
      else if (e.key === "Escape") { if (open) { e.preventDefault(); close(); } else input.value = ""; }
      else if (e.key === "Tab") close();
    });
    input.addEventListener("blur", function () { setTimeout(close, 0); });
    form.addEventListener("submit", function (e) {
      e.preventDefault(); close();
      status.textContent = input.value.trim() ? "In the site this shows all results. The query is never put in the address." : "Type something to search.";
    });
  }

  /* ---------- Sortable table: buttons in headers, aria-sort on the sorted column only ---------- */
  $all("table[data-sortable]").forEach(function (table) {
    var buttons = $all("button.sort", table), tbody = table.tBodies[0];
    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var th = btn.closest("th"), col = +btn.getAttribute("data-col"), isNum = btn.getAttribute("data-type") === "num";
        var dir = th.getAttribute("aria-sort") === "ascending" ? "descending" : "ascending";
        buttons.forEach(function (b) {
          var h = b.closest("th"); h.removeAttribute("aria-sort");
          b.querySelector("use").setAttribute("href", "assets/icons.svg#sort");
        });
        th.setAttribute("aria-sort", dir);
        btn.querySelector("use").setAttribute("href", "assets/icons.svg#sort-" + (dir === "ascending" ? "asc" : "desc"));
        var rows = Array.prototype.slice.call(tbody.rows);
        rows.sort(function (a, b) {
          var x = a.cells[col].textContent.trim(), y = b.cells[col].textContent.trim();
          var c = isNum ? (parseFloat(x) - parseFloat(y)) : x.localeCompare(y);
          return dir === "ascending" ? c : -c;
        });
        rows.forEach(function (r) { tbody.appendChild(r); });
        var hint = table.querySelector(".data-table__hint");
        if (hint) hint.textContent = "First 5 of 35 tasks. Sorted by " + btn.textContent.trim().toLowerCase() + ", " + dir + ".";
      });
    });
  });

  /* ---------- Copy citation ---------- */
  $all("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var src = doc.getElementById(btn.getAttribute("data-copy")), out = btn.parentNode.querySelector("[data-copy-status]");
      var text = src.textContent.trim();
      function done(ok) {
        if (out) out.textContent = ok ? "Citation copied." : "Copy did not work. Select the citation text and copy it yourself.";
        var label = btn.querySelector("span"), use = btn.querySelector("use");
        if (ok && label) { label.textContent = "Copied"; use.setAttribute("href", "assets/icons.svg#check"); setTimeout(function () { label.textContent = "Copy citation"; use.setAttribute("href", "assets/icons.svg#copy"); }, 2500); }
      }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(false); });
      else done(false);
    });
  });

  /* ---------- Print: open evidence drawers for paper, restore afterwards ---------- */
  var reopened = [];
  window.addEventListener("beforeprint", function () {
    reopened = $all("details.drawer:not([open])");
    reopened.forEach(function (d) { d.open = true; });
  });
  window.addEventListener("afterprint", function () { reopened.forEach(function (d) { d.open = false; }); reopened = []; });
  $all("[data-print]").forEach(function (b) { b.addEventListener("click", function () { window.print(); }); });

  /* ---------- Filter demo: live count ---------- */
  var filterForm = $("#filter-demo");
  if (filterForm) {
    var count = $("#filter-count");
    function update() {
      var n = $all("input:checked", filterForm).length;
      count.textContent = n ? n + (n === 1 ? " filter selected" : " filters selected") : "No filters selected: showing all 37 roles";
    }
    filterForm.addEventListener("change", update);
    filterForm.addEventListener("reset", function () { setTimeout(update, 0); });
  }

  /* ---------- "On this page": mark the section in view ---------- */
  var tocLinks = $all(".toc__link");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var byId = {};
    tocLinks.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && byId[en.target.id]) {
          tocLinks.forEach(function (a) { a.removeAttribute("aria-current"); });
          byId[en.target.id].setAttribute("aria-current", "true");
        }
      });
    }, { rootMargin: "0px 0px -70% 0px" });
    Object.keys(byId).forEach(function (id) { var s = doc.getElementById(id); if (s) io.observe(s); });
  }
})();
