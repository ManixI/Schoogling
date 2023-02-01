#!/usr/bin/python3

import os
import pandas as pd


# script to merge ajacency matrix json's into one file
def merge_jsons(directory, json_list):
	with open("reverse_index.json","a") as fp:
		for file in json_list:
			df = pd.read_json(directory+"/"+file, lines=True)
			df.to_json(fp, orient='records', lines=True)


# returns a list of all files in a directory
# dose not do error checking
# @param {string} dir name
# @return {list} list of file names
def list_of_json_files_in_dir(directory):
	#path = os.path.dirname(directory)
	file_list = os.listdir(directory)
	json_list = list()
	for i in range(len(file_list)):
		# drop files not ending in .json
		#print(file_list[i][-5:])
		#print(file_list[i])
		if file_list[i][-5:] == ".json":
			json_list.append(file_list[i])
	return json_list	


def cleanAdjList(adj_list, new_list_output):

	# remove useless URL's - i.e. URL's that we didn't crawl
	df = pd.read_json(adj_list, lines=True)
	i = 0
	URLlist = df['URL'].tolist()

	for k in URLlist:
		print(k)

	while i < len(URLlist):
		url = df.iloc[i][0]
		adj = df.iloc[i][1]
		newAdjList = list()
		for adj_url in adj:
			if adj_url in URLlist:
				newAdjList.append(adj_url)
		newdf = pd.DataFrame([[url], [newAdjList]])
		df.update(newdf)
		i += 1

	with open(new_list_output, "w") as fp:
            df.to_json(fp, orient='records', lines=True)

	# remove multiple outgoing links to same destination
		# not needed because of crawler's method for creating the adjacency list
	# remove self-loops (webpage pointing to itself)
		# not needed because of crawler's method for creating the adjacency list

if __name__ == "__main__":
	cleanAdjList("WSU-visited-domains.json", "cleaned-WSU-test.json")

#----------------------------------------------------------------------------
#print("test")
# generate list of json files in directory jsonTest
#json_list = list_of_json_files_in_dir('jsonTest')
#print(json_list)
# merge all jaons in list into single master json in same dir as script
#merge_jsons('jsonTest',json_list)