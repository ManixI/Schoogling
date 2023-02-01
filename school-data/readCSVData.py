#!/usr/bin/python3

import pandas as pd
import numpy as np
import csv
import os
from sys import exit
from functools import lru_cache

# global variable for debuging, higher values print more debuging statements
verbose = 0

# set debuging text value
# @param {int} new debugging val
def set_verbose(val):
	verbose = val
	print("Set verbose to "+str(verbose))

# read all csvs in specified dir into pandas object
# @param {string} directory name
# @return {PandasDataframe}
@lru_cache() 
def read_csv_data(directory):
	if not os.path.exists(directory):
		print('ERROR: '+str(directory)+" dose not exist!")
		exit()
	file_list = os.listdir(directory)
	frame_list = list()
	'''
	for i in range(len(file_list)):
		# skip files that can't be read without dying
		try:
			tmp_df = pd.read_csv(file_list[i])
		except:
			if verbose > 0:
				print("error reading "+(str(file_list[i])))
			continue
		frame_list.append(tmp_df)
	'''
	data = pd.read_csv('CSV_1152022-131.csv')
	#data = pd.concat(frame_list, axis=1)
	data.fillna(0, inplace=True)
	data = data.T.drop_duplicates().T
	return data

# get all data on specific collage
# @param {PandasDataframe} collage data (can get from read_csv_data)
# @param {list} list of collage IDs
# @return {PandasDataframe} collage data
def get_data_on_collage(data, ids):
	frame_list = data.loc[data['unitid'].isin(ids)]
	#print(frame_list)
	return frame_list

# return a list of tuples with a school's name and ids
# @param {PandasDataframe} collage data
# @param {string} collage name
# @return {string} paired IDs and names
# TODO: Dose not work
def get_ID_from_name(data, name):
	data = get_data_on_collage(data, school_id)
	data.fillna(0)
	school_list = data['unitid'].tolist()
	return school_list[0]

def get_name_from_id(data, school_id):
	data = get_data_on_collage(data, school_id)
	data.fillna(0)
	school_list = data['institution name'].tolist()
	return school_list[0]

# take a field name and field value, and returns all urls of schools that match that value
# @param {void} field val, can be int, float, bool, or string
# @param {string} field_name
#
# @return {list} url list
def get_url_from_field(data, field_val, field_name):
	frame_list = data.loc[data[field_name].isin(field_val)]
	frame_list.fillna(0)
	url_list = frame_list["HD2021.Institution's internet website address"].tolist()
	return url_list


# get a list of school ids of schools in state
def get_schools_in_state(data, state):
	df = data.loc[data['HD2021.State abbreviation'] == state]
	return df[unitid].tolist()

# same as above but for states
def get_schools_in_city(data, city):
	df = data.loc[data['HD2021.City location of institution'] == city]
	return df[unitid].tolist()

# same as above but for zip codes
def get_schools_in_zip(data, zipc):
	df = data.loc[data['HD2021.ZIP code'] == zipc]
	return df[unitid].tolist()

# return schoold url given id
def get_school_url(data, school_id):
	return data.loc[data['unitid'] == name]['HD2021.Institution\'s internet website address'].index.values
#---------------------------------------------------------------------------------
