"""ArgumentParser for ``__main__``."""

import argparse
import datetime

import dateutil.parser


TIME_PARSER = argparse.ArgumentParser(add_help=False)
TIME_PARSER.add_argument(
    "-s",
    "--start",
    help="Observations recorded after this date (by default, 14 days ago).",
    type=dateutil.parser.parse,
    default=datetime.datetime.now() - datetime.timedelta(days=14),
)
TIME_PARSER.add_argument(
    "-e",
    "--end",
    help="Observations recorded before this date (by default, now).",
    type=dateutil.parser.parse,
    default=datetime.datetime.now(),
)
TIME_PARSER.add_argument(
    "-d",
    "--delta",
    help="A delta in days from to subtract from '--end' - overrides '--start' if also given.",
    type=dateutil.parser.parse,
    default=None,
)

ID_PARSER = argparse.ArgumentParser(add_help=False)
ID_PARSER.add_argument(
    "id", help="The ID (or slug if applicable) of the object to query for."
)

MAIN_PARSER = argparse.ArgumentParser(
    description="The caic-python CLI.",
    prog="python3 -m caic_python"
)
MAIN_PARSER.add_argument(
    "--debug",
    help="Display debug output.",
    action="store_true",
)
MAIN_PARSER.add_argument(
    "--version",
    help="Display the version and exit.",
    action="store_true",
)
SUBPARSER = MAIN_PARSER.add_subparsers(dest="command", title="Commands")

AVY_OBS_PARSER = SUBPARSER.add_parser(
    "avy-obs", description="Query avalanche observations.", parents=[TIME_PARSER]
)
FIELD_REPORTS_PARSER = SUBPARSER.add_parser(
    "field-reports",
    description="Query field (or observation) report.",
    parents=[TIME_PARSER],
)
FIELD_REPORT_PARSER = SUBPARSER.add_parser(
    "field-report",
    description="Query for a single field (or observation) report.",
    parents=[ID_PARSER],
)
SNOWPACK_PARSER = SUBPARSER.add_parser(
    "snowpack-observation",
    description="Query for a single Snowpack Observation.",
    parents=[ID_PARSER],
)
AVALANCHE_PARSER = SUBPARSER.add_parser(
    "avalanche-observation",
    description="Query for a single Avalanche Observation.",
    parents=[ID_PARSER],
)
WEATHER_PARSER = SUBPARSER.add_parser(
    "weather-observation",
    description="Query for a single Weather Observation.",
    parents=[ID_PARSER],
)
BZONE_PARSER = SUBPARSER.add_parser(
    "bc-zone",
    description="Query for a single Backcountry Zone.",
    parents=[ID_PARSER],
)
HZONE_PARSER = SUBPARSER.add_parser(
    "highway-zone",
    description="Query for a single Highway Zone.",
    parents=[ID_PARSER],
)
AVYFORECAST_PARSER = SUBPARSER.add_parser(
    "avy-forecast",
    description="Query for a the avalanche forecast on the given date.",
)
AVYFORECAST_PARSER.add_argument(
    "-d",
    "--date",
    help="The date (and optional time) to get the forecast for.",
    type=dateutil.parser.parse,
    default=datetime.datetime.now(),
)
