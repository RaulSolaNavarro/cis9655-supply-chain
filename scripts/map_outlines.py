"""Read Natural Earth outlines from data/raw/natural_earth/ as plain coordinate rings.

The files are Natural Earth 1:110m GeoJSON (public domain, naturalearthdata.com),
downloaded from github.com/nvkelso/natural-earth-vector at tag v5.1.2. Reading
them with the json module keeps maps free of geo dependencies.

Usage:
    from map_outlines import rings
    for ring in rings("ne_110m_land"):
        lon, lat = ring[:, 0], ring[:, 1]
"""
import json
from pathlib import Path

import numpy as np

NE_DIR = Path(__file__).resolve().parent.parent / "data" / "raw" / "natural_earth"


def rings(name: str, keep=None) -> list[np.ndarray]:
    """Exterior rings of every polygon in `name`.geojson, as (n, 2) lon/lat arrays.

    `keep` is an optional predicate on a feature's properties dict.
    Holes are dropped; at 1:110m they're lakes too small to matter.
    """
    data = json.loads((NE_DIR / f"{name}.geojson").read_text(encoding="utf-8"))
    out = []
    for feature in data["features"]:
        if keep and not keep(feature["properties"]):
            continue
        geom = feature["geometry"]
        polygons = ([geom["coordinates"]] if geom["type"] == "Polygon"
                    else geom["coordinates"])
        for polygon in polygons:
            out.append(np.asarray(polygon[0], dtype=float))
    return out
