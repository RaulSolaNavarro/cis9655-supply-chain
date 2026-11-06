"""Generate tableau/supply_chain_resilience.twbx from the CSVs in tableau/data/.

CONFIRMED BROKEN, NOT JUST UNTESTED. Tableau Desktop refuses to load the output
(error D2E8DA72: schema errors on the reference-line elements and the
storyboard window element). Don't use the output or try to repair it; build
from tableau/BUILD_GUIDE.md. This script is kept only as a record of the
attempt. The .twb XML was written from memory of the Tableau 2018.1+ format,
not checked against Tableau's schema. validate() checks only what can be
checked offline (well-formed XML, every field a sheet uses is declared in its
datasource, every sheet the dashboard/action/story names exists, packaged CSV
paths resolve) and passes despite the schema errors.

Colors (hex), the same as tableau/build_tableau_data.py and the q1-q4 scripts:
  Pacific-direct / LA-LB / GSCPI   #2a78d6
  Panama-dependent / Savannah      #eb6834
  All Other Ports                  #8a8984
  Disruption-window bands          #d9d8d3 at 45% opacity
  Reference lines                  #52514e

Usage:  python tableau/build_tableau_data.py && python tableau/build_twbx.py
"""
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import quoteattr

import pandas as pd

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data"
OUT = HERE / "supply_chain_resilience.twbx"
TWB_NAME = "supply_chain_resilience.twb"
# Where the CSVs sit inside the .twbx, relative to the .twb.
PACKAGED_DIR = "Data/tableau"

BLUE, ORANGE, GRAY, BAND, REF = "#2a78d6", "#eb6834", "#8a8984", "#d9d8d3", "#52514e"
LANE_PALETTE = {"Pacific-direct": BLUE, "Panama-dependent": ORANGE,
                "All Other Ports": GRAY}
# Tableau mark transparency is 0-255; 45% opacity ~ 115.
BAND_ALPHA = "115"

DASHBOARD = "Supply chain overview"
STORY = "Disruption story"
SOURCES = {
    "gscpi": "gscpi_tableau.csv",
    "lane": "lane_share_tableau.csv",
    "map": "port_map_tableau.csv",
    "ports": "port_series_tableau.csv",
}
GEO_ROLES = {"lat": "[Geographical].[Latitude]", "lon": "[Geographical].[Longitude]"}


def a(value) -> str:
    """Attribute value, XML-quoted."""
    return quoteattr(str(value))


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def ds_name(key: str) -> str:
    return f"federated.{key}"


# ---------------------------------------------------------------- datasources

def column_types(path: Path) -> list[tuple[str, str]]:
    """(column, tableau datatype) for each CSV column."""
    df = pd.read_csv(path, keep_default_na=False, na_values=[""])
    out = []
    for col in df.columns:
        s = df[col]
        if col == "date":
            out.append((col, "date"))
        elif pd.api.types.is_integer_dtype(s) or (
                pd.api.types.is_float_dtype(s) and s.dropna().mod(1).eq(0).all()
                and col.startswith(("in_", "window_band"))):
            out.append((col, "integer"))
        elif pd.api.types.is_numeric_dtype(s):
            out.append((col, "real"))
        else:
            out.append((col, "string"))
    return out


REMOTE_TYPE = {"date": 133, "integer": 20, "real": 5, "string": 129}


