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


CRAWLER_DEBUG = False
DOMAIN_DEBUG = False

#TODO: don't let bad URLs get to the que to preserve memory
#TODO: enable multithreading when there is no specified crawl and request rate
#TODO: let program dump memory to file on occasion to prevent balooning memory
#TODO: only get so many lines of the que at once from the file for the same reason

#TODO: Can speed up by makeing visited a tree instead of a set for faster comparason to cursor



# web crawler class
# @param {string} seed URL
class crawler:
    def __init__ (self, seed, restrict_domain=True, num_cores=1, que_file="oldQue.txt", ajacency_file="visited-domains.json",headers=None):
        # ensure file directory exists
        dir_path = os.path.dirname(os.path.realpath(__file__))
        try:
            os.mkdir(dir_path + ' / files')
            print("made files directory")
        except OSError as error:
            print("files directory exists, using existing directory")
        except:
            print("something went wrong") 

        if headers == None:
            self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
        else:
            self.headers = headers
        

        # Important: set base info here
        # Drop trailing / as it causes issues
        tmp = seed.rfind('/')
        if tmp > 0:
            seed = seed[0:tmp]

        # append http:// to seed 
        if ('http://' not in seed) and ('https://' not in seed):
            seed = 'http://' + seed

        self.seed = seed
        self.restrict_domain = restrict_domain
        self.domain = self.extract_domain()
        self.num_cores = num_cores
        self.que_file = que_file
        self.ajacency_file = ajacency_file

    # get the domain of the current seed
    # @return {string} domain
    def extract_domain(self):
        domain = self.seed
        if DOMAIN_DEBUG:
            print("domain: "+domain)
        if domain[0:7] == 'http://':
            # strip http:// from domain
            domain = domain[7:]
        if DOMAIN_DEBUG:
            print("strip http:// "+domain)
        if domain[0:8] == 'https://':
            # strip https://
            domain = domain[8:]
        if DOMAIN_DEBUG:
            print("strip https:// "+domain)
        if domain[0:4] == 'www.':
            # strip www.
            domain = domain[4:]
        if DOMAIN_DEBUG:
            print("strip www. "+domain)
        tmp = domain.find('/')
        if tmp > 0:
            domain = domain[0:tmp]
        if DOMAIN_DEBUG:
            print("drop everything after .com "+domain)
        return domain



    # call to update seed domain
    # @param {string} seed domain
    # @param {string} domain to stay within (set None to explore other domains)
    def update_seed(self, seed, domain):
        self.seed = seed
        self.domain = domain

    # call to change name of que file
    # @param {string} que_file
    def update_que_file_name(self, que_file):
        self.que_file = que_file

    # call to change name of ajacency file
    # @param {string} que_file
    def update_ajacency_file_name(self, ajacency_file):
        self.ajacency_file = ajacency_file


    # find robots.txt associated with given url
    # @param {string} seed url
    # @param {bool} update robots if found
    # @return {string} robots.txt url
    def find_robots(self, seed, update=False):
        pass
        # find robots.txt
        # TODO: This
        if update == True:
            # update robots
            self.update_robots(rb_url)

    # update paramaters for robots.txt
    # make sure this isn't done until previous robots is exhausted
    # @param {string} new robots url
    def update_robots(self, rb_url):
        pass
        # TODO: This

    # check if new robots for give URL
    # for use in cases where the domain is constant but different subdomains have different robots.txt
    # @param {string} URL to check
    # @return {bool}
    def check_if_new_robots(self, url):
        pass
        # check if new superdomain (e.x. from www.foo.org to www.en.foo.org)
        # TODO: This

    # call to start crawling
    # @param {int} page_limit
    # @param {int} number of cores to run on
    # @param {bool} verbose, print what's being called
    def crawl(self, page_limit, verbose=False):
        if verbose == True:
            start_time = time()
            time_delta = time()
            j = 0

        # get robots.txt
        #TODO: better parsing and use seed not domain
        # add / only if seed dosn't end in /
        rp = urllib.robotparser.RobotFileParser()
        if DOMAIN_DEBUG:
            print(self.domain)
        rp.set_url("http://www."+self.domain+'/robots.txt')
        '''
        if self.domain[-1] != '/':
            rp.set_url(self.domain+'/robots.txt')
        else:
            rp.set_url(self.domain+'robots.txt')
        '''

        rp.read()
        # max request and call rate, currently unused
        rrate = rp.request_rate("*")
        crate = rp.crawl_delay("*")

        if verbose:
            print("request rate: "+str(rrate))
            print("crawl rate:   "+str(crate))

        # use set to avoid duplicates
        self.que = self.__get_old_que()

        '''
        # this dose the same as __get_old_que(), should be unnecessary
        # read old que into program if it exists
        try:
            # if file exists and has size > 0 read it into
            if os.stat(os.path.realpath(self.que_file)).st_size != 0:
                with open("oldQue.txt", "r") as fp:
                    for line in fp:
                        self.que.append(line)
                    cursor = self.que.pop()
            else:
                cursor = self.seed
            # open with "w" to wipe file once it's been read
            with open(oldQue.txt, "w") as fp:
                pass
        except:
            cursor = self.seed
        '''

        if len(self.que) > 0:
            cursor = self.que.pop()
        else:
            cursor = self.seed

        # make list of visited sites from ajacency matrix
        self.ajacent_matrix = self.get_ajacent_from_file()
        # TODO: maybe do this with if-else instead of try-except
        try:
            visited = self.ajacent_matrix.drop_duplicates(subset=['URL'], keep='first')
            visited = visited['URL'].tolist()
        except KeyError:
            # if empty ajacency matrix
            visited = list()

        sig.signal(sig.SIGINT, self.__sig_handler_dump)

        i = 0
        # crawl infinatly if page limit < 1
        if (page_limit < 1):
            i = page_limit-1
        while i < page_limit:
            # delay if required by robots.txt
            if crate != None:
                sleep(crate)
            if rrate != None:
                sleep(rrate)

            # get URLs ajacent to cursor as dataframe
            # instead of this, could make visited set, then test if adding cursor to visited grows set, if not skip cursor
            if cursor not in visited:
                # print current page, time since last page, and total time in seconds
                if verbose:
                    t1 = round((time()-time_delta)*10) / 10
                    t2 = round(time()-start_time)
                    j += 1
                    print(cursor+" "+str(t1)+" "+str(t2)+" num: "+str(j))
                    time_delta = time()
                tmp_set = self.crawl_page(cursor)
                if tmp_set != None:
                    # if crawler didn't encounter an error
                    tmp_list = list(tmp_set)
                    tmp_df = pd.DataFrame({'URL':[cursor], 'Ajacent':[tmp_list]})
                    self.ajacent_matrix = pd.concat([self.ajacent_matrix, tmp_df])
                    for ent in tmp_list:
                        self.que.add(ent)
                    
                    
                    # rawl infinatly if page limit < 1
                    if page_limit > 0:
                        i+=1
                # get next page to crawl
                visited.append(cursor)
                try:
                    cursor = self.que.pop()
                except KeyError:
                    print("Que is empty, ending")
                    return

            try:
            # if visited or dissalowed, skip page
                if (self.restrict_domain == False):
                    while (cursor in visited) or (not rp.can_fetch("*", cursor)) or (len(cursor) > 245):
                        cursor = self.que.pop()
                        while cursor == None:
                            cursor = self.que.pop()
                else:
                    # use this while to ignore robots.txt
                    while (cursor in visited) or (self.domain not in cursor) or (len(str(cursor)) > 245):
                    #while (cursor in visited) or (not rp.can_fetch("*", cursor)) or (self.domain not in cursor) or (len(str(cursor)) > 245):
                        '''
                        if(self.domain in cursor):
                            print(rp.can_fetch("*", cursor))
                        '''
                        #print(cursor)
                        cursor = self.que.pop()
                        while cursor == None:
                            cursor = self.que.pop()
                
            # TODO: get rid of this try-except
            except KeyboardInterrupt:
                # so keyboard interupt dosn't call other error by accadent
                print("User ended early")
                self.dump()
                exit()
            except:
                if len(self.que) > 0:
                    if verbose:
                        print("\nerror with cursor: "+str(cursor)+'\n')
                    cursor = self.que.pop()
                else:
                    print("Que empty, ending early")
                    self.dump()
                    return
                    
        self.dump()


    def crawl_with_threading(self, page_limit, verbose=False, num_cores=None):
        pass
        if num_cores == None:
            num_cores = self.num_cores



    # crawl a specified page
    # write contents to txt file and return dataframe of ajacent URLs
    # @param {string} page to crawl
    # @return {set} set of ajacent URLs
    def crawl_page(self, cursor):
        #rawPage = requests.get(cursor).txt
        try:
            rawPage = requests.get(cursor, timeout=10, headers=(self.headers)).text
        except requests.exceptions.Timeout:
            print("Error: request timed out for page: "+str(cursor))
            return None
        except:
            print("\nError getting page: "+cursor+'\n')
            return None

        # load page into beutiful Soup
        bs = BeautifulSoup(rawPage, 'lxml')
        content = bs.get_text(",", strip=True)
        pageName = cursor.replace('/','').replace(':','')
        # write page contents to file
        with open(f'files/{pageName}.txt', 'w') as f:
            f.write(content)

        #array to track ajacent URLs
        ajacent = []

        for link in bs.find_all('a'):
            inQue = False
            visited = False
            stop_dupe = False

            # add all links to que
            # get link and make it absolute if relative
            tmp = link.get('href')
            if tmp and tmp.startswith('/'):
                tmp = urljoin(self.seed, tmp)
            ajacent.append(tmp)
        # cast to set to remove duplicates
        return set(ajacent)

    # get url ajacency matrix from file
    # ! potental error with empty file, in that case delete existing but empty file
    # @return {DataFrame} returns empty file if file is empty
    def get_ajacent_from_file(self):
        if os.path.exists(os.path.abspath(self.ajacency_file)):
            # if file exists, read it
            ajacent = pd.read_json(self.ajacency_file, lines=True)
            return ajacent
        else:
            print("json file "+str(self.ajacency_file)+" dose not exist, starting new file")
            #tmp = pd.DataFrame({'URL':filler, 'Ajacent':['one', 'two']})
            tmp = pd.DataFrame()
            return tmp


    # get old que from file
    # @return {set} old que
    def __get_old_que(self):
        s = set()
        try:
            with open(self.que_file, 'r+') as fp:
                for line in fp:
                    s.add(line.strip())
        except:
            # if error opening oldQue file, return empty set
            pass
        # wipe old file once read, make it if it didn't exist
        open(self.que_file,'w').close()
        return s  

    #dump que and ajacency matrix to file
    def dump(self):
        # new way to write json to file
        if CRAWLER_DEBUG:
            print("\nCRAWLER_DEBUG: dump\n")
            print(self.ajacent_matrix)

        # open with w as old file already in memory
        with open(self.ajacency_file, "w") as fp:
            #json.dump(self.ajacent_matrix.to_json(orient='records'), fp, indent=4, sort_keys=True)
            self.ajacent_matrix.to_json(fp, orient='records', lines=True)
        
        # odump que to text file
        with open(self.que_file, "w") as fp:
            while len(self.que) > 0:
                s = self.que.pop()
                fp.write(str(s)+'\n')        


    # signal handler to dump que and ajacency matrix to file
    # provides graceful exit on ^C
    # private function
    def __sig_handler_dump(self, signo, frame):
        with open(self.que_file, "w") as fp:
            while len(self.que) > 0:
                s = self.que.pop()
                fp.write(str(s)+'\n')

        # open with w as old file already in memory
        with open(self.ajacency_file, "w") as fp:
            #json.dump(self.ajacent_matrix.to_json(orient='records'), fp, indent=4, sort_keys=True)
            self.ajacent_matrix.to_json(fp, orient='records', lines=True)

        # exit on ^C
        exit()
        