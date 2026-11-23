# The World Today — Monday, 23 November 2026

A newspaper front page summing up the world news of Monday 23 November
2026, drawn with PIL: COP31 ending with no deal, the Russian strike on
Dymer, the AI-led market sell-off, Ukraine saying it sank the corvette
*Merkury* off Benghazi, the Democrats clinching 258 House seats, and the
Belgian strike grounding flights — plus an "also today" strip.

## Files

- `render.py` — draws `entry.png` (1024×1024, under 1 MiB) with PIL.
- `entry.png` — the finished front page.
- `main.ts` — the entrypoint: copies `entry.png` to `$MAKEFUN_OUTPUT_DIR`
  (or `/output`), failing loudly if the copy is a different size or over
  1 MiB.

## Run

```sh
python3 render.py          # redraw entry.png
mkdir -p out1 out2
MAKEFUN_OUTPUT_DIR=out1 node main.ts
MAKEFUN_OUTPUT_DIR=out2 node main.ts
cmp out1/entry.png out2/entry.png   # the two runs must be identical
```
