// News in one image — entrypoint (Node 22, standard library only).
//
// Copies the pre-rendered front page (entry.png, drawn by
// tools/generate_image.py during the build session) to the grader's output
// directory. The program is deterministic: it writes the same bytes on
// every run, uses no network, and leaves the output readable (mode 0644).
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { chmodSync, copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const target = join(outDir, 'entry.png');
copyFileSync(new URL('./entry.png', import.meta.url), target);
chmodSync(target, 0o644);
