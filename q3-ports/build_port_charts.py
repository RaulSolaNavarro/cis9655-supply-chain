"""Q3: port congestion (ships awaiting berths) and throughput for the 9 BTS ports.

Reads the newest data/processed/bts_port_indicators_<date>.csv and marks the
disruption windows from q1-pressure/build_gscpi_chart.py. Writes:

  q3-ports/port_backlog.png                   ships awaiting berths, monthly mean
  q3-ports/port_throughput_small_multiples.png  loaded import TEUs, 2019 = 100
  q3-ports/port_backlog_stats.csv             backlog peak and recovery time
  q3-ports/port_throughput_stats.csv          throughput trough and recovery time

BTS only splits the berth backlog into LA-LB, Savannah, and all other ports,
and that series starts Jul 2021. Throughput covers all 9 ports from 2019.

Usage:  python q3-ports/build_port_charts.py
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

# Reuse Q1's window definitions so all charts mark the same months.
_spec = importlib.util.spec_from_file_location(
    "build_gscpi_chart", ROOT / "q1-pressure" / "build_gscpi_chart.py")
_q1 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_q1)
WINDOWS = _q1.WINDOWS

BACKLOG = "Number of Containerships Awaiting Berths at all U.S. Ports"
THROUGHPUT = "Loaded Import Containers at Select U.S. Ports in TEUs"
BACKLOG_GROUPS = ["LA-LB", "Savannah", "All Other Ports"]
BASELINE = "2019"
SMOOTH_MONTHS = 3
# A backlog counts as cleared once the monthly mean falls below this share of its peak.
CLEARED_FRACTION = 0.25
# Throughput troughs are searched after the congestion window's peak volumes.
TROUGH_SEARCH = ("2022-07", "2023-12")
# A recovered port whose latest index is below this is flagged as having fallen back.
RELAPSE_BELOW = 90

# Small-multiple order: Pacific-direct ports first, then Panama-dependent.
# Chart labels: "Sea-Tac" is the BTS data key for the Seattle-Tacoma seaport.
DISPLAY_NAMES = {"Sea-Tac": "Seattle-Tacoma"}
PORT_ORDER = ["Los Angeles", "Long Beach", "Oakland", "Sea-Tac",
              "NY-NJ", "Savannah", "Port of VA", "Charleston", "Houston"]

# Reference palette (light mode). Lane colors match Q2.
SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3df"
BAND = "#d9d8d3"
LANE_COLORS = {"Pacific-direct": "#2a78d6", "Panama-dependent": "#eb6834"}
BACKLOG_COLORS = {"LA-LB": LANE_COLORS["Pacific-direct"],
                  "Savannah": LANE_COLORS["Panama-dependent"],
                  "All Other Ports": "#8a8984"}


def load_bts() -> pd.DataFrame:
    path = sorted(PROCESSED_DIR.glob("bts_port_indicators_*.csv"))[-1]
    return pd.read_csv(path, parse_dates=["date"])


def load_lane_groups() -> dict[str, str]:
    """BTS port -> lane group, taken from the Q2 Census lanes table."""
    path = sorted(PROCESSED_DIR.glob("census_porths_5700_lanes_*.csv"))[-1]
    lanes = pd.read_csv(path, usecols=["bts_port", "lane_group"]).dropna()
    return lanes.drop_duplicates().set_index("bts_port")["lane_group"].to_dict()


def monthly_backlog(bts: pd.DataFrame) -> pd.DataFrame:
    weekly = bts[bts["indicator"] == BACKLOG]
    weekly = weekly[weekly["port_or_region"].isin(BACKLOG_GROUPS)]
    month = weekly["date"].dt.to_period("M")
    # Drop a trailing partial month (last weekly reading more than a week before month end).
    last_obs = weekly["date"].max()
    if (last_obs.to_period("M").end_time - last_obs).days > 7:
        weekly = weekly[month < last_obs.to_period("M")]
        month = month[month < last_obs.to_period("M")]
    out = weekly.pivot_table(index=month, columns="port_or_region",
                             values="value", aggfunc="mean")
    # Keep gaps (e.g. no Oct 2025 readings) visible as breaks in the line.
    out = out.reindex(pd.period_range(out.index[0], out.index[-1], freq="M"))
    out.index = out.index.to_timestamp()
    return out[BACKLOG_GROUPS]


def throughput_index(bts: pd.DataFrame) -> pd.DataFrame:
    rows = bts[bts["indicator"] == THROUGHPUT]
    teu = rows.pivot_table(index="date", columns="port_or_region", values="value")
    teu.index = teu.index.to_period("M").to_timestamp()
    index = teu / teu.loc[BASELINE].mean() * 100
    return index.rolling(SMOOTH_MONTHS, min_periods=2).mean()[PORT_ORDER]


def months_between(a: pd.Timestamp, b: pd.Timestamp) -> int:
    return (b.year - a.year) * 12 + b.month - a.month


def backlog_stats(backlog: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for group in BACKLOG_GROUPS:
        s = backlog[group].dropna()
        peak_month = s.idxmax()
        after = s[peak_month:]
        cleared = after[after < s.max() * CLEARED_FRACTION]
        cleared_month = cleared.index[0] if len(cleared) else None
        row = {
            "group": group,
            "peak_ships": round(s.max(), 1),
            "peak_month": peak_month.strftime("%Y-%m"),
            "cleared_month": cleared_month.strftime("%Y-%m") if cleared_month else "",
            "months_to_clear": months_between(peak_month, cleared_month) if cleared_month else None,
        }
        # Mean backlog in each window, e.g. "mean_west", "mean_panama".
        for name, start, end in WINDOWS:
            key = "mean_" + name.split()[0].lower()
            row[key] = round(s[start:end or s.index[-1]].mean(), 1)
        row["latest_ships"] = round(s.iloc[-1], 1)
        rows.append(row)
    return pd.DataFrame(rows)


def throughput_stats(index: pd.DataFrame, lanes: dict[str, str]) -> pd.DataFrame:
    rows = []
    for port in PORT_ORDER:
        s = index[port].dropna()
        search = s[TROUGH_SEARCH[0]:TROUGH_SEARCH[1]]
        trough_month = search.idxmin()
        after = s[trough_month:]
        recovered = after[after >= 100]
        below = search.min() < 100
        recovered_month = recovered.index[0] if below and len(recovered) else None
        rows.append({
            "port": port,
            "lane_group": lanes.get(port, ""),
            "congestion_window_peak": round(s["2021-01":"2022-12"].max(), 0),
            "trough_index": round(search.min(), 0),
            "trough_month": trough_month.strftime("%Y-%m"),
            "recovered_month": recovered_month.strftime("%Y-%m") if recovered_month else "",
            "months_to_recover": (months_between(trough_month, recovered_month)
                                  if recovered_month else (0 if not below else None)),
            "latest_index": round(s.iloc[-1], 0),
            "latest_month": s.index[-1].strftime("%Y-%m"),
        })
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


def shade_windows(ax, last: pd.Timestamp) -> None:
    pad = pd.Timedelta(days=15)
    for _, start, end in WINDOWS:
        lo = pd.Timestamp(start)
        hi = pd.Timestamp(end) if end else last
        ax.axvspan(lo - pad, hi + pad, color=BAND, alpha=0.45, lw=0, zorder=0)


def set_rc() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "text.color": TEXT_PRIMARY,
        "axes.labelcolor": TEXT_SECONDARY,
        "xtick.color": TEXT_SECONDARY,
        "ytick.color": TEXT_SECONDARY,
    })


def build_backlog_chart(backlog: pd.DataFrame, stats: pd.DataFrame) -> Path:
    set_rc()
    fig, (strip, ax) = plt.subplots(
        2, 1, figsize=(12, 6.4), sharex=True,
        gridspec_kw={"height_ratios": [1, 5], "hspace": 0.04},
    )
    fig.patch.set_facecolor(SURFACE)
    pad = pd.Timedelta(days=15)
    last = backlog.index[-1]

    # Same window strip as Q1/Q2: overlapping Panama and Red Sea on separate rows.
    rows = [0, 1, 0, 0]
    for (name, start, end), row in zip(WINDOWS, rows):
        lo = pd.Timestamp(start)
        hi = pd.Timestamp(end) if end else last
        strip.barh(row, (hi + pad) - (lo - pad), left=lo - pad, height=0.62,
                   color=BAND, edgecolor=SURFACE, linewidth=2)
        label = "2026 pressure" if end is None else name
        strip.text(lo, row, f" {label}", va="center", ha="left",
                   fontsize=9, color=TEXT_PRIMARY)
    strip.set_ylim(1.6, -0.6)
    strip.axis("off")
    strip.set_facecolor(SURFACE)

    style_axes(ax)
    shade_windows(ax, last)
    for group in BACKLOG_GROUPS:
        color = BACKLOG_COLORS[group]
        s = backlog[group]
        ax.plot(s.index, s.values, color=color, lw=2, zorder=3,
                solid_capstyle="round", label=group)
        r = stats.set_index("group").loc[group]
        peak = pd.Timestamp(r["peak_month"])
        ax.plot(peak, r["peak_ships"], "o", ms=6, color=color, zorder=4,
                markeredgecolor=SURFACE, markeredgewidth=2)
        label = f"{group} peak {r['peak_ships']:.0f}\n({peak:%b %Y})"
        if group == "Savannah":
            # The other two lines crowd Savannah's peak; label it in open space.
            ax.annotate(label, (peak, r["peak_ships"]),
                        xytext=(pd.Timestamp("2023-02-01"), 52),
                        ha="left", va="center", fontsize=8.5,
                        color=TEXT_PRIMARY,
                        arrowprops={"arrowstyle": "-", "color": TEXT_SECONDARY,
                                    "lw": 0.8, "shrinkA": 2, "shrinkB": 5})
        else:
            ax.annotate(label, (peak, r["peak_ships"]), xytext=(8, 4),
                        textcoords="offset points", ha="left", va="bottom",
                        fontsize=8.5, color=TEXT_PRIMARY)

    ax.legend(loc="upper right", frameon=False, fontsize=9, ncols=3)
    ax.set_ylabel("Containerships awaiting a berth (monthly mean)")
    ax.set_ylim(0, 120)
    ax.set_xticks(pd.date_range("2021-01-01", last, freq="YS"))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_xlim(pd.Timestamp("2021-01-01") - pad * 2, last + pd.Timedelta(days=60))

    fig.suptitle("Ships waiting for a berth at US container ports, "
                 f"Jul 2021 – {last:%b %Y}", x=0.07, ha="left", y=0.985,
                 fontsize=14, fontweight="bold")
    fig.text(0.07, 0.925, "BTS splits this count only into LA-LB, Savannah, and "
             "all other ports; the series starts Jul 2021. Gap = no Oct 2025 data.",
             fontsize=9.5, color=TEXT_SECONDARY)
    fig.text(0.07, 0.015, "Source: BTS Supply Chain and Freight Indicators "
             "(MARAD / Marine Exchange of SoCal).", fontsize=8,
             color=TEXT_SECONDARY)
    fig.subplots_adjust(left=0.07, right=0.97, top=0.9, bottom=0.08)

    out = OUT_DIR / "port_backlog.png"
    fig.savefig(out, dpi=200, facecolor=SURFACE)
    plt.close(fig)
    return out


def build_throughput_chart(index: pd.DataFrame, stats: pd.DataFrame) -> Path:
    set_rc()
    fig, axes = plt.subplots(3, 3, figsize=(12, 9), sharex=True, sharey=True)
    fig.patch.set_facecolor(SURFACE)
    last = index.index[-1]
    stats = stats.set_index("port")

    for ax, port in zip(axes.flat, PORT_ORDER):
        r = stats.loc[port]
        color = LANE_COLORS[r["lane_group"]]
        s = index[port]
        style_axes(ax)
        shade_windows(ax, last)
        ax.axhline(100, color=TEXT_SECONDARY, lw=0.8, ls=(0, (3, 3)), zorder=1)
        ax.plot(s.index, s.values, color=color, lw=2, zorder=3,
                solid_capstyle="round")
        ax.set_title(f"{DISPLAY_NAMES.get(port, port)}  ·  {r['lane_group']}", loc="left", fontsize=10,
                     color=TEXT_PRIMARY)
        # Selective label: the post-congestion trough and how long recovery took.
        trough = pd.Timestamp(r["trough_month"])
        if r["trough_index"] < 100:
            months = r["months_to_recover"]
            if pd.isna(months):
                note = "not yet back to 100"
            elif r["latest_index"] < RELAPSE_BELOW:
                note = f"{months:.0f} mo to 100, then fell back"
            else:
                note = f"{months:.0f} mo to 100"
            ax.plot(trough, r["trough_index"], "o", ms=6, color=color, zorder=4,
                    markeredgecolor=SURFACE, markeredgewidth=2)
            ax.annotate(f"{r['trough_index']:.0f} ({trough:%b %Y})\n{note}",
                        (trough, r["trough_index"]), xytext=(0, -8),
                        textcoords="offset points", ha="center", va="top",
                        fontsize=8, color=TEXT_PRIMARY)
        else:
            ax.text(0.98, 0.06, "no post-2022 dip below 100",
                    transform=ax.transAxes, ha="right", fontsize=8,
                    color=TEXT_PRIMARY)

    # Number the windows once, on the first panel; the subtitle is the key.
    first = axes.flat[0]
    for i, (_, start, end) in enumerate(WINDOWS, 1):
        lo = pd.Timestamp(start)
        hi = pd.Timestamp(end) if end else last
        x = lo + (hi - lo) / 2 if i != 3 else hi - pd.Timedelta(days=60)
        first.text(x, 182, str(i), ha="center", va="top", fontsize=8,
                   color=TEXT_SECONDARY)

    for ax in axes[:, 0]:
        ax.set_ylabel("2019 avg = 100")
    axes.flat[0].set_ylim(40, 185)
    axes.flat[0].set_xticks(pd.date_range("2019-01-01", last, freq="2YS"))
    axes.flat[0].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    fig.suptitle("Loaded import containers by port, Jan 2019 – "
                 f"{last:%b %Y}", x=0.06, ha="left", y=0.985,
                 fontsize=14, fontweight="bold")
    fig.text(0.06, 0.935,
             f"{SMOOTH_MONTHS}-month average TEUs, indexed to each port's 2019 "
             "average. Blue = Pacific-direct, orange = Panama-dependent.\n"
             "Shaded windows: 1 West Coast congestion, 2 Panama drought, "
             "3 Red Sea rerouting, 4 renewed 2026 pressure.",
             fontsize=9.5, color=TEXT_SECONDARY, va="top")
    fig.text(0.06, 0.012, "Source: BTS Supply Chain and Freight Indicators "
             "(TEU data published by US ports).", fontsize=8,
             color=TEXT_SECONDARY)
    fig.subplots_adjust(left=0.06, right=0.98, top=0.86, bottom=0.06,
                        hspace=0.3, wspace=0.08)

    out = OUT_DIR / "port_throughput_small_multiples.png"
    fig.savefig(out, dpi=200, facecolor=SURFACE)
    plt.close(fig)
    return out


def main() -> None:
    bts = load_bts()
    backlog = monthly_backlog(bts)
    index = throughput_index(bts)
    b_stats = backlog_stats(backlog)
    t_stats = throughput_stats(index, load_lane_groups())
    b_stats.to_csv(OUT_DIR / "port_backlog_stats.csv", index=False)
    t_stats.to_csv(OUT_DIR / "port_throughput_stats.csv", index=False)
    print(b_stats.to_string(index=False))
    print()
    print(t_stats.to_string(index=False))
    print(f"\nWrote {build_backlog_chart(backlog, b_stats).relative_to(ROOT)}")
    print(f"Wrote {build_throughput_chart(index, t_stats).relative_to(ROOT)}")


if __name__ == "__main__":
    main()
