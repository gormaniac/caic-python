"""Mappings of abbreviations to definitions/long-names.

See more on the `CAIC website`_

.. _CAIC website: https://avalanche.state.co.us/forecasts/help/observation-avalanche
"""

AVALANCHE_TYPES = {
    "L": "Loose",
    "WL": "Wet Loose",
    "SS": "Soft Slab",
    "HS": "Hard Slab",
    "WS": "Wet Slab",
    "G": "Glide",
    "I": "Ice Fall",
    "SF": "Slush Flow",
    "C": "Cornice Fall",
    "R": "Roof",
    "U": "Unknown",
}
"""The codes for types of avalanches mapped to their descriptive names."""

PRIMARY_TRIGGER_DESC = {
    "N": 'Natural',
    "AS": 'Skier',
    "AR": 'Snowboarder',
    "AI": 'Snowshoer',
    "AF": 'Foot penetration',
    "AC": 'Cornice fall triggered by explosive action',
    "AM": 'Snowmobile',
    "AK": 'Snowcat',
    "AV": 'Vehicle (Specified in comments)',
    "AA": 'Artillery',
    "AE": 'An explosive thrown or placed on or under the snow surface by hand',
    "AL": 'Avalauncher',
    "AB": 'An explosive detonated above the surface (air blast)',
    "AX": 'Gas exploder',
    "AH": 'Explosive placed via helicopter',
    "AP": 'Pre-placed, remotely detonated explosive charge',
    "AW": 'Wildlife',
    "AU": 'Unknown artificial trigger',
    "AO": 'Unclassified artificial trigger (Specified in comments)',
    "UKN": 'Unknown',
    "A": 'Unknown',
}
"""The codes for types of primary avalanche triggers mapped to their descriptive names."""

SECONDARY_TRIGGER_DESC = {
    'u': 'An unintentional release',
    'c': 'A controlled or intentional release',
    'r': 'A remote avalanche released by the indicated trigger',
    'y': 'An avalanche released in sympathy with another avalanche'
}
"""The codes for types of secondary avalanche triggers mapped to their descriptive names."""

ELEV_DESC = {
    '>TL': 'Above Treeline',
    'TL': 'Near Treeline',
    '<TL': 'Below treeline',
}
"""The codes for elevation bands mapped to their descriptive names.

The API returns the ``<`` and ``>`` URL encoded - so this object isn't useful
for comparing to API responses.
"""

ASPECT_DESC = {
    "All": 'All aspects',
    "ALL": 'All aspects',
    "N": 'North',
    "NE": 'Northeast',
    "E": 'East',
    "SE": 'Southeast',
    "S": 'South',
    "SW": 'Southwest',
    "W": 'West',
    "NW": 'Northwest',
    "U": 'Unknown',
    "UNK": 'Unknown',
}
"""The codes for types of avalanche triggers mapped to their descriptive names."""

R_SIZE_DESC = {
    "R1": 'Very small, relative to the path',
    "R2": 'Small, relative to the path',
    "R3": 'Medium, relative to the path',
    "R4": 'Large, relative to the path',
    "R5": 'Major or maximum, relative to path',
    "U": 'Unknown',
    "UNK": 'Unknown'
}
"""The codes for avalanche R size mapped to their descriptive names."""

D_SIZE_DESC = {
    'D1': 'Relatively harmless to people',
    'D1.5': 'Relatively harmless to people ',
    'D2': 'Could bury, injure, or kill a person',
    'D2.5': 'Could bury, injure, or kill a person',
    'D3': (
        'Could bury and destroy a car, damage a truck, '
        'destroy a wood frame house, or break a few trees'
    ),
    'D3.5': (
        'Could bury and destroy a car, damage a truck, '
        'destroy a wood frame house, or break a few trees'
    ),
    'D4': (
        'Could destroy a railway car, large truck, several '
        'buildings, or a substantial amount of trees'
    ),
    'D4.5': (
        'Could destroy a railway car, large truck, several '
        'buildings, or a substantial amount of trees'
    ),
    'D5': 'Could gouge the landscape, largest snow avalanche known',
    'U': 'Unknown',
    'UNK': 'Unknown'
}
"""The codes for avalanche D size mapped to their descriptive names."""
