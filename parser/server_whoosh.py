from flask import Flask, render_template, url_for, request, Response
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
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib import pyplot as plt
import requests
from bs4 import BeautifulSoup

'''
NOTE: Schema attributes
so I can find them easily

url=ID(unique=True, stored=True) 
content=TEXT(stored=True)
title=TEXT(stored=True)
desc=TEXT(stored=True)
time=STORED
'''


app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
	print("Someone is at the home page.")
	return render_template('bootstrap.html')

@app.route('/my-link/')
def my_link():
	print('I got clicked!')
	return 'Click.'

@app.route('/results/', methods=['GET', 'POST'])
def results():
	global mySearcher
	if request.method == 'POST':
		data = request.form
		#searchtype = request.label
	else:
		data = request.args
		#searchtype = request.label

	query = data.get('searchterm')
	#pageRank = searchtype.get('pagerank')
	#print(pageRank)
	url, title, desc = mySearcher.search(query)
	print("You searched for: " + query)
 
	return render_template('results.html', query=query, results=zip(url, title, desc))


@app.route('/plot.png')
def plot_png():
	fig = Figure()
	axis = fig.add_subplot(1,1,1)
	xs = range(100)
	ys = [random.randint(1,50) for x in xs]
	axis.plot(xs, ys)
	output = io.BytesIO()
	FigureCanvas(plt.gcf()).print_png(output)

	return Response(output.getvalue(), mimetype='image/png')


class MyWhooshSearcher(object):
	"""docstring for MyWhooshSearcher"""
	def __init__(self):
		super(MyWhooshSearcher, self).__init__()
		
	#implement page rank
		
	def search(self, queryEntered):
		url = list()
		title = list()
		desc = list()

		#if pageRank == True:
			# obtain page rank values
			# run TF-IDF
			# traverse through PRList and if url in pageRankList is also in TF-IDF list -> add to newList
			# if size(newList) < 10 -> start at beg. of TF-IDF list and add values to NewList as long as not in newList already
			# if no items in pageRankList also in TF-IDF list -> return TF-IDF list

		#else:
			# Use TF-IDF only
		with self.indexer.searcher() as search:
			query = QueryParser("content", schema=self.get_schema())
			if (queryEntered != None):
				query = query.parse(queryEntered)
				results = search.search(query, terms=True)
				
				for x in results:
					url.append(str(x['url']))
					title.append(x['title'])
					desc.append(x['desc'])

			
		return url, title, desc

		# run pageRank right after indexing! only need to run once,
		# values should be stored and only returned when someone searches with pagerank

	def get_schema(self):
		return Schema(url=ID(unique=True, stored=True), content=TEXT(stored=True), title=TEXT(stored=True), desc=TEXT(stored=True), time=STORED)

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
			title = None
			for key,value in URLdict.items():
				if path == value:
					url = key
					#headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'}
					#response = None
					#try:
					#	response = requests.get(url, timeout=5, headers=headers)
					#	print("success")
					#except:
					#	print("error")
						
					#if response != None:
					#	soup = BeautifulSoup(response.text, 'html.parser')
					#	if (soup.title is not None):
					#		title = soup.find('title')
					#	else:
					#		title = url
					#else:
					title = url

			self.add_doc(writer, path, url, title)
		writer.commit()
		self.indexer = indexer

	def set_index(self, indexdir):
		try:
			index = open_dir(indexdir)
		except:
			print("index not found")
			return None
		self.indexer = index

	def add_doc(self, writer, path, url, title):
		fp = open(path, "r", encoding = "latin-1")
		content = fp.read()
		desc = content[:100]
		
	    #need keywords
		fp.close()
		modtime = os.path.getmtime(path)
		writer.add_document(url=str(url), content=str(content), title=str(title), desc=str(desc), time=modtime)

if __name__ == '__main__':
	global mySearcher
	mySearcher = MyWhooshSearcher()
	#mySearcher.index("files", "index", "visited-domains.json")
	mySearcher.set_index("index")
	#title, description = mySearcher.search('hello')
	#print(title)
	app.run(debug=False)
