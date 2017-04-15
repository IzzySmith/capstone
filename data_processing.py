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
            book_dict[f] = date_match.group(0)
       
        else:
            no_date += 1
          
    return book_dict, no_date
   
print retrieve_date(sample, adventure_books) 

