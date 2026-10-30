// Copy, print and download helpers. Everything is built in the browser from the loaded data; nothing is sent anywhere.
// Exports always carry the release, date, page address, AI-drafting status and the use limits, so caveats travel with the text.
// Licence: Apache-2.0.

export function pageUrl() { return String(location.href); }

/** Copy text to the clipboard. Returns true on success. */
export async function copyText(text) {
  try {
    if (navigator.clipboard && window.isSecureContext) { await navigator.clipboard.writeText(text); return true; }
  } catch (e) { /* fall through */ }
  const ta = document.createElement("textarea");
  ta.value = text;
  ta.setAttribute("readonly", "");
  ta.className = "vh";
  document.body.appendChild(ta);
  ta.select();
  let ok = false;
  try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
  ta.remove();
  return ok;
}

/** Save a text file the user asked for. A local object URL; no request leaves the browser. */
export function download(filename, text, mime = "text/plain") {
  const blob = new Blob([text], { type: `${mime};charset=utf-8` });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.className = "vh";
  document.body.appendChild(a);
  a.click();
  setTimeout(() => { URL.revokeObjectURL(url); a.remove(); }, 1000);
}

const csvCell = (v) => {
  let s = v === null || v === undefined ? "" : Array.isArray(v) ? v.join("; ") : String(v);
  if (/^[=+\-@\t\r]/.test(s)) s = "'" + s; // keep spreadsheet apps from treating text as a formula
  return /[",\n\r]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
};
export const toCsv = (rows) => rows.map((r) => r.map(csvCell).join(",")).join("\r\n") + "\r\n";

export const safeName = (s) => String(s || "emst").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 60);

/** Header and footer lines shared by every export. */
export function exportFrame(core, title) {
  const r = core.release;
  const head = [
    `${title}`,
    `Environmental Management Skills Taxonomy (EMST), draft release ${r.id} (${r.date}).`,
    `Source page: ${pageUrl()}`,
    `Drafted by AI agents. Not yet reviewed by people. Describes work only: not a job analysis, classification basis, assessment, or input to hiring, performance or reduction-in-force decisions.`,
  ];
  const foot = [
    `Data licence: CC0 1.0 (public domain dedication). Cite: EMST project lead (${String(r.date).slice(0, 4)}). Environmental Management Skills Taxonomy, release ${r.id}.`,
    `Report a problem: ${core.text?.issuesUrl || "https://github.com/jrwashebek/Enviroskillstaxonomy/issues"}`,
  ];
  return { head, foot };
}

export function citation(core, { title, kind, id }) {
  const r = core.release;
  return `EMST project lead (${String(r.date).slice(0, 4)}). "${title}" [${kind}]. Environmental Management Skills Taxonomy, draft release ${r.id}, drafted by AI agents and not yet reviewed by people. Record ${id || "(no ID)"}. ${pageUrl()}. CC0 1.0.`;
}

export function correctionTemplate(core, { title, kind, id }) {
  return [
    `Record: ${id || "(no ID)"} (${kind})`,
    `Title: ${title}`,
    `Release: ${core.release.id}`,
    `Page: ${pageUrl()}`,
    ``,
    `What is wrong:`,
    ``,
    `What it should say:`,
    ``,
    `How you know (your role or a source; optional, and please no personal or employee information):`,
  ].join("\n");
}
