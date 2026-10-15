"""Export frozen, cleaned CSV snapshots of the validated sources to data/processed/.

Reads the raw files written by the validate_*.py scripts (run those first) and
writes one CSV per source, named with the date the raw file was pulled.

Usage:  python scripts/export_snapshots.py
"""
from datetime import datetime
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
OUT_DIR = ROOT / "data" / "processed"

# Census monthly fields -> clean names. Exports report ALL_VAL_MO and imports
# GEN_VAL_MO ("general imports"); both are total value across all modes.
CENSUS_COLUMNS = {
    "CTY_CODE": "country_code",
    "CTY_NAME": "country_name",
    "E_COMMODITY": "hs_code",
    "I_COMMODITY": "hs_code",
    "E_COMMODITY_LDESC": "hs_description",
    "COMM_LVL": "hs_level",
    "ALL_VAL_MO": "total_value_usd",
    "GEN_VAL_MO": "total_value_usd",
    "VES_VAL_MO": "vessel_value_usd",
    "CNT_VAL_MO": "containerized_value_usd",
    "AIR_VAL_MO": "air_value_usd",
    "VES_WGT_MO": "vessel_weight_kg",
    "CC_MO": "shipment_count",
}


def pull_date(path: Path) -> str:
    return datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")


def write(df: pd.DataFrame, name: str, src: Path) -> None:
    out = OUT_DIR / f"{name}_{pull_date(src)}.csv"
    df.to_csv(out, index=False)
    print(f"{out.relative_to(ROOT)}: {len(df):,} rows, columns={list(df.columns)}")


def export_gscpi() -> None:
    src = RAW_DIR / "gscpi_data.xls"
    raw = pd.read_excel(src, sheet_name="GSCPI Monthly Data", usecols=[0, 1], engine="xlrd")
    df = pd.DataFrame({
        "date": pd.to_datetime(raw.iloc[:, 0], format="%d-%b-%Y", errors="coerce"),
        "value": pd.to_numeric(raw.iloc[:, 1], errors="coerce"),
    }).dropna()
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    write(df, "gscpi", src)


def export_bts() -> None:
    src = RAW_DIR / "bts_port_indicators_sample.csv"
    raw = pd.read_csv(src)
    df = pd.DataFrame({
        "date": pd.to_datetime(raw["date"]).dt.strftime("%Y-%m-%d"),
        "indicator": raw["indicator"],
        "port_or_region": raw["measure1"],
        "value": raw["value1"],
        "units": raw["units"],
        "source": raw["source"],
    }).sort_values(["indicator", "port_or_region", "date"], na_position="first")
    write(df, "bts_port_indicators", src)


def export_census(query: str, name: str) -> None:
    src = RAW_DIR / f"census_sample_{query}.csv"
    raw = pd.read_csv(src, dtype=str)
    if "time" in raw.columns:
        month = raw["time"]
    else:
        month = raw["YEAR"] + "-" + raw["MONTH"].str.zfill(2)
    keep = [c for c in raw.columns if c in CENSUS_COLUMNS]
    df = raw[keep].rename(columns=CENSUS_COLUMNS)
    df.insert(0, "month", month)
    for c in df.columns:
        if c.endswith(("_usd", "_kg", "_count")):
            df[c] = pd.to_numeric(df[c])
    write(df.sort_values(["month", "hs_code"]), name, src)


if __name__ == "__main__":
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    export_gscpi()
    export_bts()
    export_census("brief_example", "census_exports_all_hs_2013-04")
    export_census("imports_china_hs2", "census_imports_china_hs2")
    export_census("exports_mexico_hs2", "census_exports_mexico_hs2")
