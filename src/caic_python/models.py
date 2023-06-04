"""Pydantic models used by caic-python."""

import datetime
from typing import Literal, Optional, Union

import pydantic

from . import enums
from . import LOGGER


class DetailObject(pydantic.BaseModel):
    """A base for several, similar, details objects attached to a field report.

    This is where ``classic_id`` ended up in the V2 API.
    """

    id: str
    type: enums.DetailsTypes
    description: Optional[str] = None
    classic_id: Optional[int] = None


class AvalancheDetail(DetailObject):
    """Summary details of an observed avalanche."""


class SnowpackDetail(DetailObject):
    """Summary details of the observed snowpack."""


class WeatherDetail(DetailObject):
    """Summary details of the observed weather.

    There is occasionally data here even when
    not in ``weather_observations`` for a field report.
    """


class ForecastSummaryDay(pydantic.BaseModel):
    """An individual day's forecast summary - base for several forecast types."""

    date: Optional[datetime.datetime]
    content: Optional[str]


class ForecastSummary(pydantic.BaseModel):
    """Forecast summaries for several days - base for several forecast types."""

    days: list[ForecastSummaryDay]


class ExpectedSize(pydantic.BaseModel):
    """Expected avalanche size in an avalanche forecast."""

    min: str
    max: str


class AvalancheProblem(pydantic.BaseModel):
    """A described avalanche problem in a forecast.

    TODO - enums here for everything
    """

    type: str
    aspectElevations: list[str]
    likelihood: str
    expectedSize: ExpectedSize
    comment: str


class AvalancheProblems(pydantic.BaseModel):
    """A collection of the next few days' avalanche problems."""

    days: list[list[AvalancheProblem]]


class ForecastConfidence(pydantic.BaseModel):
    """An avalanche forecast's confidence details."""

    date: datetime.datetime
    rating: str
    statements: list[str] = pydantic.Field(default_factory=list)


class ForecastConfidences(pydantic.BaseModel):
    """The avalanche forecast confidence details for the next few days."""

    days: list[ForecastConfidence]


class ForecastComms(pydantic.BaseModel):
    """Special forecast communications - not sure how this get's used yet."""

    headline: str
    sms: str


class DangerRating(pydantic.BaseModel):
    """An avalanche forecast's danger rating.

    TODO - enums for everything here.
    """

    position: int
    alp: str
    tln: str
    btl: str
    date: datetime.datetime


class DangerRatings(pydantic.BaseModel):
    """A list of the avalanche danger ratings for the next few days."""

    days: list[DangerRating]


class ForecastImage(pydantic.BaseModel):
    """An image attached to an avalanche forecast."""

    id: str
    url: str
    width: int
    height: int
    credit: str
    caption: str
    tag: str


class ForecastMedia(pydantic.BaseModel):
    """All of the images attached to an avalanche forecast."""

    Images: list[ForecastImage]


class AvalancheForecast(pydantic.BaseModel):
    """A CAIC avalanche forecast."""

    id: str
    title: str
    type: Literal["avalancheforecast"]
    polygons: list
    areaId: str
    forecaster: str
    issueDateTime: datetime.datetime
    expiryDateTime: datetime.datetime
    weatherSummary: ForecastSummary
    snowpackSummary: ForecastSummary
    avalancheSummary: ForecastSummary
    avalancheProblems: AvalancheProblems
    terrainAndTravelAdvice: dict
    confidence: ForecastConfidences
    communication: ForecastComms
    dangerRatings: DangerRatings
    media: ForecastMedia


class RegionalDiscussionForecast(pydantic.BaseModel):
    """An avalanche forecast discussion covering a regional area."""

    id: str
    title: str
    type: str
    polygons: list[str]
    areaId: str
    forecaster: str
    issueDateTime: datetime.datetime
    expiryDateTime: datetime.datetime
    message: str
    communications: ForecastComms
    media: ForecastMedia


