"""Validate the NY Fed Global Supply Chain Pressure Index (GSCPI) download.

Downloads the published workbook, parses the monthly series, and prints a
summary: date range, units, gaps, and the largest values.

Usage:  python scripts/validate_gscpi.py
Output: data/raw/gscpi_data.xls (snapshot of the file as downloaded)
"""
from datetime import date
from pathlib import Path

import pandas as pd
import requests
import truststore

truststore.inject_into_ssl()  # trust the OS certificate store, not just certifi

URL = "https://www.newyorkfed.org/medialibrary/research/interactives/gscpi/downloads/gscpi_data.xlsx"
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def download() -> Path:
    resp = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
    resp.raise_for_status()
    # The file is served with an .xlsx name but is actually legacy Excel 97-2003
    # (OLE2 signature D0 CF 11 E0), so it needs the xlrd engine, not openpyxl.
    is_xls = resp.content[:4] == b"\xd0\xcf\x11\xe0"
    path = RAW_DIR / ("gscpi_data.xls" if is_xls else "gscpi_data.xlsx")
    path.write_bytes(resp.content)
    print(f"Downloaded {len(resp.content):,} bytes, content-type={resp.headers.get('content-type')}")
    print(f"Real file format: {'legacy .xls (OLE2)' if is_xls else '.xlsx (zip)'} -> saved to {path}")
    return path


def parse(path: Path) -> pd.DataFrame:
    engine = "xlrd" if path.suffix == ".xls" else "openpyxl"
    sheets = pd.ExcelFile(path, engine=engine).sheet_names
    print(f"Sheets: {sheets}")
    # Data sheet has a "Date | GSCPI" header row followed by a few banner rows
    # (NY Fed logo/URL in column D), so keep only rows where both columns parse.
    raw = pd.read_excel(path, sheet_name="GSCPI Monthly Data", usecols=[0, 1], engine=engine)
    print(f"Raw columns: {list(raw.columns)}")
    df = pd.DataFrame({
        "date": pd.to_datetime(raw.iloc[:, 0], format="%d-%b-%Y", errors="coerce"),
        "gscpi": pd.to_numeric(raw.iloc[:, 1], errors="coerce"),
    })
    dropped = df[df["date"].isna() | df["gscpi"].isna()]
    print(f"Non-data rows dropped (banner/blank): {len(dropped)}")
    return df.dropna().reset_index(drop=True)


def summarize(df: pd.DataFrame) -> None:
    print("\n--- GSCPI summary ---")
    print(f"Rows: {len(df)}  |  {df['date'].min():%Y-%m} -> {df['date'].max():%Y-%m}")
    print("Units: standard deviations from the series' historical average (0 = average pressure)")
    print("Dates are month-end; one global value per month (no region breakdown)")

    expected = pd.date_range(df["date"].min(), df["date"].max(), freq="ME")
    missing = expected.difference(df["date"])
    print(f"Missing months: {len(missing)}" + (f" -> {[d.strftime('%Y-%m') for d in missing]}" if len(missing) else ""))
    print(f"Duplicate dates: {df['date'].duplicated().sum()}")
    print(f"Min {df['gscpi'].min():.2f} ({df.loc[df['gscpi'].idxmin(), 'date']:%Y-%m}), "
          f"max {df['gscpi'].max():.2f} ({df.loc[df['gscpi'].idxmax(), 'date']:%Y-%m})")

    print("\nTop 5 months:")
    print(df.nlargest(5, "gscpi").to_string(index=False))
    print("\nLast 12 months:")
    print(df.tail(12).to_string(index=False))
    print(f"\nNote: NY Fed revises past values each release; this snapshot was taken {date.today()}.")


if __name__ == "__main__":
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    summarize(parse(download()))
