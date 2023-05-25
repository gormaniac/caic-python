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
    description: Optional[str] = None
    classic_id: Optional[str] = None


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
    parent_id: Optional[str] = None
    slug: Optional[str] = None
    title: Optional[str] = None
    category: Optional[str] = None
    category_order: Optional[int] = None
    is_root: Optional[bool] = None
    is_leaf: Optional[bool] = None
    tree_level: Optional[int] = None
    parent_url: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    url: Optional[str] = None
    geojson_url: Optional[str] = None


class ObsReport(pydantic.BaseModel):
    """Really a pared down FieldReport."""

    id: Optional[str] = None
    status: Optional[str] = None
    is_locked: Optional[bool] = None
    is_anonymous: Optional[bool] = None
    url: Optional[str] = None

class AvalancheObservation(pydantic.BaseModel):
    """A single avalanche observation from the CAIC website."""

    id: str
    type: Optional[str] = None
    backcountry_zone_id: Optional[str] = None
    backcountry_zone: Optional[BackcountryZone] = None
    highway_zone_id: Optional[str] = None
    observed_at: Optional[datetime.datetime] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    classic_id: Optional[int] = pydantic.Field(default=None, description="V1 only")
    classic_observation_report_id: Optional[int] = pydantic.Field(default=None, description="V1 only")
    classic_observation_report_url: Optional[str] = pydantic.Field(default=None, description="V1 only")
    observation_report_status: Optional[str] = pydantic.Field(default=None, description="V1 only")
    observation_report_url: Optional[str] = pydantic.Field(default=None, description="V1 only")
    comments: Optional[str] = None
    location: Optional[str] = None
    lastname: Optional[str] = None
    full_name: Optional[str] = None
    date_known: Optional[str] = None
    time_known: Optional[str] = None
    op_name: Optional[str] = None
    is_locked: Optional[bool] = None
    number: Optional[int] = None
    hw_op_bc: Optional[str] = None
    path: Optional[str] = None
    landmark: Optional[str] = None
    type_code: Optional[enums.TypeCode] = None
    problem_type: Optional[str] = None
    aspect: Optional[enums.Aspect] = None
    elevation: Optional[str] = None
    relative_size: Optional[enums.RSize] = None
    destructive_size: Optional[enums.DSize] = None
    primary_trigger: Optional[enums.PrimaryTrigger] = None
    secondary_trigger: Optional[enums.SecondaryTrigger] = None
    is_incident: Optional[bool] = None
    area: Optional[str] = None
    angle_average: Optional[float] = None
    angle_maximum: Optional[float] = None
    elevation_feet: Optional[int] = None
    surface: Optional[str] = None
    weak_layer: Optional[str] = None
    grain_type: Optional[str] = None
    crown_average: Optional[float] = None
    crown_maximum: Optional[float] = None
    crown_units: Optional[str] = None
    width_average: Optional[float] = None
    width_maximum: Optional[float] = None
    width_units: Optional[str] = None
    vertical_average: Optional[float] = None
    vertical_maximum: Optional[float] = None
    vertical_units: Optional[str] = None
    terminus: Optional[str] = None
    road_status: Optional[str] = None
    road_depth: Optional[float] = None
    road_units: Optional[str] = None
    road_depth_units: Optional[str] = None
    highway_zone_id: Optional[str] = None
    road_length: Optional[str] = None
    road_length_units: Optional[str] = None
    observation_report: Optional[ObsReport] = None
    avalanche_detail: Optional['AvalancheDetail'] = None

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

    first: Optional[str] = None
    prev: Optional[str] = None
    next: Optional[str] = None
    last: Optional[str] = None


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
    backcountry_zone_id: Optional[str] = None
    backcountry_zone: Optional[BackcountryZone] = None
    highway_zone_id: Optional[str] = None
    observed_at: Optional[datetime.datetime] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    comments: Optional[str] = None
    url: Optional[str] = None
    cracking: Optional[str] = None
    collapsing: Optional[str] = None
    weak_layers: Optional[str] = None
    rose: Optional[str] = None


class ObservationAsset(pydantic.BaseModel):
    """An asset (image/video) attached to a field report."""

    id: str
    type: enums.ObsTypes
    status: Optional[str] = None
    caption: Optional[str] = None
    tags: Optional[str] = None
    is_redacted: Optional[bool] = None
    is_locked: Optional[bool] = None
    is_avalanche: Optional[bool] = None
    location_context: Optional[str] = None
    full_url: Optional[str] = None
    reduced_url: Optional[str] = None
    thumb_url: Optional[str] = None
    external_url: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None


