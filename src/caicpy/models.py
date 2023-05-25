"""Pydantic models used by caicpy."""

import datetime
from typing import Optional, Union

import pydantic

from . import enums
from . import LOGGER


class DetailObject(pydantic.BaseModel):
    """A base for several, similar, details objects attached to a field report.
    
    This is where `classic_id` ended up in the V2 API.
    """

    id: str
    type: enums.DetailsTypes
    description: Optional[str]
    classic_id: Optional[str]


class AvalancheDetail(DetailObject):
    """Summary details of an observed avalanche."""


class SnowpackDetail(DetailObject):
    """Summary details of the observed snowpack."""


class WeatherDetail(DetailObject):
    """Summary details of the observed weather.
    
    There is occasionally data here even when
    not in `weather_observations` for a field report.
    """


class V1AvalancheObservation(pydantic.BaseModel):
    """A single avalanche observation from the /api/avalanche_observations endpoint.

    The `/api/avalanche_observations` endpoint returns a slightly different
    object than the v2 `avalanche_observations` endpoint.

    This object allows us to transform to the standardized `AvalancheObservation`
    via `to_obs`.
    """

    id: str
    type: enums.ObsTypes
    attributes: dict
    relationships: dict

    def to_obs(self) -> "AvalancheObservation":
        """Convert this instance to an `AvalancheObservation`."""

        if (bc_zone := "backcountry_zone") in self.relationships.keys():
            zone_dict = self.relationships[bc_zone]
        else:
            if len(self.relationships) > 0:
                LOGGER.warning(
                    "Found new relationship objects, please report these: %s",
                    str(self.relationships),
                )
            zone_dict = None

        return AvalancheObservation(
            id=self.id, type=self.type, backcountry_zone=zone_dict, **self.attributes
        )


class BackcountryZone(pydantic.BaseModel):
    """A backcountry_zone object - these are in most responses."""

    id: str
    type: enums.ObsTypes
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


class AvalancheObservation(pydantic.BaseModel):
    """A single avalanche observation from the CAIC website."""

    id: str
    type: Optional[str]
    backcountry_zone_id: Optional[str]
    backcountry_zone: Optional[BackcountryZone]
    highway_zone_id: Optional[str]
    observed_at: Optional[datetime.datetime]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    latitude: Optional[float]
    longitude: Optional[float]
    classic_id: Optional[int] = pydantic.Field(description="V1 only")
    classic_observation_report_id: Optional[int] = pydantic.Field(description="V1 only")
    classic_observation_report_url: Optional[str] = pydantic.Field(description="V1 only")
    observation_report_status: Optional[str] = pydantic.Field(description="V1 only")
    observation_report_url: Optional[str] = pydantic.Field(description="V1 only")
    comments: Optional[str]
    location: Optional[str]
    lastname: Optional[str]
    full_name: Optional[str]
    date_known: Optional[str]
    time_known: Optional[str]
    op_name: Optional[str]
    is_locked: Optional[bool]
    number: Optional[int]
    hw_op_bc: Optional[str]
    path: Optional[str]
    landmark: Optional[str]
    type_code: Optional[enums.TypeCode]
    problem_type: Optional[str]
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
    road_depth_units: Optional[str]
    highway_zone_id: Optional[str]
    road_length: Optional[str]
    road_length_units: Optional[str]
    observation_report: Optional['FieldReport']
    avalanche_detail: Optional['AvalancheDetail']

    async def fieldobs(self, caic_client) -> Union["FieldReport", None]:
        """Get the associated `FieldReport` using the provided `CaicClient`."""

        if self.id is not None:
            return await caic_client.field_report(self.id)

        return None

    class Config:
        undefined_types_warning=False


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


class V1AvyResponse(pydantic.BaseModel):
    """A response from the CAIC API."""

    meta: CaicResponseMeta
    links: CaicResponseLinks
    data: list[AvalancheObservation]

    class Config:
        undefined_types_warning=False


