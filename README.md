# satellite-rsr
## Purpose
Interactively examine relative spectral response (RSR) curves relative to other spaceborne spectral bands, relative 
to ground target reflectances. 

## Methodology
This work is largely based around improving the exiting (and functional) 
[Landsat Spectral Characteristics Viewer](https://landsat.usgs.gov/spectral-characteristics-viewer). Here, the same 
principles are reimplemented using the [Plotly (Dash) library](https://plotly.com/) in Python. This project aims 
to: 
1) make the plotting framework open-source,
2) make it easy for a user/developer to add or remove spectra, and
3) allow for creation of publication-grade figures within the web UI.

## Python environment
Requires two non-standard Python libraries:
- dash
- pandas

which will install other dependencies as needed.

Install using a `conda` one-liner: 
```
conda create --name dash python=3.8 dash pandas
```
The exact configuration used in development is provided in the `environment.yml` file, which can be loaded using: 
```
conda env create -f environment.yml
```

## Input data formats
## Satellite RSRs
- Stored in file [rsr_ALL.csv](./data/rsr_ALL.csv)
- Header: `wavelength_um,rsr_watts,sensor,band`

## Environmental RSRs
- Stored in file [env_spectra_ALL.csv](./data/env_spectra_ALL.csv)
- Header: `wavelength_um,rsr_watts,spectra_type`

## TODOs
- Add more sensors
  - Aqua, ASTER, EO-1 ALI (MODIS): https://mcst.gsfc.nasa.gov/calibration/parameters
  - Sentinel: https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi/document-library/-/asset_publisher/Wk0TKajiISaR/content/sentinel-2a-spectral-responses
  - VIIRS (Suomi NPP): https://ncc.nesdis.noaa.gov/VIIRS/VIIRSSpectralResponseFunctions.php
  - Commercial?
- Add more environmental spectra
  - Minerals
  - Water
  - Snow
  - Cloud/shadow
- Lookup table to prettify display text (e.g, `l8_oli` --> `L8 OLI`)

## Data Sources
### Satellite sensors
- Terra (MODIS): https://mcst.gsfc.nasa.gov/calibration/parameters

- Landsat: https://landsat.usgs.gov/spectral-characteristics-viewer

### Ground spectral features
- Landing page: https://crustal.usgs.gov/speclab/QueryAll07a.php
  - Lawn Grass (2228)
  - H2O Ice (1499)

## Dev notes
### Create `environment.yml`
```
conda env export > environment.yml
```

### Licensing
See [LICENSE.md](LICENSE.md).
