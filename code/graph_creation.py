#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 05:53:41 2017

@author: diop
"""

from library_graph import terms_to_graph, csv_writer
import csv

def create_graph(tokens, w=5):
    """Return the graph of words given the corpus(=text)

    Parameters
    ----------
    tokens : list of string
        e.g :   ["Santé","Business","Immobilier","Sport", "Automobile"]
        
    w : sliding_window size
       
    Returns
    -------
    g : directed weigthed graph 
   
    """
    
    g = terms_to_graph(tokens, w)
    return g
    
def get_weights(g):
     """Return the weights of a graph of words

     Parameters
     ----------
     g : directed graph
       
     Returns
     -------
     weights : list of num
        
    
     """
     edge_weights = []
     for edge in g.es:
         #source = g.vs[edge.source]['name']
         #target = g.vs[edge.target]['name']
         #edges.append([source, target])
         weight = edge['weight']
         edge_weights.append(weight) 
     return edge_weights
    
def save_specificity_scores(corpus, nbre_elements = 20):
    """Print the nbre_elements most specific elements

    Parameters
    ----------
    corpus : dictionary 
        key = category 
        value = list of tokens obtained from the text in a given domain e.g ["Quick", "Fox",..]
        
    nbre_elements : num
   
    """ 
    for category, document in corpus.iteritems() :
        print "Constructing sliding window graph for the category "+ category+ "..."  
        g = create_graph(document)
        weights = get_weights(g)
        cc = g.transitivity_local_undirected(weights=weights)
        words = g.vs["name"]
        scores = zip(words, cc)
        scores.sort(reverse=True, key=lambda x:x[1])         
        print("Top words in category: {}".format(category))
        top_words = scores[:nbre_elements]  
        for word, score in top_words:
            print("\tWord: {}, Clustering Coefficient: {}".format(word, round(score, 5)))
        print 
        path = "../results/graph_of_words/"+category+".csv" 
        #path = "../results/graph_of_words/"+category+"_stemmed.csv" 
        csv_writer(scores, path)