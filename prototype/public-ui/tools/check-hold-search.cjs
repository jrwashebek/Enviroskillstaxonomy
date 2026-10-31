// Regression test for the Tribal content hold in search: every governed trigger query (schema/lint/governed_content.yaml),
// and common misspellings, must get only the held-records answer, never "not covered yet" or "suggest a role"; ordinary
// words near them must not. Usage (app served): node prototype/public-ui/tools/check-hold-search.cjs http://127.0.0.1:8811
// Licence: Apache-2.0.

const { chromium } = require("playwright");
const Q = ['tribe', 'tribes', 'tribal', 'Indigenous', 'Native American', 'Native Hawaiian', 'Alaska Native', 'First Nations', 'traditional knowledge', 'traditional ecological knowledge', 'TEK', 'THPO', 'THPOs', 'treaty', 'treaties', 'treaty rights', 'sovereign nations', 'sovereign government', 'tribal sovereignty', 'indigenous data sovereignty', 'government-to-government', 'Indian preference', 'Indian country', 'Indian self-determination', 'trust responsibility', 'CARE principles', 'ANCSA', 'tribel', 'indigenus', 'triibal', 'treety', 'sovereignity', 'tribally', 'intertribal', 'first nation', 'native amercian', 'nativeamerican', 'alaska natve', 'traditonal knowledge'];
const CONTROL = ['prescribed fire', 'trial', 'treatment', 'water treatment', 'tek', 'care', 'trust', 'native plants', 'sovereign', 'ecological knowledge', 'first national', 'distribution', 'attribute', 'native seed'];
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto(process.argv[2] + "/index.html#/"); await p.waitForSelector("#main h1");
  let bad = 0;
  for (const q of [...Q, ...CONTROL]) {
    await p.fill("#q", ""); await p.fill("#q", q); await p.keyboard.press("Enter");
    await p.waitForFunction(() => location.hash.startsWith("#/search") && document.querySelector("#main h1") && !document.querySelector("#main[aria-busy]"));
    await p.waitForTimeout(250);
    const t = (await p.innerText("#main")).replace(/\s+/g, " ");
    const held = /Held records/.test(t) && !/may not cover this work yet|Suggest a role/i.test(t);
    const isQ = Q.includes(q);
    if (isQ !== held) bad++;
    console.log((isQ ? "HOLD " : "CTRL ") + (isQ === held ? "ok  " : "FAIL") + " " + q + (isQ ? "" : " -> " + (held ? "held page" : t.match(/\d[\d,]* results?|No results[^.]*/)?.[0] || "?")));
  }
  console.log("failures:", bad);
  await b.close(); process.exit(bad ? 1 : 0);
})();
