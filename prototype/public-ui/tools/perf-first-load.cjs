// First-load performance measurement (performance round 2). Same method as the round 1 evaluator's perf.js (R4's method):
// CDP network emulation (Slow 3G = 2,000 ms latency, 50 kB/s; Fast 3G = 562.5 ms, 180 kB/s), cache disabled, 390x844,
// an in-process static server with optional gzip (level 6), and "first view" = time until the route's <h1> in <main>
// is in the DOM with a height, polled every 50 ms.
// One guard is added so a prerendered <h1> is not counted before it can paint: the page's screen stylesheets must
// have loaded (they block rendering). Also recorded: FCP (first contentful paint, from the Paint Timing API), the time
// the site header is styled and visible ("chrome"), and, on role pages, the time "Where it can lead" fills in.
// Kept in tools/ so the first-load budget (route H1 in 8 s or less on Slow 3G with gzip) can be re-measured the same way.
// Usage (from the repository root): node prototype/public-ui/tools/perf-first-load.cjs <label> [profiles=slow3g,fast3g]
//   [gzip=1|0|both] [runs=1] [pages=all|home,role,forester,comp,changing,oldhome,oldrole]
// Writes perf_<label>.json in the current directory. The old explorer pages need site/_site to be built.
// Licence: Apache-2.0.
const http = require('http'); const zlib = require('zlib'); const fs = require('fs'); const path = require('path');
const { chromium } = require('playwright');
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.mjs': 'text/javascript', '.woff2': 'font/woff2', '.svg': 'image/svg+xml', '.png': 'image/png', '.json': 'application/json', '.map': 'application/json' };
let GZIP = false;
function serve(root, port) {
  return new Promise((ok) => {
    const s = http.createServer((req, res) => {
      let p = decodeURIComponent(req.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html';
      const f = path.join(root, path.normalize(p));
      if (!f.startsWith(root) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) { res.writeHead(404); return res.end(); }
      const ext = path.extname(f); const body = fs.readFileSync(f);
      const c = GZIP && ['.html', '.css', '.js', '.svg', '.json'].includes(ext);
      res.writeHead(200, { 'Content-Type': TYPES[ext] || 'application/octet-stream', ...(c ? { 'Content-Encoding': 'gzip' } : {}) });
      res.end(c ? zlib.gzipSync(body, { level: 6 }) : body);
    });
    s.listen(port, '127.0.0.1', () => ok(s));
  });
}
const PROFILES = { slow3g: { offline: false, latency: 2000, downloadThroughput: 50000, uploadThroughput: 50000 },
  fast3g: { offline: false, latency: 562.5, downloadThroughput: 180000, uploadThroughput: 84375 } };
const NEW = 'http://127.0.0.1:8842/index.html';
const ALL = {
  home: ['new', `${NEW}#/`, 'home #/'],
  role: ['new', `${NEW}#/role/rol-zjfcc09`, 'role rol-zjfcc09'],
  forester: ['new', `${NEW}#/role/rol-g0wbahh/federal`, 'role forester federal'],
  comp: ['new', `${NEW}#/competency/cmp-vmk86p6`, 'competency cmp-vmk86p6'],
  changing: ['new', `${NEW}#/changing`, "what's changing"],
  oldhome: ['old', 'http://127.0.0.1:8843/', 'old explorer home'],
  oldrole: ['old', 'http://127.0.0.1:8843/roles/rol-g0wbahh/federal/', 'old forester federal'],
};
const [label = 'run', profArg = 'slow3g,fast3g', gzArg = '1', runsArg = '1', pagesArg = 'all'] = process.argv.slice(2);
const pages = pagesArg === 'all' ? Object.values(ALL) : pagesArg.split(',').map((k) => ALL[k]);
const gzs = gzArg === 'both' ? [true, false] : [gzArg === '1'];
(async () => {
  const s1 = await serve(path.join(__dirname, '..', 'app'), 8842);
  const s2 = await serve(path.join(__dirname, '..', '..', '..', 'site', '_site'), 8843);
  const browser = await chromium.launch();
  const rows = [];
  for (const gz of gzs) {
    GZIP = gz;
    for (const pname of profArg.split(',')) {
      const cond = PROFILES[pname];
      for (const [site, url, name] of pages) for (let run = 0; run < Number(runsArg); run++) {
        const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
        const page = await ctx.newPage();
        const errors = [];
        page.on('pageerror', (e) => errors.push(e.message)); page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()); });
        const cdp = await ctx.newCDPSession(page);
        await cdp.send('Network.enable'); await cdp.send('Network.setCacheDisabled', { cacheDisabled: true });
        await cdp.send('Network.emulateNetworkConditions', cond);
        let bytes = 0, n = 0; const urls = [];
        cdp.on('Network.requestWillBeSent', (e) => urls.push(e.request.url));
        cdp.on('Network.loadingFinished', (e) => { bytes += e.encodedDataLength; n++; });
        const t0 = Date.now();
        await page.goto(url, { waitUntil: 'commit', timeout: 600000 });
        const chromeP = page.waitForFunction(() => { const ok = [...document.querySelectorAll('link[rel=stylesheet]')].filter((l) => l.media !== 'print').every((l) => l.sheet); const e = document.querySelector('.site-header') || document.querySelector('header'); return ok && e && e.getBoundingClientRect().height > 0; }, null, { timeout: 600000, polling: 50 }).then(() => Date.now() - t0);
        await page.waitForFunction(() => { const ok = [...document.querySelectorAll('link[rel=stylesheet]')].filter((l) => l.media !== 'print').every((l) => l.sheet); const h = document.querySelector('main h1'); return ok && h && h.getBoundingClientRect().height > 0; }, null, { timeout: 600000, polling: 50 });
        const h1At = Date.now() - t0;
        const chromeAt = await chromeP;
        let pathsAt = null;
        if (/#\/role\//.test(url)) {
          await page.waitForFunction(() => { const s = document.querySelector('#paths'); return s && !s.querySelector('[aria-busy]'); }, null, { timeout: 600000, polling: 50 });
          pathsAt = Date.now() - t0;
        }
        await page.waitForLoadState('load', { timeout: 600000 });
        await page.waitForTimeout(site === 'new' ? 12000 : 500); // let lazily injected data scripts finish
        const nav = await page.evaluate(() => { const nv = performance.getEntriesByType('navigation')[0]; const p = performance.getEntriesByType('paint').find((x) => x.name === 'first-contentful-paint'); return { dcl: Math.round(nv.domContentLoadedEventEnd), load: Math.round(nv.loadEventEnd), fcp: p ? Math.round(p.startTime) : null, h1text: (document.querySelector('main h1') || {}).textContent }; });
        const row = { label, site, page: name, gzip: gz, profile: pname, run, requests: n, kb: Math.round(bytes / 1024), fcp: nav.fcp, chrome: chromeAt, h1: h1At, paths: pathsAt, dcl: nav.dcl, load: nav.load, h1text: nav.h1text, errors, urls: [...new Set(urls)].map((u) => u.replace(/^http:\/\/127\.0\.0\.1:884\d\//, '')) };
        rows.push(row);
        console.log(`${label} ${site} ${name.padEnd(24)} ${gz ? 'gzip' : 'raw '} ${pname} req ${n} KB ${row.kb} FCP ${nav.fcp} chrome ${chromeAt} h1 ${h1At} paths ${pathsAt} DCL ${nav.dcl} load ${nav.load} err ${errors.length}`);
        await ctx.close();
      }
    }
  }
  fs.writeFileSync(path.join(process.cwd(), `perf_${label}.json`), JSON.stringify(rows, null, 1));
  await browser.close(); s1.close(); s2.close();
})();
