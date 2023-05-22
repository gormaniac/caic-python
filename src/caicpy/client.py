"""An async HTTP client to interface with the CAIC website.

CAIC Website Avy Obs request::

     /**
     * @param startDatetime a utc date string in format YYYY-MM-DD HH:mm:ss
     * @param endDatetime a utc date string in format YYYY-MM-DD HH:mm:ss
     * @param header the caic auth header (shared between all of the pagination requests should be fine)
     * @param page offset page
     * @return raw caic response json (including pagination data so we can call this function again if there is more data)
     */
    async getCaicPaginated (startDatetime, endDatetime, headers, page = 1) {
        queryArgs = new URLSearchParams({
        per: 1000,
        page,
        observed_after: startDatetime,
        observed_before: endDatetime,
        t: Date.now()
        });
        const result = await fetch(`https://api.avalanche.state.co.us/api/avalanche_observations?${queryArgs}`, { headers });
        return await result.json();
    },

"""

import enum
from json import JSONDecodeError
import time
import typing

import aiohttp
import pydantic

from . import LOGGER
from . import errors
from . import fieldobs
from . import models


API_BASE = "https://api.avalanche.state.co.us/api"
CLASSIC_BASE = "https://classic.avalanche.state.co.us"


class APIEndpoints(enum.Enum):
    """Endpoints for `API_BASE`."""

    AVY_OBS = "/avalanche_observations"

class ClassicEndpoints(enum.Enum):
    """Endpoints for `CLASSIC_BASE`."""

    OBS_REPORT = "/caic/obs/obs_report.php"


class CaicClient:
    def __init__(self) -> None:
        self.headers = {}
        self.api_session = aiohttp.ClientSession(base_url=API_BASE)
        self.classic_session = aiohttp.ClientSession(base_url=CLASSIC_BASE)

    async def _api_get(self, endpoint: str, params: dict | None = None):
        try:
            resp = await self.api_session.get(endpoint, params=params)
            if resp.status >= 400:
                raise errors.CaicRequestException(f"Error status from CAIC: {resp.status}")

            data = await resp.json()

        except aiohttp.ClientError as err:
            raise errors.CaicRequestException(f"Error connecting to CAIC: {err}") from err
        except JSONDecodeError as err:
            raise errors.CaicRequestException(f"Error decoding CAIC response: {err}") from err

        else:
            return data

    async def _classic_get(self, endpoint: ClassicEndpoints, params: dict | None = None):
        return await self.classic_session.get(endpoint, params=params)

    async def _classic_post(self, endpoint: ClassicEndpoints, json: dict | None = None):
        return await self.classic_session.post(endpoint, json=json)

    async def _api_paginate_get(self, page: int, per: int, uri: str, params: typing.Mapping | None = None) -> dict | None:
        if params is None:
            params = {}

        params["per"] = per
        params["page"] = page

        data = await self._api_get(uri, params=params)

        return data

    async def avy_obs(self, obs_before: str, obs_after: str) -> list[Observation]:
        paginating = True

        obs = []
        page = 1

        params = {
            "observed_after": obs_after,
            "observed_before": obs_before,
            "t": time.time().split(".")[0]
        }

        while paginating:
            try:
                obs_resp = await self._api_paginate_get(page, 1000, APIEndpoints.AVY_OBS, params)
            except Exception as err:
                LOGGER.error("Failed to request the CAIC avy obs endpoint: %s" % err)
                page += 1
                continue

            try:
                caic_resp = models.CaicResponse(**obs_resp)
            except pydantic.ValidationError as err:
                LOGGER.warning("Unexpected response from the avy obs endpoint: %s\n%s" % (str(err), str(obs_resp)))
                page += 1
                continue

            if caic_resp.meta.current_page == caic_resp.meta.total_pages:
                paginating = False
            # Just a sanity check to avoid infinite looping
            elif page == caic_resp.meta.total_pages:
                LOGGER.debug("Paginating mismatch: %s" % caic_resp.json())
                paginating = False

            for item in caic_resp.data:
                try:
                    obs_obj = item.attrs_to_obs()
                except (pydantic.ValidationError, ValueError) as err:
                    LOGGER.warning("Unable to cast a response object to an Observation: %s\n%s" % (str(err), str(obs_resp)))
                else:
                    obs.append(obs_obj)

            page += 1

        return obs

    async def field_report(self, report_id: str) -> fieldobs.FieldObservation:
        """Get a single field report from CAIC."""

        params = dict(
            obs_id=report_id,
        )

        resp = await self._classic_get(ClassicEndpoints.OBS_REPORT, params)
        page = await resp.text

        return fieldobs.FieldObservation.from_obs_page(page)
