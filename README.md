# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/anemomonimo12-sys/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/anemomonimo12-sys/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A program that sums up the world news of Monday 23 November 2026 in one picture: a newspaper front page drawn by render.py (PIL) — masthead naming the day, six panels covering COP31 ending with no deal, the Russian strike on Dymer, the AI-led market sell-off, Ukraine saying it sank the corvette Merkury off Benghazi, the Democrats clinching 258 House seats, and the Belgian strike grounding flights — plus an "also today" strip. main.ts copies the finished entry.png to /output/entry.png byte for byte, deterministically, with no network.

## Run it

```sh
python3 render.py          # redraw entry.png
MAKEFUN_OUTPUT_DIR=/output node main.ts   # writes /output/entry.png
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=pqs0bqkp&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
