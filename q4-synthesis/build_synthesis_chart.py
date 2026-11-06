"""Q4: stacked synthesis of Q1-Q3 on one shared monthly axis.

Panels, top to bottom: GSCPI (Q1); China lane share (Q2) with the Shanghai-LA
freight rate shifted forward six months underneath it; ships awaiting berths
(Q3). Every panel shades the Q1 disruption windows.

Also tests the pitch deck's claim (docs/index.html, slide 8) that the freight
rate lagged six months correlates with lane share at r ~ 0.45, and writes the
results to q4-synthesis/lag_correlations.csv.

Usage:  python q4-synthesis/build_synthesis_chart.py
"""
import importlib.util
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = Path(__file__).resolve().parent


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Reuse each question's loaders and Q1's windows so the numbers match Q1-Q3.
q1 = _load("build_gscpi_chart", "q1-pressure/build_gscpi_chart.py")
q2 = _load("build_lane_share_chart", "q2-trade-volume/build_lane_share_chart.py")
q3 = _load("build_port_charts", "q3-ports/build_port_charts.py")
WINDOWS = q1.WINDOWS

FREIGHT_RATE = "Freight Rates in $ per 40ft Container from Shanghai to LA"
LAG_MONTHS = 6
START = "2019-01-01"
# Split for the robustness check: the 2021-22 episode vs. everything after it.
SPLIT = "2023-01-01"

SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3df"
BAND = "#d9d8d3"
GSCPI_COLOR = q1.SERIES
LANE_COLORS = q2.COLORS
BACKLOG_COLORS = q3.BACKLOG_COLORS
# Neutral ink for the freight rate, so it doesn't read as a third lane.
RATE_COLOR = "#52514e"


def load_freight_rate() -> pd.Series:
    bts = q3.load_bts()
    rate = bts[bts["indicator"] == FREIGHT_RATE].set_index("date")["value"]
    rate.index = rate.index.to_period("M").to_timestamp()
    return rate.sort_index()


def lag_correlations(rate: pd.Series, gscpi: pd.Series,
                     panama_share: pd.Series) -> pd.DataFrame:
    """Pearson r between each driver at month t-lag and Panama-dependent share at t."""
    rows = []
    for driver, series in [("freight_rate", rate), ("gscpi", gscpi)]:
        for lag in range(0, 13):
            shifted = series.copy()
            shifted.index = shifted.index + pd.DateOffset(months=lag)
            pair = pd.concat([shifted, panama_share], axis=1, join="inner").dropna()
            row = {"driver": driver, "lag_months": lag, "n": len(pair),
                   "r": round(pair.iloc[:, 0].corr(pair.iloc[:, 1]), 3)}
            if lag == LAG_MONTHS:
                early, late = pair[pair.index < SPLIT], pair[pair.index >= SPLIT]
                row.update({
                    "r_through_2022": round(early.iloc[:, 0].corr(early.iloc[:, 1]), 3),
                    "n_through_2022": len(early),
                    "r_2023_on": round(late.iloc[:, 0].corr(late.iloc[:, 1]), 3),
                    "n_2023_on": len(late),
                })
            rows.append(row)
    return pd.DataFrame(rows)


def style_axes(ax) -> None:
    ax.set_facecolor(SURFACE)
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(length=0)


def panel_title(ax, text: str, note: str = "") -> None:
    ax.set_title(text, loc="left", fontsize=10.5, fontweight="bold",
                 color=TEXT_PRIMARY, pad=14)
    if note:
        ax.text(0, 1.02, note, transform=ax.transAxes, fontsize=8.5,
                color=TEXT_SECONDARY, va="bottom")


def end_label(ax, s: pd.Series, text: str, color: str) -> None:
    s = s.dropna()
    ax.plot(s.index[-1], s.iloc[-1], "o", ms=5, color=color, zorder=4,
            markeredgecolor=SURFACE, markeredgewidth=2)
    ax.annotate(text, (s.index[-1], s.iloc[-1]), xytext=(8, 0),
                textcoords="offset points", ha="left", va="center",
                fontsize=8.5, color=TEXT_PRIMARY)


