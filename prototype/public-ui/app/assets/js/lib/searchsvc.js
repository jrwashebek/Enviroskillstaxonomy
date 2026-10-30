// Builds the search index once from data/search.js (and data/search-tasks.js when available). Licence: Apache-2.0.
import { SearchIndex } from "./search.js";
import * as data from "./data.js";

let base = null, full = null, buildingFull = null;

/** Index without tasks: small and fast, used for suggestions. */
export async function baseIndex() {
  if (base) return base;
  const s = await data.search();
  base = new SearchIndex(s.docs, s.syn);
  return base;
}
/** Full index including 1,317 tasks, used for the results page. */
export function fullIndex() {
  if (full) return Promise.resolve(full);
  if (!buildingFull) buildingFull = Promise.all([data.search(), data.searchTasks()]).then(([s, t]) => (full = new SearchIndex([...s.docs, ...t.docs], s.syn)));
  return buildingFull;
}
export const KIND_LABEL = { role: "Roles", series: "OPM series", class: "State and local classes", comp: "Competencies", task: "Tasks", module: "Modules", tool: "Tools", credential: "Credentials", signal: "Change signals" };
export const KIND_ORDER = ["role", "series", "class", "comp", "task", "module", "tool", "credential", "signal"];
export function hrefFor(doc) {
  switch (doc.k) {
    case "role": return `#/role/${doc.s}`;
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
