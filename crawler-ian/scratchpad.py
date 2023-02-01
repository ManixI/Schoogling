#!/usr/bin/python3

import requests
import urllib.robotparser
import os
import json
import signal as sig
from time import sleep
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from time import time
from sys import exit
#from pandas_multiprocess import multi_process
import pandas as pd
from functools import lru_cache


url = 'https://www.usnews.com/best-colleges/rankings/computer-science-overall'
with open('test_data.txt', 'r') as fp:
	for line in fp:
		print(line)
		print()