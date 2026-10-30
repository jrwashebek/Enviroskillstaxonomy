// Client-side search for the EMST prototype: job titles, codes, synonyms, prefixes and typos.
// Everything runs in the browser; queries never leave the page and never enter the URL.
// Licence: Apache-2.0.

const STOP = new Set("a an and are as at be by for from in into is it its my of on or our that the their this to with we you your i me what how do does job jobs work".split(" "));
const KIND_BOOST = { role: 1.45, series: 1.3, class: 1.15, comp: 1.1, module: 1.0, task: 0.85, tool: 0.8, credential: 0.8, signal: 0.6 };
const FIELD = { t: 10, a: 8, c: 14, x: 2 };

export function normalize(s) {
  return String(s || "")
    .normalize("NFKD").replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/o\*net/g, "onet")
    .replace(/[’']/g, "")
    .replace(/[^a-z0-9.\-]+/g, " ")
    .replace(/(^|\s)[.\-]+|[.\-]+(?=\s|$)/g, " ")
    .trim();
}

export function stem(w) {
  if (w.length <= 3 || /\d/.test(w)) return w;
  if (w.endsWith("ies") && w.length > 4) return w.slice(0, -3) + "y";
  if (/(ss|us|is)$/.test(w)) return w;
  if (/(xes|ches|shes|sses)$/.test(w)) return w.slice(0, -2);
  if (w.endsWith("s")) return w.slice(0, -1);
  return w;
}

const words = (s) => normalize(s).split(/\s+/).flatMap((w) => (/^[a-z]+-[a-z]+$/.test(w) ? [w, ...w.split("-")] : [w])).filter((w) => w && !STOP.has(w));
const codeKey = (s) => String(s || "").toLowerCase().replace(/^gs[\s-]*/, "").replace(/[^a-z0-9]/g, "");

function editDistance(a, b, max) {
  // Damerau-Levenshtein (optimal string alignment) with an early exit above max
  if (Math.abs(a.length - b.length) > max) return max + 1;
  let prev2 = null, prev = Array.from({ length: b.length + 1 }, (_, i) => i);
  for (let i = 1; i <= a.length; i++) {
    const cur = [i];
    let rowMin = i;
    for (let j = 1; j <= b.length; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      let v = Math.min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost);
      if (prev2 && i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) v = Math.min(v, prev2[j - 2] + 1);
      cur.push(v);
      if (v < rowMin) rowMin = v;
    }
    if (rowMin > max) return max + 1;
    prev2 = prev; prev = cur;
  }
  return prev[b.length];
}

export class SearchIndex {
  /** docs: [{k, s, t, a?, c?, x?, w?}], syn: {term: [expansion, …]} */
  constructor(docs, syn = {}) {
    this.docs = docs;
    this.post = new Map();          // token -> Map(docIdx -> best field weight)
    this.codes = new Map();         // normalized code -> [docIdx]
    this.syn = new Map();           // normalized term -> [normalized expansions]
    this.maxSynWords = 1;
    docs.forEach((d, i) => {
      const add = (text, f) => {
        for (const w of words(text)) {
          for (const tok of new Set([w, stem(w)])) {
            let m = this.post.get(tok);
            if (!m) this.post.set(tok, (m = new Map()));
            if ((m.get(i) || 0) < FIELD[f]) m.set(i, FIELD[f]);
          }
        }
      };
      add(d.t, "t");
      for (const a of d.a || []) add(a, "a");
      add(d.x, "x");
      for (const c of d.c || []) {
        const k = codeKey(c);
        if (!k) continue;
        if (!this.codes.has(k)) this.codes.set(k, []);
        this.codes.get(k).push(i);
        add(c, "c");
      }
    });
    for (const [term, exps] of Object.entries(syn)) {
      const k = normalize(term);
      if (!k) continue;
      this.syn.set(k, (exps || []).map(normalize).filter(Boolean));
      this.maxSynWords = Math.max(this.maxSynWords, k.split(" ").length);
    }
    this.vocab = [...this.post.keys()].sort();
  }

  // tokens starting with prefix (binary search over the sorted vocabulary)
  prefixed(prefix, limit = 60) {
    let lo = 0, hi = this.vocab.length;
    while (lo < hi) { const mid = (lo + hi) >> 1; if (this.vocab[mid] < prefix) lo = mid + 1; else hi = mid; }
    const out = [];
    for (let i = lo; i < this.vocab.length && out.length < limit && this.vocab[i].startsWith(prefix); i++) out.push(this.vocab[i]);
    return out;
  }

  fuzzy(w) {
    const max = w.length >= 8 ? 2 : w.length >= 4 ? 1 : 0;
    if (!max) return [];
    const out = [];
    for (const v of this.vocab) {
      if (Math.abs(v.length - w.length) > max || v[0] !== w[0]) continue;
      const d = editDistance(w, v, max);
      if (d <= max) out.push([v, d]);
    }
    return out.sort((a, b) => a[1] - b[1]).slice(0, 8);
  }