def datasource_xml(key: str, filename: str) -> str:
    cols = column_types(DATA_DIR / filename)
    table = filename.replace(".", "#")
    rel_cols = "".join(
        f"<column datatype={a(t)} name={a(c)} ordinal={a(i)} />"
        for i, (c, t) in enumerate(cols))
    meta = "".join(
        f"<metadata-record class='column'><remote-name>{esc(c)}</remote-name>"
        f"<remote-type>{REMOTE_TYPE[t]}</remote-type><local-name>[{esc(c)}]</local-name>"
        f"<parent-name>[{esc(filename)}]</parent-name><remote-alias>{esc(c)}</remote-alias>"
        f"<ordinal>{i}</ordinal><local-type>{t}</local-type>"
        f"<aggregation>{'Sum' if t in ('real', 'integer') else 'Count'}</aggregation>"
        f"<contains-null>true</contains-null></metadata-record>"
        for i, (c, t) in enumerate(cols))
    fields = []
    for c, t in cols:
        measure = t in ("real", "integer")
        role = "measure" if measure else "dimension"
        kind = "quantitative" if measure else "nominal"
        extra = f" semantic-role={a(GEO_ROLES[c])}" if c in GEO_ROLES else ""
        fields.append(f"<column datatype={a(t)} name={a(f'[{c}]')} role={a(role)} "
                      f"type={a(kind)}{extra} />")
    # Lane colors travel with the datasource, so every sheet that colors by
    # lane_group gets the same hex values.
    style = ""
    if any(c == "lane_group" for c, _ in cols):
        maps = "".join(f"<map to={a(hexv)}><bucket>&quot;{esc(v)}&quot;</bucket></map>"
                       for v, hexv in LANE_PALETTE.items())
        style = (f"<style><style-rule element='mark'><encoding attr='color' "
                 f"field='[lane_group]' type='palette'>{maps}</encoding>"
                 f"</style-rule></style>")
    caption = filename.removesuffix(".csv")
    return (
        f"<datasource caption={a(caption)} inline='true' name={a(ds_name(key))} version='18.1'>"
        f"<connection class='federated'><named-connections>"
        f"<named-connection caption={a(caption)} name={a(f'textscan.{key}')}>"
        f"<connection class='textscan' directory={a(PACKAGED_DIR)} filename={a(filename)} "
        f"password='' server='' /></named-connection></named-connections>"
        f"<relation connection={a(f'textscan.{key}')} name={a(filename)} "
        f"table={a(f'[{table}]')} type='table'>"
        f"<columns character-set='UTF-8' header='yes' locale='en_US' separator=','>"
        f"{rel_cols}</columns></relation>"
        f"<metadata-records>{meta}</metadata-records></connection>"
        f"{''.join(fields)}{style}</datasource>"
    )


# ----------------------------------------------------------------- worksheets

DERIVATIONS = {"sum": "Sum", "max": "Max", "avg": "Avg", "none": "None",
               "tmn": "Month-Trunc"}


def inst(key: str, agg: str, field: str, kind: str) -> str:
    """Fully qualified column-instance reference, e.g. [federated.gscpi].[sum:x:qk]."""
    return f"[{ds_name(key)}].[{agg}:{field}:{kind}]"


def dependencies(key: str, refs: list[str], cols: dict[str, str]) -> str:
    """datasource-dependencies block declaring every column-instance used."""
    seen, base, insts = set(), [], []
    for ref in refs:
        m = re.fullmatch(rf"\[{re.escape(ds_name(key))}\]\.\[(\w+):(\w+):(\w+)\]", ref)
        if not m:
            continue
        agg, field, kind = m.groups()
        if field not in seen:
            seen.add(field)
            t = cols[field]
            measure = t in ("real", "integer")
            extra = f" semantic-role={a(GEO_ROLES[field])}" if field in GEO_ROLES else ""
            base.append(f"<column datatype={a(t)} name={a(f'[{field}]')} "
                        f"role={a('measure' if measure else 'dimension')} "
                        f"type={a('quantitative' if measure else 'nominal')}{extra} />")
        insts.append(f"<column-instance column={a(f'[{field}]')} "
                     f"derivation={a(DERIVATIONS[agg])} name={a(f'[{agg}:{field}:{kind}]')} "
                     f"pivot='key' type={a('quantitative' if kind == 'qk' else 'nominal')} />")
    return (f"<datasource-dependencies datasource={a(ds_name(key))}>"
            f"{''.join(base)}{''.join(dict.fromkeys(insts))}</datasource-dependencies>")


