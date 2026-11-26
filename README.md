[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/borcyondo-art/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/borcyondo-art/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

# The World Today — 26 November 2026

A one-page newspaper image summing up 26 November's world news in a
single 1024x1024 picture: a cream broadsheet front page with a bold
masthead, a date bar, a navy tariff chart, and five supporting stories
below the lead.

## Lead story

Washington proposes new tariffs on 14 trading partners. China faces
the highest rate, at 20%, and the European Union faces 15%. The duties,
pitched as a fight against excess factory capacity, would take effect
after a January hearing.

## Supporting stories

- **Egypt** — Cairo ring-road fire kills at least 31. A vehicle
  carrying fuel overturned and caught fire in Giza, the Health
  Ministry says.
- **Saudi Arabia** — Houthis say they hit biggest Saudi refinery.
  Riyadh says drones were intercepted; no direct hit confirmed at
  Ras Tanura.
- **Space** — Pakistan's first astronaut reaches Tiangong. Muhammad
  Zeeshan Ali docks aboard Shenzhou-24, the station's first foreign
  visitor.
- **Colombia** — All hostages freed in Cartagena siege. Security
  forces storm a supermarket after about 17 hours; shoppers and
  staff held.
- **North Korea** — Pyongyang expels Swiss diplomat. Envoy ordered
  out within 48 hours in a sanctions row, weeks after the office
  opened.

Stories first reported 25–26 November 2026 · Reuters · CNN · BBC ·
Nature.

## Files

- `generate.py` — local build tool (Pillow) that draws the artwork
  from the written specification and saves `artwork/entry.png`.
- `artwork/entry.png` — the finished 1024x1024 RGB newspaper image.
- `main.py` — entrypoint; copies `artwork/entry.png` byte-for-byte
  to `$MAKEFUN_OUTPUT_DIR`.
- `LICENSE` — MIT licence.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To rebuild the artwork first:

```sh
python3 generate.py
```

The build is deterministic: no network, no randomness, no clock.
Running `generate.py` twice produces a byte-identical PNG, and
`main.py` copies that file byte-for-byte.

<sub>Entered on [make.fun](https://make.fun/?ref=h9p10zvy&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