  /** Expand the raw query into term groups; each group is satisfied by any of its alternatives. */
  plan(query) {
    const raw = normalize(query);
    const ws = raw.split(/\s+/).filter(Boolean);
    const groups = [];
    const notes = [];
    let i = 0;
    while (i < ws.length) {
      let used = 0;
      for (let n = Math.min(this.maxSynWords, ws.length - i); n >= 1 && !used; n--) {
        const phrase = ws.slice(i, i + n).join(" ");
        const exps = this.syn.get(phrase) || (n === 1 ? this.syn.get(stem(phrase)) : null);
        if (exps && exps.length) {
          groups.push({ terms: [phrase, ...exps], label: phrase, syn: exps });
          notes.push({ type: "synonym", from: phrase, to: exps });
          used = n;
        }
      }
      if (!used) {
        if (!STOP.has(ws[i])) groups.push({ terms: [ws[i]], label: ws[i] });
        used = 1;
      }
      i += used;
    }
    return { raw, groups, notes };
  }

  search(query, { limit = 50, kinds = null } = {}) {
    const q = String(query || "").trim();
    if (!q) return { results: [], notes: [], total: 0, byKind: {} };
    const { groups, notes } = this.plan(q);
    const scores = new Map(); // docIdx -> {score, hits:Set(groupIndex), fuzzy:boolean}
    const bump = (i, g, s, fz) => {
      let e = scores.get(i);
      if (!e) scores.set(i, (e = { score: 0, hits: new Map(), fuzzy: false }));
      if ((e.hits.get(g) || 0) < s) e.hits.set(g, s);
      if (fz) e.fuzzy = true;
    };

    // codes: exact match on any code ("0460", "GS-0460", "19-1031.00")
    const ck = codeKey(q);
    if (ck.length >= 3 && /\d/.test(ck)) for (const i of this.codes.get(ck) || []) bump(i, -1, 60, false);

    const corrections = [];
    // Score one word: exact token, stem, then prefixes. Returns Map(docIdx -> score).
    const wordHits = (w) => {
      const m = new Map();
      const put = (i, v) => { if ((m.get(i) || 0) < v) m.set(i, v); };
      for (const tok of new Set([w, stem(w)])) {
        const exact = this.post.get(tok);
        if (exact) for (const [i, fw] of exact) put(i, fw);
        if (tok.length >= 3) for (const p of this.prefixed(tok)) {
          if (p !== tok) for (const [i, fw] of this.post.get(p)) put(i, fw * 0.75);
        }
      }
      return m;
    };
    groups.forEach((g, gi) => {
      let found = false;
      // OR across alternatives; AND across the words inside one alternative (so a synonym phrase must match as a whole)
      for (const term of g.terms) {
        const ws = words(term);
        if (!ws.length) continue;
        const maps = ws.map(wordHits);
        const [first, ...rest] = maps;
        for (const [i, v] of first) {
          let total = v, ok = true;
          for (const mm of rest) { const x = mm.get(i); if (x === undefined) { ok = false; break; } total += x; }
          if (!ok) continue;
          found = true;
          bump(i, gi, (total / ws.length) * (ws.length > 1 ? 1.15 : 1), false);
        }
      }
      if (!found) {
        for (const w of words(g.terms[0])) {
          for (const [v, d] of this.fuzzy(w)) {
            if (!corrections.some((c) => c.from === w)) corrections.push({ from: w, to: v });
            for (const [i, fw] of this.post.get(v)) bump(i, gi, fw * (d === 1 ? 0.6 : 0.4), true);
          }
        }
      }
    });
    if (corrections.length) notes.push({ type: "spelling", items: corrections });

    const need = groups.length;
    const nq = normalize(q);
    let results = [];
    for (const [i, e] of scores) {
      const d = this.docs[i];
      if (kinds && !kinds.includes(d.k)) continue;
      const matched = [...e.hits.keys()].filter((g) => g >= 0).length;
      const codeHit = e.hits.has(-1);
      let s = [...e.hits.values()].reduce((a, b) => a + b, 0);
      const coverage = need ? matched / need : 1;
      if (!codeHit && coverage < 1) s *= coverage * coverage * 0.6;
      const nt = normalize(d.t);
      if (nt === nq) s += 40; else if (nt.startsWith(nq)) s += 15;
      if ((d.a || []).some((a) => normalize(a) === nq)) s += 30;
      s *= (KIND_BOOST[d.k] || 1) * (d.w || 1);
      results.push({ doc: d, score: s, complete: codeHit || coverage === 1, fuzzy: e.fuzzy });
    }
    results.sort((a, b) => (b.complete - a.complete) || (b.score - a.score) || a.doc.t.localeCompare(b.doc.t));
    const complete = results.filter((r) => r.complete);
    if (complete.length >= 3) results = complete; // partial matches only fill thin result sets
    const byKind = {};
    for (const r of results) byKind[r.doc.k] = (byKind[r.doc.k] || 0) + 1;
    return { results: results.slice(0, limit), total: results.length, byKind, notes };
  }
}

/** Highlight helper: returns [{text, mark:boolean}] segments for the query words found in text. */
export function segments(text, query) {
  const qs = [...new Set(normalize(query).split(/\s+/).filter((w) => w.length >= 2 && !STOP.has(w)))];
  if (!qs.length) return [{ text, mark: false }];
  const lower = text.toLowerCase();
  const marks = new Array(text.length).fill(false);
  for (const w of qs) {
    let at = 0;
    while ((at = lower.indexOf(w, at)) >= 0) {
      const before = at === 0 || /[^a-z0-9]/.test(lower[at - 1]);
      if (before) for (let k = at; k < at + w.length; k++) marks[k] = true;
      at += w.length;
    }
  }
  const out = [];
  for (let i = 0; i < text.length; i++) {
    if (!out.length || out[out.length - 1].mark !== marks[i]) out.push({ text: text[i], mark: marks[i] });
    else out[out.length - 1].text += text[i];
  }
  return out;
}
