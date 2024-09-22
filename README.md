# Waterway Datasets
This repository contains waterway datasets from different sources across Victoria.

## Updating datasets
`update-datasets.py` is a Python script that can be used to download the latest versions of datasets.  
It reads from a list of datasets (by default `datasets.json`), and a list of default URL headers for downloading datasets (by default `headers.json`).

It can also merge datasets and output the merged datasets to a CSV file (by default `datasets.csv`).

### Requirements
- Python 3.10 - 3.12
- aiohttp library (`pip install aiohttp`)
- matplotlib library (`pip install matplotlib`)
- pandas library (`pip install pandas`)
- pybomwater library (`pip install git+https://github.com/csiro-hydroinformatics/pybomwater.git`)

## Folder structure
The current folder structure for datasets is as follows:

- **Source of data** (The org or company it came from)
- **River** (The river the data is from)
- **Location** (The specific location name)
- ***Variable** (Optionally: The variable being recorded)*

## DELWP Output
The output from the `merge_delwp` function contains the following variables:

- **Rainfall**: The sum of the total rainfall for each hour at a point.
- **Flow**/**Height**: The mean (average) flow/height of the river for each hour at a point.

## Geofabric files (BOM)
In the `geofabric/` folder, there are shapefiles representing river basins and river catchment areas.  
These shapefiles contain objects showing the geographic border of these areas, and are categorised as detailed below.

There is also a QGIS Project file containing data from the BOM, that contains a layer showing all river basins and one showing all river catchment areas in Australia.

### Requirements
- [QGIS](https://qgis.org/en/site/forusers/download.html) can open the shapefiles and the QGIS project file.

### Folder structure
The current folder structure for geofabric files is as follows:

- **Source of data** (The org or company it came from)
- **River** (The river basin or catchment area the shapefile represents)
