// Builds the search index once from data/search.js (and data/search-tasks.js when available). Licence: Apache-2.0.
import { SearchIndex } from "./search.js";
import * as data from "./data.js";
import { COPY } from "../content.js";

// Help topics: the sections of "How to read EMST", findable by the words people meet on records.
const HELP_ALT = {
  "use-tiers": ["use tier", "use tiers", "what can i use this for"], "use-describe": ["describe", "describe tier"], "use-exploratory": ["exploratory", "explore only"],
  "use-develop": ["develop", "develop tier"], "use-select": ["select tier", "selection"], "ai-drafted": ["ai drafted", "ai-drafted", "drafted by ai", "ai generated"],
  review: ["reviewed", "not reviewed", "review status"], evidence: ["evidence label", "sourced", "judgment", "speculation"], pending: ["assessment pending", "not yet assessed", "pending"],
  lifecycle: ["watch", "on watch", "established", "emerging"], matches: ["crosswalk", "close match", "related match", "match type"], "source-grades": ["source grade"], formation: ["formation task"],
};
function helpDocs() {
  return (COPY.about?.read || []).filter((b) => b.t === "h2" && b.id && HELP_ALT[b.id]).map((b) => ({ k: "help", s: b.id, t: b.text, a: HELP_ALT[b.id], x: "How to read EMST", w: 0.9 }));
}

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
  base = new SearchIndex([...s.docs, ...helpDocs()], s.syn);
  return base;
}
/** Full index including 1,317 tasks, used for the results page. */
export function fullIndex() {
  if (full) return Promise.resolve(full);
  if (!buildingFull) buildingFull = Promise.all([data.search(), data.searchTasks()]).then(async ([s, t]) => { await tidy(s.docs); return (full = new SearchIndex([...s.docs, ...helpDocs(), ...t.docs], s.syn)); });
  return buildingFull;
}
export const KIND_LABEL = { policy: "About EMST", help: "How to read EMST", role: "Roles", series: "OPM series", class: "State and local classes", comp: "Competencies", task: "Tasks", module: "Modules", tool: "Tools", credential: "Credentials", signal: "Change signals" };
export const KIND_ONE = { policy: "about EMST", role: "role", series: "OPM series", class: "state or local class", comp: "competency", task: "task", module: "module", tool: "tool", credential: "credential", signal: "change signal", help: "help" };
export const KIND_ORDER = ["policy", "help", "role", "series", "class", "comp", "task", "module", "tool", "credential", "signal"];
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
    case "help": return `#/about/read@${doc.s}`;
    case "credential": return `#/credential/${doc.s}`;
    default: return doc.u || `#/search`;
  }
}
