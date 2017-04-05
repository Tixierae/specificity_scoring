#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 05:53:41 2017

@author: diop
"""

from library_graph import terms_to_graph
import networkx as nx
from tfidf import get_vector_and_features

def create_graph(tokens, w=6):
    """This function has as input a text specific to a corpus and will return the graph of words
    w is the sliding window
    tokens = list of words
    """
    g = terms_to_graph(tokens, w)
    return g
    
    
def get_graphs(corpus):
    """this function create a dictionnary of graphs with as key the category and as value a graph on the category"""
    graphs = {}
    for key, document in corpus.iteritems() :
        #print document
        graph = create_graph(document)
        graphs[key] = graph
    return graphs    
    
def print_more_specific_elements(corpus, nbre_elements = 20):
    """Takes a dictionnary in entry"""
    X, feature_names, vectorizer = get_vector_and_features(corpus)
    idf = vectorizer.idf_
    for category, document in corpus.iteritems() :
        print "Constructing sliding window graph for the category "+ category+ "..."  
        g = create_graph(document)
        cc = nx.clustering(g)   
#        for w in cc :
#            if w in idf :
#                cc[w] = 1/(cc[w] + 1)
        cc_sorted = sorted(cc.items(), key=lambda x:x[1], reverse=True)
        #max_cc = cc_sorted[0][1]   
        #cc_sorted = [(a,b) for a,b in cc_sorted]           
        print("Top words in category: {}".format(category))
        top_words = cc_sorted[:nbre_elements]
        for word, score in top_words:
            print("\tWord: {}, Clustering Coefficient: {}".format(word, round(score, 5)))
        print    