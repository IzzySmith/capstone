from __future__ import division
from collections import Counter,defaultdict
from bs4 import BeautifulSoup as bs
from bs4 import Comment
import re
import os
import glob
import nltk
import math
import urllib2
import time
import numpy as np
from gensim.models import word2vec
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

adventure_books = 'Adventure'
filenames = os.listdir(adventure_books)

test_files = filenames
# returns a list of the names of each of the .txt files
sample = filenames[:10]

# open each file and extract the date 
def retrieve_date(list_file_names, file_path):
    """
    takes a list of file names and parses the data to find
    the date the book was written.
    returns a dict with {filename:date}
    """
    book_dict = {}
    no_date = 0
    for f in list_file_names:
        #no_date = 0
        #book_dict = {}
        open_file = open(file_path + '/' + f, 'r')
        #bs_f = bs(open_file, "lxml")
        read_file = open_file.read()
        open_file.close
        """
        A date is a string of 4 numbers, and usually appears
        near the beginning of the document
        
        """
        date_match = re.search(r"\s[0-9]{4}\s", read_file)
        if date_match:
            """ 
            if a date is found we create a dict"
            """
            date = date_match.group(0)
            #we remove the newlines
            cleaned_date = date.strip('\n')
            #we remove the whitespaces
            cleaner_date = cleaned_date.strip(' ')
            #we create a dict with {filename: date}
            book_dict[f] = cleaner_date
       
        else:
            no_date += 1
          
    return book_dict
   
dated_books = retrieve_date(sample, adventure_books) 

#print 'dated_books_dict %s' %str(dated_books)

#test = dated_books.items()[1]
#print test[1]


#improve this function later with recursion/ only thing that changes is the
#century and decade input into the regex
#arrange books into decade
def sort_to_decade(regex, input_dict):
    """
    takes a dict of the format {filename: date}
    and creates a list of dicts sorted into the
    correct decade as specified by the input regex
    """
    match_exp_dict={}
    #we sort the dict into values from lowest to highest
    #sorted_dates = sorted(input_dict.values())
    #print [type(i) for i in input_dict.values()]
    #The input_dict.values() are strings, therefore we will parse
    # using regex
    for i in input_dict.items():
	match_exp = re.search(regex, i[1])
	if match_exp:
	    match_exp_group = match_exp.group(0)
	    match_exp_dict[i[0]] = match_exp_group
    return match_exp_dict
	   
test_tts = sort_to_decade(r"(201){1}[1-9]{1}", dated_books)
test_naughties = sort_to_decade(r"(200){1}[0-9]{1}", dated_books)
test_nineties = sort_to_decade(r"(199){1}[1-9]{1}", dated_books)

print 'twenty tens dict: %s' % str(test_tts)
print 'naughtes dict: %s' % str(test_naughties)
print 'nineties dict: %s' % str(test_nineties)

# the files need to be organised into a list of sentances.
# word2vec requires that each sentance is a list of utf8 strings
# e.g [['sentace', 'one'], ['sentance', 'two'], ['sentance, 'three']]

def divide_files(input_dict, file_path):
    """
    takes the dict, and opens the associated .txt file
    and uses the nltk tokenised to tokenise into sentances.
    it outputs a list of sentances- which is a list of words.
    """
    sentance_list = []
    word_list = []
    for i in input_dict.items():
        #open the file at i[0] of dict
        open_file = open(file_path + '/' + i[0], 'r')
        r_file = open_file.read()
        open_file.close
        read_file = r_file.decode('utf8')
        #we remove the newline characters
        #we split the strings on full stops
        s_list = nltk.sent_tokenize(read_file)
        sentance_list = [w.split(" ") for w in s_list]
    return sentance_list
        
#test  
#print divide_files(test_nineties, adventure_books)

