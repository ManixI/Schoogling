import queue
import networkx as nx
import pandas as pd
import json
import requests
from requests.exceptions import Timeout
import time
import socket
import errno
from bs4 import BeautifulSoup
import urllib.robotparser

# CS 454 - Assignment 1 - Web Crawling
# Janna Tikka 8/25/2022

#run with python3.9 -W ignore crawlcrawl.py

#FIXES TO MAKE:
#SET SOCKET TIMEOUT FOR ROBOTS REQUEST
#CHECK THAT ADJ MATRIX LABELING ACTUALLY WORKS


#declarations
q = queue.Queue()
visited = []
label = []
G = nx.DiGraph()
socket.setdefaulttimeout(20)
rp = urllib.robotparser.RobotFileParser()

def crawl():
	i = 0
	while i < count:
		if not q.empty():

			#gets seed and gets the raw page using bs after performing
			#series of checks.
			seed = q.get()
			if rp.can_fetch("*", seed) and seed not in visited:
				try:
					rawPage = requests.get(seed, timeout=20)
				except Timeout:
					continue
				
				#changes url to name for text documents and
				#checks that length can actually be used for text doc
				#if not then it will not actually crawl this page.
				url4doc = seed.replace('/','').replace(':','')
				if len(url4doc) > 255:
					continue

				bs = BeautifulSoup(rawPage.text, 'lxml')
				print("Crawling:  ", seed)

				#adds seed to label list used to label adj.matrix
				if seed not in label:
					label.append(seed)	

				#finds all outgoing links on current url and after performing series of checks,
				#adds new url to queue, diGraph, and label list for adj.matrix	
				for link in bs.find_all('a'):
					
					url = link.get('href')
					if url == None:
						continue
					if url in visited:
						continue
					if url.startswith('/'):
						url = seed + url
					if url.startswith(domain) and rp.can_fetch("*", url):
						q.put(str(url))
						if url not in label:
							label.append(url)
						G.add_edges_from([(seed, url)])
						
				#print out content to txt file, strip=True strips out all whitespaces, separated by " "
				content = bs.get_text(" ", strip=True)
				with open(f'files/{url4doc}.txt', 'w') as f:
					f.write(content)
				
				#adds seed to visited list after all crawling op's complete and
				#converts to json doc	
				visited.append(seed)
				with open("visitedURLs.json", 'w') as f:
					json.dump(visited, f)

				#creates adjacency matrix and outputs to CSV
				m = nx.adjacency_matrix(G)
				df = pd.DataFrame(m.todense())
				df.columns = label
				df.index = label
				df.to_csv('matrix.csv')
				
				#sleeps for 5 seconds, increments loop count
				time.sleep(5)
				i += 1
			else:
				#print("--we cannot visit this page or this page has already been visited--")
				continue
		else:
			#print("Queue is empty")
			break

if __name__ == '__main__':

	count = 10
	domain = "https://www.usnews.com/"
	rp.set_url("https://www.usnews.com/robots.txt")
	rp.read()
	q.put("https://www.usnews.com/education?top_nav_Education")
	crawl()

	#UNBLOCK BELOW CODE TO CRAWL ANOTHER SEED
		#while not q.empty():
			#q.get()
		#count = 50
		#domain = "wsu.edu"
		#rp.set_url("https://www.wsu.edu/robots.txt")
		#rp.read()
		#q.put('https://wsu.edu/about/facts/')
		#count = 50
		#crawl()
	

	print("crawlcrawl is done! Crawled ",len(visited)," pages.")

