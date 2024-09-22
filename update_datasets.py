#!/usr/bin/env python

#################
# Update datasets
# This script downloads the latest versions of datasets from the datasets list and saves it in a consistent directory structure

# Imports
from datetime import datetime
import aiohttp, asyncio, argparse, json, os, re, urllib.request
import pandas as pd
# import pybomwater.bom_water

###################
# Program arguments
parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("output_dir", default = "output", nargs = "?", help = "Directory to output NMEA-formatted CSV files to")
parser.add_argument("output_datasets_file", default = "output/datasets.csv", nargs = "?", help = "Output CSV file with merged datasets")
parser.add_argument("output_metadata_file", default = "output/metadata.csv", nargs = "?", help = "Output CSV file with location metadata")
parser.add_argument("-bf", "--bom-config-file", default = "datasets/bom.json", help = "JSON file containing pybomwater configuration") # Allow passing in BOM config file location, with a default location
parser.add_argument("-dsf", "--datasets-file", default = "datasets/datasets.json", help = "JSON file with list of datasets") # Allow passing in datasets file location, with a default location
parser.add_argument("-dwf", "--delwp-datasets-file", default = "datasets/delwp_datasets.json", help = "JSON file with list of DELWP datasets") # Allow passing in DELWP datasets file location, with a default location
parser.add_argument("-hf", "--headers-file", default = "datasets/headers.json", help = "JSON file with list of default URL headers") # Allow passing in default URL headers file location, with a default location
parser.add_argument("-t", "--tasks", action = "append", choices = ["download", "merge", "output-csv", "output-json"], help = "List of tasks to run") # Allow passing in list of tasks to run, just one or none at all

# Check if running using an ipython kernel
try:
    get_ipython().__class__.__name__
    args = parser.parse_args("")
except NameError:
    args = parser.parse_args()

# Read pybomwater configuration file
bom_config = json.load(open(args.bom_config_file, "r"))
# Read list of datasets from file
datasets = json.load(open(args.datasets_file, "r"))
# Read list of DELWP datasets from file
delwp_datasets = json.load(open(args.delwp_datasets_file, "r"))
# Read list of default URL headers
headers = json.load(open(args.headers_file, "r"))

#########################################
# Create directories if they do not exist
def create(datasets, output_dir):
    print("Creating directories...")

    # Loop through datasets
    for d in datasets:
        dir = d["filename"].rsplit("/", 1)[0] # Extract directory from filename
        # Check if directory exists
        if not os.path.isdir(dir):
            os.makedirs(dir) # Create the directory
            print(f'\t{dir}/') # Print out what directory was created

    # Check if output directory exists
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir) # Create the directory
        print(f'\t{output_dir}/') # Print out what directory was created

###################
# Download datasets
# Function to asynchronously download data from URL
async def download_url(session, url, filename):
    async with session.get(url) as resp:
        # Construct response dictionary
        response = {
            "filename": url,
            "text": await resp.text(), # Response text
            "filename": filename
        }
        return response

# Download datasets from URLs in datasets.json
async def download_urls(datasets, headers):
    print("Downloading datasets...")

    # Set up aiohttp session
    async with aiohttp.ClientSession() as session:
        # Initialise tasks list
        tasks = []

        # Loop through datasets
        for d in datasets:
            # Check if dataset URL has included headers
            if "headers" in d:
                # Check if dataset URL has default headers
                if d["filename"] in headers:
                    d["headers"].update(headers[d["filename"]]) # Add default headers to included headers
                # Add headers onto end of URL
                d["filename"] = d["url"] + "?" + urllib.parse.urlencode(d["headers"])
            # Append download URL to async tasks list
            tasks.append(asyncio.ensure_future(download_url(session, d["filename"], d["filename"])))

        # Download the files asynchronously
        responses = await asyncio.gather(*tasks)
        # Loop through responses
        for r in responses:
            # Save response text to file
            with open(r["filename"], "w") as file:
                file.write(r["text"])
                file.close()
            print(f'\t{r["filename"]} --> {r["filename"]}') # Print out info about saved file and URL
    
# # Download BOM datasets with pybomwater
# def download_bom():
#     # Initialise pybomwater
#     bm = pybomwater.bom_water.BomWater()
#     # Set procedure and property to get
#     procedure = bm.procedures.Pat4_C_B_1_DailyMean
#     prop = bm.properties.Water_Course_Discharge
#
#     # Create rectangle boundary coordinates for Murray-Darling Basin
#     low_left_lat = -37.505032
#     low_left_long = 138.00
#     upper_right_lat = -24.00
#     upper_right_long = 154.00
#
#     lower_left_coords = f'{low_left_lat} {low_left_long}'
#     upper_right_coords = f'{upper_right_lat} {upper_right_long}'
#     coords = tuple((lower_left_coords, upper_right_coords))
#
#     # Set maximum begin and end time
#     t_begin = "2000-01-01T00:00:00+10"
#     t_end = datetime.strftime(datetime.now(), "%Y-%m-%dT00:00:00+10")
#
#     # Get all observations within an area provided by a shapefile
#     spatial_path = "geofabric/bom/mdb_buffer_1km.shp"
#     results = bm.get_spatially_filtered_observations(None, spatial_path, coords, prop, procedure, t_begin, t_end)
#     print(results)

