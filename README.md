# caicpy

An async Python client for the [CAIC](https://avalanche.state.co.us) website data using the undocumented HTTP APIs.

`caicpy` (will be) available on `PyPI`, run the following to get started!
```
pip3 install caicpy
```

`caicpy` is capable of retrieving information on the following from the CAIC website:
- Search field reports (aka observation reports) submitted to the CAIC website.
- Search avalanche observation reports submitted as part of a field report.
- Retrieve the CAIC's avalanche forecast on a given date.
- Retrieve information on CAIC's defined backcountry zones and highway zones.
- Retrieve individual observation objects of the following type:
    - Field Report
    - Avalanche Observation
    - Snowpack Observation
    - Weather Observation

See `docs/` for further information.

The `data` directory contains sample API responses that were used to help build this client. They are saved in this repository to aid future research.