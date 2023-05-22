#     /**
#     * @param startDatetime a utc date string in format YYYY-MM-DD HH:mm:ss
#     * @param endDatetime a utc date string in format YYYY-MM-DD HH:mm:ss
#     * @param header the caic auth header (shared between all of the pagination requests should be fine)
#     * @param page offset page
#     * @return raw caic response json (including pagination data so we can call this function again if there is more data)
#     */
#    async getCaicPaginated (startDatetime, endDatetime, headers, page = 1) {
#        queryArgs = new URLSearchParams({
#        per: 1000,
#        page,
#        observed_after: startDatetime,
#        observed_before: endDatetime,
#        t: Date.now()
#        });
#        const result = await fetch(`https://api.avalanche.state.co.us/api/avalanche_observations?${queryArgs}`, { headers });
#        return await result.json();
#    },

from enum import Enum
import time

import requests

from .avalanche import Avalanche
from .fieldobs import Observation

API_BASE = "https://api.avalanche.state.co.us/api"
CLASSIC_BASE = "https://classic.avalanche.state.co.us"

class APIEndpoints(Enum):
    """Endpoints for `API_BASE`."""

    AVY_OBS = "/avalanche_observations"

class ClassicEndpoints(Enum):
    """Endpoints for `CLASSIC_BASE`."""

    OBS_REPORT = "/caic/obs/obs_report.php"


class CAICClient:
    """The HTTP client that interacts with the CAIC API."""

    def __init__(self) -> None:
        self.session = requests.Session()

    def _api_get(self, endpoint: APIEndpoints, params: dict):
        return self.session.get(API_BASE + endpoint, params=params)

    def _classic_get(self, endpoint: ClassicEndpoints, params: dict):
        return self.session.get(CLASSIC_BASE + endpoint, params=params)

    def _classic_post(self, endpoint: ClassicEndpoints, data: dict):
        return self.session.get(CLASSIC_BASE + endpoint, data=data)

    def get_avy_obs(self, before: str, after: str, page: int = 1, count: int = 1000):
        """Get avalance observations from CAIC."""
        # TODO Need to validate times here.

        params = dict(
            observed_after=after,
            observed_before=before,
            page=page,
            per=count,
            t=time.time().split(".")[0]
        )

        resp = self._api_get(APIEndpoints.AVY_OBS, params)

        return Avalanche.from_response(resp)

    def field_report(self, report_id: str) -> Observation:
        """Get a single field report from CAIC."""

        params = dict(
            obs_id=report_id,
        )

        resp = self._classic_get(ClassicEndpoints.OBS_REPORT, params)

        return Observation.from_response(resp)

    def get_field_reports(self):
        """Get field reports from CAIC."""