def pane(idx, mark, axis=None, encodings="", style="") -> str:
    attrs = f" id={a(idx)}" if idx is not None else ""
    if axis:
        attrs += f" y-axis-name={a(axis)}"
    enc = f"<encodings>{encodings}</encodings>" if encodings else ""
    return (f"<pane{attrs} selection-relaxation-option='selection-relaxation-allow'>"
            f"<view><breakdown value='auto' /></view><mark class={a(mark)} />"
            f"{enc}{style}</pane>")


def band_style() -> str:
    return (f"<style><style-rule element='mark'><format attr='mark-color' value={a(BAND)} />"
            f"<format attr='mark-transparency' value={a(BAND_ALPHA)} />"
            f"<format attr='size' value='1' /></style-rule></style>")


def line_style(color=None) -> str:
    color_rule = f"<format attr='mark-color' value={a(color)} />" if color else ""
    return f"<style><style-rule element='mark'>{color_rule}</style-rule></style>"


def hide_axis(ref: str) -> str:
    """Hide the band's axis and fix it at 0-1 so bars fill the pane height."""
    return (f"<style-rule element='axis'>"
            f"<encoding attr='space' class='0' field={a(ref)} field-type='quantitative' "
            f"max='1' min='0' range-type='fixed' scope='rows' type='space' />"
            f"<format attr='display' class='0' field={a(ref)} scope='rows' value='false' />"
            f"</style-rule>")


def ref_lines(ref: str, values: list[float]) -> str:
    return "".join(
        f"<reference-line axis-column={a(ref)} enable-instant-analytics='true' "
        f"formula='constant' id={a(f'refline{i}')} label-type='none' scope='per-table' "
        f"value={a(v)} value-column={a(ref)} z-order='1' />"
        for i, v in enumerate(values))


def worksheet(name, key, cols, rows_expr, cols_expr, panes, refs, filters="",
              table_style="", title="") -> str:
    deps = dependencies(key, refs, cols)
    title_xml = (f"<layout-options><title><formatted-text><run>{esc(title)}</run>"
                 f"</formatted-text></title></layout-options>") if title else ""
    return (
        f"<worksheet name={a(name)}>{title_xml}<table><view>"
        f"<datasources><datasource caption={a(SOURCES[key].removesuffix('.csv'))} "
        f"name={a(ds_name(key))} /></datasources>{deps}{filters}"
        f"<aggregation value='true' /></view>"
        f"<style>{table_style}</style>"
        f"<panes>{''.join(panes)}</panes>"
        f"<rows>{esc(rows_expr)}</rows><cols>{esc(cols_expr)}</cols></table></worksheet>"
    )


