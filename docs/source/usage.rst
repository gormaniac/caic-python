Usage
=====

Using `caicpy` is straight-forward. The CAIC APIs do not require any authentication, all that is needed is an internet connection.

To get an idea of the data returned, or the endpoints you would like to use, you may start with the minimal `caicpy` CLI (`python3 -m caicpy --help`). The CLI uses subcommands that map to method names of `caicpy.client.CaicClient` (albeit with dash instead of an underscore).

To use `caicpy` as a library, start with the `caicpy.client` module. Other supporting modules may be used if calling code requires it.

Examples
--------

::

    import datetime

    from caicpy.client import CaicClient
    from caicpy.enums import (
        ObsTypes, ReportsSearchCrackObs, BCZoneTitles
    )

    now = datetime.datetime.now().isoformat()
    two_weeks_ago = (now - datetime.timedelta(days=14)).isoformat()

    client = CaicClient()

    # For every D3 avalanche in the last 2 weeks, print some detials.
    avy_observations = await client.avy_obs(two_weeks_ago, now)
    for avy in avy_observations:
        if avy.destructive_size.value == "D3":
            print(f"Aspect: {avy.aspect})
            print(f"Elevation: {avy.elevation_feet}")
            print(f"Area: {avy.area}")
            print(f"Description: {avy.description}")
            print(f"Classic ID: {avy.avalanche_detail.classic_id}")
            print(f"Field Report: {avy.observation_report.id}")

    field_reports = await client.field_reports(two_weeks_ago, now)

    # For every recent field report that has
    # multiple avalanches, download any attached images.
    for report in field_reports:
        if report.avalanche_observations_count > 1:
            if report.assets and len(report.assets) > 1:
                for asset in assets:
                    # There's also a VIDEO_ASSET type
                    if asset.type == ObsTypes.IMAGE_ASSET.value:
                        # HTTP GET request for `asset.full_url`

    # If a recent field report has a weather
    # observation, print the recorded temperature.
    for report in field_reports:
        if report.weather_observations_count >= 1:
            for weather_obs in report.weather_observations:
                print(f"Parent Field Report: {report.id}")
                print(f"Location: {weather_obs.location}")
                print(f"Temperature: {weather_obs.temperature}")

    # Some more refined field reports searches.

    # Show me all field reports from the Sawatch in
    # Jan 2023 that reported shooting cracks.
    jan_cracking_reports = await client.field_reports(
        "2023-01-01 00:00:00",
        "2023-01-31 11:59:59",
        bc_zones=[BCZoneTitles.SAWATCH],
        cracking_obs=[ReportsSearchCrackObs.SHOOTING]
    )

    # Show me all field reports in 2022 where an avalanche
    # was seen and the word "bluebird" appears in the report.
    bluebird_avys = await client.field_reports(
        "2022-01-01 00:00:00",
        "2022-12-31 11:59:59",
        query="bluebird",
        avy_seen=True,
    )

Why async?
----------

The author has a future project that will require the HTTP requests that this client makes to be asynchronous.

The author believes that asynchronous code will not hinder those that wish to use this library synchronously, but non-async code would hinder the author.

Conversion to a synchronous API should be simple enough, simply replace the `aiohttp` calls with `requests` calls and remove all the `await` statements. If you go about this work, please submit a PR that defines a `SyncCaicClient` class with a `CaicClient` compatible API so that others may benefit.
