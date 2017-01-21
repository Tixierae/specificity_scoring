# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


from data_collecting import get_corpus
import tfidf 
from CoreRank_functions import clean_text_simple
#import graph_creation
#list of categories
categories = ["International", "Economy", "Science", "Technology", "Sport", "Culture", "Health", "Politics", "Society", "Business", "Car", "Start-up", "Food"]

print "Getting corpus..."
corpus = get_corpus(categories) #dic of lists
print "Corpus collected...."
for category in corpus:
    print("Size of the corpus  {} = {} words".format(category, len(corpus[category])))
        
cleaned_corpus = corpus
for category in cleaned_corpus :
    cleaned_corpus[category] = clean_text_simple(cleaned_corpus[category])

print ""    
print "Using tf-idf..."   
tfidf.print_more_specific_elements(cleaned_corpus) #using tf-idf
#print ""
#print "Using clustering coefficient..."  
#graph_creation.print_more_specific_elements(cleaned_corpus) #using clustering coefficient


