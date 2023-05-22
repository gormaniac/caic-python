from dataclasses import dataclass
from datetime import datetime

import dateutil.parser
import requests

from .enums import Aspect, DSize, PrimaryTrigger, RSize, SecondaryTrigger, TypeCode


AvalancheAttr = str | int | bool | None
"""A value in the `attributes` key of an `avalanche_obs` response."""

AvalancheObsDict = dict
"""A single avalanche observation found in an `avalanche_obs` response."""


@dataclass
class AvalancheExtras:
    """Extra details for a specific avalanche."""

    angle_average: AvalancheAttr
    angle_maximum: AvalancheAttr
    elevation_feet: AvalancheAttr
    surface: AvalancheAttr
    weak_layer: AvalancheAttr
    grain_type: AvalancheAttr
    crown_average: AvalancheAttr
    crown_maximum: AvalancheAttr
    crown_units: AvalancheAttr
    width_average: AvalancheAttr
    width_maximum: AvalancheAttr
    width_units: AvalancheAttr
    vertical_average: AvalancheAttr
    vertical_maximum: AvalancheAttr
    vertical_units: AvalancheAttr
    terminus: AvalancheAttr
    road_status: AvalancheAttr
    road_depth: AvalancheAttr
    road_units: AvalancheAttr


class Avalanche:
    """An avalanche observation from the CAIC website."""

    def __init__(
        self,
        avy_id: str,
        relationships: dict,
        observed_at: AvalancheAttr = None,
        created_at: AvalancheAttr = None,
        updated_at: AvalancheAttr = None,
        latitude: AvalancheAttr = None,
        longitude: AvalancheAttr = None,
        classic_id: AvalancheAttr = None,
        classic_observation_report_id: AvalancheAttr = None,
        classic_observation_report_url: AvalancheAttr = None,
        observation_report_status: AvalancheAttr = None,
        comments: AvalancheAttr = None,
        location: AvalancheAttr = None,
        date_known: AvalancheAttr = None,
        time_known: AvalancheAttr = None,
        op_name: AvalancheAttr = None,
        number: AvalancheAttr = None,
        hw_op_bc: AvalancheAttr = None,
        path: AvalancheAttr = None,
        landmark: AvalancheAttr = None,
        type_code: AvalancheAttr = None,
        aspect: AvalancheAttr = None,
        elevation: AvalancheAttr = None,
        relative_size: AvalancheAttr = None,
        destructive_size: AvalancheAttr = None,
        primary_trigger: AvalancheAttr = None,
        secondary_trigger: AvalancheAttr = None,
        is_incident: AvalancheAttr = None,
        area: AvalancheAttr = None,
        **kwargs,
    ) -> None:

        self.avy_id = avy_id
        self.relationships = relationships
        self.observed_at: datetime = dateutil.parser.parse(observed_at)
        self.created_at: datetime = dateutil.parser.parse(created_at)
        self.updated_at: datetime = dateutil.parser.parse(updated_at)
        self.latitude: int = latitude
        self.longitude: int = longitude
        self.classic_id: int = classic_id
        self.classic_observation_report_id: int = classic_observation_report_id
        self.classic_observation_report_url: str = classic_observation_report_url
        self.observation_report_status: str = observation_report_status
        self.comments: str | None = comments
        self.location: str | None = location
        self.date_known: str = date_known
        self.time_known: str = time_known
        self.op_name: str = op_name
        self.number: str = number
        self.hw_op_bc: str = hw_op_bc
        self.path: str | None = path
        self.landmark: str = landmark
        self.type_code: TypeCode = type_code
        self.aspect: Aspect = aspect
        self.elevation: str = elevation
        self.relative_size: RSize = relative_size
        self.destructive_size: DSize = destructive_size
        self.primary_trigger: PrimaryTrigger | None = primary_trigger
        self.secondary_trigger: SecondaryTrigger | None = secondary_trigger
        self.is_incident: bool = is_incident
        self.area: str | None = area

        self.extras = AvalancheExtras(**kwargs)

        self.observation = None

    @classmethod
    def from_observation(cls, obs_dict: AvalancheObsDict) -> "Avalanche":
        """Return an Avalanche object from a single avy observation dict."""

        avy_id = obs_dict.get("id", "")
        attributes = obs_dict.get("attributes", {})
        relationships = obs_dict.get("relationships", {})

        return cls(avy_id, relationships, **attributes)

    @classmethod
    def from_response(cls, response: requests.Response) -> list["Avalanche"]:
        """Return a list of Avalanche objects found in a response object."""

        avalanches = []

        data = response.json().get("data", [])

        for obs_dict in data:
            avalanches.append(cls.from_observation(obs_dict))

        return avalanches

    def obs(self, client):
        """Get the associated Field Observation using the provided `CAICClient`."""

        return client.field_report(self.classic_observation_report_id)
