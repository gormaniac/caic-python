"""Pydantic models used by caicpy."""

import datetime
import enum
from typing import Optional

import pydantic

from . import enums
from . import Observation


class CaicAvyObsResponse(pydantic.BaseModel):
    """A single avalanche observation from the /api/avalanche_observations endpoint.
    
    The `/api/avalanche_observations` endpoint returns a slightly different
    object than the `avalanche_observations` key in an `/api/observation_report`
    response.

    This object allows us to transform to the standardized `AvalancheObservation`
    via `to_obs`.
    """

    id: str
    type: enums.ObsTypes
    attributes: dict
    relationships: dict

    def to_obs(self) -> 'AvalancheObservation':
        """Convert this instance to an `AvalancheObservation`."""

        if (bc_zone := "backcountry_zone") in self.relationships.keys():
            zone_dict = self.relationships[bc_zone]
        else:
            zone_dict = None

        return AvalancheObservation(
            id=self.id, type=self.type, backcountry_zone=zone_dict, **self.attributes
        )


class BackcountryZone(pydantic.BaseModel):
    """A backcountry_zone object - these are in most responses."""

    id: str
    type: str
    parent_id: Optional[str]
    slug: Optional[str]
    title: Optional[str]
    category: Optional[str]
    category_order: Optional[int]
    is_root: Optional[bool]
    is_leaf: Optional[bool]
    tree_level: Optional[int]
    parent_url: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    url: Optional[str]
    geojson_url: Optional[str]


class AvalancheObservation(Observation, pydantic.BaseModel):
    """A single avalanche observation from the CAIC website."""

    id: str
    type: Optional[str]
    backcountry_zone_id: Optional[str]
    backcountry_zone: Optional[BackcountryZone]
    rel_dict: Optional[dict]
    observed_at: Optional[datetime.datetime]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    latitude: Optional[float]
    longitude: Optional[float]
    classic_id: Optional[int]
    classic_observation_report_id: Optional[int]
    classic_observation_report_url: Optional[str]
    observation_report_status: Optional[str]
    observation_report_url: Optional[str]
    url: Optional[str]
    comments: Optional[str]
    location: Optional[str]
    date_known: Optional[str]
    time_known: Optional[str]
    op_name: Optional[str]
    number: Optional[int]
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
    highway_zone_id: Optional[str]

    async def fieldobs(self, caic_client) -> Observation | None:
        """Get the associated `FieldObservation` using the provided `CaicClient`."""

        if self.classic_observation_report_id is not None:
            return await caic_client.field_report(self.classic_observation_report_id)

        return None


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


class SnowpackObservation(Observation, pydantic.BaseModel):
    """An observation about the snowpack in a field report."""

    id: str
    type: enums.ObsTypes
    backcountry_zone_id: str
    backcountry_zone: BackcountryZone
    highway_zone_id: Optional[str]
    observed_at: Optional[datetime.datetime]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    latitude: Optional[float]
    longitude: Optional[float]
    comments: Optional[str]
    url: Optional[str]
    cracking: Optional[str]
    collapsing: Optional[str]
    weak_layers: Optional[str]
    rose: Optional[str]


class ObservationAsset(pydantic.BaseModel):
    """An asset (image/video) attached to a field report."""

    id: str
    type: str
    status: Optional[str]
    caption: Optional[str]
    tags: Optional[str]
    is_redacted: Optional[bool]
    is_locked: Optional[bool]
    is_avalanche: Optional[bool]
    location_context: Optional[str]
    full_url: Optional[str]
    reduced_url: Optional[str]
    thumb_url: Optional[str]
    external_url: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]


class WeatherObservation(Observation, pydantic.BaseModel):
    """An observation about the weather in a field report."""

class FieldReport(Observation, pydantic.BaseModel):
    """A field (or observation) report."""

    id: str
    type: enums.ObsTypes
    backcountry_zone: str
    backcountry_zone: BackcountryZone
    url: str
    avalanche_observations_count: int
    avalanche_observations: AvalancheObservation
    weather_observations_count: int
    weather_observations: list[WeatherObservation]
    snowpack_observations_count: int
    snowpack_observations: list[SnowpackObservation]
    assets_count: int
    assets: list[ObservationAsset]
    highway_zone_id: Optional[str]
    observed_at: Optional[datetime.datetime]
    observation_form: Optional[str]
    is_anonymous: Optional[bool]
    firstname: Optional[str]
    lastname: Optional[str]
    full_name: Optional[str]
    status: Optional[str]
    date_known: Optional[str]
    time_known: Optional[str]
    hw_op_bc: Optional[str]
    area: Optional[str]
    route: Optional[str]
    is_locked: Optional[bool]
    objective: Optional[str]
    saw_avalanche: Optional[bool]
    triggered_avalanche: Optional[bool]
    caught_in_avalanche: Optional[bool]
    state: Optional[str]
    landmark: Optional[str]
    description: Optional[str]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    is_anonymous_location: Optional[bool]
    latitude: Optional[float]
    longitude: Optional[float]


class ObsClasses(enum.Enum):
    """Observation classes enum for (CaicResponse)."""

    FIELD_REPORT = FieldReport
    WEATHER_OBSERVATION = WeatherObservation
    SNOWPACK_OBSERVATION = SnowpackObservation
    AVALANCHE_OBSERVATION = CaicAvyObsResponse
    

OBSERVATION_MODELS = {
    "avalanche_observation": AvalancheObservation,
    "observation_report": FieldReport,
}
