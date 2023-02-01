#!/usr/bin/python3


from crawler import crawler
import json
import os


TEST_1 = False
TEST_2 = False
TEST_3 = True

if TEST_1:
	# test issue with losing old ajacency matrix data
	crawler_1 = crawler('https://en.wikipedia.org/wiki/Main_Page',
		que_file="que_1.1.txt", ajacency_file="ajacent_1.1.json")
	crawler_1.crawl(10, verbose=True)
	#with open("ajacent_1.1.json", "r") as fp:
	#	dic1 = json.load(fp)

	#print(crawler_1.ajacent_matrix)
	print()
	print(crawler_1.get_ajacent_from_file())
	print()

	#crawler_1.update_ajacency_file_name("ajacent_1.2.json")
	crawler_1.crawl(10, verbose=True)
	#with open("ajacent_1.2.json", "r") as fp:
	#	dic2 = json.load(fp)
	
	#print("num items in first file: "+str(len(dic1))+", expected 10")
	#print("num items in second file: "+str(len(dic1))+" expected 20")

if TEST_2:
	# just run for 10 URLs and stop
	# remove files
	try:
		crawler_2 = crawler('https://en.wikipedia.org/wiki/Main_Page',
			que_file="que_2.txt", ajacency_file="ajacent_2.json")
		crawler_2.crawl(10, verbose=True)
		print(crawler_2.get_ajacent_from_file())
	finally:
		os.remove("que_2.txt")
		os.remove("ajacent_2.json")

if TEST_3:
	crawler_3 = crawler('https://www.niche.com/',que_file='niche.txt',ajacency_file='niche.json')
	#print(crawler_3.extract_domain())
	#print(crawler_3.extract_domain()[0:7])
	crawler_3.crawl(-1, verbose=True)

