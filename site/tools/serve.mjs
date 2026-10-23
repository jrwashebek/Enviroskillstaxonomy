#!/usr/bin/env node
// Minimal local static server for the built explorer (no dependency). Binds to 127.0.0.1 only and logs nothing.
// It also sends the response headers a header-capable host should send (see SECURITY_PACKET.md §4); GitHub Pages
// cannot set headers, so the pages carry the same CSP in a <meta> element as well.
//   npm run serve            -> http://127.0.0.1:8080/
//   PORT=9000 npm run serve
// Licence: Apache-2.0.
import { createServer } from "node:http";
import { createReadStream, existsSync, statSync } from "node:fs";
import { extname, join, normalize, resolve, dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const SITE = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const TYPES = {
  ".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8", ".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg",
  ".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf", ".csv": "text/csv; charset=utf-8",
  ".md": "text/markdown; charset=utf-8", ".txt": "text/plain; charset=utf-8", "": "text/plain; charset=utf-8",
};
export const HEADERS = {
  "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'none'; media-src 'none'; object-src 'none'; frame-src 'none'; worker-src 'none'; manifest-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'",
  "Referrer-Policy": "no-referrer",
  "X-Content-Type-Options": "nosniff",
  "Permissions-Policy": "camera=(), microphone=(), geolocation=(), interest-cohort=(), browsing-topics=()",
  "Cross-Origin-Opener-Policy": "same-origin",
  "Cross-Origin-Resource-Policy": "same-origin",
};

export function startServer({ root = join(SITE, "_site"), port = Number(process.env.PORT) || 8080, host = "127.0.0.1" } = {}) {
  const server = createServer((req, res) => {
    let p;
    try { p = decodeURIComponent(new URL(req.url, "http://x").pathname); } catch { res.writeHead(400); return res.end(); }
    let file = normalize(join(root, p));
    if (!file.startsWith(root)) { res.writeHead(403); return res.end(); }
    if (existsSync(file) && statSync(file).isDirectory()) file = join(file, "index.html");
    if (!existsSync(file)) { file = join(root, "404.html"); res.statusCode = 404; }
    res.setHeader("Content-Type", TYPES[extname(file)] || "application/octet-stream");
    for (const [k, v] of Object.entries(HEADERS)) res.setHeader(k, v);
    res.setHeader("Cache-Control", "no-cache");
    createReadStream(file).pipe(res);
  });
  return new Promise((ok) => server.listen(port, host, () => ok(server)));
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  const s = await startServer();
  const { port } = s.address();
  console.log(`EMST explorer at http://127.0.0.1:${port}/ (Ctrl+C to stop). Serving ${join(SITE, "_site")}`);
}