def build_chart(gscpi, shares, rate_lagged, backlog, corr) -> Path:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "text.color": TEXT_PRIMARY,
        "axes.labelcolor": TEXT_SECONDARY,
        "xtick.color": TEXT_SECONDARY,
        "ytick.color": TEXT_SECONDARY,
    })
    fig, axes = plt.subplots(
        5, 1, figsize=(12, 13), sharex=True,
        gridspec_kw={"height_ratios": [0.9, 3, 3, 1.4, 3], "hspace": 0.38},
    )
    strip, ax_g, ax_s, ax_r, ax_b = axes
    fig.patch.set_facecolor(SURFACE)
    pad = pd.Timedelta(days=15)
    last = max(gscpi.index[-1], shares.index[-1], backlog.index[-1])
    x_end = last + pd.Timedelta(days=120)

    # Window strip, as in Q1-Q3.
    rows = [0, 1, 0, 0]
    for (name, start, end), row in zip(WINDOWS, rows):
        lo = pd.Timestamp(start)
        hi = pd.Timestamp(end) if end else last
        strip.barh(row, (hi + pad) - (lo - pad), left=lo - pad, height=0.62,
                   color=BAND, edgecolor=SURFACE, linewidth=2)
        label = "2026 pressure" if end is None else name
        strip.text(lo, row, f" {label}", va="center", ha="left",
                   fontsize=9, color=TEXT_PRIMARY)
        for ax in axes[1:]:
            ax.axvspan(lo - pad, hi + pad, color=BAND, alpha=0.45, lw=0, zorder=0)
    strip.set_ylim(1.6, -0.6)
    strip.axis("off")
    strip.set_facecolor(SURFACE)

    # 1. GSCPI
    style_axes(ax_g)
    ax_g.axhline(0, color=TEXT_SECONDARY, lw=0.8, zorder=1)
    ax_g.axhline(q1.ELEVATED, color=TEXT_SECONDARY, lw=0.8, ls=(0, (3, 3)), zorder=1)
    ax_g.plot(gscpi.index, gscpi.values, color=GSCPI_COLOR, lw=2, zorder=3)
    end_label(ax_g, gscpi, f"{gscpi.iloc[-1]:.2f}", GSCPI_COLOR)
    ax_g.set_ylim(-2, 5)
    ax_g.set_ylabel("Std. dev.")
    panel_title(ax_g, "1  Supply chain pressure (GSCPI)",
                "0 = long-run average, dashed = +1 (elevated)")

    # 2. Lane share
    style_axes(ax_s)
    smooth = shares.rolling(q2.SMOOTH_MONTHS).mean()
    for group in q2.GROUPS:
        ax_s.plot(smooth.index, smooth[group], color=LANE_COLORS[group], lw=2,
                  zorder=3, label=group)
        end_label(ax_s, smooth[group], f"{smooth[group].iloc[-1]:.0f}%",
                  LANE_COLORS[group])
    ax_s.set_ylim(20, 75)
    ax_s.set_ylabel("% of value")
    ax_s.legend(loc="upper left", frameon=False, fontsize=8.5, ncols=2,
                bbox_to_anchor=(0, 1.0))
    panel_title(ax_s, "2  China containerized imports by lane group",
                f"{q2.SMOOTH_MONTHS}-month average share of all US ports; "
                "China-origin only")

    # 2b. Freight rate, shifted forward so it lines up with the share it precedes.
    style_axes(ax_r)
    shown = rate_lagged[:last]
    ax_r.plot(shown.index, shown.values / 1000, color=RATE_COLOR, lw=2, zorder=3)
    end_label(ax_r, shown / 1000, f"${shown.iloc[-1] / 1000:.1f}k",
              RATE_COLOR)
    ax_r.set_ylim(0, 13)
    ax_r.set_ylabel("$k / 40ft")
    six = corr[(corr["driver"] == "freight_rate") &
               (corr["lag_months"] == LAG_MONTHS)].iloc[0]
    panel_title(
        ax_r, f"2b  Shanghai–LA freight rate, {LAG_MONTHS} months earlier",
        f"Plotted at month t = rate at t−{LAG_MONTHS}. r with Panama-dependent "
        f"share = {six['r']:.2f} (n={six['n']}): {six['r_through_2022']:.2f} "
        f"through 2022, {six['r_2023_on']:.2f} from 2023")

    # 3. Ships awaiting berths
    style_axes(ax_b)
    for group in q3.BACKLOG_GROUPS:
        s = backlog[group]
        ax_b.plot(s.index, s.values, color=BACKLOG_COLORS[group], lw=2,
                  zorder=3, label=group)
    ax_b.set_ylim(0, 110)
    ax_b.set_ylabel("Ships")
    ax_b.legend(loc="upper right", frameon=False, fontsize=8.5, ncols=3)
    panel_title(ax_b, "3  Containerships awaiting a berth",
                "Monthly mean; BTS series starts Jul 2021")

    ax_b.set_xticks(pd.date_range(START, last, freq="YS"))
    ax_b.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax_b.set_xlim(pd.Timestamp(START) - pad * 2, x_end)

    fig.suptitle("Supply chain pressure, lane share, and port backlogs, "
                 f"Jan 2019 – {last:%b %Y}", x=0.07, ha="left", y=0.995,
                 fontsize=14, fontweight="bold")
    fig.text(0.07, 0.963, "One shared monthly axis; shaded bands are the four "
             "disruption windows.", fontsize=9.5, color=TEXT_SECONDARY)
    fig.text(0.07, 0.008, "Sources: NY Fed GSCPI; US Census Bureau imports/porths; "
             "BTS Supply Chain and Freight Indicators (Drewry via USDA AMS for "
             "freight rates).", fontsize=8, color=TEXT_SECONDARY)
    fig.subplots_adjust(left=0.07, right=0.96, top=0.95, bottom=0.04)

    out = OUT_DIR / "synthesis_small_multiples.png"
    fig.savefig(out, dpi=200, facecolor=SURFACE)
    plt.close(fig)
    return out


def main() -> None:
    gscpi = q1.load_gscpi()
    shares = q2.load_shares()
    backlog = q3.monthly_backlog(q3.load_bts())
    rate = load_freight_rate()
    rate_lagged = rate.copy()
    rate_lagged.index = rate_lagged.index + pd.DateOffset(months=LAG_MONTHS)

    corr = lag_correlations(rate, gscpi, shares["Panama-dependent"])
    corr.to_csv(OUT_DIR / "lag_correlations.csv", index=False)
    print(corr.to_string(index=False))
    print(f"\nWrote {build_chart(gscpi, shares, rate_lagged, backlog, corr).relative_to(ROOT)}")


if __name__ == "__main__":
    main()
