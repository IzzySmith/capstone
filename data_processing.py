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

#test = dated_books.items()[1]
#print test[1]

#arrange books into decade
def sort_twenty_tens_decade(input_dict):
    """
    takes a dict of the format {filename: date}
    and creates a list of dicts sorted into the
    correct decade
    """
    twenty_tens_dict={}
    #we sort the dict into values from lowest to highest
    #sorted_dates = sorted(input_dict.values())
    #print [type(i) for i in input_dict.values()]
    #The input_dict.values() are strings, therefore we will parse
    # using regex
    for i in input_dict.items():
	twenty_tens = re.search(r"(20){1}[0-9]{2}", i[1])
	if twenty_tens:
	    twenty_tens_group = twenty_tens.group(0)
	    twenty_tens_dict[i[0]] = twenty_tens_group
    return twenty_tens_dict
	    

print sort_twenty_tens_decade(dated_books)