class HighwayZone(pydantic.BaseModel):

    id: Optional[str] = None
    type: Optional[str] = None
    parent_id: Optional[str] = None
    slug: Optional[str] = None
    title: Optional[str] = None
    category: Optional[str] = None
    category_order: Optional[int] = None
    is_root: Optional[bool] = None
    is_leaf: Optional[bool] = None
    tree_level: Optional[int] = None
    parent_url: Optional[str] = None
    children_urls: Optional[list[str]] = pydantic.Field(default_factory=list)
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    url: Optional[str] = None
    geojson_url: Optional[str] = None

class WeatherObservation(pydantic.BaseModel):
    """An observation about the weather in a field report."""

    id: str
    type: enums.ObsTypes
    backcountry_zone_id: Optional[str] = None
    backcountry_zone: Optional[BackcountryZone] = None
    highway_zone_id: Optional[str] = None
    highway_zone: Optional[HighwayZone] = None
    observed_at: Optional[datetime.datetime] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    classic_id: Optional[int] = None
    classic_observation_report_id: Optional[int] = None
    classic_observation_report_url: Optional[str] = None
    comments: Optional[str] = None
    url: Optional[str] = None
    location: Optional[str] = None
    temperature: Optional[int] = None
    temperature_maximum: Optional[int] = None
    temperature_minimum: Optional[int] = None
    temperature_units: Optional[str] = None
    temperature_at_negative_20cm: Optional[int] = None
    temperature_at_negative_20cm_units: Optional[str] = None
    relative_humidity: Optional[str] = None
    precipitation_rate: Optional[str] = None
    precipitation_type: Optional[str] = None
    sky_cover: Optional[str] = None
    height_of_snow: Optional[int] = None
    height_of_snow_units: Optional[str] = None
    height_of_new_snow_12_hours: Optional[int] = None
    height_of_new_snow_24_hours: Optional[int] = None
    height_of_new_snow_units: Optional[str] = None
    height_of_new_snow_water_equivalent_12_hours: Optional[int] = None
    height_of_new_snow_water_equivalent_24_hours: Optional[int] = None
    height_of_new_snow_water_equivalent_units: Optional[str] = None
    windspeed_ridgeline: Optional[str] = None
    wind_direction_ridgeline: Optional[str] = None
    windspeed: Optional[str] = None
    wind_direction: Optional[str] = None
    windspeed_units: Optional[str] = None
    maximum_gust_speed: Optional[str] = None
    maximum_gust_direction: Optional[str] = None
    maximum_gust_duration_seconds: Optional[str] = None
    blowing_snow: Optional[str] = None
    windloading: Optional[str] = None
    weather_detail: Optional['WeatherDetail'] = None

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
    backcountry_zone: Optional[str] = None
    backcountry_zone: Optional[BackcountryZone] = None
    url: Optional[str] = None
    creator: Optional[Creator] = None
    avalanche_observations_count: Optional[int] = None
    avalanche_observations: Optional[list[AvalancheObservation]] = pydantic.Field(default_factory=list)
    avalanche_detail: Optional[AvalancheDetail] = None
    weather_observations_count: Optional[int] = None
    weather_observations: Optional[list[WeatherObservation]] = pydantic.Field(default_factory=list)
    weather_detail: Optional[WeatherDetail] = None
    snowpack_observations_count: Optional[int] = None
    snowpack_observations: Optional[list[SnowpackObservation]] = pydantic.Field(default_factory=list)
    assets_count: Optional[int] = None
    assets: Optional[list[ObservationAsset]] = pydantic.Field(default_factory=list)
    highway_zone_id: Optional[str] = None
    observed_at: Optional[datetime.datetime] = None
    snowpack_detail: Optional[SnowpackDetail] = None
    observation_form: Optional[str] = None
    is_anonymous: Optional[bool] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    full_name: Optional[str] = None
    organization: Optional[str] = None
    status: Optional[str] = None
    date_known: Optional[str] = None
    time_known: Optional[str] = None
    hw_op_bc: Optional[str] = None
    area: Optional[str] = None
    route: Optional[str] = None
    is_locked: Optional[bool] = None
    objective: Optional[str] = None
    saw_avalanche: Optional[bool] = None
    triggered_avalanche: Optional[bool] = None
    caught_in_avalanche: Optional[bool] = None
    state: Optional[str] = None
    landmark: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None
    is_anonymous_location: Optional[bool] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

models = [value for value in locals().values() if isinstance(value, pydantic.BaseModel)]
for model in models:
    print(model)
    if model.__module__ == __name__:
        model.model_rebuild()