################
# Merge datasets
#
# Merge DELWP datasets
def merge_delwp(delwp_datasets):
    print("Merging DELWP datasets...")
    # Read parameters from DELWP datasets file
    params = delwp_datasets["parameters"]
    # Output DataFrames
    datasets_df, metadata_df = pd.DataFrame(), pd.DataFrame()
    index_inc = 0 # Metadata index incrementer

    # Loop through each object in the DELWP datasets file
    for basin in delwp_datasets["basins"]:
        # Print basin name
        print(f'{basin["basin_name"]} Basin')
        # Create basin DataFrame with a Basin column
        basin_df = pd.DataFrame()

        # Read site metadata file for that basin
        site_metadata = pd.read_csv(f'{basin["dirname"]}/{params["metadata_file"]}')

        # Loop through each row (location in basin)
        for index, location in site_metadata.iterrows():
            # Create location DataFrame
            location_df = pd.DataFrame()
            # Get location directory location (lol)
            location_dir = str(location["Site ID"]) + params["location_dir_ext"]

            # Add new row to metadata DataFrame
            metadata_df = pd.concat([metadata_df, pd.DataFrame({"Site ID": location["Site ID"], "Basin": basin["basin_name"], "Location": location["Name"], "Latitude": location["Latitude"], "Longitude": location["Longitude"]}, index=[index_inc])])
            index_inc += 1

            # Loop through file in location directory
            for file in params["files"]:
                filename = f'{basin["dirname"]}/{location_dir}/{location["Site ID"]}.{file["file_ext"]}'
                # Check if the file exists first
                if os.path.isfile(filename):
                    # Read results from CSV (only use first two columns and replace the header names with the ones below)
                    measurement_df = pd.read_csv(filename, header=0, names=["Date", file["measurement"]], usecols=[0,1])
                    # Floor date strings to the hour and change Date column to DateTime data type
                    measurement_df["Date"] = pd.to_datetime(measurement_df["Date"].str.replace(":[0-9]{2}:[0-9]{2}$", '', regex=True))

                    # Do different actions to DF based on measurement
                    match file["measurement"]:
                        case "Rainfall":
                            # Sum all rainfall values for each hour
                            measurement_df = measurement_df.groupby("Date").sum()
                        case "Flow" | "Height":
                            # Use mean flow/height value for each hour
                            measurement_df = measurement_df.groupby("Date").mean()

                    # Insert site ID column
                    measurement_df.insert(0, "Site ID", location["Site ID"])

                    # Merge location_df and measurement_df
                    if location_df.empty:
                        location_df = measurement_df
                    else:
                        # Merge location_df and measurement_df together on common columns
                        location_df = pd.merge(location_df, measurement_df, on=["Site ID", "Date"], how="outer")
            # Print message about what is being merged
            print(f'\t{location["Name"]}', end='')
            # Sort all rows in location_df by Date
            try:
                location_df.sort_values("Date")
                print() # \n
            except:
                if location_df.empty:
                    # DataFrame is empty
                    print(f' \x1B[3m(No data for this location)\x1B[0m')
            # Concatenate basin_df and location_df
            basin_df = pd.concat([basin_df, location_df])
        # Concatenate output_df and basin_df
        datasets_df = pd.concat([datasets_df, basin_df])
    # Return output dfs
    return datasets_df, metadata_df


def merge(datasets):
    print("Merging datasets...")

    dfs, locations = [], [] # Setup lists of datasets and locations

    # Loop through datasets
    for d in datasets:
        pd_args = {"filepath_or_buffer": d["filename"], "index_col": 0, "on_bad_lines": "skip"} # Setup pd args
        # Add additional args for MDBA datasets
        if d["filename"].startswith("mdba"):
            pd_args.update({"header": 2, "skiprows": [3]}) # Remove most of the headers
        # Add additional args for BOM datasets
        elif d["filename"].startswith("bom"):
            pd_args.update({"header": 9}) # Remove most of the headers

        # Read CSV and append dataset to list of datasets
        dfs.append(pd.read_csv(**pd_args))
        # Get location
        location = d["location"]
        # Append location name to list of locations
        locations.append(location)
        # Print out info about location
        print(f'\t{d["filename"]} ({location})')

    # Merge the dataframes together, putting locations in the index column and naming the DateTime column as Date
    return pd.concat(dfs, keys = locations, names = ["Location", "Date"]) 

#################
# Output datasets
# Output to a single CSV file
def output_csv(merged_df, output_file):
    print("Writing merged data to a CSV file...")

    # Write the dataframes to the output file
    merged_df.to_csv(output_file)
    # Print out output file location and confirmation
    print(f'\tWritten to {output_file}')

# Output to formatted JSON files
def output_json(merged_df, output_dir):
    print("Writing merged data to JSON files...")

    ########################
    ## TODO: FILL THIS IN ##
    ########################

###############
# Run functions
# Check if running as a script
if __name__ == "__main__":
    # Populate tasks argument if no value was given
    if (args.tasks == None):
        args.tasks = ["download", "merge", "output-csv"]

    # Check if argument for task was given before running
    if ("download" in args.tasks):
        create(datasets, args.output_dir)
        asyncio.run(download_urls(datasets, headers)) # Run download datasets function asynchronously
    # Merge needs to be run for datasets to be outputted
    if ("merge" in args.tasks or "output-csv" in args.tasks or "output-nmea" in args.tasks):
        datasets, metadata = merge_delwp(delwp_datasets)
        # merged_df = merge(datasets)

        if ("output-csv" in args.tasks):
            output_csv(datasets, args.output_datasets_file)
            output_csv(metadata, args.output_metadata_file)
        if ("output-json" in args.tasks):
            output_json(datasets, args.output_dir)
