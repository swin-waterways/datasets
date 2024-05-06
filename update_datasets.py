#!/usr/bin/python

#################
# Update datasets
# This script downloads the latest versions of datasets from the datasets list and saves it in a consistent directory structure

# Imports
import aiohttp, asyncio, argparse, json, os, re, urllib.request
import pandas as pd

###################
# Program arguments
parser = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("outfile", default = "datasets.csv", nargs = "?", help = "Output CSV file with merged datasets")
parser.add_argument("-df", "--datasets-file", default = "datasets.json", help = "JSON file with list of datasets") # Allow passing in datasets file location, with a default location
parser.add_argument("-hf", "--headers-file", default = "headers.json", help = "JSON file with list of default URL headers") # Allow passing in default URL headers file location, with a default location
parser.add_argument("-t", "--tasks", action = "append", choices = ["mkdirs", "download", "merge", "output"], help = "List of tasks to run") # Allow passing in list of tasks to run, just one or none at all
args = parser.parse_args("")

# Read list of datasets from file
datasets = json.load(open(args.datasets_file, "r"))
# Read list of default URL headers
headers = json.load(open(args.headers_file, "r"))

#########################################
# Create directories if they do not exist
def create(datasets):
    print("Creating directories...")

    # Loop through datasets
    for d in datasets:
        dir = d["filename"].rsplit("/", 1)[0] # Extract directory from filename
        # Check that directory exists
        if not os.path.isdir(dir):
            os.makedirs(dir) # Create the directory
            print(f'\t{dir}') # Print out what directory was created

###################
# Download datasets
# Function to asynchronously download data from URL
async def download_url(session, url, filename):
    async with session.get(url) as resp:
        # Construct response dictionary
        response = {
            "url": url,
            "text": await resp.text(), # Response text
            "filename": filename
        }
        return response

async def download(datasets, headers):
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
                if d["url"] in headers:
                    d["headers"].update(headers[d["url"]]) # Add default headers to included headers
                # Add headers onto end of URL
                d["url"] = d["url"] + "?" + urllib.parse.urlencode(d["headers"])
            # Append download URL to async tasks list
            tasks.append(asyncio.ensure_future(download_url(session, d["url"], d["filename"])))

        # Download the files asynchronously
        responses = await asyncio.gather(*tasks)
        # Loop through responses
        for r in responses:
            # Save response text to file
            with open(r["filename"], "w") as file:
                file.write(r["text"])
                file.close()
            print(f'\t{r["url"]} --> {r["filename"]}') # Print out info about saved file and URL

################
# Merge datasets
def merge(datasets):
    print("Merging datasets...")

    dfs, locations = [], [] # Setup lists of datasets and locations

    # Loop through datasets
    for d in datasets:
        pd_args = {"filepath_or_buffer": d["filename"], "index_col": 0, "on_bad_lines": "skip"} # Setup pd args
        # Add additional args for MDBA datasets
        if d["url"].startswith("https://riverdata.mdba.gov.au"):
            pd_args.update({"header": 2, "skiprows": [3]}) # Remove most of the headers
        # Add additional args for BOM datasets
        elif d["url"].startswith("http://www.bom.gov.au"):
            pd_args.update({"header": 9}) # Remove most of the headers

        # Read CSV and append dataset to list of datasets
        dfs.append(pd.read_csv(**pd_args))
        # Trim down filename to get location
        location = re.sub("-", " ", re.sub("(\/\w+)*.csv$", "", re.sub("^(\w+\/){2}", "", d["filename"])))
        # Clean up location string
        location = re.sub("-", " ", location).title()
        # Append location name to list of locations
        locations.append(location)
        # Print out info about location
        print(f'\t{d["filename"]} ({location})')

    # Merge the dataframes together, putting locations in the index column and naming the DateTime column as Date
    return pd.concat(dfs, keys = locations, names = ["Location", "Date"]) 

#################
# Output datasets
def output(merged_df, outfile):
    print("Writing merged data...")

    # Write the dataframes to the output file
    merged_df.to_csv(outfile)
    # Print out output file location and confirmation
    print(f'\tWritten to {outfile}')

###############
# Run functions
# Check if running as a script
if __name__ == "__main__":
    # Populate tasks argument if no value was given
    if (args.tasks == None):
        args.tasks = ["mkdirs", "download", "merge", "output"]

    # Check if argument for task was given before running
    if ("mkdirs" in args.tasks):
        create(datasets)
    if ("download" in args.tasks):
        asyncio.run(download(datasets, headers)) # Run download datasets function asynchronously
    # Merge needs to be run for a dataset to be outputted
    if ("merge" in args.tasks or "output" in args.tasks):
        merged_df = merge(datasets)

        if ("output" in args.tasks):
            output(merged_df, args.outfile)
