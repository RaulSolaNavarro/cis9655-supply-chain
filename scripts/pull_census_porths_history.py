"""Pull monthly Census imports by port (all commodities) for one country.

Pulls one calendar year per request (multi-year requests are slow and can time
out), writes the untouched raw pull, then a cleaned snapshot with the port
lane grouping used in the project.

Usage:  python scripts/pull_census_porths_history.py [CTY_CODE] [START_YEAR]
        defaults: 5700 (China), 2019
Output: data/raw/census_porths_<cty>_<start>_<end>.csv           (raw, all rows)
        data/processed/census_porths_<cty>_lanes_<pull date>.csv (cleaned snapshot)
"""
import os
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import requests
import truststore
from dotenv import load_dotenv

truststore.inject_into_ssl()  # trust the OS certificate store, not just certifi

URL = "https://api.census.gov/data/timeseries/intltrade/imports/porths"
ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
OUT_DIR = ROOT / "data" / "processed"
VALUES = ["GEN_VAL_MO", "VES_VAL_MO", "CNT_VAL_MO", "CNT_WGT_MO", "AIR_VAL_MO"]

# Census port code -> BTS port name, for the 9 ports the BTS TEU data covers
BTS_PORTS = {
    "1001": "NY-NJ", "1003": "NY-NJ",
    "1703": "Savannah",
    "1401": "Port of VA",
    "1601": "Charleston",
    "5301": "Houston",
    "2704": "Los Angeles",
    "2709": "Long Beach",
    "2811": "Oakland",
    "3001": "Sea-Tac", "3002": "Sea-Tac",
}
# Asia cargo to East/Gulf ports transits Panama (or Suez); West Coast ports are reached directly
LANES = {
    "NY-NJ": "Panama-dependent", "Savannah": "Panama-dependent", "Port of VA": "Panama-dependent",
    "Charleston": "Panama-dependent", "Houston": "Panama-dependent",
    "Los Angeles": "Pacific-direct", "Long Beach": "Pacific-direct",
    "Oakland": "Pacific-direct", "Sea-Tac": "Pacific-direct",
}
TOTAL_PORT = "-"         # "TOTAL FOR ALL PORTS" row, returned in every response
LOW_VALUE_PORT = "7070"  # pseudo-port for low-value shipments, not a location


def fetch_year(year: int, cty: str, key: str) -> pd.DataFrame:
    params = {"get": "PORT,PORT_NAME,CTY_NAME," + ",".join(VALUES),
              "time": str(year), "CTY_CODE": cty, "I_COMMODITY": "-", "key": key}
    resp = requests.get(URL, params=params, timeout=300, allow_redirects=False)
    if resp.status_code == 204:
        return pd.DataFrame()
    if resp.status_code != 200 or "json" not in resp.headers.get("content-type", ""):
        raise RuntimeError(f"{year}: HTTP {resp.status_code}: {resp.text[:300]}")
    rows = resp.json()
    df = pd.DataFrame(rows[1:], columns=rows[0])
    return df.loc[:, ~df.columns.duplicated()]  # predicates are echoed back


if __name__ == "__main__":
    cty = sys.argv[1] if len(sys.argv) > 1 else "5700"
    start = int(sys.argv[2]) if len(sys.argv) > 2 else 2019
    load_dotenv(ROOT / ".env")
    key = os.getenv("CENSUS_API_KEY", "").strip() or sys.exit("CENSUS_API_KEY is not set (see README).")
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    frames = []
    for year in range(start, date.today().year + 1):
        df = fetch_year(year, cty, key)
        print(f"{year}: {len(df):,} rows, months {sorted(df['time'].unique()) if len(df) else 'none'}")
        frames.append(df)
    raw = pd.concat(frames, ignore_index=True)
    for c in VALUES:
        raw[c] = pd.to_numeric(raw[c])
    first, last = raw["time"].min(), raw["time"].max()
    raw_path = RAW_DIR / f"census_porths_{cty}_{first}_{last}.csv"
    # Raw keeps everything, including the all-ports total row and 7070 LOW VALUE
    raw.to_csv(raw_path, index=False)
    print(f"Raw: {raw_path.relative_to(ROOT)} ({len(raw):,} rows)")

    months = pd.period_range(first, last, freq="M").strftime("%Y-%m")
    missing = sorted(set(months) - set(raw["time"]))
    print(f"Months {first} -> {last}, missing: {missing or 'none'}")

    # Check the total row still reconciles before dropping it
    totals = raw[raw["PORT"] == TOTAL_PORT].set_index("time")[VALUES]
    port_sums = raw[raw["PORT"] != TOTAL_PORT].groupby("time")[VALUES].sum()
    print(f"Months where ports don't sum to the total row: {int((totals != port_sums).any(axis=1).sum())}")

    clean = raw[~raw["PORT"].isin([TOTAL_PORT, LOW_VALUE_PORT])].copy()
    clean["bts_port"] = clean["PORT"].map(BTS_PORTS)
    clean["lane_group"] = clean["bts_port"].map(LANES).fillna("Other")
    clean = clean.rename(columns={
        "time": "month", "PORT": "port_code", "PORT_NAME": "port_name", "CTY_NAME": "country_name",
        "GEN_VAL_MO": "total_value_usd", "VES_VAL_MO": "vessel_value_usd",
        "CNT_VAL_MO": "containerized_value_usd", "CNT_WGT_MO": "containerized_weight_kg",
        "AIR_VAL_MO": "air_value_usd",
    })
    cols = ["month", "port_code", "port_name", "bts_port", "lane_group", "country_name",
            "total_value_usd", "vessel_value_usd", "containerized_value_usd",
            "containerized_weight_kg", "air_value_usd"]
    clean = clean[cols].sort_values(["month", "port_code"])
    out = OUT_DIR / f"census_porths_{cty}_lanes_{date.today():%Y-%m-%d}.csv"
    clean.to_csv(out, index=False)
    print(f"Snapshot: {out.relative_to(ROOT)} ({len(clean):,} rows)")

    # Port codes/names should be stable over time for the mapped ports
    mapped = clean[clean["bts_port"].notna()]
    names = mapped.groupby("port_code")["port_name"].unique()
    print("Mapped port names over time:", {k: list(v) for k, v in names.items()})
    print("Months each mapped port appears:", mapped.groupby("port_code")["month"].nunique().to_dict())