def build_worksheets(all_cols: dict[str, dict[str, str]]) -> tuple[str, list[str]]:
    sheets, names = [], []

    # 1. GSCPI line with window bands on a hidden second axis.
    k = "gscpi"
    date, val = inst(k, "tmn", "date", "qk"), inst(k, "sum", "gscpi_value", "qk")
    band, win = inst(k, "max", "window_band", "qk"), inst(k, "none", "disruption_window", "nk")
    detail = f"<lod column={a(win)} />"
    sheets.append(worksheet(
        "GSCPI", k, all_cols[k], f"({val} + {band})", date,
        [pane(None, "Automatic", encodings=detail),
         pane(1, "Line", val, detail, line_style(BLUE)),
         pane(2, "Bar", band, detail, band_style())],
        [date, val, band, win],
        table_style=hide_axis(band) + ref_lines(val, [0, 1]),
        title="Supply chain pressure (GSCPI), std. dev. from long-run average"))
    names.append("GSCPI")

    # 2. Lane share: two lines (3-month average) plus bands.
    k = "lane"
    date = inst(k, "tmn", "date", "qk")
    pac = inst(k, "sum", "pacific_direct_share_3mo_pct", "qk")
    pan = inst(k, "sum", "panama_dependent_share_3mo_pct", "qk")
    band, win = inst(k, "max", "window_band", "qk"), inst(k, "none", "disruption_window", "nk")
    detail = f"<lod column={a(win)} />"
    # Two share lines share one axis (synchronized dual axis), bands on a third pane.
    sheets.append(worksheet(
        "Lane share", k, all_cols[k], f"({pac} + {pan} + {band})", date,
        [pane(None, "Automatic", encodings=detail),
         pane(1, "Line", pac, detail, line_style(BLUE)),
         pane(2, "Line", pan, detail, line_style(ORANGE)),
         pane(3, "Bar", band, detail, band_style())],
        [date, pac, pan, band, win],
        table_style=hide_axis(band) + (
            f"<style-rule element='axis'><encoding attr='space' class='0' field={a(pan)} "
            f"field-type='quantitative' fold='true' scope='rows' synchronized='true' "
            f"type='space' /></style-rule>"),
        title="China containerized imports: share by lane group (%), 3-month average"))
    names.append("Lane share")

    # 3. Port symbol map from lat/lon columns (no geocoding).
    k = "map"
    lon, lat = inst(k, "avg", "lon", "qk"), inst(k, "avg", "lat", "qk")
    port, lane = inst(k, "none", "port", "nk"), inst(k, "none", "lane_group", "nk")
    size, dipped = inst(k, "sum", "map_marker_size", "qk"), inst(k, "none", "dipped", "nk")
    trough = inst(k, "sum", "trough_index", "qk")
    enc = (f"<color column={a(lane)} /><size column={a(size)} /><shape column={a(dipped)} />"
           f"<lod column={a(port)} /><text column={a(port)} /><text column={a(trough)} />")
    sheets.append(worksheet(
        "Port map", k, all_cols[k], lat, lon,
        [pane(None, "Shape", encodings=enc)],
        [lon, lat, port, lane, size, dipped, trough],
        title="2022-23 import slump by port (size = points below 2019; proxy, see guide)"))
    names.append("Port map")

    # 4. Port backlog / throughput, one metric at a time via a filter.
    k = "ports"
    date, val = inst(k, "tmn", "date", "qk"), inst(k, "sum", "value", "qk")
    band, win = inst(k, "max", "window_band", "qk"), inst(k, "none", "disruption_window", "nk")
    who, lane = inst(k, "none", "port_or_group", "nk"), inst(k, "none", "lane_group", "nk")
    metric = inst(k, "none", "metric_name", "nk")
    enc = f"<color column={a(lane)} /><lod column={a(who)} /><lod column={a(win)} />"
    metric_filter = (
        f"<filter class='categorical' column={a(metric)}>"
        f"<groupfilter function='member' level={a(f'[none:metric_name:nk]')} "
        f"member='&quot;Loaded imports index&quot;' user:ui-domain='database' "
        f"user:ui-enumeration='inclusive' user:ui-marker='enumerate' /></filter>")
    sheets.append(worksheet(
        "Port series", k, all_cols[k], f"({val} + {band})", date,
        [pane(None, "Automatic", encodings=enc),
         pane(1, "Line", val, enc, line_style()),
         pane(2, "Bar", band, f"<lod column={a(win)} />", band_style())],
        [date, val, band, win, who, lane, metric],
        filters=metric_filter, table_style=hide_axis(band),
        title="Ports: berth backlog or loaded-import index (pick a metric)"))
    names.append("Port series")
    return "".join(sheets), names


# ------------------------------------------------- dashboard, action, story

def zone(zid, name, x, y, w, h, kind=None, extra="") -> str:
    attrs = f" name={a(name)}" if name else ""
    attrs += f" type={a(kind)}" if kind else ""
    return (f"<zone h={a(h)} id={a(zid)}{attrs} w={a(w)} x={a(x)} y={a(y)}{extra}>"
            f"<zone-style><format attr='border-style' value='none' />"
            f"<format attr='margin' value='4' /></zone-style></zone>")


