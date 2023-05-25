"""A CLI entry point for caicpy - meant for testing."""

import asyncio

from ._args import MAIN_PARSER
from .client import CaicClient


async def main():
    args = MAIN_PARSER.parse_args()

    client = CaicClient()

    match args.command:
        case "avy-obs":
            obs = await client.avy_obs(args.start.isoformat(), args.end.isoformat())
            for ob in obs:
                print("\n", ob, "\n")
        case "field-reports":
            obs = await client.field_reports(args.start.isoformat(), args.end.isoformat())
            for ob in obs:
                print("\n", ob, "\n")
        case "field-report":
            obs = await client.field_report(args.id)
            print("\n", obs, "\n")
        case "snowpack-observation":
            obs = await client.snowpack_observation(args.id)
            print("\n", obs, "\n")
        case "avalanche-observation":
            obs = await client.avy_observation(args.id)
            print("\n", obs, "\n")
        case "weather-observation":
            obs = await client.weather_observation(args.id)
            print("\n", obs, "\n")
        case "bc-zone":
            obs = await client.bc_zone(args.id)
            print("\n", obs, "\n")
        case "highway-zone":
            obs = await client.highway_zone(args.id)
            print("\n", obs, "\n")
        case _:
            print("Unsupported command!")

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