class V1AvalancheObservation(pydantic.BaseModel):
    """A single avalanche observation from the /api/avalanche_observations endpoint.

    The ``/api/avalanche_observations`` endpoint returns a slightly different
    object than the v2 ``avalanche_observations`` endpoint.

    This object allows us to transform to the standardized ``AvalancheObservation``
    via ``to_obs``.
    """

    id: str
    type: enums.ObsTypes
    attributes: dict
    relationships: dict

    def to_obs(self) -> "AvalancheObservation":
        """Convert this instance to an ``AvalancheObservation``."""

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
    classic_observation_report_id: Optional[int] = pydantic.Field(
        default=None, description="V1 only"
    )
    classic_observation_report_url: Optional[str] = pydantic.Field(
        default=None, description="V1 only"
    )
    observation_report_status: Optional[str] = pydantic.Field(
        default=None, description="V1 only"
    )
    observation_report_url: Optional[str] = pydantic.Field(
        default=None, description="V1 only"
    )
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
    road_length: Optional[int | float] = None
    road_length_units: Optional[str] = None
    observation_report: Optional[ObsReport] = None
    avalanche_detail: Optional[AvalancheDetail] = None

    async def fieldobs(self, caic_client) -> Union["FieldReport", None]:
        """Get the associated ``FieldReport`` using the provided ``CaicClient``."""

        if self.id is not None:
            return await caic_client.field_report(self.id)

        return None


class CaicResponseMeta(pydantic.BaseModel):
    """The ``meta`` portion of a ``V1AvyResponse``.

    Contains pagination info.
    """

    current_page: int
    page_items: int
    total_pages: int
    total_count: int


class CaicResponseLinks(pydantic.BaseModel):
    """The ``links`` portion of a ``V1AvyResponse``.

    Contains pagination info.
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
    tags: Optional[list[str]] = pydantic.Field(default_factory=list)
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
    """A highway avalanche zone - similar to a BC zone but specific to CDOT/CAIC avy control."""

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
    temperature: Optional[int | float] = None
    temperature_maximum: Optional[int | float] = None
    temperature_minimum: Optional[int | float] = None
    temperature_units: Optional[str] = None
    temperature_at_negative_20cm: Optional[int | float] = None
    temperature_at_negative_20cm_units: Optional[str] = None
    relative_humidity: Optional[int | float] = None
    precipitation_rate: Optional[str] = None
    precipitation_type: Optional[str] = None
    sky_cover: Optional[str] = None
    height_of_snow: Optional[int | float] = None
    height_of_snow_units: Optional[str] = None
    height_of_new_snow_12_hours: Optional[int | float] = None
    height_of_new_snow_24_hours: Optional[int | float] = None
    height_of_new_snow_units: Optional[str] = None
    height_of_new_snow_water_equivalent_12_hours: Optional[int | float] = None
    height_of_new_snow_water_equivalent_24_hours: Optional[int | float] = None
    height_of_new_snow_water_equivalent_units: Optional[str] = None
    windspeed_ridgeline: Optional[int | float | str] = None
    wind_direction_ridgeline: Optional[str] = None
    windspeed: Optional[int | float] = None
    wind_direction: Optional[str] = None
    windspeed_units: Optional[str] = None
    maximum_gust_speed: Optional[int | float | str] = None
    maximum_gust_direction: Optional[str] = None
    maximum_gust_duration_seconds: Optional[str | float | int] = None
    blowing_snow: Optional[str] = None
    windloading: Optional[str] = None
    weather_detail: Optional["WeatherDetail"] = None


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
    avalanche_observations: Optional[list[AvalancheObservation]] = pydantic.Field(
        default_factory=list
    )
    avalanche_detail: Optional[AvalancheDetail] = None
    weather_observations_count: Optional[int] = None
    weather_observations: Optional[list[WeatherObservation]] = pydantic.Field(
        default_factory=list
    )
    weather_detail: Optional[WeatherDetail] = None
    snowpack_observations_count: Optional[int] = None
    snowpack_observations: Optional[list[SnowpackObservation]] = pydantic.Field(
        default_factory=list
    )
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
