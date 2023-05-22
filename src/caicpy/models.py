"""Pydantic models used by caicpy."""

import datetime
from typing import Optional

import pydantic

from . import enums


class Observation:
    """A generic observation object returned by the CAIC API.
    
    Meant for subclassing, to group all *Observation models.

    See `OBSERVATION_MODELS` for a mapping of all CAIC observation names
    to their `Observation` subclass types.

    See `enums.OBS_TYPES` for an enumeration of all possible types.
    """


class CaicObsRelationships(pydantic.BaseModel):
    """The relationships a `CAICObsObject` can have.
    
    Example::

        "relationships": {
            "backcountry_zone": {
                "data": {
                    "id": "d074e08f-cc75-41b1-93a0-04637480c832",
                    "type": "zone"
                }
            }
        }

    """


class CaicObsObject(pydantic.BaseModel):
    """A single object returned by the API, may be part of a list of other objects."""

    id: str
    type: enums.ObsTypes
    attributes: dict
    relationships: dict

    def attrs_to_obs(self) -> Observation:
        """Convert this instance to an `Observation` based on `type`.
        
        Raises
        ------
        ValueError
            If somehow `self.type` is not in `OBSERVATION_MODELS`.
        """

        if self.type in OBSERVATION_MODELS:
            return OBSERVATION_MODELS[self.type](
                id=self.id, rel_dict=self.relationships, **self.attributes
            )

        raise ValueError(f"An unsupported observation type ({self.type}) was encountered.")

class AvalancheObservation(Observation, pydantic.BaseModel):
    """A single avalanche observation from the CAIC website."""

    id: str
    rel_dict: dict = pydantic.Field(default_factory=dict)
    observed_at: Optional[datetime.datetime]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    latitude: Optional[int]
    longitude: Optional[int]
    classic_id: Optional[int]
    classic_observation_report_id: Optional[int]
    classic_observation_report_url: Optional[str]
    observation_report_status: Optional[str]
    observation_report_url: Optional[str]
    comments: Optional[str]
    location: Optional[str]
    date_known: Optional[str]
    time_known: Optional[str]
    op_name: Optional[str]
    number: Optional[str]
    hw_op_bc: Optional[str]
    path: Optional[str]
    landmark: Optional[str]
    type_code: Optional[enums.TypeCode]
    aspect: Optional[enums.Aspect]
    elevation: Optional[str]
    relative_size: Optional[enums.RSize]
    destructive_size: Optional[enums.DSize]
    primary_trigger: Optional[enums.PrimaryTrigger]
    secondary_trigger: Optional[enums.SecondaryTrigger]
    is_incident: Optional[bool]
    area: Optional[str]
    angle_average: Optional[float]
    angle_maximum: Optional[float]
    elevation_feet: Optional[int]
    surface: Optional[str]
    weak_layer: Optional[str]
    grain_type: Optional[str]
    crown_average: Optional[float]
    crown_maximum: Optional[float]
    crown_units: Optional[str]
    width_average: Optional[float]
    width_maximum: Optional[float]
    width_units: Optional[str]
    vertical_average: Optional[float]
    vertical_maximum: Optional[float]
    vertical_units: Optional[str]
    terminus: Optional[str]
    road_status: Optional[str]
    road_depth: Optional[float]
    road_units: Optional[str]

class CaicResponseMeta(pydantic.BaseModel):
    """The `meta` portion of a `CaicResponse`.
    
    Contains pagination info.

    Example::

        {"current_page":1,"page_items":100,"total_pages":241,"total_count":24045}

    """

    current_page: int
    page_items: int
    total_pages: int
    total_count: int


class CaicResponseLinks(pydantic.BaseModel):
    """The `links` portion of a `CaicResponse`.
    
    Contains pagination info.

    Example::

        {
            "first": "https://api.avalanche.state.co.us/api/avalanche_observations?page=1\u0026per=100",
            "prev": null,
            "next": "https://api.avalanche.state.co.us/api/avalanche_observations?page=2\u0026per=100",
            "last": "https://api.avalanche.state.co.us/api/avalanche_observations?page=241\u0026per=100"
        }

    """

    first: Optional[str]
    prev: Optional[str]
    next: Optional[str]
    last: Optional[str]


class CaicResponse(pydantic.BaseModel):
    """A response from the CAIC API."""

    meta: CaicResponseMeta
    links: CaicResponseLinks
    data: list[CaicObsObject]


OBSERVATION_MODELS = {
    "avalanche_observation": AvalancheObservation
}
