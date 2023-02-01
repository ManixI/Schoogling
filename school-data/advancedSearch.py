#!user/bin/python3
"""advancedSearch.py"""

import os
import sys
import pandas as pd
import whoosh.index as index
from whoosh.filedb.filestore import FileStorage
from whoosh import qparser
from whoosh.qparser import QueryParser
from whoosh.fields import *
from whoosh.query import Phrase
import readCSVData as c

'''
This function is for the advanced search feature
It is currently skeleton code
It will take arguments and use them to preform advanced search functions

Features:
NOTE: required
@param {string} whoos_index_dir, path to whoosh index directory
@param {string} page_dir, path tondirectory of scraped pages
@param {string} query, query as entered by user
@param {string} school_data_csv, path to school data csv
@param {string} ajacency_json, path to ajacency matrix jsonn

NOTE: Optional
@param {string} disjunctive querys
@param {list} list of strings that must be included in return
@param {list} list of states of collages to restrict to
@param {list} list of city of collages to retrict to
@param {list} list of zipcodes of collages to restrict to
@param {list} list of URLs the returned pages must fall within
@param {bool} use pagerang, do by default
@param {list} list of tages pages must fall withing (tages are one we define to use for determining graph)
<<<<<<< HEAD
=======
@param {string} controll of school (public/private), None returns both

>>>>>>> school-data

NOTE: return
@return {whooshResultsObject} returns the result of a whoosh search

'''

def advanced_search(whoosh_index_dir, page_dir, query, school_data_csv, ajacency_json, 
	disjunctive_query_list=None, exact_terms=None, state=None, city=None, zipcode=None, 
	school_id=None, url=None, use_pagerank=True, tages=None, public=None,
	):

	if not os.path.exists(whoosh_index_dir):
		print("Error: could not find whoosh directory: "+whoosh_index_dir)
		return None

	if not os.path.exists(page_dir):
		print("Error: could not find page directory: "+page_dir)
		return None

	if not os.path.exists(school_data_csv):
		print("Error: cound not find csv: "+school_data_csv+" errors may occure")

	if query == None or query == "":
		print("Error, no query")

	# only read csv if it will be used
	if (state!=None) or (city!=None) or (zipcode!=None) or (school_id!=None) or (public!=None):
		data = c.read_csv_data(school_data)
		url_set = set()
		if url != None:
			for i in url:
				url_set.push(i)

	# open index
	'''
	schema = Schema(url=ID(unique=True, stored=True), content=TEXT(stored=True), 
		title=TEXT(stored=True), desc=TEXT(stored=True), time=STORED)
	'''
	storage = FileStorage(whoosh_index_dir)
	ix = storage.open_index()
	qp = QueryParser("content", schema=ix.schema)

	# Start with broadest aspect, and narrow with each aditional param
	if use_pagerank == True:
		searcher = ix.searcher(weighting='''page rank here''')

	else:
		searcher = ix.searcher(weithging=scoring.TF_IDF())
		# use TF-IDF as that's what the fig selector uses

	# normal search
	q = qp.parse(query)
	results = searcher.search(q, limit=None)
	filter_list = list()
	#results = searcher.search(q, limit=None)

	# TODO: can speed up by not searching and instead building queries to filter/mask by
	# refrence: https://stackoverflow.com/questions/63057552/multi-field-search-whoosh-with-field-filters
	# build disjunctive query object for filter list
	if disjunctive_query_list != None:
		dis_parser = QueryParser("content", schema=ix.schema, group=qparser.OrGroup)
		q = dis_parser.parse(disjunctive_query_list)
		r = searcher.search(q, limit=1) # NOTE: is a limit of one correct?
		filter_list.append(r)
		#q = dis_parser.parse(disjunctive_query_list)
		#tmp_results = searcher.search(q, limit=None)

	# filter results based on location (if school site is associate with city/state/zip in csv)
	if state != None and state != []:
		for ent in state:
			tmp = c.get_url_from_field(data, ent, "HD2021.State abbreviation")
			for i in tmp:
				url_set.push(i)


	if city != None and city != []:
		for ent in city:
			tmp = c.get_url_from_field(data, ent, "HD2021.City location of institution")
			for i in tmp:
				url_set.push(i)

	if zipcode != None and zipcode != []:
		for ent in zipcode:
			tmp = c.get_url_from_field(data, ent, "HD2021.ZIP code")
			for i in tmp:
				url_set.push(i)

	# filter for school id
	if school_id != None and school_id != []:
		for ent in school_id:
			tmp = c.get_url_from_field(data, ent, "unitid")
			for i in tmp:
				url_set.push(i)

	# filter results for school ownership
	if public != None:
		for ent in school_id:
			tmp = c.get_url_from_field(data, ent, "HD2021.Sector of institution")
			for i in tmp:
				url_set.push(i)


	# UNF: needs to hanle list of urls not just url
	# build url query object for filter
	if url != None:
		url_str = ''
		for ent in url:
			url_str+= ent + ' ' 
		# NOTE: will a string of urls work as I think it will?
		url_parser = QueryParser("url", schema=ix.schema)
		q = url_parser.parse(url)
		r = searcher.search(q, limit=1)
		filter_list.append(r)


	# filter results for exact terms
	if exact_terms != None and exact_terms!= "":
		for ent in exact_terms:
			exact_list = ent.split(' ')
			p = Phrase("content",exact_list)
			exact_results = ix.searcher().search(p)
			filter_list.append(r)

			#results.filter(exact_results)
		
	# combine all filters in list
	if len(filter_list) > 0:
		# filter results by all resultsObjects in filter_list
		for r in filter_list:
			results.filter(r)
	else:
		results = searcher.search(q, limit=None)

	searcher.close()

	
	return results