"""Shared enums for typing."""

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

class PrimaryTrigger(Enum):
    """Avalanche primary trigger codes."""

    N: str = "N"
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

class SecondaryTrigger(Enum):
    """Avalanche secondary trigger codes."""

    u: str = "u"
    c: str = "c"
    r: str = "r"
    y: str = "y"


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

class RSize(Enum):
    """Avalanche relative size values."""

    R1: str = "R1"
    R2: str = "R2"
    R3: str = "R3"
    R4: str = "R4"
    R5: str = "R5"
    U: str = "U"
    UNK: str = "UNK"

class DSize(Enum):
    """Avalanche desctructive size values.

    Because these can have half values, `P` is a substitute for decimals.
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

class ObsTypes(Enum):
    """The types that Observation objects can have."""

    AVY_OBS: str = "avalanche_observation"
    REPORT_OBS: str = "report_observation"
