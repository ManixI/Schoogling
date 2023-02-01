from flask import Flask, render_template, url_for, request, Response
from flask_paginate import Pagination, get_page_args
import whoosh
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import qparser
import os
import sys
import pandas as pd
import io
import random
import requests
from bs4 import BeautifulSoup
import json
import operator

from figures import figSelector as select
import matplotlib.pyplot as plt, mpld3

import advancedSearch


#from flask_paginate import Pagination, get_page_args


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	print("Someone is at the home page.")
	return render_template('original.html')

@app.route('/my-link/')
def my_link():
	print('I got clicked!')
	return 'Click.'

def get_results(offset=0, per_page=10):
	global mySearcher
	if request.method == 'POST':
		data = request.form
	else:
		data = request.args

	query = data.get('searchterm')
	exact_terms = data.get('exact_terms')
	state = data.get('state')
	city = data.get('city')
	zipcode = data.get('zipcode')
	school_id = data.get('school_id')
	url = data.get('url')
	disjunctive_query_list = data.get('disjunct')
	use_pagerank = data.get('searchtype')
	public = data.get('public')
	if public == "unspecified":
		public = None
	csv_data = "figures/csvs"
	whoosh_index_dir = "index"
	json = "reverse_index.json"
	#url, desc = advancedSearch.advanced_search(whoosh_index_dir=whoosh_index_dir, query=query, school_data_csv=csv_data, ajacency_json=json, disjunctive_query_list=disjunctive_query_list, exact_terms=exact_terms, state=state, city=city, zipcode=zipcode, school_id=school_id, url=url, use_pagerank=use_pagerank, public=public)
	
	url, desc = mySearcher.search(query)
	#figures = figures(url, 'figures/csvs', self.indexer)
	return zip(url[offset: offset+per_page], desc[offset: offset+per_page])

@app.route('/results/', methods=['GET', 'POST'])
def return_results():

	page, per_page, offset = get_page_args(page_parameter="page", per_page_parameter="per_page")

	total = 100
	pagination_results = get_results(offset=offset, per_page=per_page)
	pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

	return render_template('index.html', results=pagination_results, page=page, per_page=50, pagination=pagination)


class MyWhooshSearcher(object):
	"""docstring for MyWhooshSearcher"""
	def __init__(self):
		super(MyWhooshSearcher, self).__init__()

	def get_schema(self):
		return Schema(path=ID(unique=True, stored=True), content=TEXT, desc=TEXT(stored=True), url=STORED, time=STORED)

	def search(self, queryEntered):
		url = list()
		desc = list()

		with self.indexer.searcher() as search:
			query = QueryParser("content", schema=self.get_schema())
			if (queryEntered != None):
				query = query.parse(queryEntered)
				results = search.search(query, terms=True, limit=100)
			
				for x in results:
					url.append(str(x['url']))
					desc.append(str(x['desc']))
			
		return url, desc

	def figures(url, csvdir, ix):

		figs = select.fallback_figs
		return figs
		#should return list of figure filenames in same order as URL names

	def index(self, filesdir, indexdir, adj_matrix):
		if not os.path.exists(indexdir):
			os.mkdir(indexdir)
		schema = self.get_schema()
		indexer = create_in(indexdir, schema)
		writer = indexer.writer()
		filepaths = [os.path.join(filesdir, i) for i in os.listdir(filesdir)]

		df = pd.read_json(adj_matrix, lines=True)
		URLlist = df['URL'].tolist()
		URLdict = {}

		for u in URLlist:
			URLdict[u] = 'files/'+u.replace('/','').replace(':','')+'.txt'

		for path in filepaths:
			url = None
			for key,value in URLdict.items():
				if path == value:
					url = key
					self.add_doc(writer, path, url)

		writer.commit()
		self.indexer = indexer

	def set_index(self, indexdir):
		try:
			index = open_dir(indexdir)
		except:
			print("index not found")
			return None
		self.indexer = index

	def add_doc(self, writer, path, url):
		fp = open(path, "r", encoding = "latin-1")
		content = fp.read()
		desc = content[:100]
		fp.close()
		modtime = os.path.getmtime(path)
		writer.add_document(path=str(path), content=str(content), desc=str(desc), url=str(url), time=modtime)

if __name__ == '__main__':
	global mySearcher
	mySearcher = MyWhooshSearcher()
	#mySearcher.index("files", "index", "reverse_index.json")
	mySearcher.set_index("index")
	app.run(debug=False)


# CODE TO ADD TITLE TO SCHEMA TO DISPLAY INSTEAD OF URL
		#headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
					#response = None
					#try:
					#	response = requests.get(url, timeout=2, headers=headers)
					#except:
					#	pass
						
					#if response != None:
					#	soup = BeautifulSoup(response.text, 'html.parser')
					#	if (soup.title is not None):
					#		title = soup.find('title')
					#	else:
					#		title = url
					#else:
			#		title = url