def dashboard_xml() -> str:
    # Tableau zone coordinates run 0-100000 across the dashboard.
    zones = "".join([
        zone(3, "GSCPI", 0, 0, 62000, 33000),
        zone(4, "Lane share", 0, 33000, 62000, 33000),
        zone(5, "Port series", 0, 66000, 62000, 34000),
        zone(6, "Port map", 62000, 0, 38000, 80000),
        zone(7, "Port series", 62000, 80000, 38000, 20000, kind="filter",
             extra=f" param={a(inst('ports', 'none', 'metric_name', 'nk'))} mode='radiolist'"),
    ])
    return (
        f"<dashboard name={a(DASHBOARD)}><style />"
        f"<size maxheight='720' maxwidth='1280' minheight='720' minwidth='1280' />"
        f"<zones><zone h='100000' id='1' type='layout-basic' w='100000' x='0' y='0'>"
        f"{zones}</zone></zones></dashboard>"
    )


def action_xml() -> str:
    # Click a band (or line point) in GSCPI -> filter the time-series sheets to
    # that disruption_window. Different datasources, same field name.
    return (
        f"<actions><action caption='Filter by disruption window' "
        f"name='[Action_disruption_window]'>"
        f"<activation auto-clear='true' type='on-select' />"
        f"<source dashboard={a(DASHBOARD)} type='sheet' worksheet='GSCPI' />"
        f"<command command='tsc:tsl-filter'>"
        f"<param name='exclude' value='Port map' />"
        f"<param name='field-captions' value='disruption_window' />"
        f"<param name='target' value={a(DASHBOARD)} />"
        f"</command></action></actions>"
    )


STORY_POINTS = [
    "Four disruptions on one timeline",
    "West Coast congestion: cargo shifted east",
    "Panama drought and Red Sea: small westward drift",
    "2026: pressure up, ports clear",
]


def story_xml() -> str:
    points = "".join(f"<story-point captured-sheet={a(DASHBOARD)} id={a(i + 1)} />"
                     for i in range(len(STORY_POINTS)))
    captions = "".join(
        f"<zone h='10000' id={a(100 + i)} type='text' w='25000' x={a(i * 25000)} y='0'>"
        f"<formatted-text><run>{esc(c)}</run></formatted-text></zone>"
        for i, c in enumerate(STORY_POINTS))
    return (
        f"<dashboard name={a(STORY)} type='storyboard'><style />"
        f"<size maxheight='964' maxwidth='1280' minheight='964' minwidth='1280' />"
        f"<zones><zone h='100000' id='1' type='layout-basic' w='100000' x='0' y='0'>"
        f"<zone h='10000' id='2' type='flipboard-nav' w='100000' x='0' y='0'>{captions}</zone>"
        f"<zone h='90000' id='3' type='flipboard' w='100000' x='0' y='10000'>"
        f"<flipboard active-id='1' nav-type='caption' show-nav-arrows='true'>"
        f"<story-points>{points}</story-points></flipboard></zone>"
        f"</zone></zones></dashboard>"
    )


def windows_xml(sheet_names: list[str]) -> str:
    cards = ("<cards><edge name='left'><strip size='160'><card type='pages' />"
             "<card type='filters' /><card type='marks' /></strip></edge></cards>")
    sheets = "".join(f"<window class='worksheet' name={a(n)}>{cards}</window>"
                     for n in sheet_names)
    views = "".join(f"<viewpoint name={a(n)} />" for n in sheet_names)
    return (f"<windows source-height='30'>{sheets}"
            f"<window class='dashboard' name={a(DASHBOARD)}><viewpoints>{views}"
            f"</viewpoints></window>"
            f"<window class='storyboard' maximized='true' name={a(STORY)} />"
            f"</windows>")


def palette_xml() -> str:
    colors = "".join(f"<color>{c}</color>" for c in (BLUE, ORANGE, GRAY, BAND, REF))
    return (f"<preferences><color-palette custom='true' name='Supply chain resilience' "
            f"type='regular'>{colors}</color-palette></preferences>")


