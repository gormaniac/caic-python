"""A CLI entry point for caicpy - meant for testing."""

import argparse
import asyncio

import datetime
import dateutil.parser

from .client import CaicClient


PARSER = argparse.ArgumentParser(
    description=__doc__,
)
SUBPARSER = PARSER.add_subparsers(dest="command", title="Commands")

AVY_OBS_PARSER = SUBPARSER.add_parser("avy-obs", description="Query avalanche obs.")
AVY_OBS_PARSER.add_argument(
    "-a",
    "--after",
    help="Observations recorded after this date (by default, 14 days ago).",
    type=dateutil.parser.parse,
    default=datetime.datetime.now() - datetime.timedelta(days=14),
)
AVY_OBS_PARSER.add_argument(
    "-b",
    "--before",
    help="Observations recorded before this date (by default, now).",
    type=dateutil.parser.parse,
    default=datetime.datetime.now(),
)
AVY_OBS_PARSER.add_argument(
    "-d",
    "--delta",
    help="A delta in days from '--before' - overrides '--after' if also given.",
    type=dateutil.parser.parse,
    default=None,
)


async def main():
    args = PARSER.parse_args()

    client = CaicClient()

    match args.command:
        case "avy-obs":
            obs = await client.avy_obs(args.before.isoformat(), args.after.isoformat())
            for ob in obs:
                print("\n", ob, "\n")
        case _:
            print("Unsupported command!")

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
