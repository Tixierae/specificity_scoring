# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


from data_collecting import get_corpus
import tfidf 
import graph_creation
import pmi_matrix
#list of categories
categories = ["Santé","Business","Immobilier","Sport", "Automobile"]
    
print "Getting corpus..."
#corpus = get_corpus(categories, lang="fr", download=True) #dic of lists
print "Corpus collected...."
for category in corpus:
    print("Size of the corpus  {} = {} words".format(category, len(corpus[category])))
    
print ""    
print "Using tf-idf..."   
tfidf.print_more_specific_elements(corpus) #using tf-idf
#print ""
#print "Using clustering coefficient..."  
graph_creation.print_more_specific_elements(corpus) #using clustering coefficient
#print "PMI Matrix..."  
#pmi_matrix.print_more_specific_elements(corpus, categories) #using clustering coefficient

    
