from __future__ import division
from collections import Counter,defaultdict
from bs4 import BeautifulSoup as bs
from bs4 import Comment
from pattern.en import sentiment
import re
import os
import os.path
import glob
import nltk
import math
import urllib2
import time
import numpy as np
#from gensim.models import word2vec
import gensim, logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


adventure_books = 'Adventure'
fantasy_books = 'Fantasy'
filenames = os.listdir('books')

files = [f for f in filenames]

test_files = files[:1]
# returns a list of the names of each of the .txt files
#sample = filenames[:10]

# open each file and extract the date 
def retrieve_date(list_file_names):
    
   # takes a list of file names and parses the data to find
   # the date the book was written.
   # returns a dict with {filename:date}
   # a date is assumed to be 4 numbers with trailing whitespace
    book_dict = {}
    no_date = 0
    for f in list_file_names:
        #print f 
        txt_files = os.listdir('books/' + f)
        #print txt_files
        for tf in txt_files:
            file_name = f + '/' + tf
            #print 'file name is %s' % file_name
            open_file = open('books/' + file_name, 'r')
            read_file = open_file.read()
            open_file.close
            
            #A date is a string of 4 numbers, and usually appears
            #near the beginning of the document
        
            
            date_match = re.search(r"\s[0-9]{4}\s", read_file)
            if date_match:
                 
             #   if a date is found we create a dict"
                
                date = date_match.group(0)
                #we remove the newlines
                cleaned_date = date.strip('\n')
                #we remove the whitespaces
                cleaner_date = cleaned_date.strip(' ')
                #we create a dict with {filename: date}
                book_dict[file_name] = cleaner_date  
          
    return book_dict
   
dated_books = retrieve_date(test_files) 

print dated_books

# 'dated_books_dict %s' %str(dated_books)

#print len(dated_books)

#test = dated_books.items()[1]
#print test[1]

#sorts the books into decades
def into_decade(in_dict):
    #dict declarations
    e_zero_d = {}
    e_twenty_d = {}
    e_forty_d = {}
    e_sixty_d = {}
    e_eighty_d = {}
    n_zero_d = {}
    n_twenty_d = {}
    n_forty_d = {}
    n_sixty_d = {}
    n_eighty_d = {}
    t_zero_d = {} 
    #list declerations
    e_zero_l = []
    e_twenty_l = []
    e_forty_l = []
    e_sixty_l = []
    e_eighty_l = []
    n_zero_l = []
    n_twenty_l = []
    n_forty_l = []
    n_sixty_l = []
    n_eighty_l = []
    t_zero_l = []
    #regex declarations
    eighteen_zeros = r'(180){1}[0-9]{1}'
    eighteen_twenties = r'(182){1}[0-9]{1}'
    eighteen_forties = r'(184){1}[0-9]{1}'
    eighteen_sixties = r'(186){1}[0-9]{1}'
    eighteen_eighties = r'(188){1}[0-9]{1}'
    nineteen_zeros = r'(190){1}[0-9]{1}'
    nineteen_twenties = r'(192){1}[0-9]{1}'
    nineteen_forties = r'(194){1}[0-9]{1}'
    nineteen_sixties = r'(196){1}[0-9]{1}'
    nineteen_eighties = r'(198){1}[0-9]{1}'
    twothousand_zeros = r'(200){1}[0-9]{1}'
    for i in in_dict.items():
        e_zero_match = re.search(eighteen_zeros, i[1])
        e_twenty_match = re.search(eighteen_twenties, i[1])
        e_forty_match = re.search(eighteen_forties, i[1])
        e_sixty_match = re.search(eighteen_sixties, i[1])
        e_eighty_match = re.search(eighteen_eighties, i[1])
        n_zero_match = re.search(nineteen_zeros, i[1])
        n_twenty_match = re.search(nineteen_twenties, i[1])
        n_forty_match = re.search(nineteen_forties, i[1])
        n_sixty_match = re.search(nineteen_sixties, i[1])
        n_eighty_match = re.search(nineteen_eighties, i[1])
        t_zero_match = re.search(twothousand_zeros, i[1])
        if e_zero_match:
            e_zero_l.append(i[0])
            e_zero_d['1800'] = e_zero_l
        if e_twenty_match:
            e_twenty_l.append(i[0])
            e_twenty_d['1820'] = e_twenty_l
        if e_forty_match:
            e_forty_l.append(i[0])
            e_forty_d['1840'] = e_forty_l
        if e_sixty_match:
            e_sixty_l.append(i[0])
            e_sixty_d['1860'] = e_sixty_l
        if e_eighty_match:
            e_eighty_l.append(i[0])
            e_eighty_d['1880'] = e_eighty_l
        if n_zero_match:
            n_zero_l.append(i[0])
            n_zero_d['1900'] = n_zero_l
        if n_twenty_match:
            n_twenty_l.append(i[0])
            n_twenty_d['1920'] = n_twenty_l
        if n_forty_match:
            n_forty_l.append(i[0])
            n_forty_d['1940'] = n_forty_l
        if n_eighty_match:
            n_eighty_l.append(i[0])
            n_eighty_d['1980'] = n_eighty_l
        if t_zero_match:
            t_zero_l.append(i[0])
            t_zero_d['2000'] = t_zero_l
    return e_zero_d, e_twenty_d, e_forty_d, e_sixty_d, e_eighty_d, n_zero_d, n_twenty_d, n_forty_d, n_sixty_d, n_eighty_d, t_zero_d
      
            