class SnowpackObservation(pydantic.BaseModel):
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
    type: enums.ObsTypes
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


class HighwayZone(pydantic.BaseModel):

    id: Optional[str]
    type: Optional[str]
    parent_id: Optional[str]
    slug: Optional[str]
    title: Optional[str]
    category: Optional[str]
    category_order: Optional[int]
    is_root: Optional[bool]
    is_leaf: Optional[bool]
    tree_level: Optional[int]
    parent_url: Optional[str]
    children_urls: Optional[list[str]]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    url: Optional[str]
    geojson_url: Optional[str]

class WeatherObservation(pydantic.BaseModel):
    """An observation about the weather in a field report."""

    id: str
    type: enums.ObsTypes
    backcountry_zone_id: Optional[str]
    backcountry_zone: Optional[BackcountryZone]
    highway_zone_id: Optional[str]
    highway_zone: Optional[HighwayZone]
    observed_at: Optional[datetime.datetime]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    latitude: Optional[float]
    longitude: Optional[float]
    classic_id: Optional[int]
    classic_observation_report_id: Optional[int]
    classic_observation_report_url: Optional[str]
    comments: Optional[str]
    url: Optional[str]
    location: Optional[str]
    temperature: Optional[int]
    temperature_maximum: Optional[int]
    temperature_minimum: Optional[int]
    temperature_units: Optional[str]
    temperature_at_negative_20cm: Optional[int]
    temperature_at_negative_20cm_units: Optional[str]
    relative_humidity: Optional[str]
    precipitation_rate: Optional[str]
    precipitation_type: Optional[str]
    sky_cover: Optional[str]
    height_of_snow: Optional[int]
    height_of_snow_units: Optional[str]
    height_of_new_snow_12_hours: Optional[int]
    height_of_new_snow_24_hours: Optional[int]
    height_of_new_snow_units: Optional[str]
    height_of_new_snow_water_equivalent_12_hours: Optional[int]
    height_of_new_snow_water_equivalent_24_hours: Optional[int]
    height_of_new_snow_water_equivalent_units: Optional[str]
    windspeed_ridgeline: Optional[str]
    wind_direction_ridgeline: Optional[str]
    windspeed: Optional[str]
    wind_direction: Optional[str]
    windspeed_units: Optional[str]
    maximum_gust_speed: Optional[str]
    maximum_gust_direction: Optional[str]
    maximum_gust_duration_seconds: Optional[str]
    blowing_snow: Optional[str]
    windloading: Optional[str]
    weather_detail: Optional['WeatherDetail']

class Creator(pydantic.BaseModel):
    """The creator object of a field report.

    We'll want to track this, but it is sparse on details.
    """

    id: str
    type: str

class FieldReport(pydantic.BaseModel):
    """A field (or observation) report."""

    id: str
    type: enums.ObsTypes
    backcountry_zone: Optional[str]
    backcountry_zone: Optional[BackcountryZone]
    url: Optional[str]
    creator: Optional[Creator]
    avalanche_observations_count: Optional[int]
    avalanche_observations: Optional[list[AvalancheObservation]]
    avalanche_detail: Optional[AvalancheDetail]
    weather_observations_count: Optional[int]
    weather_observations: Optional[list[WeatherObservation]]
    weather_detail: Optional[WeatherDetail]
    snowpack_observations_count: Optional[int]
    snowpack_observations: Optional[list[SnowpackObservation]]
    assets_count: Optional[int]
    assets: Optional[list[ObservationAsset]]
    highway_zone_id: Optional[str]
    observed_at: Optional[datetime.datetime]
    snowpack_detail: Optional[SnowpackDetail]
    observation_form: Optional[str]
    is_anonymous: Optional[bool]
    firstname: Optional[str]
    lastname: Optional[str]
    full_name: Optional[str]
    organization: Optional[str]
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
