# Tableau build — split four ways

Everything you need is already in the GitHub repo under `tableau/`. You don't need to run any Python — the four CSVs are pre-built and already have every column the build needs (window labels, map coordinates, marker sizes). You just need **Tableau Desktop or Tableau Public Desktop** (both free; Tableau Public doesn't require a license, only a free account to publish) and the file `tableau/BUILD_GUIDE.md`.

**Do not open `tableau/supply_chain_resilience.twbx`.** It's a generated file that's confirmed broken — Tableau refuses to load it. Build from scratch using the guide below; it's quick because it tells you exactly which shelf each field goes on.

## Get the data

1. On GitHub, go to the repo's `tableau/data/` folder and download the one CSV listed below for your piece (click the file → the "Download raw file" button, or `git pull` if you already have the repo cloned).
2. Open `tableau/BUILD_GUIDE.md` in the repo (plain text/markdown — readable in any browser or editor) and read **only your numbered section** below. Section 0 (palette) is optional and quick; do it if you want the colors to match exactly, skip it if you're short on time.

## Your assignment

| Person | Section of BUILD_GUIDE.md | Sheet you're building | CSV you need | Est. time |
|---|---|---|---|---|
| **Jason** | Section 1 | "GSCPI" — pressure index line with shaded disruption windows | `tableau/data/gscpi_tableau.csv` | ~12 min |
| **Paven** | Section 2 | "Lane share" — two lines (Pacific-direct vs. Panama-dependent) | `tableau/data/lane_share_tableau.csv` | ~10 min |
| **Supriya** | Sections 3 + 4 | "Port map" (symbol map) and "Port series" (backlog/throughput toggle) | `tableau/data/port_map_tableau.csv` and `tableau/data/port_series_tableau.csv` | ~18 min |
| **Raul** | Sections 0, 5, 6 | Palette setup, then the combined Dashboard + filter action + Story, once everyone's sheet exists | all four CSVs | ~20 min |

This matches how the written analysis was already split (Jason=Q1, Paven=Q2, Supriya=Q3, Raul=Q4/synthesis) — the dashboard-and-story step is literally the "put it all together" step, so it's Raul's natural piece.

## When you're done with your sheet

1. **File → Save**, then **Server → Tableau Public → Save to Tableau Public** (free account, one-time sign-up). This gives you a shareable link to your own visualization — that's your individual contribution, and it's fine to stop here if that's all the time you have.
2. When you publish, there's a toggle for whether others can **download your workbook**. Turn it **on** — Raul needs to pull your sheet into one combined workbook for the dashboard/story step. (Settings → "Show workbook" on the published viz, or the checkbox at publish time.)
3. Send Raul the Tableau Public link (and confirm downloads are on). That's it for your piece.

## If Tableau gives you trouble

Don't sink time fighting it. Take a screenshot of whatever you did get working in Tableau — even a single chart with no filter action is a legitimate, honest "here's my piece in Tableau" — and send Raul the screenshot plus a one-line note on what didn't work. We'll drop the screenshot into the deck in place of (or next to) the matplotlib version. Partial, labeled honestly, beats nothing or a rebuild from scratch under time pressure.

## Combining into one dashboard (Raul's step, after everyone's sheet is in)

1. Download each person's published `.twbx` from their Tableau Public link (the "Download" button on the viz page, now that downloads are on).
2. Open your own workbook (with your palette/sheets if you did Section 0), then open each downloaded `.twbx` in its own Tableau window.
3. Drag each person's sheet tab from their window into yours — Tableau copies the sheet, its data source connection, and formatting over. Do this for Jason's, Paven's, and Supriya's two sheets.
4. Follow BUILD_GUIDE.md Sections 5 (dashboard + filter action) and 6 (story) exactly as written, now that all four sheets live in one workbook.
5. Publish the combined result to Tableau Public too. That link becomes the "centerpiece" for the Q4/synthesis slide in the final deck — or, if time runs short, a screenshot of the finished dashboard works the same way.

Either the fully combined dashboard, or four separate individual links/screenshots, satisfies "preferably your interactive Tableau dashboard" from the presentation guidelines. Don't let the combining step become a blocker on the rest of the deck.