#the files are grouped by decade
decade_dicts = into_decade(dated_books)
  
#print test_tts


#Used to take a dict that was {'filename' : date, filename : date}
#needs to take a dict in the form of {date : [filename, filename, filename], date: [filename, #filename, filename]}


def divide_files(input_tuple):
    
    #takes the dict, and opens the associated .txt file
    #and uses the nltk tokenised to tokenise into sentances.
    #it outputs a list of sentances- which is a list of words.
    
    pos_dict = {}
    sentance_list = []
    sentance = []
    for dicts in input_tuple:
        for i in dicts.items():
            for e in i[1]:
                #print e
                #my_file = os.path(e)
                #print e
                path = '/home/isobel/capstone/books/' + e
                if os.path.exists(path):
                    #print e
                    open_file = open(path, 'r')
                    if open_file:
                        print path
                        r_file = open_file.read()
                        open_file.close
                        read_file = r_file.decode('utf8', 'ignore')
                        #we remove the newline characters
                        #we split the strings on full stops
                        s_list = nltk.sent_tokenize(read_file)
                        #sentance_list.append([nltk.pos_tag(nltk.word_tokenize(s)) for s in s_list])
                        for s in s_list:
                            p = nltk.pos_tag(nltk.word_tokenize(s))
                            sentance_list.append(p)
                        pos_dict[i[0]] = sentance_list 
                else:
                    pass
    return pos_dict
                
                      
test_of_divide_files = divide_files(decade_dicts)     

def get_rid(list_of_p):
    no_pos = {}
    new_list = []
    new_txt = ""
    for i in list_of_p.items():
        for p in i[1]:
            for l in p:
                if l[1] != "TO":
                    if l[1] != "PRP":      
                        if l[1] != "PRP$":
                            if l[1] != "DT":
                                if l[1] != "IN":
                                    if l[1] != "CC":
                                        if l[1] != "''":
                                            important_words = l
                                            keys = l[0]
                                            
                                            #To make models from data we need to 
                                            #make lists of sentances
                                            #print keys
                                            new_list.append(keys)
                                            no_pos[i[0]] = new_list
    return no_pos


#test  
#naughties_adventure_tokenised = divide_files(test_tts)

test_get_rid = get_rid(test_of_divide_files)

#print test_get_rid
#cleaned_up_words = get_rid(naughties_adventure_tokenised)

def format_groups(in_dict):
    format_dict = {}
    for i in in_dict.items():
        cleaned_words = " ".join(i[1])
        tokens = nltk.sent_tokenize(cleaned_words)
        word_tokens = [nltk.word_tokenize(s) for s in tokens]
        format_dict[i[0]] = word_tokens
    return format_dict    

test_format_groups = format_groups(test_get_rid)


# we create a string of the new words so we can get it back into the
# correct format for the modelling
#string_cleaned_words = " ".join(cleaned_up_words)

#we split the new strings into sentances
#tokens = nltk.sent_tokenize(string_cleaned_words)

# creates a list of sentances
#word_tokens = [nltk.word_tokenize(s) for s in tokens]

#print word_tokens


#we then need to train a model with word2vec


def create_model(in_dict):
    models = []
    for i in in_dict.items():
        print i[0]
        model_name = str(i[0]) + 'model'
        model = gensim.models.Word2Vec(i[1])
        model.save(model_name)
        models.append(model_name)
    return models 

#test_create_model = create_model(test_format_groups)

#model = gensim.models.Word2Vec(, size=200)

#we save the model
#model.save('mymodel')

eighteen_model = gensim.models.Word2Vec.load('1800model')
eighteenforty_forty = gensim.models.Word2Vec.load('1840model')
nineteen_model = gensim.models.Word2Vec.load('1900model')
#nineteenforty_model = gensim.models.Word2Vec('1940model')
twothousand_model = gensim.models.Word2Vec.load('2000model')
#model = gensim.models.Word2Vec(nineties_adventure_tokenised, size=200)

eighteen_child = eighteen_model.most_similar('children')
eighteenforty_child = eighteenforty_forty.most_similar('children')
nineteen_child = nineteen_model.most_similar('children')
#nineteenforty_child = nineteenforty_model.most_similar('chlidren')
twothousand_child = twothousand_model.most_similar('children')

#print child

#sentiment analysis ran on the 10 most similar words
eighteen_words = [i[0] for i in eighteen_child]
print "eighteen words"
print eighteen_words
eighteenforty_words = [i[0] for i in eighteenforty_child]
print "eighteen forty"
print eighteenforty_words
nineteen_words = [i[0] for i in nineteen_child]
print "nineteen words"
print nineteen_words
#nineteenforty_words = [i[0] for i in nineteenforty_child]
twothousand_words = [i[0] for i in twothousand_child]
print "two thousand"
print twothousand_words

eighteen_sentiment_score = sentiment(eighteen_words)
eighteenforty_score= sentiment(eighteenforty_words)
nineteen_score = sentiment(nineteen_words)
#nineteenforty_score = sentiment(nineteen_forty_words)
twothousand_sentiment_score = sentiment(twothousand_words)

print "eighteen sentiment"
print eighteen_sentiment_score

print "eighteen forty score"
print eighteenforty_score

print "nineteen score"
print nineteen_score

#print "nineteenforty score"
#print nineteenforty_score

print "two thousand sentiment"
print twothousand_sentiment_score
