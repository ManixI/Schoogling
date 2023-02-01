#!/bin/user/python3

# Test harnes for Fig Selector

import figSelector as fs
from parser import parser
import time
# TODO: Titles accross all graphs

TEST_FALLBACK = False
TEST_SINGLE = False
TEST_MULTI = False

start_time = time.time()
p = parser()
p.create_schema()
p.create_index()
setup_time = time.time()-start_time
p.add_dir_to_index("files", "reverse_index.json") # NOTE: Only run once
index_time = time.time() - start_time - setup_time
#p.add_url_to_schema("reverse_index.json") # NOTE: Only run if needed
#p.search("school") 
print()
#p.search_by_url("https://wsu.edu/")


tmp = p.search("school")
print()
print(tmp[0])



search_time = time.time() - start_time-setup_time-index_time
print(str(start_time/60))

print()
print("setup time: "+str(setup_time/60))
print("index time: "+str(index_time/60))
print("search_time: "+str(search_time/60))

if TEST_FALLBACK:
	fs.fallback_figs()

if TEST_SINGLE:
	pass

if TEST_MULTI:
	print("testing figs for search 'school'")
	result = p.search("school", quiet=True)
	fs.fig_selector(result, 0, "csvs",p.load_index("index"))