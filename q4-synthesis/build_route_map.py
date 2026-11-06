"""Q4: schematic flow map of the two China-to-US lanes.

Explanatory, not analytical: one short Pacific crossing to the West Coast ports
(Pacific-direct) versus the long route through the Panama Canal to the East and
Gulf Coast ports (Panama-dependent). Ocean legs are great-circle arcs between a
few waypoints, so paths and distances are approximate. Each route is labeled
with its weak point, which is why the two lane groups react to different kinds
of disruption.

Writes q4-synthesis/route_map.png.

Usage:  python q4-synthesis/build_route_map.py
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
from map_outlines import rings  # noqa: E402
from port_locations import (PANAMA_CANAL_ATLANTIC, PANAMA_CANAL_PACIFIC,  # noqa: E402
                            PORT_LOCATIONS, SHANGHAI)

LANE_PORTS = {
    "Pacific-direct": ["Los Angeles", "Long Beach", "Oakland", "Sea-Tac"],
    "Panama-dependent": ["NY-NJ", "Port of VA", "Charleston", "Savannah", "Houston"],
}
# Waypoints (lat, lon) that keep the drawn routes at sea. The Panama route takes
# a mid-Pacific leg so it doesn't sit on top of the Pacific-direct arc.
MID_PACIFIC = (24.0, -168.0)
OFF_CENTRAL_AMERICA = (11.0, -95.0)
YUCATAN_CHANNEL = (21.8, -85.5)
WINDWARD_PASSAGE = (20.0, -73.8)
OFF_CAROLINAS = (32.0, -76.5)

# View: Pacific-centered, longitudes shifted to 0-360.
LON_RANGE = (98, 302)
LAT_RANGE = (-6, 58)
EARTH_NMI = 3440.1

SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
LAND = "#e9e8e3"
LANE_COLORS = {"Pacific-direct": "#2a78d6", "Panama-dependent": "#eb6834"}


def to_xyz(lat, lon):
    la, lo = np.radians(lat), np.radians(lon)
    return np.array([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)])


def great_circle(a, b, n=80) -> np.ndarray:
    """Points from a to b along the great circle, as (lat, lon 0-360) rows."""
    pa, pb = to_xyz(*a), to_xyz(*b)
    omega = np.arccos(np.clip(pa @ pb, -1, 1))
    t = np.linspace(0, 1, n)[:, None]
    pts = (np.sin((1 - t) * omega) * pa + np.sin(t * omega) * pb) / np.sin(omega)
    lat = np.degrees(np.arcsin(pts[:, 2]))
    lon = np.degrees(np.arctan2(pts[:, 1], pts[:, 0])) % 360
    return np.column_stack([lat, lon])


def route(*waypoints) -> np.ndarray:
    return np.vstack([great_circle(a, b) for a, b in zip(waypoints, waypoints[1:])])


def length_nmi(path: np.ndarray) -> float:
    xyz = np.array([to_xyz(lat, lon) for lat, lon in path])
    dots = np.clip(np.einsum("ij,ij->i", xyz[:-1], xyz[1:]), -1, 1)
    return float(np.arccos(dots).sum() * EARTH_NMI)


def draw_land(ax) -> None:
    for ring in rings("ne_110m_land"):
        lon = ring[:, 0] % 360
        # Skip rings that would wrap across the view (Antarctica, antimeridian splits).
        if np.ptp(lon) > 180:
            continue
        ax.fill(lon, ring[:, 1], color=LAND, lw=0, zorder=0)


def draw_route(ax, path, color, lw=3) -> None:
    ax.plot(path[:, 1], path[:, 0], color=SURFACE, lw=lw + 3, zorder=2,
            solid_capstyle="round")
    ax.plot(path[:, 1], path[:, 0], color=color, lw=lw, zorder=3,
            solid_capstyle="round")


def build_map() -> Path:
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "text.color": TEXT_PRIMARY})
    fig, ax = plt.subplots(figsize=(12, 6.6))
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    draw_land(ax)

    ports = {p: PORT_LOCATIONS[p] for group in LANE_PORTS.values() for p in group}
    pacific = route(SHANGHAI, ports["Los Angeles"])
    to_canal = route(SHANGHAI, MID_PACIFIC, OFF_CENTRAL_AMERICA,
                     PANAMA_CANAL_PACIFIC, PANAMA_CANAL_ATLANTIC)
    to_east = route(PANAMA_CANAL_ATLANTIC, WINDWARD_PASSAGE, OFF_CAROLINAS,
                    ports["NY-NJ"])
    to_gulf = route(PANAMA_CANAL_ATLANTIC, YUCATAN_CHANNEL, ports["Houston"])
    pacific_nmi = length_nmi(pacific)
    east_nmi = length_nmi(to_canal) + length_nmi(to_east)

    blue, orange = LANE_COLORS["Pacific-direct"], LANE_COLORS["Panama-dependent"]
    for path in (to_canal, to_east, to_gulf):
        draw_route(ax, path, orange)
    draw_route(ax, pacific, blue)

    for group, names in LANE_PORTS.items():
        for name in names:
            lat, lon = ports[name]
            ax.plot(lon % 360, lat, "o", ms=7, color=LANE_COLORS[group], zorder=4,
                    markeredgecolor=SURFACE, markeredgewidth=2)
    lat, lon = SHANGHAI
    ax.plot(lon, lat, "o", ms=10, color=TEXT_PRIMARY, zorder=4,
            markeredgecolor=SURFACE, markeredgewidth=2)
    ax.annotate("China\n(Shanghai)", (lon, lat), xytext=(-10, -6),
                textcoords="offset points", ha="right", va="top", fontsize=10,
                fontweight="bold")

    # Route labels, placed along each line.
    mid = pacific[len(pacific) // 2]
    ax.annotate(f"Pacific-direct\n≈ {pacific_nmi:,.0f} nautical miles",
                (mid[1], mid[0]), xytext=(0, 12), textcoords="offset points",
                ha="center", va="bottom", fontsize=10, color=TEXT_PRIMARY,
                fontweight="bold")
    # Label the Panama route under its mid-Pacific leg (second of four legs).
    mid = to_canal[int(len(to_canal) * 0.4)]
    ax.annotate(f"Panama-dependent\n≈ {east_nmi:,.0f} nautical miles to NY-NJ",
                (mid[1], mid[0]), xytext=(0, -14), textcoords="offset points",
                ha="center", va="top", fontsize=10, color=TEXT_PRIMARY,
                fontweight="bold")

    # Weak points: why each lane group reacts to a different disruption.
    weak = dict(fontsize=9, color=TEXT_SECONDARY, va="center",
                arrowprops={"arrowstyle": "-", "color": TEXT_SECONDARY, "lw": 0.7,
                            "shrinkA": 2, "shrinkB": 6})
    lat, lon = ports["Los Angeles"]
    ax.annotate("Weak point: the West Coast ports\njammed in 2021–22",
                (lon % 360, lat), xytext=(lon % 360 - 24, lat - 5), ha="center",
                **weak)
    lat, lon = PANAMA_CANAL_PACIFIC
    ax.annotate("Weak point: the Panama Canal\ndrought limited ships in 2023–24",
                (lon % 360, lat), xytext=(lon % 360 - 24, lat - 9), ha="center",
                **weak)

    ax.set_xlim(*LON_RANGE)
    ax.set_ylim(*LAT_RANGE)
    # Equirectangular, stretched for ~30°N so shapes aren't squashed.
    ax.set_aspect(1 / np.cos(np.radians(30)))
    ax.axis("off")

    fig.suptitle("Two ways China's cargo reaches the US", x=0.03, ha="left",
                 y=0.97, fontsize=14, fontweight="bold")
    fig.text(0.03, 0.905, "Blue: straight across the Pacific to the West Coast. "
             "Orange: through the Panama Canal to the East and Gulf Coasts, about "
             f"{east_nmi / pacific_nmi:.1f}× as far.",
             fontsize=9.5, color=TEXT_SECONDARY)
    fig.text(0.03, 0.02, "Schematic: routes and distances are approximate "
             "(great-circle legs between a few waypoints). Natural Earth outlines.",
             fontsize=8, color=TEXT_SECONDARY)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.88, bottom=0.05)

    out = OUT_DIR / "route_map.png"
    fig.savefig(out, dpi=200, facecolor=SURFACE)
    plt.close(fig)
    print(f"Pacific-direct ~ {pacific_nmi:,.0f} nmi; via Panama to NY-NJ ~ "
          f"{east_nmi:,.0f} nmi")
    return out


if __name__ == "__main__":
    print(f"Wrote {build_map().relative_to(ROOT)}")
