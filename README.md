# Waterway Datasets
This repository contains waterway datasets from different sources across Victoria.

## Updating datasets
`update-datasets.py` is a Python script that can be used to download the latest versions of datasets.  
It reads from a list of datasets (by default `datasets.json`), and a list of default URL headers for downloading datasets (by default `headers.json`).

### Requirements
- Python 3.9 or later
- aiohttp library (`pip install aiohttp`)
- pandas library (`pip install pandas`)

## Folder structure
The current folder structure for datasets is as follows:

- **Source of data** (The org or company it came from)
- **River** (What river the data is from)
- **Location** (The specific location name)
- ***Variable** (Optionally: The variable being recorded)*
