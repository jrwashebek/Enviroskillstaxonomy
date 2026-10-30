// Hash router with accessible page changes. Navigation happens only through ordinary links (<a href="#/…">);
// the app never writes to the address bar (no pushState, no location writes), and no user input goes into URLs.
// Licence: Apache-2.0.
import { h, clear, $ } from "./dom.js";
import { NotFound } from "./data.js";

const routes = [];
let current = { path: null, section: null };
const scrollMemory = new Map(); // in-memory only; lost on reload by design
const focusMemory = new Map();  // path -> href (or #id) of the element that had focus when the user left
let renderToken = 0;
let hooks = { notFound: null, error: null, afterRender: null };

/** route("/role/:slug", view)   view = async ({params, section}) => ({title, node, crumbs?}) */
export function route(pattern, view) {
  const keys = [];
  const rx = new RegExp("^" + pattern.replace(/\/:([a-zA-Z]+)/g, (_, k) => { keys.push(k); return "/([^/]+)"; }) + "/?$");
  routes.push({ pattern, rx, keys, view });
}

export function configure(h) { hooks = { ...hooks, ...h }; }

export function parseHash(hash = location.hash) {
  let s = decodeURIComponent((hash || "").replace(/^#/, ""));
  if (!s.startsWith("/")) return { path: null, section: null, anchor: s || null };
  let section = null;
  const at = s.indexOf("@");
  if (at >= 0) { section = s.slice(at + 1) || null; s = s.slice(0, at); }
  return { path: s || "/", section };
}

export function href(path, section) { return "#" + path + (section ? "@" + section : ""); }

function match(path) {
  for (const r of routes) {
    const m = r.rx.exec(path);
    if (m) return { r, params: Object.fromEntries(r.keys.map((k, i) => [k, m[i + 1]])) };
  }
  return null;
}

function announce(msg) {
  const live = $("#route-announcer");
  if (!live) return;
  live.textContent = "";
  // a fresh text node after a tick makes screen readers re-read the message
  setTimeout(() => { live.textContent = msg; }, 60);
}

export function focusSection(id) {
  const el = id && document.getElementById(id);
  if (!el) return false;
  if (!el.hasAttribute("tabindex")) el.setAttribute("tabindex", "-1");
  el.scrollIntoView({ block: "start" });
  el.focus({ preventScroll: true });
  return true;
}

async function render() {
  let { path, section, anchor } = parseHash();
  if (path === null) { // a plain in-page anchor such as #main: never re-render, except on first load
    if (current.path !== null || refreshing) { if (anchor) focusSection(anchor); return; }
    path = "/";
  }
  if (path === current.path) { // same page, different section
    current.section = section;
    if (section) focusSection(section);
    return;
  }
  if (current.path) {
    scrollMemory.set(current.path, window.scrollY);
    const act = document.activeElement;
    const key = act && act.closest && (act.closest("[href]")?.getAttribute("href") || (act.id ? "#" + act.id : null));
    if (key) focusMemory.set(current.path, key);
  }
  const token = ++renderToken;
  const main = $("#main");
  main.setAttribute("aria-busy", "true");
  const slow = setTimeout(() => {
    if (token !== renderToken) return;
    clear(main).appendChild(h("div", { class: "loading", role: "status" }, h("span", { class: "spinner", "aria-hidden": "true" }), "Loading…"));
  }, 180);

  let out;
  try {
    const m = match(path);
    if (!m) throw new NotFound(path);
    out = await m.r.view({ params: m.params, section, path });
  } catch (err) {
    out = err instanceof NotFound && hooks.notFound ? await hooks.notFound(err, path) : hooks.error ? await hooks.error(err, path) : { title: "Error", node: h("p", String(err)) };
    if (!(err instanceof NotFound)) console.error(err);
  }
  clearTimeout(slow);
  if (token !== renderToken) return; // a newer navigation won
  const prevPath = current.path || refreshing;
  refreshing = null;
  current = { path, section };
  clear(main).appendChild(h("div", { class: "container" }, out.node));
  main.removeAttribute("aria-busy");
  document.title = out.title ? `${out.title} · EMST` : "EMST · Environmental Management Skills Taxonomy";
  hooks.afterRender?.({ path, out });

  if (section && focusSection(section)) { /* deep link to a section */ }
  else {
    const back = stack.length >= 2 && stack[stack.length - 2] === path;
    if (back) stack.pop(); else stack.push(path);
    const remembered = scrollMemory.get(path);
    const h1 = main.querySelector("h1");
    const fkey = back ? focusMemory.get(path) : null;
    const target = fkey ? (fkey.startsWith("#") && !fkey.startsWith("#/") ? document.getElementById(fkey.slice(1)) : main.querySelector(`[href="${CSS.escape(fkey)}"]`)) : null;
    if (back && remembered !== undefined && target) { window.scrollTo(0, remembered); target.focus({ preventScroll: true }); }
    else {
      window.scrollTo(0, 0);
      if (h1) { h1.setAttribute("tabindex", "-1"); if (prevPath) h1.focus({ preventScroll: true }); }
    }
  }
  if (prevPath) announce(out.announce || `${out.title || "Page"} loaded`);
}

const stack = []; // in-memory visit stack, used only to restore scroll position on Back
export function start() {
  window.addEventListener("hashchange", render);
  return render();
}

/** Re-render the current page (used after data that a view depends on changes in memory). */
let refreshing = null;
export function refresh() { refreshing = current.path; current.path = null; return render(); }
