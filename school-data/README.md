# Collage Data Parser

## TODO:
- list collage IDs given state
- list collage IDs given city
- 4-5 graphs given list of collage IDs
- 4-5 graphs given signle collage
- list collages based on specific field

## General
This exists to read csv data on collages from https://nces.ed.gov/IPEDS/use-the-data
and return either plots based on the data, pandas dataframes of the data, or human
redable formating of the data.

## Dependancies
The big one is matplotlib
install with command: python3 -mpip install -U matplotlib

## Setup
Data must be in csv format
Store data in dedicated subdirectory

## Functions
### read_csv_data
read all csvs in specified dir into pandas object
@param {string} directory name
@return {PandasDataframe}

### get_data_on_collage
get all data on specific collage
@param {string} location of data in csv format
@param {string} collage ID as string
@return {PandasDataframe} collage data

## Data Headers (inc.)
- UNITID: School ID
- 