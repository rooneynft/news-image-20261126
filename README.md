# The World in One Page — Thursday 26 November 2026

**36 stories · 9 regions · every story dated honestly**

A newspaper front page summing up the world's news of Thursday
26 November 2026, rendered as a single 1024×1024 PNG.

## Angle: the EU summit + peace

- **Lead:** the special European Council in Brussels (26–27 Nov) —
  Ukraine funding for 2027 and the EU's 2028–2034 budget.
- **War:** Ukraine strikes a Russian airbase (5 jets damaged, 2 oil
  refineries hit); Russia's overnight missile + 113-drone attack;
  Ukraine hits Marinovka airfield and a Transneft terminal; Zelensky's
  mass-strike warning; 34 nations urge Russia to halt alleged riot-gas
  use; the UK puts 100,000 reservists on standby.
- **Peace:** Colombia marks 10 years of its peace accord (the UN warns
  the promises are unfinished); Mumbai marks 18 years since the 26/11
  attacks; Melania Trump returns 9 more Ukrainian children (43 total).
- **The day's other big stories:** the Macy's 100th parade postponed
  by storm (a first in 100 years); Shenzhou-24 launches the first
  Pakistani astronaut to Tiangong (25 Nov); Cairo's tanker fire kills
  31 (25 Nov); Hong Kong's renovation fire kills 168; BepiColombo
  enters Mercury orbit after 8 years (21 Nov); US tariffs on 14
  economies; S&P 500 and Dow enter correction; Black Friday online
  sales forecast at $12.9B.

## Honest dates

Every story carries its real date. News from 25 Nov (Shenzhou-24,
Cairo) is dated 25 Nov, the Sudan Damazin strike is 24 Nov,
BepiColombo is 21 Nov, Black Friday is a 27 Nov forecast. The
unverified Jensen Huang / Nvidia exit claim and the Houthi Ras Tanura
claim are left out (see the DATE CHECK line in the footer).

## Regions (9)

Africa · Asia · Caribbean · Europe · Middle East · North America ·
Oceania · South America · Ukraine.

## How it is built

- `render_front.py` — draws the page with Pillow (DejaVu fonts):
  masthead, a 6-number strip, a lead story with a drawn EU scene,
  four feature cards with drawn scenes, four "in pictures" cards,
  a schematic world map with 6 numbered pins, and 27 dated briefs.
  Run `python3 render_front.py` to regenerate `entry.png`.
- `main.py` — the entry program. It copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (stdlib only, no network, two runs
  write identical bytes).
- `entry.png` — the rendered front page (1024×1024, under 1 MiB).
