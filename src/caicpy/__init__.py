import logging

logging.basicConfig()
LOGGER = logging.getLogger(__name__)


class Observation:
    """A generic observation object returned by the CAIC API.
    
    Meant for subclassing, to group all *Observation models.

    See `models.OBSERVATION_MODELS` for a mapping of all CAIC observation names
    to their `Observation` subclass types.

    See `enums.OBS_TYPES` for an enumeration of all possible types.
    """
