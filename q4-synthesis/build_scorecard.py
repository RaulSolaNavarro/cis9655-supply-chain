"""Q4: episode scorecard, one row per disruption window, one column per measure.

Reads the per-window stats that Q1-Q3 already wrote, so every number on the
chart is traceable to those CSVs:

  q1-pressure/gscpi_window_stats.csv        peak GSCPI in the window
  q2-trade-volume/lane_share_window_stats.csv  change in East and Gulf share
  q3-ports/port_backlog_stats.csv           LA-Long Beach ships waiting, window mean

Writes q4-synthesis/episode_scorecard.png and q4-synthesis/episode_scorecard.csv.

Each measure gets its own column with one baseline and one scale, so values
compare by bar length down a column, and an episode reads across its row.

Usage:  python q4-synthesis/build_scorecard.py
"""
import importlib.util
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = Path(__file__).resolve().parent


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


q1 = _load("build_gscpi_chart", "q1-pressure/build_gscpi_chart.py")
WINDOWS = q1.WINDOWS

GSCPI_STATS = ROOT / "q1-pressure" / "gscpi_window_stats.csv"
LANE_STATS = ROOT / "q2-trade-volume" / "lane_share_window_stats.csv"
BACKLOG_STATS = ROOT / "q3-ports" / "port_backlog_stats.csv"
BACKLOG_GROUP = "LA-LB"
# Shifts smaller than this (in points) read as "No change".
NO_CHANGE_PP = 0.5

SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
RULE = "#e4e3df"
PRESSURE = "#52514e"
EAST = "#eb6834"   # toward East and Gulf ports (Panama-dependent lane color)
WEST = "#2a78d6"   # toward the West Coast (Pacific-direct lane color)
SHIPS = "#8a8984"


def _month(ym: str) -> str:
    return pd.Timestamp(ym).strftime("%b %Y")


def load_table() -> pd.DataFrame:
    gscpi = pd.read_csv(GSCPI_STATS).set_index("window")
    lanes = pd.read_csv(LANE_STATS).set_index("window")
    ports = pd.read_csv(BACKLOG_STATS).set_index("group").loc[BACKLOG_GROUP]
    rows = []
    for name, _, _ in WINDOWS:
        key = "mean_" + name.split()[0].lower()
        shift = float(lanes.loc[name, "change_pp"]) + 0.0  # turns -0.0 into 0.0
        if shift >= NO_CHANGE_PP:
            moved = "East"
        elif shift <= -NO_CHANGE_PP:
            moved = "West"
        else:
            moved = "No change"
        rows.append({
            "window": name,
            "start": gscpi.loc[name, "start"],
            "end": gscpi.loc[name, "end"],
            "peak_gscpi": float(gscpi.loc[name, "peak"]),
            "share_change_pp": shift,
            "lalb_ships_waiting_mean": float(ports[key]),
            "cargo_moved": moved,
        })
    return pd.DataFrame(rows)


