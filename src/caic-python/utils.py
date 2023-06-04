"""Helpful methods."""

from . import models


def find_classic_id(report: models.FieldReport) -> int | None:
    """
    Find a classic ID from a given ``FieldReport``.

    Not every field report from the v2 API has an associated classic ID. It is
    nested in one of several possible child objects, which are not always present
    themselves. This method looks in all known locations of a ``FieldReport``
    object for a classic ID. It first checks all ``*_details`` attrs, then checks
    each ``*Observation`` in all ``*_observations`` attrs. The first classic ID
    found is returned.

    Parameters
    ----------
    report : models.FieldReport
        The ``FieldReport`` to search in.

    Returns
    -------
    int | None
        Returns the classic ID, or None if the ``FieldReport`` doesn't have one.
    """

    clsc_id_locs = ["avalanche_detail", "snowpack_detail", "weather_detail"]
    clsc_rprt_id_locs = [
        "avalanche_observations",
        "snowpack_observations",
        "weather_observations",
    ]

    # Search in detail objects first, for less loops.
    for loc in clsc_id_locs:
        details = getattr(report, loc, None)
        if details and getattr(details, "classic_id", None) is not None:
            return details.classic_id

    # Then, if we didn't find anything in details, loop through all
    # observations of a report to find one with a classic report id.
    for loc in clsc_rprt_id_locs:
        obs = getattr(report, loc, [])
        for ob in obs:
            if ob and getattr(ob, "classic_observation_report_id", None) is not None:
                return ob.classic_observation_report_id

    return None
