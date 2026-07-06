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

There's a V2 of the avalanche_observations endpoint that we should switch to::

    https://api.avalanche.state.co.us/api/v2/avalanche_observations?

A field reports example API call::

    https://api.avalanche.state.co.us/api/v2/observation_reports?page=1&per=250&r[observed_at_gteq]=2023-05-14T06%3A00%3A00.000Z&r[observed_at_lteq]=2023-05-22T05%3A59%3A59.999Z&r[sorts][]=observed_at+desc&r[sorts][]=created_at+desc
    https://api.avalanche.state.co.us/api/v2/observation_reports?page=1&per=250&r[backcountry_zone_title_in][]=Front+Range&r[snowpack_observations_cracking_in][]=Minor&r[snowpack_observations_collapsing_in][]=Rumbling&r[observed_at_gteq]=2023-05-14T06:00:00.000Z&r[observed_at_lteq]=2023-05-22T05:59:59.999Z&r[sorts][]=observed_at+desc&r[sorts][]=created_at+desc
    https://api.avalanche.state.co.us/api/v2/observation_reports?page=1&per=250&r[observed_at_gteq]=2023-05-14T06:00:00.000Z&r[observed_at_lteq]=2023-05-22T05:59:59.999Z&r[saw_avalanche_eq]=true&r[sorts][]=observed_at%20desc&r[sorts][]=created_at%20desc

A forecast API call - must use the proxy for these - the avid API is behind auth::

    https://avalanche.state.co.us/api-proxy/avid?_api_proxy_uri=/products/all?datetime=2023-01-22T12:00:00.000Z&includeExpired=true

Weather dispatches API call - also a different domain::

    https://m.avalanche.state.co.us/api/dispatches/current?type=zone-weather-forecast

Example weather plot download::

    https://classic.avalanche.state.co.us/caic/obs_stns/hplot.php?title=VailResort%20CAVMM%20(10303%20ft)%20-%20Vail%20&%20Summit%20County&st=CAVMM&date=2023-05-22-06

Example Wind Rose download::

    https://classic.avalanche.state.co.us/caic/obs_stns/windrose.php?st=UP396&date=2023-01-12+17&elev=6325&unit=e&area=caic
    
Example Weather Station Tables - would require webpage scraping, but may be helpful::

    https://classic.avalanche.state.co.us/caic/obs_stns/zones.php?date=2023-05-25+17&stnlink=hourly&unit=e&flag=on&area=caic&span=6

