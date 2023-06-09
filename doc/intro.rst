Introduction
============

The ``caic-python`` package helps researchers explore `CAIC <https://avalanche.state.co.us>`_ data locally and programmatically rather than on the CAIC website.

``caic-python`` relies on the same API endpoints used by the CAIC website. Partial motivation for development of this package was to serve as pseodo-documentation for these endpoints as they are not documented elsewhere.

While the ``caic-python`` module exposes a CLI (via ``python3 -m caic-python ...``), it is intended mostly for testing. The primary use case of ``caic-python`` is as library code called by other programs.

``caic-python`` relies heavily on `Pydantic <https://docs.pydantic.dev/latest/>`_ models to validate response objects, and speed up development. Responses from CAIC APIs do not always contain values for all fields. As a result, most attributes of a ``caic-python`` Pydantic response model are optional, and may be ``None`` rather than a type appropriate default. Attempts were made to include all possible attributes of a response for a given endpoint for maximum use case coverage.

``caic-python`` is capable of retrieving information on the following from the CAIC website:

- Search field reports (aka observation reports) submitted to the CAIC website.
- Search avalanche observation reports submitted as part of a field report.
- Retrieve the CAIC's avalanche forecast on a given date.
- Retrieve information on CAIC's defined backcountry zones and highway zones.
- Retrieve individual observation objects of the following type:

    - Field Report
    - Avalanche Observation
    - Snowpack Observation
    - Weather Observation

Future versions of ``caic-python`` would like to include the following features:

- Weather forecast information
- Weather station information
- Weather station observation graphics
- Accident report details
- Further coverage of static avalanche reporting terms, abbreviations, codes, etc. in ``caic-python.enums``.

The data that helped build ``caic-python`` is stored in the `co-avy-research <https://github.com/gormaniac/co-avy-research/tree/main/data/caic-python>`_ repo.

Why async?
----------

The author has a future project that will require the HTTP requests this client makes to be asynchronous.

Conversion to a synchronous API should be easy enough, simply replace the ``aiohttp`` calls with ``requests`` calls and remove all the ``await`` statements. If you go about this work, please submit a PR that defines a ``SyncCaicClient`` class with a ``CaicClient`` compatible API so that others may benefit.