def build_twb() -> tuple[str, list[str]]:
    all_cols = {k: dict(column_types(DATA_DIR / f)) for k, f in SOURCES.items()}
    datasources = "".join(datasource_xml(k, f) for k, f in SOURCES.items())
    sheets, names = build_worksheets(all_cols)
    twb = (
        "<?xml version='1.0' encoding='utf-8' ?>\n"
        "<workbook original-version='18.1' source-build='2020.2.0 (20202.20.0525.1210)' "
        "source-platform='win' version='18.1' "
        "xmlns:user='http://www.tableausoftware.com/xml/user'>"
        f"{palette_xml()}<datasources>{datasources}</datasources>"
        "<mapsources><mapsource name='Tableau' /></mapsources>"
        f"{action_xml()}<worksheets>{sheets}</worksheets>"
        f"<dashboards>{dashboard_xml()}{story_xml()}</dashboards>"
        f"{windows_xml(names)}</workbook>"
    )
    return twb, names


# ----------------------------------------------------------------- validation

def validate(twb: str, sheet_names: list[str], packaged: set[str]) -> list[str]:
    """Offline consistency checks. Returns a list of problems (empty = passed)."""
    problems = []
    root = ET.fromstring(twb.encode("utf-8"))
    ns_user = "{http://www.tableausoftware.com/xml/user}"
    assert ns_user  # namespace declared on the root; ET would fail to parse otherwise

    declared = {ds.get("name"): {c.get("name") for c in ds.findall("column")}
                for ds in root.find("datasources")}
    for ds in root.find("datasources"):
        conn = ds.find(".//connection[@class='textscan']")
        path = f"{conn.get('directory')}/{conn.get('filename')}"
        if path not in packaged:
            problems.append(f"{ds.get('name')}: {path} not in package")

    for ws in root.find("worksheets"):
        deps = ws.find(".//datasource-dependencies")
        key = deps.get("datasource")
        if key not in declared:
            problems.append(f"{ws.get('name')}: unknown datasource {key}")
            continue
        instances = {f"[{key}].{ci.get('name')}" for ci in deps.findall("column-instance")}
        for col in deps.findall("column"):
            if col.get("name") not in declared[key]:
                problems.append(f"{ws.get('name')}: {col.get('name')} not in {key}")
        text = " ".join(filter(None, [ws.findtext(".//rows"), ws.findtext(".//cols")]))
        used = set(re.findall(r"\[federated\.\w+\]\.\[[^\]]+\]", text))
        for el in ws.iter():
            for attr in ("column", "y-axis-name"):
                v = el.get(attr)
                if v and v.startswith("[federated."):
                    used.add(v)
        for ref in used - instances:
            problems.append(f"{ws.get('name')}: {ref} used but not declared")

    for z in root.iter("zone"):
        name = z.get("name")
        if name and name not in sheet_names:
            problems.append(f"dashboard zone names unknown sheet {name!r}")
    src = root.find(".//action/source")
    if src.get("worksheet") not in sheet_names:
        problems.append(f"action source {src.get('worksheet')!r} missing")
    dashboards = {d.get("name") for d in root.find("dashboards")}
    for sp in root.iter("story-point"):
        if sp.get("captured-sheet") not in dashboards:
            problems.append(f"story point captures unknown {sp.get('captured-sheet')!r}")
    window_names = {w.get("name") for w in root.find("windows")}
    for n in sheet_names + [DASHBOARD, STORY]:
        if n not in window_names:
            problems.append(f"no window for {n!r}")
    return problems


def main() -> None:
    twb, names = build_twb()
    packaged = {f"{PACKAGED_DIR}/{f}" for f in SOURCES.values()}
    problems = validate(twb, names, packaged)
    if problems:
        raise SystemExit("Validation failed:\n  " + "\n  ".join(problems))
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(TWB_NAME, twb)
        for f in SOURCES.values():
            z.write(DATA_DIR / f, f"{PACKAGED_DIR}/{f}")
    (HERE / TWB_NAME).write_text(twb, encoding="utf-8")
    print(f"Offline checks passed. Wrote {OUT.name} ({OUT.stat().st_size:,} bytes) "
          f"and {TWB_NAME} for review.")


if __name__ == "__main__":
    main()
