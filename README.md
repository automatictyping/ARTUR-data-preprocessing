# ARTUR Data Processing

This repository contains Python scripts for data processing in the ARTUR project.

## Folder Structure

- **calculate-population**: Scripts for creating the population layer.
- **generate-data**: Scripts for generating dummy data.
- **geocoding**: Scripts using the Mapbox Geocoding API to generate coordinates.
- **isochrone**: Scripts for generating isochrones or catchment areas.

## Getting Started

### Prerequisites

- Python 3.x
- Required Python packages (listed in `requirements.txt`)
- `ogr2ogr` tool from the GDAL library

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/ARTUR-data-processing.git
   cd ARTUR-data-processing
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Install GDAL (which includes `ogr2ogr`):
   - On Ubuntu:
     ```bash
     sudo apt-get install gdal-bin
     ```
   - On macOS using Homebrew:
     ```bash
     brew install gdal
     ```
   - On Windows, download and install from the [OSGeo4W](https://trac.osgeo.org/osgeo4w/) installer.

````bash
python import_to_db.py

### Usage

#### Calculate Population

```bash
cd calculate-population
python3 population-overlay.py
````

#### Generate Data

```bash
cd generate-data
python3 generator.py
```

#### Geocoding

```bash
cd geocoding
python3 geocoding.py
```

#### Isochrone

```bash
cd isochrone
# for isochrones:
python3 isochrone.py
# for catchment areas:
python3 catchment.py
```

#### Import GeoJSON to PostGIS

To import GeoJSON files into the PostGIS database, use the `import_to_db.py` script. Ensure `ogr2ogr` is installed and accessible from your command line.
