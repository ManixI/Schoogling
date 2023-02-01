#!/usr/bin/python3

from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
import whoosh as ws
from whoosh.index import create_in, exists_in, open_dir
import pandas as pd
import os
import time
import signal as sig

DEBUG = True

class parser:
    def __init__(self):
        self.verbose=True
        pass

    def create_schema(self):
        if self.verbose:
            print ("creting schema")
        self.schema = ws.fields.Schema(title=TEXT(stored=True), content=TEXT,
            path=ID(stored=True), tags=KEYWORD, icon=STORED, url=ID(stored=True, unique=True))

    def create_index(self):
        if self.verbose:
            print ("creating index")
        if not os.path.exists("index"):
            os.mkdir("index")
        if not ws.index.exists_in("index"):
            if self.verbose:
                print ("index dose not exist, makeing new one")
            self.ix = ws.index.create_in("index",self.schema)
        else:
            self.ix = ws.index.open_dir("index")


    def load_index(self, index_name):
        ix = ws.index.open_dir(index_name)
        return ix

        
    def add_to_index(self, title, content, path, tags=None):
        if self.verbose:
            print("adding file: "+str(title)+" to index")
        writer = self.ix.writer()
        writer.add_document(title=title, content=content, path=path, tags=tags)
        writer.commit()

    # TODO: add signle for ^C to commit what has been indexed
    # TODO: way to track what has been indexed
    def add_dir_to_index(self, fdir, file_name):
        if self.verbose:
            print("adding dir: "+str(fdir)+" to index")
            print()
        if not os.path.exists(fdir):
            print("ERROR: dir: "+fdir+" not found")
            return
        if not os.path.exists("index"):
            if self.verbose:
                print ("creating new index")
            self.create_index()
        if not ws.index.exists_in("index"):
            self.create_index()
        else:
            self.ix = ws.index.open_dir("index")
        #ix = ws.index.open_dir("index")
        writer = self.ix.writer()
        self.writer = writer
        sig.signal(sig.SIGINT, self.__writer_sig_handler)
        file_list = os.listdir(fdir)

        # get url list
        json = pd.read_json(file_name, lines=True)
        if DEBUG:
            print(json)
        json.drop_duplicates(subset=['URL'], keep='first')
        if DEBUG:
            print(json)
        url_list = json['URL'].tolist()
        if DEBUG:
            #print(url_list)
            pass
        title_list = list()
        for ent in url_list:
            tmp = ent.replace('/','').replace(':','')
            tmp = tmp+".txt"
            title_list.append(tmp)
        final_list = zip(url_list, title_list)
        final_list = set(final_list)

        for i in range(len(file_list)):
            with open(("files/"+file_list[i]), 'r') as file:
                name = file_list[i]
                url = None
                for ent in final_list:
                    if name == ent[1]:
                        url = ent[0]
                        #print("added url: "+str(ent[0]))
                c_time = time.ctime(os.path.getctime("files/"+name))
                tags = None
                icon = None
                contents = file.read()
                if self.verbose:
                    print("adding file: "+str(name)+" to index")
                writer.add_document(title=name, content=contents)
        if self.verbose:
            print("Commiting to index")
        writer.commit()

    # commit on ^C
    def __writer_sig_handler(self):
        self.writer.commit()


    # adds urls to docs with titles derived from thier url based on list of urls
    # created from ajacency matrix json
    def add_url_to_schema(self, file_name):
        json = pd.read_json(file_name, lines=True)
        if DEBUG:
            print(json)
        json.drop_duplicates(subset=['URL'], keep='first')
        if DEBUG:
            print(json)
        url_list = json['URL'].tolist()
        if DEBUG:
            #print(url_list)
            pass
        title_list = list()
        for ent in url_list:
            tmp = ent.replace('/','').replace(':','')
            tmp = tmp+".txt"
            title_list.append(tmp)
        final_list = zip(url_list, title_list)
        final_list = set(final_list)
        
        ix = self.load_index("index")
        writer = ix.writer()
        '''
        writer.remove_field("url")
        writer.commit()
        writer = ix.writer()
        '''
        writer.add_field("url", ID(stored=True, unique=True))
        parser = ws.qparser.QueryParser("title", ix.schema)
        if DEBUG:
            #print(final_list)
            print()
        for ent in final_list:
            writer.update_document(title=ent[1], url=ent[0])
            if DEBUG:
                print(ent[1]+" "+ent[0])
        writer.commit()


    def add_page_rank_to_schema(self, file_name):
        pass
        # UNF: add page rank to schema


    # @param {string} query to search for
    # @param {int} which page to display (1 page is 10 results)
    def search(self, query, page=1, disjunctive=False, quiet=False):
        if self.verbose:
            print("searcing for: "+str(query))
        ix = self.load_index("index")
        print(ix.schema)
        with ix.searcher() as searcher:
            if disjunctive == True:
                parser = ws.qparser.QueryParser("content", ix.schema, group=ws.qparser.OrGroup)
            else:
                parser = ws.qparser.QueryParser("content", ix.schema)
            query = parser.parse(query)
            result = searcher.search(query)
            print("Showing results "+str(page-1)*10+" - "+str(page*10)+" out of "+str(len(result)))
            if not quiet:
                for i in range((page-1)*10,page*10):
                    print(result[i])
            # need to make new list otherwise results object dies when "with searcher() ends"
            ordered_title_list = list()
            for ent in result:
                ordered_title_list.append(ent.get("title"))
            for ent in result:
                print(ent["url"])

            # debug
            if DEBUG:
                pass



        return ordered_title_list


    def search_by_url(self, query, page=1, disjunctive=True, quiet=False):
        if self.verbose:
            print("searcing for: "+str(query))
        ix = self.load_index("index")
        with ix.searcher() as searcher:
            if disjunctive == True:
                parser = ws.qparser.QueryParser("url", ix.schema, group=ws.qparser.OrGroup)
            else:
                parser = ws.qparser.QueryParser("url", ix.schema)
            query = parser.parse(query)
            result = searcher.search(query)
            print("Showing results "+str(page-1)*10+" - "+str(page*10)+" out of "+str(len(result)))
            if not quiet:
                for i in range((page-1)*10,page*10):
                    print(result[i])
            # need to make new list otherwise results object dies when "with searcher() ends"
            ordered_title_list = list()
            for ent in result:
                ordered_title_list.append(ent.get("title"))

        return ordered_title_list        

