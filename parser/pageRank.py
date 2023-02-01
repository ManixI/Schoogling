import pandas as pd
import numpy as np
import os
import json

# PAGE RANK

# IMPORTANT
# the adjacency list used to compute pageRank must meet the following requirements:
#	- no self-loops
#	- no multiple "head" links ex: [[url1: url2, url3], [url2: url1], [url1: url3]]
#	- no links to pages that have not been crawled
# Violating these rules will cause the PageRank to break and return a vector of improper size

# for our project we are ONLY running pagerank on an adjacency list with USNews and Niche data
# this is because 99% of the other school websites do not link to each other

# converts adjacency list to a matrix and computes pageRank
# d = damping factor (click-through probability)
# e = convergence test value - if prev_rank - new_rank < e -> stop converging	
def pageRank(adj_list, d=0.85, e=0.0001):

	URLlist = adj_list['URL'].tolist()
	n = len(URLlist)
	matrix = np.zeros((n,n))
	i = 0

	while i < n:
		url = adj_list.iloc[i][0]
		adj = adj_list.iloc[i][1]
		if len(adj) > 0:
			for adj_url in adj:
				if adj_url == '':
					for j in range(n):
						matrix[j][URLlist.index(url)] = 1/n
				elif adj_url not in URLlist:
					continue
				else:
					matrix[URLlist.index(adj_url)][URLlist.index(url)] = 1/len(adj)
		else:
			for j in range(n):
				matrix[j][URLlist.index(url)] = 1/n
		i += 1

	E = np.ones((n,n))
	part1 = np.multiply(((1-d)/n), E)
	part2 = np.multiply(d, matrix)
	trans_matrix = np.add(part1, part2)

	m = len(trans_matrix)
	v1 = np.ones(m)
	v1 = np.multiply((1/m),v1)
	v2 = np.matmul(trans_matrix, v1)
	count = 1

	while converg_check(v1, v2, e):
		v1 = v2
		v2 = np.matmul(trans_matrix, v1)
		count += 1

	#pagerank list
	rankedList = v2.tolist()
	
	ranked = {URLlist[i]:rankedList[i] for i in range(len(URLlist))}

	return ranked

# compares the two vectors to see if they are below convergence value
def converg_check(v1, v2, e):
	vector = np.subtract(v1,v2)
	for diff in vector:
		if abs(diff) > e:
			return True
	return False

def get_list_from_file(adj_list):
    if os.path.exists(os.path.abspath(adj_list)):
        adjacent = pd.read_json(adj_list, lines=True)
        return adjacent
    else:
    	print("Error, adjacency list not found")
    	return None

def output_to_file(rankedDict):
  	with open("pageRanked", "w") as fp:
  		json.dump("pageRanked", fp)

if __name__ == "__main__":

	# make sure you are getting a "cleaned" adjacency list
	adj_list = get_list_from_file("cleaned-WSU-test.json")
	ranked = pageRank(adj_list)
	output_to_file(ranked)


