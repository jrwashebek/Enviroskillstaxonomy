// Data access for the prototype. Data files are plain scripts that register JSON on window.EMSTDATA;
// they load with <script src> (same origin, CSP script-src 'self'). No fetch, no XHR, no storage.
// Licence: Apache-2.0.

const BASE = "data/";
const pending = new Map();

function store() { return (window.EMSTDATA = window.EMSTDATA || {}); }

/** Load data/<file>.js once and resolve with window.EMSTDATA[key]. */
export function load(file, key) {
  const have = store()[key];
  if (have !== undefined) return Promise.resolve(have);
  if (pending.has(file)) return pending.get(file).then(() => store()[key]);
  const p = new Promise((resolve, reject) => {
    const s = document.createElement("script");
    s.src = `${BASE}${file}.js`;
    s.async = true;
    s.onload = () => resolve();
    s.onerror = () => reject(new DataError(`Could not load ${file}.js`));
    document.head.appendChild(s);
  });
  pending.set(file, p);
  return p.then(() => {
    const v = store()[key];
    if (v === undefined) throw new DataError(`${file}.js did not register "${key}"`);
    return v;
  });
}

export class DataError extends Error {}
export class NotFound extends Error {}

// ------------------------------------------------------------------ typed accessors
export const core = () => load("core", "core");
export const search = () => load("search", "search");
export const change = () => load("change", "change");
export const hr = () => load("hr", "hr");
export const paths = () => load("paths", "paths");

const pad = (n) => String(n).padStart(2, "0");
function shardFile(kind, n) {
  // The data engineer's shard naming is read from core.files when present; otherwise "<kind>-NN".
  return `${kind}-${pad(n)}`;
}

export async function role(slug) {
  const c = await core();
  if (!c.roles.some((r) => r.slug === slug)) throw new NotFound(`No role "${slug}"`);
  const file = c.files?.role?.[slug] || `role-${slug}`;
  return load(file, `role:${slug}`);
}

async function sharded(kind, slug) {
  const c = await core();
  const n = c.shards?.[kind]?.[slug];
  if (n === undefined) throw new NotFound(`No ${kind} "${slug}"`);
  const file = c.files?.[kind]?.[n] || shardFile(kind, n);
  const key = c.keys?.[kind]?.[n] || `${kind}:${pad(n)}`;
  let shard = store()[key];
  if (shard === undefined) {
    try { shard = await load(file, key); } catch (e) {
      // tolerate an unpadded key
      shard = store()[`${kind}:${n}`];
      if (shard === undefined) throw e;
    }
  }
  const rec = Array.isArray(shard) ? shard.find((x) => x.slug === slug) : shard[slug];
  if (!rec) throw new NotFound(`No ${kind} "${slug}" in shard ${n}`);
  return rec;
}

export const comp = (slug) => sharded("comp", slug);
export const task = (slug) => sharded("task", slug);

/** Preload several things in parallel; failures surface to the caller. */
export const all = (...ps) => Promise.all(ps);
