"""Q4: freight rate six months earlier vs. East and Gulf share, one dot per month.

Uses the same series and lag as build_synthesis_chart.py (Shanghai-LA spot rate
at month t-6, Panama-dependent share of China containerized imports at month t),
so the r values match q4-synthesis/lag_correlations.csv. The months split at
Jan 2023 to show that the overall r = 0.48 comes from the 2021-22 episode.

Writes q4-synthesis/rate_vs_share_scatter.png.

Usage:  python q4-synthesis/build_rate_scatter.py
"""
import importlib.util
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = Path(__file__).resolve().parent


def _load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# The synthesis script already loads Q1-Q3 and defines the rate, lag, and split.
syn = _load("build_synthesis_chart", "q4-synthesis/build_synthesis_chart.py")
q2 = syn.q2
LAG_MONTHS = syn.LAG_MONTHS
SPLIT = syn.SPLIT

SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
RULE = "#e4e3df"
# Neutral grays only: blue and orange mean lane group everywhere else.
DARK = "#3d3c39"
LIGHT = "#8a8984"


def paired_months() -> pd.DataFrame:
    rate = syn.load_freight_rate()
    shifted = rate.copy()
    shifted.index = shifted.index + pd.DateOffset(months=LAG_MONTHS)
    share = q2.load_shares()["Panama-dependent"]
    pair = pd.concat([shifted, share], axis=1, join="inner").dropna()
    pair.columns = ["rate_6m_earlier", "panama_share"]
    return pair


def stored_r() -> pd.Series:
    corr = pd.read_csv(OUT_DIR / "lag_correlations.csv")
    return corr[(corr["driver"] == "freight_rate") &
                (corr["lag_months"] == LAG_MONTHS)].iloc[0]


def build_chart(pair: pd.DataFrame, stored: pd.Series) -> Path:
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 15,
        "text.color": TEXT_PRIMARY, "axes.labelcolor": TEXT_SECONDARY,
        "xtick.color": TEXT_SECONDARY, "ytick.color": TEXT_SECONDARY,
    })
    fig, ax = plt.subplots(figsize=(16, 9))
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)

    groups = [
        ("Through 2022", pair[pair.index < SPLIT], stored["r_through_2022"],
         dict(color=DARK, edgecolor=DARK), DARK),
        ("2023 onward", pair[pair.index >= SPLIT], stored["r_2023_on"],
         dict(facecolor="none", edgecolor=LIGHT, linewidths=2), LIGHT),
    ]
    for name, g, r, style, line_color in groups:
        x = g["rate_6m_earlier"] / 1000
        y = g["panama_share"]
        ax.scatter(x, y, s=110, zorder=3, **style)
        slope, intercept = np.polyfit(x, y, 1)
        xs = np.array([x.min(), x.max()])
        ax.plot(xs, slope * xs + intercept, color=line_color, lw=2.5, zorder=2)
        # Label at the right end of each fitted line; the 2023 label sits
        # just below its line end, clear of the dots.
        early_group = name == "Through 2022"
        ax.annotate(f"{name} (n = {len(g)})\nr = {r:.2f}",
                    (xs[1], slope * xs[1] + intercept),
                    xytext=(12, 0 if early_group else -48),
                    textcoords="offset points", ha="left", va="center",
                    fontsize=16, fontweight="bold",
                    color=DARK if early_group else TEXT_SECONDARY)

    ax.set_xlabel("Shanghai to Los Angeles spot rate six months earlier "
                  "($ thousand per 40-ft box)", fontsize=16, labelpad=12)
    ax.set_ylabel("East and Gulf share of China\ncontainerized imports (%)",
                  fontsize=16, labelpad=12)
    ax.tick_params(length=0, labelsize=15)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(RULE)
    xmax = pair["rate_6m_earlier"].max() / 1000
    ax.set_xlim(0, xmax * 1.28)
    ax.set_ylim(pair["panama_share"].min() - 3, pair["panama_share"].max() + 2)

    fig.text(0.075, 0.025, "Each dot is one month. Correlation is not tested "
             "for significance.", fontsize=14, color=TEXT_SECONDARY)
    fig.subplots_adjust(left=0.12, right=0.97, top=0.96, bottom=0.17)

    out = OUT_DIR / "rate_vs_share_scatter.png"
    fig.savefig(out, dpi=200, facecolor=SURFACE)
    plt.close(fig)
    return out


def main() -> None:
    pair = paired_months()
    stored = stored_r()
    early, late = pair[pair.index < SPLIT], pair[pair.index >= SPLIT]
    checks = [
        ("all months", pair, stored["r"], stored["n"]),
        ("through 2022", early, stored["r_through_2022"], stored["n_through_2022"]),
        ("2023 onward", late, stored["r_2023_on"], stored["n_2023_on"]),
    ]
    for label, g, r_csv, n_csv in checks:
        r = g.iloc[:, 0].corr(g.iloc[:, 1])
        print(f"{label:13s} n={len(g):3d}  r={r:.3f}  (csv: n={int(n_csv)}, r={r_csv:.3f})")
        assert len(g) == int(n_csv), f"{label}: n {len(g)} != {n_csv}"
        assert round(r, 2) == round(r_csv, 2), f"{label}: r {r:.3f} != {r_csv}"
    print(f"\nWrote {build_chart(pair, stored).relative_to(ROOT)}")


if __name__ == "__main__":
    main()
