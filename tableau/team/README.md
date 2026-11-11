# Tableau team guide: start here

Each of us builds one or two views in Tableau, publishes them, and sends Raul the link. Raul combines them into one dashboard. You do **not** need Python, and you do **not** need to read the long `BUILD_GUIDE.md`. Your own guide below has everything for your piece.

## Before you start (5 minutes, once)

1. Download **Tableau Public** (free, the desktop app): https://www.tableau.com/products/public/download
2. Make a free Tableau Public account when it asks (you need it to publish).
3. Download the one data file for your piece (links in your guide). On GitHub: open the file, click the **download icon** (top right of the file view). Save it somewhere you can find, like your Desktop.

**Do not open** `tableau/supply_chain_resilience.twbx`. It is a broken file. Start from a blank Tableau and your CSV.

## Pick your guide

| Who | Your guide | Your data file | Time |
|---|---|---|---|
| Jason | [01_jason_gscpi.md](01_jason_gscpi.md) | `gscpi_tableau.csv` | about 15 min |
| Paven | [02_paven_lane_share.md](02_paven_lane_share.md) | `lane_share_tableau.csv` | about 15 min |
| Supriya | [03_supriya_ports.md](03_supriya_ports.md) | `port_map_tableau.csv` and `port_series_tableau.csv` | about 25 min |
| Raul | [04_raul_dashboard.md](04_raul_dashboard.md) | all four | about 25 min, after the others finish |

## How each guide is set up

- Each guide has **three levels**. Level 1 gives you a working chart. Level 2 adds the shaded disruption bands. Level 3 adds labels and polish. **Stop after any level.** Level 1 alone is a valid contribution.
- Every step is one action. After each group of steps there is a **You should see** line. If your screen does not match it, stop and take a screenshot to send us. Do not keep clicking.
- Words in **bold** are things you click or type exactly.

## When you finish

1. In Tableau Public: **File**, then **Save to Tableau Public As...**. Sign in. Name it as your guide says.
2. Your browser opens the published page. **Copy that link.**
3. On that page, make sure **Allow downloads** is on (the little download icon should show). Raul needs to pull your sheet into the combined workbook.
4. Send the link to the group chat. Also send **one screenshot** of your chart. That is the backup if anything fails.

## If Tableau misbehaves

Do not fight it for more than 10 minutes. Screenshot whatever you got working, even half a chart, and send it with one line on what went wrong. That is a real, honest contribution and we will use it in the deck.

## Colors (copy exactly)

| Use | RGB (type these into Tableau's color picker) | Hex |
|---|---|---|
| Blue: Pacific-direct, Los Angeles and Long Beach, the pressure line | 42, 120, 214 | `#2a78d6` |
| Orange: Panama-dependent, Savannah | 235, 104, 52 | `#eb6834` |
| Gray: all other ports | 138, 137, 132 | `#8a8984` |
| Shaded disruption bands | 217, 216, 211 | `#d9d8d3` |
