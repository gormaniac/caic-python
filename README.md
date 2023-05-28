# caicpy

An async Python client for the [CAIC](https://avalanche.state.co.us) website data using the undocumented HTTP APIs.

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


For local installation there are 3 options:

- The make file
```bash
git clone https://github.com/gormaniac/caicpy.git
cd caicpy
make setup
make install-self
```
- The install script containing the above
```bash
curl https://raw.githubusercontent.com/gormaniac/caicpy/main/scripts/install.sh | bash
```
- Or build manually after cloning the repo and entering the project dir
```bash
pip3 install build setuptools
python3 -m build .
pip3 install dist/caicpy-<VERSION>.tar.gz
```
