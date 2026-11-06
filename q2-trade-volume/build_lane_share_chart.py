"""Q2: Panama-dependent vs. Pacific-direct share of China containerized imports.

Reads the newest data/processed/census_porths_5700_lanes_<date>.csv, computes
each lane group's share of all-port China containerized import value by month,
marks the disruption windows from q1-pressure/build_gscpi_chart.py, writes
q2-trade-volume/lane_share_disruption_windows.png, and prints and saves
per-window share shifts (q2-trade-volume/lane_share_window_stats.csv).

Usage:  python q2-trade-volume/build_lane_share_chart.py
"""
import importlib.util
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = ROOT / "data" / "processed"
OUT_DIR = Path(__file__).resolve().parent

# Reuse Q1's window definitions so both charts mark the same months.
_spec = importlib.util.spec_from_file_location(
    "build_gscpi_chart", ROOT / "q1-pressure" / "build_gscpi_chart.py")
_q1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_q1)
WINDOWS = _q1.WINDOWS

GROUPS = ["Pacific-direct", "Panama-dependent"]
# Containerized value tracks ocean routing; total value also counts air and land.
MEASURE = "containerized_value_usd"
BASELINE = ("2019-01", "2019-12")
SMOOTH_MONTHS = 3

# Reference palette (light mode), categorical slots 1-2.
SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3df"
BAND = "#d9d8d3"
COLORS = {"Pacific-direct": "#2a78d6", "Panama-dependent": "#eb6834"}


def load_shares() -> pd.DataFrame:
    path = sorted(PROCESSED_DIR.glob("census_porths_5700_lanes_*.csv"))[-1]
    df = pd.read_csv(path)
    monthly = df.pivot_table(index="month", columns="lane_group",
                             values=MEASURE, aggfunc="sum")
    shares = monthly.div(monthly.sum(axis=1), axis=0) * 100
    shares.index = pd.PeriodIndex(shares.index, freq="M").to_timestamp()
    return shares[GROUPS]


def window_bounds(start: str, end: str | None, shares: pd.DataFrame):
    lo = pd.Timestamp(start)
    hi = pd.Timestamp(end) if end else shares.index[-1]
    return lo, hi


def window_stats(shares: pd.DataFrame) -> pd.DataFrame:
    """Share change across each window, in percentage points.

    "before" is the 3 months ending the month before the window starts, "end"
    the window's last 3 months, so the change reads as where cargo moved during
    the window. "vs_2019" compares the window mean to the 2019 baseline.
    """
    pd_share = shares["Panama-dependent"]
    base = pd_share[BASELINE[0]:BASELINE[1]]
    rows = []
    for name, start, end in WINDOWS:
        lo, hi = window_bounds(start, end, shares)
        w = pd_share[lo:hi]
        before = pd_share[:lo - pd.Timedelta(days=1)].iloc[-3:].mean()
        rows.append({
            "window": name,
            "start": lo.strftime("%Y-%m"),
            "end": hi.strftime("%Y-%m"),
            "panama_share_before": round(before, 1),
            "panama_share_end": round(w.iloc[-3:].mean(), 1),
            "change_pp": round(w.iloc[-3:].mean() - before, 1),
            "panama_share_mean": round(w.mean(), 1),
            "vs_2019_pp": round(w.mean() - base.mean(), 1),
        })
    stats = pd.DataFrame(rows)
    stats.attrs["baseline_mean"] = round(base.mean(), 1)
    stats.attrs["baseline_std"] = round(base.std(), 1)
    return stats


def build_chart(shares: pd.DataFrame) -> Path:
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

    # Same window strip as Q1: overlapping Panama and Red Sea on separate rows.
    rows = [0, 1, 0, 0]
    for (name, start, end), row in zip(WINDOWS, rows):
        lo, hi = window_bounds(start, end, shares)
        strip.barh(row, (hi + pad) - (lo - pad), left=lo - pad, height=0.62,
                   color=BAND, edgecolor=SURFACE, linewidth=2)
        label = "2026 pressure" if end is None else name
        strip.text(lo, row, f" {label}", va="center", ha="left",
                   fontsize=9, color=TEXT_PRIMARY)
        ax.axvspan(lo - pad, hi + pad, color=BAND, alpha=0.45, lw=0, zorder=0)
    strip.set_ylim(1.6, -0.6)
    strip.axis("off")
    strip.set_facecolor(SURFACE)

    ax.set_facecolor(SURFACE)
    smooth = shares.rolling(SMOOTH_MONTHS).mean()
    last = shares.index[-1]
    for group in GROUPS:
        color = COLORS[group]
        ax.plot(shares.index, shares[group], color=color, lw=1, alpha=0.3,
                zorder=2)
        ax.plot(smooth.index, smooth[group], color=color, lw=2, zorder=3,
                solid_capstyle="round", label=group)
        # Direct label at the line end, in text ink beside a colored marker.
        y = smooth[group].iloc[-1]
        ax.plot(last, y, "o", ms=6, color=color, zorder=4,
                markeredgecolor=SURFACE, markeredgewidth=2)
        ax.annotate(f"{group}\n{y:.0f}%", (last, y), xytext=(8, 0),
                    textcoords="offset points", ha="left", va="center",
                    fontsize=8.5, color=TEXT_PRIMARY)

    ax.legend(loc="upper left", frameon=False, fontsize=9, ncols=2,
              bbox_to_anchor=(0, 1.0))
    ax.set_ylabel("Share of China containerized import value (%)")
    ax.set_ylim(15, 80)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(length=0)
    ax.set_xticks(pd.date_range(shares.index[0], last, freq="YS"))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_xlim(shares.index[0] - pad * 2, last + pd.Timedelta(days=330))

    fig.suptitle("China imports by lane group, Jan 2019 – "
                 f"{last:%b %Y}", x=0.07, ha="left", y=0.985,
                 fontsize=14, fontweight="bold")
    fig.text(0.07, 0.925, f"Bold lines are {SMOOTH_MONTHS}-month averages, "
             "faint lines monthly. China-origin imports only. Remaining share "
             "is other US ports.", fontsize=9.5, color=TEXT_SECONDARY)
    fig.text(0.07, 0.015, "Source: US Census Bureau, international trade API "
             "(imports/porths, port of unlading).", fontsize=8,
             color=TEXT_SECONDARY)
    fig.subplots_adjust(left=0.07, right=0.97, top=0.9, bottom=0.08)

    out = OUT_DIR / "lane_share_disruption_windows.png"
    fig.savefig(out, dpi=200, facecolor=SURFACE)
    plt.close(fig)
    return out


def main() -> None:
    shares = load_shares()
    stats = window_stats(shares)
    stats.to_csv(OUT_DIR / "lane_share_window_stats.csv", index=False)
    print(stats.to_string(index=False))
    print(f"\n2019 Panama-dependent share: mean {stats.attrs['baseline_mean']}%, "
          f"monthly std {stats.attrs['baseline_std']} pp")
    print(f"Wrote {build_chart(shares).relative_to(ROOT)}")


if __name__ == "__main__":
    main()
