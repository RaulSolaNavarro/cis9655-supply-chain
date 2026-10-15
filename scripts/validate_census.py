"""Validate the Census international trade API (exports + imports, HS endpoints).

Needs a free key in CENSUS_API_KEY (environment variable or .env file at the
repo root). Get one at https://api.census.gov/data/key_signup.html; the key is
emailed to you and must be activated from the link in that email.

Runs three small queries and prints what comes back:
  1. The example call from the project brief (exports, Apr 2013, YTD fields)
  2. Monthly imports from China (Asia / Red Sea-linked lane), by HS2 chapter
  3. Monthly exports to Mexico (Latin America lane), by HS2 chapter

Usage:  python scripts/validate_census.py
Output: data/raw/census_sample_*.csv
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

BASE = "https://api.census.gov/data/timeseries/intltrade"
ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"

FIRST_YEAR = 2013  # HS-level timeseries starts Jan 2013

# Census country codes: 5700 = China, 2010 = Mexico.
# Queries without a "time"/"YEAR" param are monthly series pulled one year per
# request: a single 2013-to-present request takes 80-120s+ and can time out.
QUERIES = {
    "brief_example": ("exports/hs", {
        # Brief's YTD fields plus their monthly (_MO) counterparts and the HS level
        "get": "E_COMMODITY,E_COMMODITY_LDESC,COMM_LVL,ALL_VAL_YR,VES_VAL_YR,AIR_VAL_YR,CC_YR,"
               "ALL_VAL_MO,VES_VAL_MO,AIR_VAL_MO,CC_MO",
        "YEAR": "2013", "MONTH": "04",
    }),
    "imports_china_hs2": ("imports/hs", {
        "get": "CTY_CODE,CTY_NAME,I_COMMODITY,GEN_VAL_MO,VES_VAL_MO,CNT_VAL_MO,AIR_VAL_MO,VES_WGT_MO",
        "CTY_CODE": "5700", "COMM_LVL": "HS2",
    }),
    "exports_mexico_hs2": ("exports/hs", {
        "get": "CTY_CODE,CTY_NAME,E_COMMODITY,ALL_VAL_MO,VES_VAL_MO,CNT_VAL_MO,AIR_VAL_MO,VES_WGT_MO",
        "CTY_CODE": "2010", "COMM_LVL": "HS2",
    }),
}


def get_key() -> str:
    load_dotenv(ROOT / ".env")
    key = os.getenv("CENSUS_API_KEY", "").strip()
    if not key:
        sys.exit("CENSUS_API_KEY is not set. Copy .env.example to .env and add your key "
                 "(sign up: https://api.census.gov/data/key_signup.html).")
    return key


def fetch(endpoint: str, params: dict, key: str) -> pd.DataFrame:
    try:
        resp = requests.get(f"{BASE}/{endpoint}", params={**params, "key": key},
                            timeout=120, allow_redirects=False)
    except requests.RequestException as e:
        raise RuntimeError(f"Request failed: {e}") from e
    # Bad or missing keys come back as a redirect or an HTML page, not JSON
    if resp.status_code in (301, 302) or "html" in resp.headers.get("content-type", ""):
        raise RuntimeError(f"Key rejected (HTTP {resp.status_code}, {resp.headers.get('Location', 'HTML body')}). "
                           "Check that the key was activated from the confirmation email.")
    if resp.status_code == 204:
        raise RuntimeError("HTTP 204: query is valid but returned no data")
    if resp.status_code != 200:
        raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:300]}")
    rows = resp.json()
    df = pd.DataFrame(rows[1:], columns=rows[0])
    # Predicate fields (e.g. CTY_CODE) are echoed back even if already in "get"
    return df.loc[:, ~df.columns.duplicated()]


def fetch_by_year(endpoint: str, params: dict, key: str) -> pd.DataFrame:
    frames = []
    for year in range(FIRST_YEAR, date.today().year + 1):
        try:
            frames.append(fetch(endpoint, {**params, "time": str(year)}, key))
        except RuntimeError as e:
            print(f"  {endpoint} {year}: FAILED: {e}")
    if not frames:
        raise RuntimeError("no year returned data")
    return pd.concat(frames, ignore_index=True)


def summarize(name: str, df: pd.DataFrame) -> None:
    print(f"\n=== {name} ===")
    print(f"Rows: {len(df):,}  Columns: {list(df.columns)}")
    # The API returns every value as a string; values are US dollars, weights are kg
    num_cols = [c for c in df.columns if c.endswith(("_VAL_MO", "_VAL_YR", "_WGT_MO", "CC_YR"))]
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    if "time" in df.columns:
        months = sorted(df["time"].unique())
        expected = pd.period_range(months[0], months[-1], freq="M").strftime("%Y-%m")
        gaps = sorted(set(expected) - set(months))
        print(f"Months: {months[0]} -> {months[-1]} ({len(months)} distinct, missing: {gaps or 'none'})")
        monthly = df.groupby("time")[num_cols].sum()
        print("Last 6 months, all HS2 chapters summed (USD; *_WGT_MO in kg):")
        print(monthly.tail(6).to_string(float_format=lambda v: f"{v:,.0f}"))
    nulls = df.isna().sum()
    print(f"Nulls per column: {nulls[nulls > 0].to_dict() or 'none'}")
    print(f"Zero values per numeric column: {(df[num_cols] == 0).sum().to_dict()}")
    print(df.head(3).to_string(index=False))


if __name__ == "__main__":
    key = get_key()
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for name, (endpoint, params) in QUERIES.items():
        print(f"Fetching {name} ...")
        try:
            if "time" in params or "YEAR" in params:
                df = fetch(endpoint, params, key)
            else:
                df = fetch_by_year(endpoint, params, key)
        except RuntimeError as e:
            print(f"\n=== {name} === FAILED: {e}")
            continue
        df.to_csv(RAW_DIR / f"census_sample_{name}.csv", index=False)
        summarize(name, df)
