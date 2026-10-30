// Builds the search index once from data/search.js (and data/search-tasks.js when available). Licence: Apache-2.0.
import { SearchIndex } from "./search.js";
import * as data from "./data.js";

let base = null, full = null, buildingFull = null;
let p3 = new Set();

/** Replace internal depth labels in role context lines with the role's function statement; remember P3 roles. */
async function tidy(docs) {
  const c = await data.core();
  const roles = new Map(c.roles.map((r) => [r.slug, r]));
  p3 = new Set(c.roles.filter((r) => r.whatsComingOnly).map((r) => r.slug));
  for (const d of docs) if (d.k === "role" && roles.has(d.s)) {
    const r = roles.get(d.s);
    d.x = (p3.has(d.s) ? "Role that may be forming (in What's changing). " : "") + (r.fn || "");
  }
  return docs;
}

/** Index without tasks: small and fast, used for suggestions. */
export async function baseIndex() {
  if (base) return base;
  const s = await data.search();
  await tidy(s.docs);
  base = new SearchIndex(s.docs, s.syn);
  return base;
}
/** Full index including 1,317 tasks, used for the results page. */
export function fullIndex() {
  if (full) return Promise.resolve(full);
  if (!buildingFull) buildingFull = Promise.all([data.search(), data.searchTasks()]).then(async ([s, t]) => { await tidy(s.docs); return (full = new SearchIndex([...s.docs, ...t.docs], s.syn)); });
  return buildingFull;
}
export const KIND_LABEL = { policy: "About EMST", role: "Roles", series: "OPM series", class: "State and local classes", comp: "Competencies", task: "Tasks", module: "Modules", tool: "Tools", credential: "Credentials", signal: "Change signals" };
export const KIND_ORDER = ["policy", "role", "series", "class", "comp", "task", "module", "tool", "credential", "signal"];
export function hrefFor(doc) {
  switch (doc.k) {
    case "role": return p3.has(doc.s) ? `#/changing@${doc.s}` : `#/role/${doc.s}`;
    case "comp": return `#/competency/${doc.s}`;
    case "task": return `#/task/${doc.s}`;
    case "series": return `#/series/${doc.s}`;
    case "class": return `#/class/${doc.s}`;
    case "signal": return `#/changing@${doc.s}`;
    case "module": return `#/competencies/${doc.s}`;
    case "tool": return `#/tool/${doc.s}`;
    case "credential": return `#/credential/${doc.s}`;
    default: return doc.u || `#/search`;
  }
}
