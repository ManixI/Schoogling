#!/usr/bin/python3

from crawler import crawler
import os
from threading import Thread

num_threads = 4
site_list = ['https://en.wikipedia.org/wiki/Main_Page','https://en.wikipedia.org/wiki/Main_Page','https://en.wikipedia.org/wiki/Main_Page','https://wsu.edu/']
threads = list()

def thread_crawler(seed):
	c = crawler(seed, que_file=(seed.replace('/','').replace(':','')+"Que.txt"), ajacency_file=(seed.replace('/','').replace(':','')+"Ajacency.json"))
	c.crawl(-1, verbose=True)

while len(site_list) > 0:
	for i in range(num_threads):
		thread = Thread(target=thread_crawler, args=(site_list.pop(0),))
		threads.append(thread)
		thread.start()


	for thread in threads:
		thread.join()


