#!bin/uer/python3
""" figSelector.py """

import os
import csv
import sys
import whoosh as wh
from whoosh.qparser import QueryParser
import numpy as np
import readCSVData as c
import graphFunctions as graph
import pandas as pd
from matplotlib import pyplot as plt

# dictionary of functions and associated names
single_collage_dict = {
	"grad rate":graph.graduation_rate,
	"accept rate s":graph.admitance_rate,
	"cost":graph.cost_breakdown,
	"tuition change":graph.tuition_over_time,
}

multi_collage_dict = {
	"cost":graph.compare_costs,
	"accept rate m":graph.acceptance_rates,
	"headcount":graph.compare_population,
	"gender outcomes":graph.gender_outcomes_ratio,
}

num_axis_dict = {
	"grad rate":1,
	"accept rate s":2,
	"accept rate m":1,
	"cost":1,
	"tuition change":1,
	"headcount":1,
	"gender outcomes":1
}

fallback_dict = {
	1:graph.fallback_xkcd,
	2:graph.fallback_xkcd_2,
}

# dictionary of names and associated queries
# names corospond to functions in single and multi collage dictionarries
query_dict = {
	"grad rate":["graduation rate", "outcome", "results", "success"],
	"accept rate s":["acceptance rate", "chance", "application"],	
	"accept rate m":["acceptance rate", "chance", "application"],			
	"cost":["money", "expense", "tuition", "fee", "cost"],						# in both
	"tuition change":["money", "over time", "change"],
	"gender outcomes":["graduation rate", "outcome", "gender","male", "female"],
	"headcount":["population", "student body", "crowd", "class size"],
}

# set the number of graphs to draw
NUM_GRAPHS = 3


'''
Function to decide which three graphs to display
Calling this function will cause plt.show() which will pop out the graphs in a new window

@param {list} list of pages returned by search # TODO: refactor, can instead just take page title
@param {int} page, which page of results the graphs are for
@param {string} location of school data csv
@param {ix} whoosh index object
'''
def fig_selector(search_results, page, csv_dir, ix):
	school_data = c.read_csv_data(csv_dir)
	school_data.fillna(0)

	url = search_results[page]
	if ("USNews.com" in url) or ("niche.com" in url):
		# return group graphs
		school_list = data['institution name'].tolist()
		page_text = search_results[page].get("content")
		schools_to_graph = list()
		# loop through list of schools, if a school appears in the text of the page
		# add that school to the list of schools to graph
		for school in school_list:
			if school in page_text:
				schools_to_graph.append(school)

		# TODO: what do you do if school names are not explicitly in page
		if len(school_list) == 0:
			print("could not identify schools")
			fallback_figs()
			return

		# if page is from aggregator and refrences more then one school, do multi graphs
		if len(school_list) > 1:
			school_id = c.get_ID_from_name(school_data, school_list)

			graph_list = score_graphs(ix, multi_collage_dict, search_results[page])

	    	# count the number of graphs to draw, some draw more then one
			graph_count = 0
			for i in range(NUM_GRAPHS):
				graph_count += num_axis_dict.get(graph_list[1])

			fig, axs = plt.subplots(1,graph_count, figsize=(4*graph_count,2*graph_count))
			fig.subplots_adjust(wspace=0.5)
			i = 0
			# get graphs for graph list
			for ent in graph_list:
				tmp = num_axis_dict.get(ent[1])
				# increment by number of graphs to dray for func, not always one
				multi_collage_dict[ent[1]](axs[i:i+tmp-1], school_data, school_id)
				i+=tmp

			plt.show()
			return		
    	

#---------------------------------------------------------------------------------------------------
# Solo Graphs
	# return single graphs
	# figure out which school page belongs to
	site_list = data["HD2021.Institution's internet website address"].tolist()
	# strip excess data from urls
	for i in range(len(site_list)):
		if school_data[i] == 0:
			continue
		if "http://" in site_list[i]:
			site_list[i] = site_list[i][6:]
		if "https://" in site_list[i]:
			site_list[i] = site_list[i][7:]
		if "www." in site_list[i]:
			site_list[i] = site_list[i][4:]
	'''
	school_data["HD2021.Institution's internet website address"].where(
		~("http://" is in school_data["HD2021.Institution's internet website address"]),
		other=school_data["HD2021.Institution's internet website address"][6:], inplace=True)
	'''
	extra = {'url':site_list}
	school_data.append(pd.DataFrame(extra))

	# get id of school based on url of page
	school_id = None
	for index, row in school_data.iterrows():
		if row['url'] in url:
			school_id = row['unitid'].tolist()
			school_id=school_id[0]
			break

	# if page url is not in list of graphs
	if school_id == None:
		print("Error: could not identify school for page: "+str(search_results[page]))
		fallback_figs()
		return


	graph_list = score_graphs(ix, single_collage_dict, page_title, search_results[page])

	# count the number of graphs to draw, some draw more then one
	graph_count = 0
	for i in range(NUM_GRAPHS):
		graph_count += num_axis_dict.get(graph_list[1])

	fig, axs = plt.subplots(1,graph_count, figsize=(4*graph_count,2*graph_count))
	fig.subplots_adjust(wspace=0.5)
	i = 0
	# get graphs for graph list
	for ent in graph_list:
		tmp = num_axis_dict.get(ent[1])
		# increment by number of graphs to dray for func, not always one
		single_collage_dict[ent[1]](axs[i:i+tmp-1], school_data, school_id)
		i+=tmp

	plt.show()
	return


def draw_specific_graphs():
	pass
	# UNF: finction to draw graphs specified by user

# indivigual page score for eacy query from here:
# https://stackoverflow.com/questions/18670493/how-to-get-tf-idf-score-and-bm25f-score-of-a-term-in-a-document-using-whoosh
# graphs are scored based on TF-IDF
# @return {list} list of tuples (score, key)
def score_graphs(ix, graph_dict, page_title):
	for key in graph_dict.keys():
		query = ''
		for word in key:
			query += " "+str(word)
		qp = QueryParse('content', ix.schema)
		q = qp.parse(unicode('url:'+url))
		with ix.searcher(weighting=scoring.TF_IDF()) as searcher_tfidf:
			score = scoring.TFIDF().scorer(searcher_tfidf, 'body', query).score(q.matcher(searcher_tfidf))

		graph_list.append([score, key])
	# sort list by decending order of score then drop all but NUM_GRAPHS, draw remaining
	return graph_list.sort(reverse=True, key=__sort_helper)
	# TODO: What happens if asked to draw more graphs then are possible



# helper function for sort
# private
def __sort_helper(val):
	return val[0]

# get figs to draw if there are no other figs to draw
def fallback_figs():
	fig, axs = plt.subplots(1,2, figsize=(15,7))
	tmp = graph.fallback_xkcd(fig, axs[0])
	tmp = graph.fallback_xkcd_2(fig, axs[1])

	plt.title("You're not suppose to see these")
	plt.show()
