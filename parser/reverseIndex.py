#!/usr/bin/python3

import pandas as pd
import numpy as np

# change to generate print statements for specific words when testing
_word = "xxxx"

# TODO: optomise 
#   * sort list so it can be searched via binary search
#   * also means write search function
#   * use pointers for words instead of words
#       * further optomise by using buckets for groups of words
#       * see sparce index
#   * replace prefixes with smaller symbols
#   * gap encoding for doc ids ([5,10,11,13] becomes [5,5,1,2])
#       * also variable bit numbers
#
# TODO: update method to add additional data
#
# TODO: Update to write to file so not rebuilding for each run


# this builds a reverse index of terms for a given dataset in the format
# id, description
# id - unique doc number
# description - text contents of document, stripped of all puncuation and 
#   capotal letters


# revers index, list of each word's freuency in each doc it appears in
class reverse_index:
    def __init__(self, csv_file):
        # index of all entry objects
        self.r_dex = []
        # num terms in doc stored st doc_length[doc_id]
        self.doc_length = []
        self.num_docs = 0

        cs = pd.read_csv(csv_file)

        # for each row in file
        entry = 0
        for description in cs['description']:
            # get each word of discription
            terms = description.split(" ")
            #print(terms)
            self.doc_length.append(0)
            # for eacy word in discription
            for i in range(len(terms)):
                # if in index, increment count
                loc = self.position(terms[i])
                if loc >= 0:
                    #print(terms[i])
                    #print(loc)
                    self.r_dex[loc].add_entry(entry)
                else:
                    # else add it to index
                    self.r_dex.append(index_entry(terms[i]))
                    self.r_dex[len(self.r_dex)-1].add_entry(entry)
                self.doc_length[entry] +=1
            entry = entry + 1
            


    # return count of word in doc idt
    def count(self, idt, word):
        loc = self.position(word)
        #print(str(idt)+" "+word)
        for i in range(len(self.r_dex[loc].count)):
            #print(i)
            if self.r_dex[loc].doc_id[i] == idt:
                return self.r_dex[loc].count[i]
        return -1
        
        

    # return position of word in reverse index
    def position(self, word):
        for i in range(len(self.r_dex)):
            if word == self.r_dex[i].word:
                if word == _word:
                    print("---")
                    print(word + " - " + self.r_dex[i].word)
                    print("position = " + str(i))
                return i
        return -1


# each word in reverse index
class index_entry:
    def __init__(self, word):
        self.word = word
        self.doc_id = []
        self.count = []

    # adds new doc idt or increses count of existing doc idt for word
    def add_entry(self, idt):
        in_doc = False
        if self.word == _word:
            print(idt)
            #print(self.doc_id)
        for i in range(len(self.doc_id)):
            if idt == self.doc_id[i]:
                in_doc = True
                loc = i

        if in_doc:
            if self.word == _word:
                print(loc)
            #print(self.word)
            self.count[loc] += 1
            if self.word == _word:
                print("more")
                print(idt)
                print("doc id")
                print(self.doc_id)
                print("count")
                print(self.count)
        else:
            self.doc_id.append(idt)
            self.count.append(1)
            if self.word == _word:
                print("first")
                print("doc id")
                print(self.doc_id)
                print("count")
                print(self.count)