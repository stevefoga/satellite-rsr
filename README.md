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

## Demo
This is currently deployed in Heroku: https://satellite-rsr.herokuapp.com/. 

## Python environment
Requires two non-standard Python libraries:
- dash
- pandas
- gunicorn (only required if deploying)

which will install other dependencies as needed.

Install using a `conda` one-liner: 
```
conda create --name dash python=3.8 dash pandas gunicorn
```
The exact configuration used in development is provided in the `environment.yml` file, which can be loaded using: 
```
conda env create -f environment.yml
```

## Usage
### [plot_rsr.py](./plot_rsr.py)
- Script generates the full interface, and calls a local server, which will output its URL in the console. There are 
  some variables hard-coded at the top of the script, but it can be run as-is.

## Input data formats
## Satellite RSRs
- Stored in file [rsr_ALL.csv](./data/rsr_ALL.csv)
- Header: `wavelength_um,rsr_watts,sensor,band`

## Environmental RSRs
- Stored in file [env_spectra_ALL.csv](./data/env_spectra_ALL.csv)
- Header: `wavelength_um,rsr_watts,spectra_type`

## TODOs
- Configure Heroku to deploy from this repo's `main` branch (instead of Heroku git).
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

### Deploy to Heroku
Follow the [Plotly Deployment Guide](https://dash.plotly.com/deployment). Notes:
1) Initial setup on macos (Apple Silicon, requires `homebrew` and `xcode-select`):
```
arch -x86_64 brew install heroku/brew/heroku
```
2) To setup the Heroku CLI, follow Heroku's [Getting Started With Python](https://devcenter.heroku.com/articles/getting-started-with-python#set-up) 
   guide.
3) Setup [Procfile](Procfile) and add `plot_rsr` script.
4) Setup [requirements.txt](requirements.txt) using `pip` (there's a bug in pip that produces local paths for some 
   libs, so use `list --format=freeze` arguments to get around it):
```
pip list --format=freeze > requirements.txt
```
   - The build failed on `mkl*` dependencies, the solution was to remove all of them.
   - The build also failed on `setuptools=x.xx`, the solution was to remove the version requirement for `setuptools`.
5) Setup [runtime.txt](runtime.txt). 
6) Push to Heroku repo with `git push heroku main` 
    - If working from a local branch that is not `main`, use `git push heroku mybranch:main`

### Licensing
See [LICENSE.md](LICENSE.md).
