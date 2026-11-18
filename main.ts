// News-image entry (Node 22, standard library only).
// The image is entry.png beside this file; the program copies it to the
// output directory as entry.png. It writes the same bytes on every run,
// and refuses to run if the image is missing, so a broken repository
// fails loudly instead of producing an empty output.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = new URL("./entry.png", import.meta.url);
if (!existsSync(src)) {
  throw new Error("entry.png is missing from the repository");
}
copyFileSync(src, join(outDir, "entry.png"));
