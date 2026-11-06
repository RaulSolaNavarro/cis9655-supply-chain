"""Q1: annotated GSCPI line chart, January 2019 to the latest month.

Reads the newest data/processed/gscpi_<date>.csv, shades the four disruption
windows, writes q1-pressure/gscpi_disruption_windows.png, and prints and saves
per-window summary stats (q1-pressure/gscpi_window_stats.csv).

Usage:  python q1-pressure/build_gscpi_chart.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = ROOT / "data" / "processed"
OUT_DIR = Path(__file__).resolve().parent
START = "2019-01-01"

# GSCPI is in standard deviations from its long-run mean, so 1.0 is a natural
# "elevated pressure" line.
ELEVATED = 1.0

# Disruption windows (first month, last month). End=None runs to the latest month.
# Panama and Red Sea overlap in late 2023 / early 2024.
WINDOWS = [
    ("West Coast port congestion", "2021-01", "2022-12"),
    ("Panama Canal drought", "2023-06", "2024-05"),
    ("Red Sea / Suez rerouting", "2023-11", "2024-12"),
    ("Renewed 2026 pressure", "2026-01", None),
]

# Reference palette (light mode): one series, so one hue; windows are neutral.
SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3df"
SERIES = "#2a78d6"
BAND = "#d9d8d3"


def load_gscpi() -> pd.Series:
    path = sorted(PROCESSED_DIR.glob("gscpi_*.csv"))[-1]
    df = pd.read_csv(path, parse_dates=["date"])
    s = df.set_index("date")["value"].sort_index()
    # Index by month start so bands and points line up on the axis.
    s.index = s.index.to_period("M").to_timestamp()
    return s[START:]


def window_bounds(start: str, end: str | None, s: pd.Series):
    lo = pd.Timestamp(start)
    hi = pd.Timestamp(end) if end else s.index[-1]
    return lo, hi


def window_stats(s: pd.Series) -> pd.DataFrame:
    rows = []
    for name, start, end in WINDOWS:
        lo, hi = window_bounds(start, end, s)
        w = s[lo:hi]
        rows.append({
            "window": name,
            "start": lo.strftime("%Y-%m"),
            "end": hi.strftime("%Y-%m"),
            "months": len(w),
            "peak": round(w.max(), 2),
            "peak_month": w.idxmax().strftime("%Y-%m"),
            "mean": round(w.mean(), 2),
            "months_above_0": int((w > 0).sum()),
            "months_above_1": int((w > ELEVATED).sum()),
        })
    return pd.DataFrame(rows)


def build_chart(s: pd.Series, stats: pd.DataFrame) -> Path:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "text.color": TEXT_PRIMARY,
        "axes.labelcolor": TEXT_SECONDARY,
        "xtick.color": TEXT_SECONDARY,
        "ytick.color": TEXT_SECONDARY,
    })
    fig, (strip, ax) = plt.subplots(
        2, 1, figsize=(12, 6.4), sharex=True,
        gridspec_kw={"height_ratios": [1, 5], "hspace": 0.04},
    )
    fig.patch.set_facecolor(SURFACE)
    pad = pd.Timedelta(days=15)

    # Window strip: one labeled bar per window, on its own row so the
    # overlapping Panama and Red Sea windows stay readable.
    rows = [0, 1, 0, 0]
    for (name, start, end), row in zip(WINDOWS, rows):
        lo, hi = window_bounds(start, end, s)
        strip.barh(row, (hi + pad) - (lo - pad), left=lo - pad, height=0.62,
                   color=BAND, edgecolor=SURFACE, linewidth=2)
        # The 2026 bar is too short for its full name.
        label = "2026 pressure" if end is None else name
        strip.text(lo, row, f" {label}", va="center", ha="left",
                   fontsize=9, color=TEXT_PRIMARY)
        ax.axvspan(lo - pad, hi + pad, color=BAND, alpha=0.45, lw=0, zorder=0)
    strip.set_ylim(1.6, -0.6)
    strip.axis("off")
    strip.set_facecolor(SURFACE)

    ax.set_facecolor(SURFACE)
    ax.axhline(0, color=TEXT_SECONDARY, lw=0.8, zorder=1)
    ax.axhline(ELEVATED, color=TEXT_SECONDARY, lw=0.8, ls=(0, (3, 3)), zorder=1)
    ax.text(s.index[0], ELEVATED + 0.08, "+1 std. dev. (elevated)",
            fontsize=8.5, color=TEXT_SECONDARY)
    ax.plot(s.index, s.values, color=SERIES, lw=2, zorder=3,
            solid_capstyle="round")

    # Selective direct labels: each window's peak, the COVID spike, the latest month.
    def mark(date, value, label, dy=12, ha="center", dx=0, va="baseline"):
        ax.plot(date, value, "o", ms=6, color=SERIES, zorder=4,
                markeredgecolor=SURFACE, markeredgewidth=2)
        ax.annotate(label, (date, value), xytext=(dx, dy),
                    textcoords="offset points", ha=ha, va=va, fontsize=8.5,
                    color=TEXT_PRIMARY)

    covid = s["2020"].idxmax()
    mark(covid, s[covid], f"COVID onset\n{s[covid]:.2f} ({covid:%b %Y})")
    for _, r in stats.iterrows():
        d = pd.Timestamp(r["peak_month"])
        if r["window"].startswith("Renewed"):
            mark(d, r["peak"], f"{r['peak']:.2f} ({d:%b %Y})")
        elif r["window"].startswith("West"):
            mark(d, r["peak"], f"Peak {r['peak']:.2f} ({d:%b %Y})")
    # Panama and Red Sea share their high point; label it once.
    calm = s["2023-06":"2024-12"]
    mark(calm.idxmax(), calm.max(),
         f"Max {calm.max():.2f}\n(Panama + Red Sea)", dy=14)
    last = s.index[-1]
    mark(last, s[last], f"Latest {s[last]:.2f}\n({last:%b %Y})",
         dx=6, dy=6, ha="left", va="bottom")

    ax.set_ylabel("GSCPI (std. dev. from long-run average)")
    ax.set_ylim(-2, 5)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(length=0)
    # Tick only years with data; the right margin holds the latest label.
    ax.set_xticks(pd.date_range(START, last, freq="YS"))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_xlim(pd.Timestamp(START) - pad * 2, last + pd.Timedelta(days=170))

    fig.suptitle("Global Supply Chain Pressure Index, Jan 2019 – "
                 f"{last:%b %Y}", x=0.07, ha="left", y=0.985,
                 fontsize=14, fontweight="bold")
    fig.text(0.07, 0.925, "Shaded bands mark the four disruption windows. "
             "Monthly; 0 = long-run average.", fontsize=9.5,
             color=TEXT_SECONDARY)
    fig.text(0.07, 0.015, "Source: Federal Reserve Bank of New York, GSCPI.",
             fontsize=8, color=TEXT_SECONDARY)
    fig.subplots_adjust(left=0.07, right=0.97, top=0.9, bottom=0.08)

    out = OUT_DIR / "gscpi_disruption_windows.png"
    fig.savefig(out, dpi=200, facecolor=SURFACE)
    plt.close(fig)
    return out


def main() -> None:
    s = load_gscpi()
    stats = window_stats(s)
    stats.to_csv(OUT_DIR / "gscpi_window_stats.csv", index=False)
    print(stats.to_string(index=False))
    print(f"\nWrote {build_chart(s, stats).relative_to(ROOT)}")


if __name__ == "__main__":
    main()
