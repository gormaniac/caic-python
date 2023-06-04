# caic-python

An async Python client for the [CAIC](https://avalanche.state.co.us) website data using the undocumented HTTP APIs.

`caic-python` is capable of retrieving information on the following from the CAIC website:
- Search field reports (aka observation reports) submitted to the CAIC website.
- Search avalanche observation reports submitted as part of a field report.
- Retrieve the CAIC's avalanche forecast on a given date.
- Retrieve information on CAIC's defined backcountry zones and highway zones.
- Retrieve individual observation objects of the following type:
    - Field Report
    - Avalanche Observation
    - Snowpack Observation
    - Weather Observation

Read the [full documentation](https://gormo.co/caic-python/) for further details. It is also available locally via `make read-docs` or the `docs/` directory.
