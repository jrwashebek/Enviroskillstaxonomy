// Minimal, safe DOM builder. Text is always inserted as text nodes; there is no innerHTML anywhere in the app.
// Licence: Apache-2.0 (code). Part of the EMST public-interface prototype.

/**
 * h("a", {href: "#/x", class: "link"}, "text", childNode, [more, children], null)
 * - attrs: class, text, html is NOT supported (by design), on: {click: fn}, data-*, aria-*, boolean attributes as true/false
 * - children: strings, numbers, Nodes, arrays (flattened), null/undefined/false (skipped)
 */
export function h(tag, attrs, ...children) {
  const el = document.createElement(tag);
  if (attrs && (typeof attrs !== "object" || attrs instanceof Node || Array.isArray(attrs))) {
    children.unshift(attrs);
    attrs = null;
  }
  if (attrs) {
    for (const [k, v] of Object.entries(attrs)) {
      if (v === null || v === undefined || v === false) continue;
      if (k === "class") el.className = Array.isArray(v) ? v.filter(Boolean).join(" ") : v;
      else if (k === "text") el.textContent = String(v);
      else if (k === "on") for (const [ev, fn] of Object.entries(v)) el.addEventListener(ev, fn);
      else if (k === "style") throw new Error("Inline styles are not allowed (CSP style-src 'self'). Use a class.");
      else if (k === "html" || k === "innerHTML") throw new Error("innerHTML is not allowed.");
      else el.setAttribute(k, v === true ? "" : String(v));
    }
  }
  append(el, children);
  return el;
}

export function append(el, children) {
  for (const c of children.flat(Infinity)) {
    if (c === null || c === undefined || c === false || c === "") continue;
    el.appendChild(c instanceof Node ? c : document.createTextNode(String(c)));
  }
  return el;
}

export const frag = (...children) => append(document.createDocumentFragment(), children);
export const clear = (el) => { while (el.firstChild) el.removeChild(el.firstChild); return el; };
export const $ = (sel, root = document) => root.querySelector(sel);
export const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];

/** SVG icon from the same-origin sprite assets/icons.svg (<symbol id="i-…">). Decorative unless a label is given. */
export function icon(name, label) {
  const ns = "http://www.w3.org/2000/svg";
  const svg = document.createElementNS(ns, "svg");
  svg.setAttribute("class", `icon icon-${name}`);
  svg.setAttribute("focusable", "false");
  if (label) { svg.setAttribute("role", "img"); svg.setAttribute("aria-label", label); }
  else svg.setAttribute("aria-hidden", "true");
  const use = document.createElementNS(ns, "use");
  use.setAttribute("href", `assets/icons.svg#i-${name}`);
  svg.appendChild(use);
  return svg;
}

let uid = 0;
export const nextId = (prefix = "id") => `${prefix}-${++uid}`;
