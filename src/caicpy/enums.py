"""Shared enums for typing/validation.

The CAIC API can return multiple values when the particular code is not known.
It is up to callers to normalize these values. They can be any of the following::

    U
    Un
    Unknown
    Unkn
    UNKNOWN
    UNK
    ---
    --

"""

from enum import Enum


class TypeCode(Enum):
    """Avalanche type codes."""

    L: str = "L"
    WL: str = "WL"
    SS: str = "SS"
    HS: str = "HS"
    WS: str = "WS"
    G: str = "G"
    I: str = "I"
    SF: str = "SF"
    C: str = "C"
    R: str = "R"
    U: str = "U"
    Un: str = "Un"
    Unknown: str = "Unknown"
    Unkn: str = "Unkn"
    UNKNOWN: str = "UNKNOWN"
    UNK: str = "UNK"
    DASHES3: str = "---"
    DASHES2: str = "--"

class PrimaryTrigger(Enum):
    """Avalanche primary trigger codes."""

    N: str = "N"
    AN: str = "AN"
    AS: str = "AS"
    AR: str = "AR"
    AI: str = "AI"
    AF: str = "AF"
    AC: str = "AC"
    AM: str = "AM"
    AK: str = "AK"
    AV: str = "AV"
    AA: str = "AA"
    AE: str = "AE"
    AL: str = "AL"
    AB: str = "AB"
    AX: str = "AX"
    AH: str = "AH"
    AP: str = "AP"
    AW: str = "AW"
    AU: str = "AU"
    AO: str = "AO"
    UKN: str = "UKN"
    A: str = "A"
    U: str = "U"
    Un: str = "Un"
    Unknown: str = "Unknown"
    Unkn: str = "Unkn"
    UNKNOWN: str = "UNKNOWN"
    DASHES3: str = "---"
    DASHES2: str = "--"

class SecondaryTrigger(Enum):
    """Avalanche secondary trigger codes."""

    u: str = "u"
    c: str = "c"
    r: str = "r"
    y: str = "y"
    U: str = "U"
    Un: str = "Un"
    Unknown: str = "Unknown"
    Unkn: str = "Unkn"
    UNKNOWN: str = "UNKNOWN"
    UNK: str = "UNK"
    DASHES3: str = "---"
    DASHES2: str = "--"


class Aspect(Enum):
    """Slope aspect values."""

    All: str = "All"
    ALL: str = "ALL"
    N: str = "N"
    NE: str = "NE"
    E: str = "E"
    SE: str = "SE"
    S: str = "S"
    SW: str = "SW"
    W: str = "W"
    NW: str = "NW"
    U: str = "U"
    UNK: str = "UNK"
    Un: str = "Un"
    Unknown: str = "Unknown"
    Unkn: str = "Unkn"
    UNKNOWN: str = "UNKNOWN"
    DASHES3: str = "---"
    DASHES2: str = "--"

class RSize(Enum):
    """Avalanche relative size values."""

    R1: str = "R1"
    R2: str = "R2"
    R3: str = "R3"
    R4: str = "R4"
    R5: str = "R5"
    U: str = "U"
    UNK: str = "UNK"
    Un: str = "Un"
    Unknown: str = "Unknown"
    Unkn: str = "Unkn"
    UNKNOWN: str = "UNKNOWN"
    DASHES3: str = "---"
    DASHES2: str = "--"


class DSize(Enum):
    """Avalanche desctructive size values.

    Because these can have half values, ``P`` is a substitute for decimals.
    """

    D1: str = 'D1'
    D1P5: str = 'D1.5'
    D2: str = 'D2'
    D2P5: str = 'D2.5'
    D3: str = 'D3'
    D3P5: str = 'D3.5'
    D4: str = 'D4'
    D4P5: str = 'D4.5'
    D5: str = 'D5'
    U: str = 'U'
    UNK: str = 'UNK'
    Un: str = "Un"
    Unknown: str = "Unknown"
    Unkn: str = "Unkn"
    UNKNOWN: str = "UNKNOWN"
    DASHES3: str = "---"
    DASHES2: str = "--"

class ObsTypes(Enum):
    """The types that CAIC observation objects can have."""

    AVY_OBS: str = "avalanche_observation"
    REPORT_OBS: str = "report_observation"
    SNOWPACK_OBS: str = "snowpack_observation"
    IMAGE_ASSET: str = "image_asset"
    WEATHER_OBS: str = "weather_observation"
    BC_ZONE: str = "backcountry_zone"
    HWY_ZONE: str = "highway_zone"
    OBS_REPORT: str = "observation_report"
    VIDEO_ASSET: str = "video_asset"
    SNOWPIT_ASSET: str = "snowpit_asset"

class BCZoneTitles(Enum):
    """Titles for backcountry zones."""

    ASPEN = "Aspen"
    FRONT_RANGE = "Front Range"
    GRAND_MESA = "Grand Mesa"
    GUNNINSON = "Gunnison"
    N_SAN_JAUN = "Northern San Juan"
    S_SAN_JAUN = "Southern San Juan"
    SANGRE = "Sangre de Cristo"
    SAWATCH = "Sawatch"
    STEAMBOAT = "Steamboat & Flat Tops"
    VAIL_SUMMIT = "Vail & Summit County"

class ReportsSearchCrackObs(Enum):
    """Cracking observation options in a Field Reports search."""

    NONE = "None"
    MINOR = "Minor"
    MODERATE = "Moderate"
    SHOOTING = "Shooting"
    UNKNOWN = "Unknown"

class ReportsSearchCollapseObs(Enum):
    """Collapsing observation options in a Field Reports search."""

    NONE = "None"
    MINOR = "Minor"
    MODERATE = "Moderate"
    RUMBLING = "Rumbling"
    UNKNOWN = "Unknown"

class ReportsSearchAvyObs(Enum):
    """Avalanche observation options in a Field Reports search."""

    SAW = "Saw"
    CAUGHT = "Caught"
    TRIGGERED = "Triggered"

class DetailsTypes(Enum):
    """The types of details objects from Field Reports."""

    AVY = "avalanche_detail"
    SNOW = "snowpack_detail"
    WEATHER = "weather_detail"