"""

from json import JSONDecodeError
import time
import typing

import requests
import aiohttp
import aiohttp.http
import pydantic

from . import __version__
from . import errors
from . import LOGGER
from . import models


def list_to_plus_args(argslist: list) -> str:
    """Join a list of strings using +."""

    return "+".join(argslist)


class CaicURLs:
    """All the different CAIC URLs that the client needs.

    With the exception of the attr for the "home" site's URL, the other class
    attrs are named after their subdomain.
    """

    API: str = "https://api.avalanche.state.co.us"
    CLSC: str = "https://classic.avalanche.state.co.us"
    M: str = "https://m.avalanche.state.co.us"
    HOME: str = "https://avalanche.state.co.us"


class CaicApiEndpoints:
    """Endpoints for the CAIC API (``api.avalanche.state.co.us``)."""

    V1_AVY_OBS: str = "/api/avalanche_observations"
    AVY_OBS: str = "/api/v2/avalanche_observations"
    OBS_REPORT: str = "/api/v2/observation_reports"
    ZONES: str = "/api/v2/zones"
    ZONES_MAP: str = "/api/v2/zones/map"
    SNOWPACK_OBS: str = "/api/v2/snowpack_observations"
    WEATHER_OBS: str = "/api/v2/weather_observations"


class ProxyEndpoints:
    """The known CAIC proxy URLs.

    Some underlying APIs (eg. avid) require auth, and this proxy auths for you.
    """

    AVID: str = "/api-proxy/avid"
    DATA: str = "/api-proxy/caic_data_api"


class CaicClient:
    """An async HTTP client for the CAIC API(s)."""

    def __init__(self) -> None:
        self.headers = {
            "User-Agent": f"{aiohttp.http.SERVER_SOFTWARE} caic-python/{__version__}"
        }
        self.session = aiohttp.ClientSession()

    async def close(self) -> None:
        """Close the underlying session."""
        await self.session.close()

    async def _get(self, url: str, params: dict | list | None = None) -> dict:
        """
        Get a URL using this client.

        Meant to be ``CaicURLs`` agnostic, so pass in a full URL.

        Parameters
        ----------
        url : str
            The full URL, in other words, an attr of ``CaicURLs`` + an API endpoint.
        params : dict | None, optional
            Optional URL parameters to pass in - the CAIC
            APIs rely on params, by default None.

        Returns
        -------
        dict
            The return from ``aiohttp.ClientResponse.json`` if, this call, or
            the HTTP request itself, did not throw an error.

        Raises
        ------
        errors.CaicRequestException
            For common HTTP errors, a >400 response status,
            an ``aiohttp.ClientError``, or a ``JSONDecodeError``.
        """

        data = {}

        try:
            resp = await self.session.get(url, params=params)
            if resp.status >= 400:
                error = await resp.text()
                raise errors.CaicRequestException(
                    f"Error status from CAIC: {resp.status} - {error}"
                )

            data = await resp.json()

        except aiohttp.ClientError as err:
            raise errors.CaicRequestException(
                f"Error connecting to CAIC: {err}"
            ) from err
        except JSONDecodeError as err:
            raise errors.CaicRequestException(
                f"Error decoding CAIC response: {err}"
            ) from err

        else:
            return data

    async def _api_id_get(
        self, obj_id: str, endpoint: str, resp_model: pydantic.BaseModel
    ) -> models.FieldReport | None:
        resp_data = await self._get(f"{CaicURLs.API}/{endpoint}/{obj_id}.json")

        try:
            return resp_model(**resp_data)
        except pydantic.ValidationError as err:
            LOGGER.warning(
                "Error parsing '%s' response (ID: %s): %s", endpoint, obj_id, str(err)
            )
            return None

    async def _api_paginate_get(
        self, page: int, per: int, uri: str, params: typing.Mapping | None = None
    ) -> dict:
        """
        A paginated get request to the CAIC API.

        Only supports ``CaicURLs.API`` endpoints - these seem to be the only
        ones that need pagination.

        Parameters
        ----------
        page : int
            The page number to get from the API.
        per : int
            The number of items to get per page.
        uri : str
            The ``CaicURLs.API`` endpoint to get.
        params : typing.Mapping | None, optional
            Optional URL parameters to include with the get request.
            Do not include ``page`` and ``per`` in ``params`` as these values
            are overwritten/set by this method. By default None.

        Returns
        -------
        dict | None
            The API's JSON response as a dict.

        Raises
        ------
        errors.CaicRequestException
            If raised by ``_get``,
        """

        if params is None:
            params = {}

        params["per"] = per
        params["page"] = page

        data = await self._get(CaicURLs.API + uri, params=params)

        return data

    async def _api_paginator(
        self,
        endpoint: str,
        resp_model: pydantic.BaseModel,
        params: dict | None,
        per: int = 1000,
        page_limit: int = 100,
        retries: int = 2,
        total_retries: int = 10,
    ) -> list[pydantic.BaseModel]:
        """
        Loop over ``_api_paginate_get`` until done, or conditions are met.

        WARNING: The ``/api/observation_reports`` doesn't give us pagination metadata.
        This means it may be possible to get stuck in a loop if you intentionally
        bypass safeguards in this method.

        Loop exit conditions:
            - The total results from a given page are less than ``per`` - in other words,
            we're on the last page.
            - The TOTAL number of caught, logged, and then thrown out exceptions is
            equal to ``total_retries``.
            - The total number of pages retrieved by this method is equal to
            ``page_limit``.
                - If ``page_limit`` negative, this check is bypassed!
            - If ``resp_model`` is ``models.V1AvyObsResponse``, there is page metadata.
            The loop will exit when the metadata reports this method has retrieved
            the last page.
                - Keep in mind that the ``page_limit`` check described above
                trumps this check. Users may have to increase or disable page
                limit when calling this method on the ``api/avalanche_observations``
                endpoint.

        Parameters
        ----------
        endpoint : str
            The API endpoint to request.
        resp_model : pydantic.BaseModel
            The model used to cast the JSON body of each response to an object.
        params : dict | None, optional
            Optional parameters for the request, by default None.
        per : int, optional
            The number of items to request per page, by default 1000.
        page_limit : int, optional
            The maximum number of pages to get. Set this to a negative number
            to disable this limit. By default 100.
            DO NOT disable this limit if ``endpoint`` is ``/api/observation_reports``.
        retries : int, optional
            The number of retries on a given page before moving to the next page,
            by default 2.
        total_retries : int, optional
            The total number of retries before this method quits, by default 10.

        Returns
        -------
        list[pydantic.BaseModel]
            A list of the ``pydantic.BaseModel`` objects defined by ``resp_model``.
            An empty list may indicate no data or it may indicate that all requests
            failed.
        """

        page = 1
        paginating = True
        results = []
        retry_count = 0
        page_retries = 0

        while paginating:
            if retry_count == total_retries:
                if not results:
                    LOGGER.critical("All queries failed!")
                LOGGER.error("Reached the maximum number of query retries.")
                break

            try:
                resp = await self._api_paginate_get(page, per, endpoint, params)
            except Exception as err:  # pylint: disable=W0718
                LOGGER.error(
                    "Failed to request the CAIC endpoint '%s': %s", endpoint, err
                )
                if page_retries == retries:
                    page += 1
                    retry_count += 1
                    page_retries = 0
                else:
                    page_retries += 1
                    retry_count += 1
                continue

            if len(resp) < per:
                LOGGER.info("Got all the results for the query: %s", str(params))
                paginating = False

            try:
                if resp_model == models.V1AvyResponse:
                    obj = resp_model(**resp)
                else:
                    obj = [resp_model(**item) for item in resp]
            except pydantic.ValidationError as err:
                LOGGER.warning(
                    "Unable to validate response from the '%s' endpoint "
                    "(Page# %s - Query (%s)): %s",
                    endpoint,
                    page,
                    str(params),
                    str(err),
                )
                # Can't find a way around the duplicate code here.
                if page_retries == retries:
                    page += 1
                    retry_count += 1
                    page_retries = 0
                else:
                    page_retries += 1
                    retry_count += 1
                continue

            if page == page_limit:
                LOGGER.warning("Reached the page limit before all pages downloaded.")
                paginating = False

            # Special handling for V1AvyObsResponse objects.
            if resp_model == models.V1AvyResponse:
                if obj.meta.current_page == obj.meta.total_pages:
                    paginating = False
                # Just a sanity check to avoid infinite looping
                elif page >= obj.meta.total_pages:
                    LOGGER.debug("Paginating mismatch")
                    paginating = False

                results.extend(obj.data)

            else:
                results.extend(obj)

            page += 1

        return results

    async def _proxy_get(
        self, proxy_endpoint: str, proxy_uri: str, proxy_params: dict
    ) -> dict | list | None:
        """Get a URL from the avalanche.state.co.us API proxy.

        This is an endpoint that can proxy to other CAIC APIs.

        Parameters
        ----------
        proxy_endpoint : str
            The actual endpoint of the proxy to request, the real URI in the
            HTTP request. Can be any of ``ProxyEndpoints``.
        proxy_uri : str
            The URI used by the proxy in its request to the proxied API.
        proxy_params : dict
            URL parameters to pass in the request to the proxied API.

        Returns
        -------
        dict | list
            The response raw response, or None
        """
        proxy_params_str = "&".join([f"{k}={v}" for k, v in proxy_params.items()])
        params = {"_api_proxy_uri": f"{proxy_uri}?{proxy_params_str}"}
        return await self._get(CaicURLs.HOME + proxy_endpoint, params=params)

    async def avy_obs(
        self, start: str, end: str, page_limit: int = 1000, ver1: bool = False
    ) -> list[models.AvalancheObservation]:
        """Query for avalanche observations on the CAIC website.

        Supports both the v1 and v2 APIs. FWIW, the website still uses v1 for this
        particular endpoint. My guess is because it supports proper pagination
        unlike v2, which supports pagination but does not return pagination
        info in response objects so clients have to guess when they're done paging.

        ``start`` and ``end`` arguments should be in this format - ``YYYY-MM-DD HH:mm:ss``.
        However, the return of a ``datetime.datetime.isoformat()`` call works as well.
        
        Parameters
        ----------
        start : str
            Query for avalanches observed after at this day (and time).
        end : str
            Query for avalanches observed before this day (and time).
        page_limit : int, optional
            Limit per page results to this amount, by default 1000.
        ver1 : bool, optional
            Use the v1 endpoint instead, not recommended, by default False.

        Returns
        -------
        list[models.AvalancheObservation]
            A list of all avalanche observations returned by the query.
        """

        if ver1:
            endpoint = "/api/avalanche_observations"
            model = models.V1AvyResponse
        else:
            endpoint = "/api/v2/avalanche_observations"
            model = models.AvalancheObservation

        params = {
            "observed_after": start,
            "observed_before": end,
            "t": str(int(time.time())),
        }

        obs = await self._api_paginator(
            endpoint,
            model,
            params=params,
            page_limit=page_limit,
        )

        return obs

    async def field_reports(  # pylint: disable=W0102
        self,
        start: str,
        end: str,
        bc_zones: list[str] = [],
        cracking_obs: list[str] = [],
        collapsing_obs: list[str] = [],
        query: str = "",
        avy_seen: bool | None = None,
        page_limit: int = 100,
    ) -> list[models.FieldReport]:
        """
        Search CAIC field reports.

        Replicates the search on the CAIC ``View Field Reports`` page.

        Parameters
        ----------
        start : str
            The start time for the query (observations after this date[+time]).
        end : str
            The end time for the query (observations before this date[+time]).
        bc_zones : list[str], optional
            One or more Backcountry Zones to limit the search results by.
            Should be one of ``enums.BCZoneTitles``. By default [].
        cracking_obs : list[str], optional
            One or more Cracking Observations to limit the search results by.
            Should be one of ``enums.CrackingObsNames``. By default [].
        collapsing_obs : list[str], optional
            One or more Collapsing Observations to limit the search results by.
            Should be one of ``enums.CollapsingObsNames``. By default [].
        query : str, optional
            A query string to limit searches by, by default "".
        avy_seen : bool | None, optional
            Whether an avalanche was seen, or None to disable this search
            modifier, by default None.
        page_limit : int, optional
            Limit the number of pages returned by the API. Must be at least 1
            or a value error is raised. By default 100.

        Returns
        -------
        list[models.FieldReport]
            All field reports returned by the search.

        Raises
        ------
        ValueError
            If ``page_limit`` is less than 1.

        """

        if page_limit <= 0:
            raise ValueError("A page_limit MUST be set for field_reports!")

        params = {
            "r[backcountry_zone_title_in][]": list_to_plus_args(bc_zones),
            "r[snowpack_observations_cracking_in]": list_to_plus_args(cracking_obs),
            "r[snowpack_observations_collapsing_in][]": list_to_plus_args(
                collapsing_obs
            ),
            "q": query,
            "r[saw_avalanche_eq]": avy_seen,
            "r[observed_at_gteq]": start,
            "r[observed_at_lteq]": end,
            "r[sorts][]": "observed_at+desc",  # We'll hard code this.
        }

        # Sanitize params
        params = {k: v for k, v in params.items() if v not in (None, "")}

        obs = await self._api_paginator(
            "/api/v2/observation_reports",
            models.FieldReport,
            params=params,
            page_limit=page_limit,
        )

        return obs

    async def field_report(self, report_id: str) -> models.FieldReport | None:
        """Get a single CAIC Feild Report (aka Observation Report) by UUID.

        Parameters
        ----------
        report_id : str
            The UUID of the field report to retrieve.

        Returns
        -------
        models.FieldReport | None
            The retrieved field report, or
            None if there was an error validating response.
        """

        report = await self._api_id_get(
            report_id, CaicApiEndpoints.OBS_REPORT, models.FieldReport
        )

        return report

    async def snowpack_observation(
        self, obs_id: str
    ) -> models.SnowpackObservation | None:
        """Get a single snowpack observation by UUID.

        Parameters
        ----------
        obs_id : str
            The ID of the snowpack observation.

        Returns
        -------
        models.SnowpackObservation | None
            The retrieved snowpack observation, or
            None if there was an error validating response.
        """

        report = await self._api_id_get(
            obs_id, CaicApiEndpoints.SNOWPACK_OBS, models.SnowpackObservation
        )

        return report

    async def avy_observation(self, obs_id: str) -> models.AvalancheObservation | None:
        """Get a single avalanche observation by UUID.

        Parameters
        ----------
        obs_id : str
            The UUID of the avalanche observation.

        Returns
        -------
        models.AvalancheObservation | None
            The retrieved avalanche observation, or
            None if there was an error validating response.
        """

        report = await self._api_id_get(
            obs_id, CaicApiEndpoints.AVY_OBS, models.AvalancheObservation
        )

        return report

    async def weather_observation(
        self, obs_id: str
    ) -> models.WeatherObservation | None:
        """Get a single weather observation by UUID.

        Parameters
        ----------
        obs_id : str
            The UUID of the weather observation.

        Returns
        -------
        models.WeatherObservation | None
            The retrieved weather observation, or
            None if there was an error validating response.
        """
        report = await self._api_id_get(
            obs_id, CaicApiEndpoints.WEATHER_OBS, models.WeatherObservation
        )

        return report

    async def bc_zone(self, zone_slug: str) -> models.BackcountryZone | None:
        """Get a single backcountry zone by UUID.

        Parameters
        ----------
        zone_slug : str
            The zone's slug name.

        Returns
        -------
        models.BackcountryZone | None
            The backcountry zone, or
            None if there was an error validating response.
        """

        report = await self._api_id_get(
            zone_slug, CaicApiEndpoints.ZONES, models.BackcountryZone
        )

        return report

    async def highway_zone(self, zone_slug: str) -> models.HighwayZone | None:
        """Get a single highway zone by UUID.

        Parameters
        ----------
        zone_slug : str
            The zone's slug name.

        Returns
        -------
        models.HighwayZone | None
            The highway zone, or
            None if there was an error validating response.
        """

        report = await self._api_id_get(
            zone_slug, CaicApiEndpoints.ZONES, models.HighwayZone
        )

        return report

    async def avy_forecast(
        self, date: str
    ) -> list[models.AvalancheForecast | models.RegionalDiscussionForecast]:
        """Get the avalanche forecasts as they were on the given date.

        Forecasts cover the date given + the following two days.

        Parameters
        ----------
        date : str
            The date that the avalanche forecast was produced for.

        Returns
        -------
        list[models.AvalancheForecast | models.RegionalDiscussionForecast]
            A list of returned forecasts. The list should contain two types.
            The localized forecast for detailed areas of CO, and the regional
            discussion pieces that cover broader portions of the state.
        """

        params = {"datetime": date, "includeExpired": "true"}
        resp = await self._proxy_get(
            proxy_endpoint=ProxyEndpoints.AVID,
            proxy_uri="/products/all",
            proxy_params=params,
        )

        ret = []

        if resp:
            try:
                for item in resp:
                    if (
                        isinstance(item, dict)
                        and item.get("type") == "avalancheforecast"
                    ):
                        ret.append(models.AvalancheForecast(**item))
                    else:
                        ret.append(models.RegionalDiscussionForecast(**item))
            except pydantic.ValidationError as err:
                LOGGER.error("Unable to decode forecast response: %s", str(err))

        return ret

class SyncCaicClient:
    """A syncronous HTTP client for the CAIC API(s)."""

    def __init__(self) -> None:
        self.headers = {
            "User-Agent": f"caic-python/{__version__}"
        }
        self.session = requests.Session()

    def close(self) -> None:
        """Close the underlying session."""
        self.session.close()

    def _get(self, url: str, params: dict | list | None = None) -> dict:
        """
        Get a URL using this client.

        Meant to be ``CaicURLs`` agnostic, so pass in a full URL.

        Parameters
        ----------
        url : str
            The full URL, in other words, an attr of ``CaicURLs`` + an API endpoint.
        params : dict | None, optional
            Optional URL parameters to pass in - the CAIC
            APIs rely on params, by default None.

        Returns
        -------
        dict
            The return from ``requests.Response.json`` if, this call, or
            the HTTP request itself, did not throw an error.

        Raises
        ------
        errors.CaicRequestException
            For common HTTP errors, a >400 response status,
            a ``requests.RequestException``, or a ``JSONDecodeError``.
        """

        data = {}

        try:
            resp = self.session.get(url, params=params)
            print("Response status:", resp.status_code)
            if resp.status_code >= 400:
                error = resp.text
                raise errors.CaicRequestException(
                    f"Error status from CAIC: {resp.status_code} - {error}"
                )
        
            # print("Response JSON:", resp.json())  # Debugging
            data = resp.json()

        except requests.RequestException as err:
            raise errors.CaicRequestException(
                f"Error connecting to CAIC: {err}"
            ) from err
        except JSONDecodeError as err:
            raise errors.CaicRequestException(
                f"Error decoding CAIC response: {err}"
            ) from err

        else:
            return data

    def _api_id_get(
        self, obj_id: str, endpoint: str, resp_model: pydantic.BaseModel
    ) -> models.FieldReport | None:
        resp_data = self._get(f"{CaicURLs.API}/{endpoint}/{obj_id}.json")

        try:
            return resp_model(**resp_data)
        except pydantic.ValidationError as err:
            LOGGER.warning(
                "Error parsing '%s' response (ID: %s): %s", endpoint, obj_id, str(err)
            )
            return None

    def _api_paginate_get(
        self, page: int, per: int, uri: str, params: typing.Mapping | None = None
    ) -> dict:
        """
        A paginated get request to the CAIC API.

        Only supports ``CaicURLs.API`` endpoints - these seem to be the only
        ones that need pagination.

        Parameters
        ----------
        page : int
            The page number to get from the API.
        per : int
            The number of items to get per page.
        uri : str
            The ``CaicURLs.API`` endpoint to get.
        params : typing.Mapping | None, optional
            Optional URL parameters to include with the get request.
            Do not include ``page`` and ``per`` in ``params`` as these values
            are overwritten/set by this method. By default None.

        Returns
        -------
        dict | None
            The API's JSON response as a dict.

        Raises
        ------
        errors.CaicRequestException
            If raised by ``_get``,
        """

        if params is None:
            params = {}

        params["per"] = per
        params["page"] = page

        print(CaicURLs.API + uri)
        data = self._get(CaicURLs.API + uri, params=params)

        return data

    def _api_paginator(
        self,
        endpoint: str,
        resp_model: pydantic.BaseModel,
        params: dict | None,
        per: int = 1000,
        page_limit: int = 100,
        retries: int = 2,
        total_retries: int = 10,
    ) -> list[pydantic.BaseModel]:
        """
        Loop over ``_api_paginate_get`` until done, or conditions are met.

        WARNING: The ``/api/observation_reports`` doesn't give us pagination metadata.
        This means it may be possible to get stuck in a loop if you intentionally
        bypass safeguards in this method.

        Loop exit conditions:
            - The total results from a given page are less than ``per`` - in other words,
            we're on the last page.
            - The TOTAL number of caught, logged, and then thrown out exceptions is
            equal to ``total_retries``.
            - The total number of pages retrieved by this method is equal to
            ``page_limit``.
                - If ``page_limit`` negative, this check is bypassed!
            - If ``resp_model`` is ``models.V1AvyObsResponse``, there is page metadata.
            The loop will exit when the metadata reports this method has retrieved
            the last page.
                - Keep in mind that the ``page_limit`` check described above
                trumps this check. Users may have to increase or disable page
                limit when calling this method on the ``api/avalanche_observations``
                endpoint.

        Parameters
        ----------
        endpoint : str
            The API endpoint to request.
        resp_model : pydantic.BaseModel
            The model used to cast the JSON body of each response to an object.
        params : dict | None, optional
            Optional parameters for the request, by default None.
        per : int, optional
            The number of items to request per page, by default 1000.
        page_limit : int, optional
            The maximum number of pages to get. Set this to a negative number
            to disable this limit. By default 100.
            DO NOT disable this limit if ``endpoint`` is ``/api/observation_reports``.
        retries : int, optional
            The number of retries on a given page before moving to the next page,
            by default 2.
        total_retries : int, optional
            The total number of retries before this method quits, by default 10.

        Returns
        -------
        list[pydantic.BaseModel]
            A list of the ``pydantic.BaseModel`` objects defined by ``resp_model``.
            An empty list may indicate no data or it may indicate that all requests
            failed.
        """

        page = 1
        paginating = True
        results = []
        retry_count = 0
        page_retries = 0

        while paginating:
            if retry_count == total_retries:
                if not results:
                    LOGGER.critical("All queries failed!")
                LOGGER.error("Reached the maximum number of query retries.")
                break

            try:
                resp = self._api_paginate_get(page, per, endpoint, params)
            except Exception as err:  # pylint: disable=W0718
                LOGGER.error(
                    "Failed to request the CAIC endpoint '%s': %s", endpoint, err
                )
                if page_retries == retries:
                    page += 1
                    retry_count += 1
                    page_retries = 0
                else:
                    page_retries += 1
                    retry_count += 1
                continue

            if len(resp) < per:
                LOGGER.info("Got all the results for the query: %s", str(params))
                paginating = False

            try:
                if resp_model == models.V1AvyResponse:
                    obj = resp_model(**resp)
                else:
                    obj = [resp_model(**item) for item in resp]
            except pydantic.ValidationError as err:
                LOGGER.warning(
                    "Unable to validate response from the '%s' endpoint "
                    "(Page# %s - Query (%s)): %s",
                    endpoint,
                    page,
                    str(params),
                    str(err),
                )
                # Can't find a way around the duplicate code here.
                if page_retries == retries:
                    page += 1
                    retry_count += 1
                    page_retries = 0
                else:
                    page_retries += 1
                    retry_count += 1
                continue

            if page == page_limit:
                LOGGER.warning("Reached the page limit before all pages downloaded.")
                paginating = False

            # Special handling for V1AvyObsResponse objects.
            if resp_model == models.V1AvyResponse:
                if obj.meta.current_page == obj.meta.total_pages:
                    paginating = False
                # Just a sanity check to avoid infinite looping
                elif page >= obj.meta.total_pages:
                    LOGGER.debug("Paginating mismatch")
                    paginating = False

                results.extend(obj.data)

            else:
                results.extend(obj)

            page += 1

        return results

    def _proxy_get(
        self, proxy_endpoint: str, proxy_uri: str, proxy_params: dict
    ) -> dict | list | None:
        """Get a URL from the avalanche.state.co.us API proxy.

        This is an endpoint that can proxy to other CAIC APIs.

        Parameters
        ----------
        proxy_endpoint : str
            The actual endpoint of the proxy to request, the real URI in the
            HTTP request. Can be any of ``ProxyEndpoints``.
        proxy_uri : str
            The URI used by the proxy in its request to the proxied API.
        proxy_params : dict
            URL parameters to pass in the request to the proxied API.

        Returns
        -------
        dict | list
            The response raw response, or None
        """
        proxy_params_str = "&".join([f"{k}={v}" for k, v in proxy_params.items()])
        params = {"_api_proxy_uri": f"{proxy_uri}?{proxy_params_str}"}
        return self._get(CaicURLs.HOME + proxy_endpoint, params=params)

    def avy_obs(
        self, start: str, end: str, page_limit: int = 1000, ver1: bool = False
    ) -> list[models.AvalancheObservation]:
        """Query for avalanche observations on the CAIC website.

        Supports both the v1 and v2 APIs. FWIW, the website still uses v1 for this
        particular endpoint. My guess is because it supports proper pagination
        unlike v2, which supports pagination but does not return pagination
        info in response objects so clients have to guess when they're done paging.

        ``start`` and ``end`` arguments should be in this format - ``YYYY-MM-DD HH:mm:ss``.
        However, the return of a ``datetime.datetime.isoformat()`` call works as well.
        
        Parameters
        ----------
        start : str
            Query for avalanches observed after at this day (and time).
        end : str
            Query for avalanches observed before this day (and time).
        page_limit : int, optional
            Limit per page results to this amount, by default 1000.
        ver1 : bool, optional
            Use the v1 endpoint instead, not recommended, by default False.

        Returns
        -------
        list[models.AvalancheObservation]
            A list of all avalanche observations returned by the query.
        """

        if ver1:
            endpoint = "/api/avalanche_observations"
            model = models.V1AvyResponse
        else:
            endpoint = "/api/v2/avalanche_observations"
            model = models.AvalancheObservation

        params = {
            "observed_after": start,
            "observed_before": end,
            "t": str(int(time.time())),
        }

        obs = self._api_paginator(
            endpoint,
            model,
            params=params,
            page_limit=page_limit,
        )

        return obs

    def field_reports(  # pylint: disable=W0102
        self,
        start: str,
        end: str,
        bc_zones: list[str] = [],
        cracking_obs: list[str] = [],
        collapsing_obs: list[str] = [],
        query: str = "",
        avy_seen: bool | None = None,
        page_limit: int = 100,
    ) -> list[models.FieldReport]:
        """
        Search CAIC field reports.

        Replicates the search on the CAIC ``View Field Reports`` page.

        Parameters
        ----------
        start : str
            The start time for the query (observations after this date[+time]).
        end : str
            The end time for the query (observations before this date[+time]).
        bc_zones : list[str], optional
            One or more Backcountry Zones to limit the search results by.
            Should be one of ``enums.BCZoneTitles``. By default [].
        cracking_obs : list[str], optional
            One or more Cracking Observations to limit the search results by.
            Should be one of ``enums.CrackingObsNames``. By default [].
        collapsing_obs : list[str], optional
            One or more Collapsing Observations to limit the search results by.
            Should be one of ``enums.CollapsingObsNames``. By default [].
        query : str, optional
            A query string to limit searches by, by default "".
        avy_seen : bool | None, optional
            Whether an avalanche was seen, or None to disable this search
            modifier, by default None.
        page_limit : int, optional
            Limit the number of pages returned by the API. Must be at least 1
            or a value error is raised. By default 100.

        Returns
        -------
        list[models.FieldReport]
            All field reports returned by the search.

        Raises
        ------
        ValueError
            If ``page_limit`` is less than 1.

        """

        if page_limit <= 0:
            raise ValueError("A page_limit MUST be set for field_reports!")

        params = {
            "r[backcountry_zone_title_in][]": list_to_plus_args(bc_zones),
            "r[snowpack_observations_cracking_in]": list_to_plus_args(cracking_obs),
            "r[snowpack_observations_collapsing_in][]": list_to_plus_args(
                collapsing_obs
            ),
            "q": query,
            "r[saw_avalanche_eq]": avy_seen,
            "r[observed_at_gteq]": start,
            "r[observed_at_lteq]": end,
            "r[sorts][]": "observed_at+desc",  # We'll hard code this.
        }

        # Sanitize params
        params = {k: v for k, v in params.items() if v not in (None, "")}

        obs = self._api_paginator(
            "/api/v2/observation_reports",
            models.FieldReport,
            params=params,
            page_limit=page_limit,
        )

        return obs

    def field_report(self, report_id: str) -> models.FieldReport | None:
        """Get a single CAIC Feild Report (aka Observation Report) by UUID.

        Parameters
        ----------
        report_id : str
            The UUID of the field report to retrieve.

        Returns
        -------
        models.FieldReport | None
            The retrieved field report, or
            None if there was an error validating response.
        """

        report = self._api_id_get(
            report_id, CaicApiEndpoints.OBS_REPORT, models.FieldReport
        )

        return report

    def snowpack_observation(
        self, obs_id: str
    ) -> models.SnowpackObservation | None:
        """Get a single snowpack observation by UUID.

        Parameters
        ----------
        obs_id : str
            The ID of the snowpack observation.

        Returns
        -------
        models.SnowpackObservation | None
            The retrieved snowpack observation, or
            None if there was an error validating response.
        """

        report = self._api_id_get(
            obs_id, CaicApiEndpoints.SNOWPACK_OBS, models.SnowpackObservation
        )

        return report

    def avy_observation(self, obs_id: str) -> models.AvalancheObservation | None:
        """Get a single avalanche observation by UUID.

        Parameters
        ----------
        obs_id : str
            The UUID of the avalanche observation.

        Returns
        -------
        models.AvalancheObservation | None
            The retrieved avalanche observation, or
            None if there was an error validating response.
        """

        report = self._api_id_get(
            obs_id, CaicApiEndpoints.AVY_OBS, models.AvalancheObservation
        )

        return report

    def weather_observation(
        self, obs_id: str
    ) -> models.WeatherObservation | None:
        """Get a single weather observation by UUID.

        Parameters
        ----------
        obs_id : str
            The UUID of the weather observation.

        Returns
        -------
        models.WeatherObservation | None
            The retrieved weather observation, or
            None if there was an error validating response.
        """
        report = self._api_id_get(
            obs_id, CaicApiEndpoints.WEATHER_OBS, models.WeatherObservation
        )

        return report

    def bc_zone(self, zone_slug: str) -> models.BackcountryZone | None:
        """Get a single backcountry zone by UUID.

        Parameters
        ----------
        zone_slug : str
            The zone's slug name.

        Returns
        -------
        models.BackcountryZone | None
            The backcountry zone, or
            None if there was an error validating response.
        """

        report = self._api_id_get(
            zone_slug, CaicApiEndpoints.ZONES, models.BackcountryZone
        )

        return report

    def highway_zone(self, zone_slug: str) -> models.HighwayZone | None:
        """Get a single highway zone by UUID.

        Parameters
        ----------
        zone_slug : str
            The zone's slug name.

        Returns
        -------
        models.HighwayZone | None
            The highway zone, or
            None if there was an error validating response.
        """

        report = self._api_id_get(
            zone_slug, CaicApiEndpoints.ZONES, models.HighwayZone
        )

        return report

    def avy_forecast(
        self, date: str
    ) -> list[models.AvalancheForecast | models.RegionalDiscussionForecast]:
        """Get the avalanche forecasts as they were on the given date.

        Forecasts cover the date given + the following two days.

        Parameters
        ----------
        date : str
            The date that the avalanche forecast was produced for.

        Returns
        -------
        list[models.AvalancheForecast | models.RegionalDiscussionForecast]
            A list of returned forecasts. The list should contain two types.
            The localized forecast for detailed areas of CO, and the regional
            discussion pieces that cover broader portions of the state.
        """

        params = {"datetime": date, "includeExpired": "true"}
        resp = self._proxy_get(
            proxy_endpoint=ProxyEndpoints.AVID,
            proxy_uri="/products/all",
            proxy_params=params,
        )

        ret = []

        if resp:
            try:
                for item in resp:
                    if (
                        isinstance(item, dict)
                        and item.get("type") == "avalancheforecast"
                    ):
                        ret.append(models.AvalancheForecast(**item))
                    else:
                        ret.append(models.RegionalDiscussionForecast(**item))
            except pydantic.ValidationError as err:
                LOGGER.error("Unable to decode forecast response: %s", str(err))

        return ret