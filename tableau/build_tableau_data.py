"""Build Tableau-ready CSVs in tableau/data/ from the Q1-Q3 loaders.

Every number comes from the same loader functions the matplotlib charts use,
so the Tableau views match q1-q4. Disruption windows are precomputed per row so
Tableau needs no calculated fields:

  disruption_window  window name, "" if none. The Panama and Red Sea windows
                     overlap (Nov 2023 - May 2024); those months get both
                     names joined with " + ".
  in_<window>        1/0 flag per window, for filtering on one window exactly.
  window_band        1 inside any window, blank outside. Drawn as max-width
                     bars on a hidden second axis, it shades the windows.

Colors (hex), copied from the q1-q4 build scripts and asserted below:
  Pacific-direct / LA-LB lines     #2a78d6   (q2 COLORS, q3 LANE_COLORS / BACKLOG_COLORS)
  Panama-dependent / Savannah      #eb6834   (q2 COLORS, q3 LANE_COLORS / BACKLOG_COLORS)
  All Other Ports (backlog)        #8a8984   (q3 BACKLOG_COLORS)
  GSCPI line                       #2a78d6   (q1 SERIES)
  Disruption-window bands          #d9d8d3 at 45% opacity, all windows (q1-q4 BAND)
  Text / reference lines           #0b0b0b primary, #52514e secondary
  Background                       #fcfcfb

Writes:
  tableau/data/gscpi_tableau.csv
  tableau/data/lane_share_tableau.csv
  tableau/data/port_map_tableau.csv
  tableau/data/port_series_tableau.csv

Usage:  python tableau/build_tableau_data.py
"""
import importlib.util
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = Path(__file__).resolve().parent / "data"
sys.path.insert(0, str(ROOT / "scripts"))
from port_locations import PORT_LOCATIONS  # noqa: E402


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


q1 = _load("build_gscpi_chart", "q1-pressure/build_gscpi_chart.py")
q2 = _load("build_lane_share_chart", "q2-trade-volume/build_lane_share_chart.py")
q3 = _load("build_port_charts", "q3-ports/build_port_charts.py")
WINDOWS = q1.WINDOWS

COLORS = {
    "Pacific-direct": "#2a78d6",
    "Panama-dependent": "#eb6834",
    "All Other Ports": "#8a8984",
    "GSCPI": "#2a78d6",
    "Window band": "#d9d8d3",
}
# Fail loudly if a build script's palette drifts from what Tableau is told to use.
assert q2.COLORS == {k: COLORS[k] for k in q2.COLORS}
assert q3.LANE_COLORS == q2.COLORS
assert q3.BACKLOG_COLORS["All Other Ports"] == COLORS["All Other Ports"]
assert q1.SERIES == COLORS["GSCPI"] and q1.BAND == COLORS["Window band"]

# Backlog groups map onto lane groups for coloring; "All Other Ports" has none.
BACKLOG_LANE = {"LA-LB": "Pacific-direct", "Savannah": "Panama-dependent",
                "All Other Ports": "All Other Ports"}
# Same slump metric as q3-ports/build_port_map.py.
NO_DIP_SIZE = 1


def flag_name(window: str) -> str:
    """'Panama Canal drought' -> 'in_panama'."""
    return "in_" + window.split()[0].lower()


def window_columns(dates: pd.Series) -> pd.DataFrame:
    """Per-row window label, per-window 1/0 flags, and the band helper."""
    out = pd.DataFrame(index=dates.index)
    names = []
    for name, start, end in WINDOWS:
        inside = dates >= pd.Timestamp(start)
        if end:
            inside &= dates <= pd.Timestamp(end)
        out[flag_name(name)] = inside.astype(int)
        names.append((name, inside))
    out["disruption_window"] = [
        " + ".join(name for name, inside in names if inside.loc[i])
        for i in dates.index
    ]
    in_any = out[[flag_name(n) for n, *_ in WINDOWS]].sum(axis=1) > 0
    out["window_band"] = pd.array([1 if x else None for x in in_any], dtype="Int64")
    return out


def with_windows(df: pd.DataFrame) -> pd.DataFrame:
    df = df.reset_index(drop=True)
    df = pd.concat([df, window_columns(df["date"])], axis=1)
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    return df


def gscpi_table() -> pd.DataFrame:
    s = q1.load_gscpi()
    df = pd.DataFrame({"date": s.index, "gscpi_value": s.values.round(4)})
    return with_windows(df)


