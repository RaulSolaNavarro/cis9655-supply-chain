"""Validate the Census imports-by-port endpoint (intltrade/imports/porths).

Pulls one month of US imports from China by port (all commodities) and checks
it against the country-level HS endpoint. Census defines the import "port" as
the port of UNLADING (where the ship/plane is unloaded), which is not
necessarily where the goods clear customs.

Usage:  python scripts/validate_census_porths.py [YYYY-MM] [CTY_CODE]
        defaults: 2026-01, 5700 (China)
Output: data/raw/census_porths_<cty>_<month>.csv
"""
import os
import sys
from pathlib import Path

import pandas as pd
import requests
import truststore
from dotenv import load_dotenv

truststore.inject_into_ssl()  # trust the OS certificate store, not just certifi

BASE = "https://api.census.gov/data/timeseries/intltrade/imports"
ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
VALUES = ["GEN_VAL_MO", "VES_VAL_MO", "CNT_VAL_MO", "CNT_WGT_MO", "AIR_VAL_MO"]


def get(endpoint: str, params: dict, key: str) -> pd.DataFrame:
    resp = requests.get(f"{BASE}/{endpoint}", params={**params, "key": key},
                        timeout=300, allow_redirects=False)
    if resp.status_code == 204:
        sys.exit(f"HTTP 204: no data for {params.get('time')} (month not released yet?)")
    if resp.status_code != 200 or "json" not in resp.headers.get("content-type", ""):
        sys.exit(f"HTTP {resp.status_code}: {resp.text[:300]}")
    rows = resp.json()
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df = df.loc[:, ~df.columns.duplicated()]  # predicates are echoed back
    for c in VALUES:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c])
    return df


if __name__ == "__main__":
    month = sys.argv[1] if len(sys.argv) > 1 else "2026-01"
    cty = sys.argv[2] if len(sys.argv) > 2 else "5700"
    load_dotenv(ROOT / ".env")
    key = os.getenv("CENSUS_API_KEY", "").strip() or sys.exit("CENSUS_API_KEY is not set (see README).")
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    # I_COMMODITY=- gives one all-commodities row per port (fast, ~10s).
    # COMM_LVL=HS2 per port works but took 60-130s for a single month.
    ports = get("porths", {"get": "PORT,PORT_NAME,CTY_NAME,COMM_LVL,SUMMARY_LVL," + ",".join(VALUES),
                           "time": month, "CTY_CODE": cty, "I_COMMODITY": "-"}, key)
    ports.to_csv(RAW_DIR / f"census_porths_{cty}_{month}.csv", index=False)
    country = get("hs", {"get": ",".join(VALUES[:3]), "time": month, "CTY_CODE": cty, "I_COMMODITY": "-"}, key)

    total = ports[ports["PORT"] == "-"]
    detail = ports[ports["PORT"] != "-"]
    print(f"=== imports/porths, CTY_CODE={cty}, {month} ===")
    print(f"Rows: {len(ports)} ({len(detail)} ports + {len(total)} 'TOTAL FOR ALL PORTS' row)")
    print(f"Columns: {list(ports.columns)}")
    print(f"COMM_LVL: {ports['COMM_LVL'].unique().tolist()}  SUMMARY_LVL: {ports['SUMMARY_LVL'].unique().tolist()}")

    print("\nReconciliation (USD):")
    for c in VALUES[:3]:
        print(f"  {c}: country-level HS = {country[c].iloc[0]:,}  porths total row = {total[c].iloc[0]:,}  "
              f"sum of ports = {detail[c].sum():,}")
    print("  -> the total row is included in every query; exclude PORT == '-' before summing ports")

    print(f"\nNull cells: {ports.isna().sum()[lambda s: s > 0].to_dict() or 'none'}"
          f"  (ports with no name: {detail.loc[detail['PORT_NAME'].isna(), 'PORT'].tolist()})")
    print(f"Ports listed with zero value: {(detail['GEN_VAL_MO'] == 0).sum()}")
    pseudo = detail[detail["PORT"].str.startswith("7")]
    print(f"Non-geographic pseudo-ports: {pseudo[['PORT', 'PORT_NAME', 'GEN_VAL_MO']].values.tolist()}")
    top_ves = detail.nlargest(12, "VES_VAL_MO")
    print(f"Top 12 ports by vessel value = {top_ves['VES_VAL_MO'].sum() / detail['VES_VAL_MO'].sum():.1%} of vessel imports:")
    print(top_ves[["PORT", "PORT_NAME", "GEN_VAL_MO", "VES_VAL_MO", "CNT_VAL_MO", "CNT_WGT_MO"]]
          .to_string(index=False))
