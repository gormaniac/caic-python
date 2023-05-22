"""This is the async client from my other attempt at this.

The goal is to adopt this, but also use the models/objects already defined in this module.
"""

import typing

import aiohttp


class Observation():
    def __init__(self, data: dict) -> None:
        self.data = data


class FieldReport:
    def __init__(self, data) -> None:
        self.data = data


class CaicClient:
    def __init__(self) -> None:
        self.headers = {}
        self.session = aiohttp.ClientSession(base_url="https://api.avalanche.state.co.us/")

    async def _get(self, uri: str, params: typing.Mapping | None = None):
        resp = await self.session.get(uri, params=params)
        data = await resp.json()
        return data

    async def _paginate_get(self, page: int, per: int, uri: str, params: typing.Mapping | None = None):
        if params is None:
            params = {}

        params["per"] = per
        params["page"] = page

        data = await self._get(uri, params=params)

        return data

    async def avy_obs(self, obs_before: str, obs_after: str) -> list[Observation]:
        paginating = True

        obs = []
        page = 1

        params = {
            "observed_after": obs_after,
            "observed_before": obs_before,
        }

        while paginating:
            obs_resp = await self._paginate_get(page, 1000, "/api/avalanche_observations", params)
            meta = obs_resp.get("meta", {})
            data = obs_resp.get("data", {})

            if meta:
                if meta.get("current_page", 0) == meta.get("total_pages", 0):
                    paginating = False
            else:
                paginating = False

            obs.extend([Observation(obs_json) for obs_json in data])

            page += 1

        return obs
