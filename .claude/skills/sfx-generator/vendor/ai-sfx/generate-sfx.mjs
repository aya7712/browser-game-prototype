#!/usr/bin/env node
// Vendored from https://github.com/siliconjungle/ai-sfx (MIT License, Copyright (c) 2025 James Addison)
// See ./LICENSE for the full license text.
// Usage: node generate-sfx.mjs '<json>' [output.wav]
import { createRequire } from 'module';
import { writeFileSync } from 'fs';
import { resolve } from 'path';

const require = createRequire(import.meta.url);
const { sfxr } = require('./jsfxr/_sfxr.js');

const raw  = process.argv[2];
const out  = process.argv[3] ?? 'output.wav';

if (!raw) {
  console.error('Usage: node generate-sfx.mjs \'<jsfxr-params-json>\' [output.wav]');
  process.exit(1);
}

let params;
try {
  params = JSON.parse(raw);
} catch {
  console.error('Invalid JSON');
  process.exit(1);
}

const wave = sfxr.toWave(params);
const path = resolve(out);
writeFileSync(path, Buffer.from(wave.wav));
console.log(`Saved: ${path}`);
