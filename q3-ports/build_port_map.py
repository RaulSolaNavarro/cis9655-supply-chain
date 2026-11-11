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
from matplotlib import patheffects
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
# White halo so labels stay readable where they cross state borders.
HALO = [patheffects.withStroke(linewidth=3.5, foreground="#fcfcfb")]
# Chart labels: "Sea-Tac" is the BTS data key for the Seattle-Tacoma seaport.
DISPLAY_NAMES = {"Sea-Tac": "Seattle-Tacoma"}

SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
# Land is a mid gray so the US shape and white state borders hold up on a projector.
LAND = "#d5d3cb"
LAND_CONTEXT = "#ebeae5"
OUTLINE = "#8a8984"
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
                edgecolor=SURFACE, lw=1.3, zorder=1)
    # US outline on top of the state fills, still behind the circles (zorder 4).
    for ring in rings("ne_110m_admin_0_countries_lakes",
                      keep=lambda p: p["ADM0_A3"] == "USA"):
        ax.plot(*albers(ring[:, 0], ring[:, 1]), color=OUTLINE, lw=1.4, zorder=1.5)


def draw_legends(fig) -> None:
    """Lane colors and circle-area key, in a strip below the map."""
    lax = fig.add_axes([0.03, 0.065, 0.94, 0.1])
    lax.axis("off")
    handles = [Line2D([], [], marker="o", ls="", ms=12, color=c, label=g)
               for g, c in LANE_COLORS.items()]
    handles.append(Line2D([], [], marker="o", ls="", ms=10, markerfacecolor=SURFACE,
                          markeredgecolor=TEXT_SECONDARY, markeredgewidth=2,
                          label="No dip below 2019"))
    lax.legend(handles=handles, loc="center left", frameon=False, fontsize=13,
               ncols=3, bbox_to_anchor=(0, 0.5), columnspacing=1.2, handletextpad=0.3)
    lax.text(0.735, 0.5, "Points below\n2019 at low", transform=lax.transAxes,
             ha="right", va="center", fontsize=12, color=TEXT_SECONDARY)
    # Key circles use the map's own area scale, at smaller example values.
    for i, pts in enumerate([5, 10, 20]):
        x = 0.765 + i * 0.08
        lax.scatter(x, 0.5, s=pts * AREA_PER_POINT, transform=lax.transAxes,
                    facecolor="none", edgecolor=TEXT_SECONDARY, linewidth=1,
                    clip_on=False)
        # Number just right of the circle edge (s = diameter^2 in points).
        lax.annotate(f"{pts}", (x, 0.5), xycoords=lax.transAxes,
                     xytext=(np.sqrt(pts * AREA_PER_POINT) / 2 + 5, 0),
                     textcoords="offset points",
                 ha="left", va="center", fontsize=12, color=TEXT_SECONDARY)


def build_map(stats: pd.DataFrame, backlog: pd.DataFrame) -> Path:
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "text.color": TEXT_PRIMARY})
    fig, ax = plt.subplots(figsize=(12, 7.4))
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
            ax.plot([x, mx], [y, my], color=TEXT_PRIMARY, lw=1, zorder=2)
            ax.plot(x, y, "o", ms=3.5, color=TEXT_PRIMARY, zorder=3)
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
                    fontsize=13.5, color=TEXT_PRIMARY, zorder=5, path_effects=HALO)

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
                    ha=ha, va="top", fontsize=12, color=TEXT_SECONDARY, path_effects=HALO,
                    arrowprops={"arrowstyle": "-", "color": TEXT_SECONDARY,
                                "lw": 0.9, "shrinkA": 2, "shrinkB": 3})

    x0, y0 = albers(-125.5, 24.0)
    x1, y1 = albers(-66.0, 49.5)
    ax.set_xlim(x0 - 1250, x1 + 650)
    ax.set_ylim(y0 - 330, y1 + 120)
    ax.set_aspect("equal")
    ax.axis("off")

    fig.suptitle("Where the 2022–23 import slump hit hardest", x=0.04, ha="left",
                 y=0.972, fontsize=19, fontweight="bold")
    fig.text(0.04, 0.018, "Sources: BTS Supply Chain and Freight Indicators; Natural Earth. "
             "LA and Long Beach circles are offset from their true locations (dots).",
             fontsize=10.5, color=TEXT_SECONDARY)
    fig.subplots_adjust(left=0.005, right=0.995, top=0.93, bottom=0.17)
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