def lane_share_table() -> pd.DataFrame:
    shares = q2.load_shares()
    smooth = shares.rolling(q2.SMOOTH_MONTHS).mean()
    df = pd.DataFrame({
        "date": shares.index,
        "panama_dependent_share_pct": shares["Panama-dependent"].round(2).values,
        "pacific_direct_share_pct": shares["Pacific-direct"].round(2).values,
        "panama_dependent_share_3mo_pct": smooth["Panama-dependent"].round(2).values,
        "pacific_direct_share_3mo_pct": smooth["Pacific-direct"].round(2).values,
    })
    return with_windows(df)


def port_map_table(bts: pd.DataFrame, lanes: dict[str, str]) -> pd.DataFrame:
    index = q3.throughput_index(bts)
    stats = q3.throughput_stats(index, lanes)
    backlog = q3.backlog_stats(q3.monthly_backlog(bts)).set_index("group")
    rows = []
    for _, r in stats.iterrows():
        lat, lon = PORT_LOCATIONS[r["port"]]
        slump = max(0.0, 100 - r["trough_index"])
        rows.append({
            "port": r["port"],
            "lat": lat,
            "lon": lon,
            "lane_group": r["lane_group"],
            "trough_index": r["trough_index"],
            "trough_month": r["trough_month"],
            "slump_points": slump,
            # Tableau can't size a mark at 0, so no-dip ports get a small fixed size
            # and an open-circle shape via `dipped`.
            "map_marker_size": slump if slump > 0 else NO_DIP_SIZE,
            "dipped": "Yes" if slump > 0 else "No",
            "months_to_recover": r["months_to_recover"],
            "latest_index": r["latest_index"],
            "latest_month": r["latest_month"],
            # The only berth backlogs BTS publishes near the port level.
            "lalb_backlog_peak_ships": (backlog.loc["LA-LB", "peak_ships"]
                                        if r["port"] in ("Los Angeles", "Long Beach")
                                        else None),
            "lalb_backlog_peak_month": (backlog.loc["LA-LB", "peak_month"]
                                        if r["port"] in ("Los Angeles", "Long Beach")
                                        else None),
            "savannah_backlog_peak_ships": (backlog.loc["Savannah", "peak_ships"]
                                            if r["port"] == "Savannah" else None),
            "savannah_backlog_peak_month": (backlog.loc["Savannah", "peak_month"]
                                            if r["port"] == "Savannah" else None),
        })
    return pd.DataFrame(rows)


def port_series_table(bts: pd.DataFrame, lanes: dict[str, str]) -> pd.DataFrame:
    backlog = q3.monthly_backlog(bts)
    index = q3.throughput_index(bts)
    parts = []
    for frame, metric, units, lane_of in [
        (backlog, "Ships awaiting a berth", "ships (monthly mean)", BACKLOG_LANE),
        (index, "Loaded imports index", f"{q3.SMOOTH_MONTHS}-month avg, 2019 = 100",
         lanes),
    ]:
        long = frame.rename_axis("date").reset_index().melt(
            id_vars="date", var_name="port_or_group", value_name="value")
        long["metric_name"] = metric
        long["metric_units"] = units
        long["lane_group"] = long["port_or_group"].map(lane_of)
        parts.append(long)
    df = pd.concat(parts, ignore_index=True)
    # Keep missing months (e.g. no Oct 2025 backlog) as blank values, not dropped rows.
    df["value"] = df["value"].round(2)
    df = df.sort_values(["metric_name", "port_or_group", "date"])
    cols = ["date", "port_or_group", "lane_group", "metric_name", "metric_units", "value"]
    return with_windows(df[cols])


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    bts = q3.load_bts()
    lanes = q3.load_lane_groups()
    missing = set(q3.PORT_ORDER) - set(PORT_LOCATIONS)
    if missing:
        raise SystemExit(f"No location for: {sorted(missing)}")
    tables = {
        "gscpi_tableau.csv": gscpi_table(),
        "lane_share_tableau.csv": lane_share_table(),
        "port_map_tableau.csv": port_map_table(bts, lanes),
        "port_series_tableau.csv": port_series_table(bts, lanes),
    }
    for name, df in tables.items():
        df.to_csv(OUT_DIR / name, index=False)
        print(f"Wrote tableau/data/{name}: {len(df)} rows, {len(df.columns)} columns")


if __name__ == "__main__":
    main()
