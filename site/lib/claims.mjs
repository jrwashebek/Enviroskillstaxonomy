// Reads the WP-15 claims register's `do_not_say` column into wrong-form rules (docs/methods/claims_register.csv).
// Shared by lib/model.mjs (to leave out vocab text that matches a wrong form) and tools/check-output.mjs (to fail the
// build on one). Licence: Apache-2.0.
//
// How the register writes `do_not_say` (WP15_SIGNOFF.md §2.3):
//  * Items are separated by semicolons; a semicolon inside parentheses or double quotes belongs to its item.
//  * A single-quoted phrase is a wrong form: 'reinstated only in plaintiff states'. An apostrophe inside a phrase
//    (Colorado's) does not close it; a possessive before a phrase (PPS's 'more than a quarter') does not open one.
//  * A phrase after "write" is the safe form the register recommends, not a wrong form: (write 'components typed as
//    monitoring').
//  * A double-quoted phrase is recorded but NOT yet enforced: the register double-quotes a wrong form while text in
//    data/v2 still uses it and a change request is open (e.g. "nine environmental bureaus", CR-FIX-A-003). The checker
//    reports where such phrases still render, without failing.
//  * An item that starts with "mixing", "conflating" or "combining" forbids putting two figures together, not either
//    figure alone: "mixing with PPS's 'more than a quarter'" on RPT-05 (the USDA OIG 16% figure) fails only where the
//    16% and "more than a quarter" appear in the same sentence without saying they rest on different bases.

const CONFLATE = /^\s*(?:mixing|conflating|combining)\b/i;
// A sentence that says why two figures differ is a distinction, not a conflation.
export const DISTINGUISH = /\bdifferent (?:base|bases|period|periods|denominator|measure|count|counts|source|scope)\b|\bnot comparable\b|\bnot the same (?:base|measure|count)\b|\bdo not (?:mix|combine|compare)\b|\bseparately\b/i;
const QUOTED = /(?:^|[\s(;])'((?:[^']|'(?=[A-Za-z]))+?)'(?=[\s,;.)]|$)/g;
const DOUBLE = /"([^"]+)"/g;
const PCT = /(?<![\d.,])(\d{1,3}(?:\.\d+)?)\s?(?:%|percent\b)/g;

const STOP = new Set("about above after again against before being below between could would should their there these those which while where whose with within without other under through during first since still often among into from that this were have been than then them they what when your more most such only also each both many much very same some over make made".split(" "));
export const anchorsOf = (claim) => [...new Set((String(claim || "").match(/[A-Za-z][A-Za-z0-9.()-]{4,}/g) || [])
  .map((w) => w.toLowerCase().replace(/[().]+$/, "")).filter((w) => !STOP.has(w)))];

const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
// A phrase matches only on word boundaries, case-insensitively, with any run of spaces between its words.
export const phraseRx = (p) => new RegExp(`(?<![A-Za-z0-9])${esc(p.trim()).replace(/\s+/g, "\\s+")}(?![A-Za-z0-9])`, "gi");
const pctRx = (n) => new RegExp(`(?<![\\d.,])${esc(n)}\\s?(?:%|percent\\b)`, "gi");

/** Split one `do_not_say` cell into items (semicolons outside parentheses and double quotes). */
export function splitItems(cell) {
  const s = String(cell || "");
  const items = [];
  let cur = "", depth = 0, dq = false;
  for (const c of s) {
    if (c === '"') dq = !dq;
    else if (!dq && c === "(") depth++;
    else if (!dq && c === ")") depth = Math.max(0, depth - 1);
    if (c === ";" && depth === 0 && !dq) { items.push(cur.trim()); cur = ""; continue; }
    cur += c;
  }
  if (cur.trim()) items.push(cur.trim());
  return items;
}

/**
 * Turn register rows into rules.
 *   strict:      single-quoted phrases of 12+ characters, wrong anywhere they appear
 *   short:       shorter single-quoted phrases, wrong only near two anchor words from the row's claim
 *   conflations: "mixing ..." items, wrong only where all their terms share a sentence (see DISTINGUISH)
 *   deferred:    double-quoted phrases, recorded but not enforced (reported by the checker)
 */
export function parseRegister(rows) {
  const out = { strict: [], short: [], conflations: [], deferred: [] };
  for (const r of rows || []) {
    for (const item of splitItems(r.do_not_say)) {
      for (const m of item.matchAll(DOUBLE)) out.deferred.push({ claim: r.claim_id, phrase: m[1].trim() });
      const masked = item.replace(DOUBLE, (m) => " ".repeat(m.length));   // quotes inside "..." are not openers
      const quoted = [];
      for (const m of masked.matchAll(QUOTED)) {
        const at = m.index + m[0].indexOf("'");
        if (/\bwrite\s*$/i.test(masked.slice(0, at))) continue;            // the safe form, not a wrong form
        quoted.push(m[1].trim());
      }
      if (CONFLATE.test(masked)) {
        const terms = quoted.filter((q) => q.length >= 2).map((q) => ({ text: q, rx: phraseRx(q) }));
        // "mixing with X": the row's own figure is the other term (its percentages, e.g. RPT-05's 16%).
        if (terms.length === 1) for (const m of String(r.claim || "").matchAll(PCT)) terms.push({ text: `${m[1]}%`, rx: pctRx(m[1]) });
        if (terms.length >= 2) out.conflations.push({ claim: r.claim_id, item, terms });
        continue;
      }
      for (const q of quoted) {
        if (q.length >= 12) out.strict.push({ claim: r.claim_id, phrase: q });
        else if (q.length >= 2) out.short.push({ claim: r.claim_id, phrase: q, anchors: anchorsOf(r.claim) });
      }
    }
  }
  return out;
}

/**
 * Sentences of a text: split at sentence punctuation and at line breaks (block boundaries such as table cells and
 * list items, when the caller marks them with "\n").
 */
export function sentencesOf(text) {
  // A full stop ends a sentence after a lower-case letter, digit, % or bracket, so "U.S. Forest Service" stays whole.
  return String(text || "").split(/\n+|(?<=[a-z0-9%)\]][.!?]|;)\s+(?=[A-Z0-9"'(])/).map((s) => s.replace(/\s+/g, " ").trim()).filter(Boolean);
}

/** Does one sentence put all of a conflation rule's terms together without distinguishing them? */
export function conflates(sentence, rule) {
  if (DISTINGUISH.test(sentence)) return false;
  // Longer terms first, masked once found, so 'deployed' is not read inside 'deployed+piloted'.
  let s = sentence;
  for (const t of [...rule.terms].sort((a, b) => b.text.length - a.text.length)) {
    const rx = new RegExp(t.rx.source, "gi");
    if (!rx.test(s)) return false;
    s = s.replace(new RegExp(t.rx.source, "gi"), (m) => " ".repeat(m.length));
  }
  return true;
}

/** Plain-text test used by the view model: true if the text contains a strict wrong form or a conflation. */
export function textViolates(text, rules) {
  const t = String(text || "");
  if (rules.strict.some((w) => new RegExp(phraseRx(w.phrase).source, "i").test(t))) return true;
  return sentencesOf(t).some((s) => rules.conflations.some((c) => conflates(s, c)));
}
