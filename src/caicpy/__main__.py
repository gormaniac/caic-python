"""A CLI entry point for caicpy - meant for testing."""

import asyncio
from pprint import pprint

from ._args import MAIN_PARSER
from .client import CaicClient


async def main():
    """The caicpy CLI function."""

    args = MAIN_PARSER.parse_args()

    client = CaicClient()

    match args.command:
        case "avy-obs":
            obs = await client.avy_obs(args.start.isoformat(), args.end.isoformat())
            for ob in obs:
                print()
                pprint(ob.model_dump(exclude_none=True), indent=2)
                print()
        case "field-reports":
            obs = await client.field_reports(args.start.isoformat(), args.end.isoformat())
            for ob in obs:
                print()
                pprint(ob.model_dump(exclude_none=True), indent=2)
                print()
        case "field-report":
            obs = await client.field_report(args.id)
            pprint(obs.model_dump(exclude_none=True), indent=2)
        case "snowpack-observation":
            obs = await client.snowpack_observation(args.id)
            pprint(obs.model_dump(exclude_none=True), indent=2)
        case "avalanche-observation":
            obs = await client.avy_observation(args.id)
            pprint(obs.model_dump(exclude_none=True), indent=2)
        case "weather-observation":
            obs = await client.weather_observation(args.id)
            pprint(obs.model_dump(exclude_none=True), indent=2)
        case "bc-zone":
            obs = await client.bc_zone(args.id)
            pprint(obs.model_dump(exclude_none=True), indent=2)
        case "highway-zone":
            obs = await client.highway_zone(args.id)
            pprint(obs.model_dump(exclude_none=True), indent=2)
        case "avy-forecast":
            obs = await client.avy_forecast(args.date)
            for ob in obs:
                pprint(ob.model_dump(exclude_none=True), indent=2)

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
