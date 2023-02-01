import os
from whoosh import index
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID, STORED
import sys
from whoosh.index import open_dir
from whoosh.query import Every
from whoosh.qparser import QueryParser
from whoosh import qparser

# creates schema for index
def get_schema():
	return Schema(path=ID(unique=True, stored=True), content=TEXT, time=STORED)

# adds a document to index. called by both new_index and incremental_index
def add_doc(writer, path):
	fp = open(path, "r", encoding = "latin-1")
	content = fp.read()
	fp.close()
	modtime = os.path.getmtime(path)
	writer.add_document(path=str(path), content=str(content), time=modtime)

# creates a new index
def new_index(filesdir, indexdir):
	if not os.path.exists(indexdir):
		os.mkdir(indexdir)
	ix = index.create_in(indexdir, schema = get_schema())
	writer = ix.writer()

	filepaths = [os.path.join(filesdir,i) for i in os.listdir(filesdir)]
	for path in filepaths:
		add_doc(writer, path)
	writer.commit()

# re-indexes documents
def incremental_index(indexdir):
	try:
		ix = open_dir(indexdir)
	except:
		print("Index not found")
		return None

	indexed_paths = set()	#the set of all paths in index
	to_index = set()		#the paths we need to re-index

	with ix.searcher() as searcher:
		writer = ix.writer()

		for fields in searcher.all_stored_fields():
			indexed_path = fields['path']
			indexed_paths.add(indexed_path)

			# remove file if it no longer exists
			if not os.path.exists(indexed_path):
				writer.delete_by_term('path', indexed_path)

			else:
				# check if file was changed since it was last indexed
				indexed_time = fields['time']
				mtime = os.path.getmtime(indexed_path)
				if mtime > indexed_time:
					writer.delete_by_term('path', indexed_path)
					to_index.add(indexed_path)

		# index files that need indexed
		for path in filepaths:
			if path in to_index or path not in indexed_paths:
				add_doc(writer, path)
		writer.commit()

# determines whether documents should be re-indexed or new index created
def index_docs(filesdir, indexdir, clean=False):
	if clean:
		new_index(filesdir, indexdir)
	else:
		incremental_index(indexdir)

# searches index for a specific query
def search(indexdir, query, qsize, qbool):
	try:
		ix = open_dir(indexdir)
	except:
		print("Index not found")
		return None
	if qbool == False:
		qp = QueryParser("content", schema=get_schema(), group=qparser.OrGroup)
	else:
		qp = QueryParser("content", schema=get_schema())
	q = qp.parse(query)
	
	try: 
		s = ix.searcher()
		results = s.search(q, limit=qsize)
	except:
		print("No Results Found\n")
	else:
		for r in results:
			print(r,"\n")
	finally:
		s.close()

# returns the size of the index
def index_size(indexdir):
	try:
		ix = open_dir(indexdir)
	except:
		print("Index not found")
		return None
	num_docs = ix.searcher().doc_count_all()
	return num_docs

if __name__ == '__main__':
	# run line 114 to index documents.
	# change True to False if you want to re-index documents if modifications made to corpus.
	#index_docs("files", "indexdir", True)

	print("\nHello! You are searching the PBS dataset")
	size = index_size("indexdir")
	print("The size of this dataset is: ", size)
	print("\nYou are now entering search mode. Enter Q to exit.\n")

	while True:
		query = input("Please enter a query: ")
		if query == "Q":
			break

		qnumchange = input("\nThe default # of results to return is 10. Would you like to change it? (y/n): ")
		if qnumchange == "y":
			qsize = int(input("Enter in the number of results you would like returned: "))
		else:
			qsize = 10

		qtype = input("\nWould you like to search disjunctively? The default is conjunctive search. (y/n): ")
		if qtype == "y":
			qbool = False
		else:
			qbool = True
			
		search("indexdir", query, qsize, qbool)
	