def build_chart(table: pd.DataFrame) -> Path:
    """Wide layout (15 x 5.4 in) so the chart can span a full slide width.

    Text sizes are set so every label stays legible when the slide is shown
    at half size: labels and values 19-21 pt, secondary lines 17 pt.
    """
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 17,
                         "text.color": TEXT_PRIMARY})
    W, H = 15, 5.4
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor(SURFACE)

    n = len(table)
    # Vertical bands in figure fractions: header on top, footnotes at the bottom.
    top, bottom = 0.735, 0.205
    # Column x-ranges in figure fractions: labels, three bar columns, text column.
    cols = {"label": (0.012, 0.31), "pressure": (0.315, 0.44),
            "shift": (0.46, 0.64), "ships": (0.66, 0.80),
            "moved": (0.825, 0.995)}
    row_h = (top - bottom) / n
    y_mid = [top - row_h * (i + 0.5) for i in range(n)]

    def column_axes(key):
        x0, x1 = cols[key]
        ax = fig.add_axes([x0, bottom, x1 - x0, top - bottom])
        ax.set_facecolor(SURFACE)
        ax.set_ylim(n - 0.5, -0.5)
        ax.axis("off")
        return ax

    def header(key, title, unit):
        x0, _ = cols[key]
        fig.text(x0, 0.92, title, fontsize=20, fontweight="bold", va="bottom")
        fig.text(x0, 0.905, unit, fontsize=17, color=TEXT_SECONDARY, va="top",
                 linespacing=1.1)

    # Faint row separators, except between the two overlapping windows,
    # which the bracket below groups instead.
    names = list(table["window"])
    i_pan, i_red = names.index("Panama Canal drought"), names.index("Red Sea / Suez rerouting")
    for i in range(1, n):
        if {i - 1, i} == {i_pan, i_red}:
            continue
        y = top - row_h * i
        fig.add_artist(plt.Line2D([0.012, 0.995], [y, y], color=RULE, lw=1))
    fig.add_artist(plt.Line2D([0.012, 0.995], [top + 0.012] * 2,
                              color=TEXT_SECONDARY, lw=1))

    # Row labels: episode name and date range.
    lx = 0.024
    for (_, r), y in zip(table.iterrows(), y_mid):
        fig.text(lx, y + 0.03, r["window"], fontsize=19, fontweight="bold",
                 va="center")
        fig.text(lx, y - 0.04, f"{_month(r['start'])} to {_month(r['end'])}",
                 fontsize=17, color=TEXT_SECONDARY, va="center")
    # Bracket joining the overlapping Panama and Red Sea rows (explained in the footnote).
    ya, yb = y_mid[i_pan] + 0.055, y_mid[i_red] - 0.065
    bx = 0.014
    fig.add_artist(plt.Line2D([bx, bx], [yb, ya], color=TEXT_SECONDARY, lw=2))
    for yy in (ya, yb):
        fig.add_artist(plt.Line2D([bx, bx + 0.006], [yy, yy],
                                  color=TEXT_SECONDARY, lw=2))

    bar_h = 0.5
    value_size = 21
    # 1. Pressure: peak GSCPI, one shared scale starting at zero.
    header("pressure", "Pressure", "Pressure score\n(peak)")
    ax = column_axes("pressure")
    vmax = table["peak_gscpi"].max()
    ax.set_xlim(0, vmax * 1.42)
    for i, v in enumerate(table["peak_gscpi"]):
        ax.barh(i, v, height=bar_h, color=PRESSURE)
        ax.text(v + vmax * 0.04, i, f"{v:.2f}", va="center", fontsize=value_size)
    ax.axvline(0, color=TEXT_PRIMARY, lw=1)

    # 2. Cargo shift: diverging from zero. Positive = toward East and Gulf.
    header("shift", "Cargo shift", "East and Gulf share,\nchange (points)")
    ax = column_axes("shift")
    # Uneven limits: most of the room goes to the long eastward bar.
    neg = -table["share_change_pp"].min()
    pos = table["share_change_pp"].max()
    lim = (neg + pos) * 0.8  # scale for the value-label offset
    ax.set_xlim(-neg * 2.75, pos * 1.68)
    for i, v in enumerate(table["share_change_pp"]):
        color = EAST if v > 0 else WEST
        ax.barh(i, v, height=bar_h, color=color)
        label = f"{v:+.1f}" if v != 0 else "0.0"
        if v >= 0:
            ax.text(v + lim * 0.04, i, label, va="center", ha="left", fontsize=value_size)
        else:
            ax.text(v - lim * 0.04, i, label, va="center", ha="right", fontsize=value_size)
    ax.axvline(0, color=TEXT_PRIMARY, lw=1)
    x0, x1 = cols["shift"]
    fig.text(x0, top + 0.022, "← West", fontsize=17, color=WEST,
             fontweight="bold", va="bottom", ha="left")
    fig.text(x1, top + 0.022, "East →", fontsize=17, color=EAST,
             fontweight="bold", va="bottom", ha="right")

    # 3. Ships waiting at LA-Long Beach, window average.
    header("ships", "Ships waiting", "LA-Long Beach\n(average)")
    ax = column_axes("ships")
    smax = table["lalb_ships_waiting_mean"].max()
    ax.set_xlim(0, smax * 1.45)
    for i, v in enumerate(table["lalb_ships_waiting_mean"]):
        ax.barh(i, v, height=bar_h, color=SHIPS)
        ax.text(v + smax * 0.04, i, f"{v:.1f}", va="center", fontsize=value_size)
    ax.axvline(0, color=TEXT_PRIMARY, lw=1)

    # 4. Plain-English direction of the cargo shift.
    header("moved", "Cargo moved", "")
    for (_, r), y in zip(table.iterrows(), y_mid):
        color = {"East": EAST, "West": WEST}.get(r["cargo_moved"], TEXT_SECONDARY)
        fig.text(cols["moved"][0], y, r["cargo_moved"], fontsize=21,
                 fontweight="bold", color=color, va="center")

    fig.text(0.012, 0.145, "Bracket: the Panama and Red Sea windows overlap, Nov 2023 to May 2024.",
             fontsize=17, color=TEXT_SECONDARY, va="center")
    fig.text(0.012, 0.09, "Cargo shift for 2026 runs through Aug 2026, the latest trade data. "
             "Pressure runs through Sep 2026.", fontsize=17, color=TEXT_SECONDARY,
             va="center")
    fig.text(0.012, 0.035, "Sources: NY Fed GSCPI; US Census Bureau imports "
             "(China-origin, containerized value); BTS Supply Chain and Freight "
             "Indicators.", fontsize=15, color=TEXT_SECONDARY, va="center")

    out = OUT_DIR / "episode_scorecard.png"
    fig.savefig(out, dpi=200, facecolor=SURFACE)
    plt.close(fig)
    return out


def main() -> None:
    table = load_table()
    table.to_csv(OUT_DIR / "episode_scorecard.csv", index=False)
    print(table.to_string(index=False))
    print(f"\nWrote {build_chart(table).relative_to(ROOT)}")


if __name__ == "__main__":
    main()
