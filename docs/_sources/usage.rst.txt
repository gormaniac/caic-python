Usage
=====

Using ``caicpy`` is straight-forward. The CAIC APIs do not require any authentication, all that is needed is an internet connection.

To get an idea of the data returned, or the endpoints you would like to use, you may start with the minimal ``caicpy`` CLI (``python3 -m caicpy --help``). The CLI uses subcommands that map to method names of ``caicpy.client.CaicClient`` (albeit with dash instead of an underscore).

To use ``caicpy`` as a library, start with the ``caicpy.client`` module. Other supporting modules may be used if calling code requires it.

Errors
------

Non-paginating ``caicpy.client.CaicClient`` methods (all except ``avy_obs`` and ``field_reports``) catch HTTP network errors and JSON decode errors and reraise them as ``caicpy.errors.CaicRequestException``s. Pydantic validation errors are caught and cause a return value of ``None``.

The paginating ``caicpy`` methods intercept exceptions to attempt retries. Exceptions are logged, but ultimately, these methods will return an empty list if too many errors ocurred. However, they may return partial data if errors ocurred but not enough to reach the max.

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
                        # HTTP GET request for ``asset.full_url``

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


    # Show me all field reports in 2012 and
    # map classic IDs to their new API UUID.
    reports_2012 = await client.field_reports(
        "2012-01-01 00:00:00",
        "2012-12-31 11:59:59",
    )

    id_map = {}
    for report in reports_2012:
        if (_id := report.avalanche_detail.classic_id):
            if _id not in id_map.keys():
                id_map[_id] = report.id
