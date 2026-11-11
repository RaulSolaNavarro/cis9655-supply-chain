"""Q3: US map of the 9 BTS ports, sized by how hard each port's imports slumped.

BTS doesn't report a berth backlog for each port (only LA-LB combined,
Savannah, and all other ports), so marker size uses a per-port proxy: how far
each port's loaded imports fell below its 2019 level at the 2022-23 low, from
port_throughput_stats.csv. The two per-port-ish backlog peaks (LA-LB, Savannah)
from port_backlog_stats.csv are added as notes.

Run build_port_charts.py first; this reads its CSVs. Writes
q3-ports/port_map.png.

Usage:  python q3-ports/build_port_map.py
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
from map_outlines import rings  # noqa: E402
from port_locations import PORT_LOCATIONS  # noqa: E402

# Area per point of slump, in pt^2 (marker area scales with the slump).
AREA_PER_POINT = 70
NO_DIP_AREA = 70

# Albers equal-area conic for the lower 48 (USGS standard parallels).
LAT1, LAT2, LAT0, LON0 = 29.5, 45.5, 37.5, -96.0
EARTH_KM = 6371.0

# LA and Long Beach are ~8 km apart; draw their markers offshore (km offsets)
# with leader lines to the true point so both stay visible.
NUDGE_KM = {"Los Angeles": (-330, 90), "Long Beach": (-110, -330)}
# Label direction per port: (x sign, y sign) from the marker edge, and alignment.
LABELS = {
    "Sea-Tac": ((-1, 0), "right"),
    "Oakland": ((-1, 0), "right"),
    "Los Angeles": ((-1, 0), "right"),
    "Long Beach": ((-1, 0), "right"),
    "NY-NJ": ((1, 0), "left"),
    "Port of VA": ((1, 0), "left"),
    "Charleston": ((1, 0.5), "left"),
    "Savannah": ((-1, 0), "right"),
    "Houston": ((0, -1), "center"),
}
LABEL_GAP_PT = 6
# Chart labels: "Sea-Tac" is the BTS data key for the Seattle-Tacoma seaport.
DISPLAY_NAMES = {"Sea-Tac": "Seattle-Tacoma"}

SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
LAND = "#e9e8e3"
LAND_CONTEXT = "#f2f1ee"
LANE_COLORS = {"Pacific-direct": "#2a78d6", "Panama-dependent": "#eb6834"}


def albers(lon, lat):
    """Project lon/lat degrees to Albers x/y in km."""
    p1, p2, p0 = np.radians([LAT1, LAT2, LAT0])
    n = (np.sin(p1) + np.sin(p2)) / 2
    c = np.cos(p1) ** 2 + 2 * n * np.sin(p1)
    rho0 = np.sqrt(c - 2 * n * np.sin(p0)) / n
    rho = np.sqrt(c - 2 * n * np.sin(np.radians(lat))) / n
    theta = n * np.radians(np.asarray(lon) - LON0)
    return EARTH_KM * rho * np.sin(theta), EARTH_KM * (rho0 - rho * np.cos(theta))


def draw_outlines(ax) -> None:
    for ring in rings("ne_110m_admin_0_countries_lakes",
                      keep=lambda p: p["ADM0_A3"] in ("CAN", "MEX")):
        ax.fill(*albers(ring[:, 0], ring[:, 1]), color=LAND_CONTEXT, lw=0, zorder=0)
    for ring in rings("ne_110m_admin_1_states_provinces_lakes",
                      keep=lambda p: p["postal"] not in ("AK", "HI")):
        ax.fill(*albers(ring[:, 0], ring[:, 1]), facecolor=LAND,
                edgecolor=SURFACE, lw=0.8, zorder=1)


def draw_legends(fig) -> None:
    """Lane colors and circle-area key, in a strip below the map."""
    lax = fig.add_axes([0.04, 0.045, 0.92, 0.09])
    lax.axis("off")
    handles = [Line2D([], [], marker="o", ls="", ms=9, color=c, label=g)
               for g, c in LANE_COLORS.items()]
    handles.append(Line2D([], [], marker="o", ls="", ms=7, markerfacecolor=SURFACE,
                          markeredgecolor=TEXT_SECONDARY, markeredgewidth=2,
                          label="No 2022–23 dip below 2019"))
    lax.legend(handles=handles, loc="center left", frameon=False, fontsize=9,
               ncols=3, bbox_to_anchor=(0, 0.5))
    lax.text(0.66, 0.5, "Points below 2019\nat the low", transform=lax.transAxes,
             ha="right", va="center", fontsize=8.5, color=TEXT_SECONDARY)
    for i, pts in enumerate([10, 20, 30]):
        x = 0.71 + i * 0.1
        lax.scatter(x, 0.5, s=pts * AREA_PER_POINT, transform=lax.transAxes,
                    facecolor="none", edgecolor=TEXT_SECONDARY, linewidth=1,
                    clip_on=False)
        lax.text(x + 0.045, 0.5, f"{pts}", transform=lax.transAxes,
                 ha="left", va="center", fontsize=8.5, color=TEXT_SECONDARY)


def build_map(stats: pd.DataFrame, backlog: pd.DataFrame) -> Path:
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "text.color": TEXT_PRIMARY})
    fig, ax = plt.subplots(figsize=(12, 8.2))
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    draw_outlines(ax)

    for _, r in stats.iterrows():
        port = r["port"]
        lat, lon = PORT_LOCATIONS[port]
        x, y = albers(lon, lat)
        color = LANE_COLORS[r["lane_group"]]
        mx, my = x, y
        if port in NUDGE_KM:
            dx, dy = NUDGE_KM[port]
            mx, my = x + dx, y + dy
            ax.plot([x, mx], [y, my], color=TEXT_SECONDARY, lw=0.8, zorder=2)
            ax.plot(x, y, "o", ms=2.5, color=TEXT_PRIMARY, zorder=3)
        slump = max(0.0, 100 - r["trough_index"])
        area = slump * AREA_PER_POINT if slump > 0 else NO_DIP_AREA
        if slump > 0:
            ax.scatter(mx, my, s=area, color=color,
                       edgecolor=SURFACE, linewidth=2, zorder=4)
        else:
            ax.scatter(mx, my, s=NO_DIP_AREA, facecolor=SURFACE, edgecolor=color,
                       linewidth=2, zorder=4)
        (sx, sy), ha = LABELS[port]
        # Start the label just outside the circle's edge (scatter s = diameter^2).
        offset = np.sqrt(area) / 2 + LABEL_GAP_PT
        value = f"{r['trough_index']:.0f}" if slump > 0 else "no dip"
        ax.annotate(f"{DISPLAY_NAMES.get(port, port)}  {value}", (mx, my),
                    xytext=(sx * offset, sy * offset),
                    textcoords="offset points", ha=ha, va="center",
                    fontsize=9, color=TEXT_PRIMARY, zorder=5)

    # Backlog notes: the only per-port berth counts BTS publishes. Anchored in
    # axes coordinates so they stay inside the frame, with leader lines.
    b = backlog.set_index("group")
    notes = [
        ("LA-LB", "LA + Long Beach combined", "Los Angeles", (0.02, 0.17), "left"),
        ("Savannah", "Savannah", "Savannah", (0.99, 0.17), "right"),
    ]
    for group, name, port, xy, ha in notes:
        r = b.loc[group]
        lat, lon = PORT_LOCATIONS[port]
        ax.annotate(f"Peak berth backlog, {name}:\n{r['peak_ships']:.0f} ships "
                    f"({pd.Timestamp(r['peak_month']):%b %Y})",
                    albers(lon, lat), xytext=xy, textcoords="axes fraction",
                    ha=ha, va="top", fontsize=8.5, color=TEXT_SECONDARY,
                    arrowprops={"arrowstyle": "-", "color": TEXT_SECONDARY,
                                "lw": 0.6, "shrinkA": 2, "shrinkB": 3})

    x0, y0 = albers(-125.5, 24.0)
    x1, y1 = albers(-66.0, 49.5)
    ax.set_xlim(x0 - 900, x1 + 500)
    ax.set_ylim(y0 - 250, y1 + 150)
    ax.set_aspect("equal")
    ax.axis("off")

    fig.suptitle("Where the 2022–23 import slump hit hardest", x=0.04, ha="left",
                 y=0.97, fontsize=14, fontweight="bold")
    fig.text(0.04, 0.905,
             "Circle area = how far each port's loaded imports fell below its 2019 "
             "level at the 2022–23 low; number = that low (2019 = 100).\n"
             "A per-port proxy: BTS reports berth backlogs only for LA + Long Beach "
             "combined, Savannah, and all other ports.",
             fontsize=9.5, color=TEXT_SECONDARY, va="top")
    fig.text(0.04, 0.012, "Sources: BTS Supply Chain and Freight Indicators; "
             "Natural Earth outlines. LA and Long Beach markers are offset from "
             "their true locations (dots) so both are visible.",
             fontsize=8, color=TEXT_SECONDARY)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.86, bottom=0.15)
    draw_legends(fig)

    out = OUT_DIR / "port_map.png"
    fig.savefig(out, dpi=200, facecolor=SURFACE)
    plt.close(fig)
    return out


def main() -> None:
    stats = pd.read_csv(OUT_DIR / "port_throughput_stats.csv")
    backlog = pd.read_csv(OUT_DIR / "port_backlog_stats.csv")
    missing = set(stats["port"]) - set(PORT_LOCATIONS)
    if missing:
        raise SystemExit(f"No location for: {sorted(missing)}")
    print(f"Wrote {build_map(stats, backlog).relative_to(ROOT)}")


if __name__ == "__main__":
    main()
