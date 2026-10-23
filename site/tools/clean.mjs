#!/usr/bin/env node
// Remove the previous build output so pages for records that left the release do not linger. Licence: Apache-2.0.
import { rmSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
const SITE = resolve(dirname(fileURLToPath(import.meta.url)), "..");
rmSync(join(SITE, "_site"), { recursive: true, force: true });
console.log("[clean] removed _site/");
