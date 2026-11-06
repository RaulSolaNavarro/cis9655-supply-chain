"""Approximate locations for the 9 BTS ports, plus reference points for route maps.

Coordinates are (lat, lon) in decimal degrees at each port's main container
terminals, good to a few kilometers. They're for maps, not distance analysis.
Two-city ports (Sea-Tac, NY-NJ) use a point between or at the main terminals.

Usage:
    from port_locations import PORT_LOCATIONS
    lat, lon = PORT_LOCATIONS["Savannah"]
"""

# Keys match the BTS `port_or_region` names used in data/processed/.
PORT_LOCATIONS = {
    "Los Angeles": (33.74, -118.27),   # San Pedro Bay terminals
    "Long Beach": (33.75, -118.19),
    "Oakland": (37.80, -122.32),
    "Sea-Tac": (47.42, -122.38),       # midpoint of Seattle (47.58) and Tacoma (47.27)
    "NY-NJ": (40.68, -74.15),          # Port Newark-Elizabeth
    "Savannah": (32.12, -81.14),       # Garden City terminal
    "Port of VA": (36.92, -76.33),     # Norfolk International Terminals
    "Charleston": (32.80, -79.93),
    "Houston": (29.68, -95.01),        # Barbours Cut / Bayport
}

# Reference points for the China-to-US route schematic.
SHANGHAI = (30.63, 122.06)             # Yangshan deep-water port
PANAMA_CANAL_PACIFIC = (8.90, -79.55)  # Balboa entrance
PANAMA_CANAL_ATLANTIC = (9.38, -79.92) # Colón entrance
