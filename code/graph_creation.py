#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 05:53:41 2017

@author: diop
"""

from library_graph import terms_to_graph

def create_graph(tokens, w=5):
    """This function has as input a text specific to a corpus and will return the graph of words
    w is the sliding window
    tokens = list of words
    """
    g = terms_to_graph(tokens, w)
    return g
    
def get_weights(g):
    """This function takes as input a graph and return weights"""
    edge_weights = []
    for edge in g.es:
        #source = g.vs[edge.source]['name']
        #target = g.vs[edge.target]['name']
        #edges.append([source, target])
        weight = edge['weight']
        edge_weights.append(weight) 
    return edge_weights
    
    
def get_graphs(corpus):
    """this function create a dictionnary of graphs with as key the category and as value a graph on the category"""
    graphs = {}
    for key, document in corpus.iteritems() :
        graph = create_graph(document)
        graphs[key] = graph
    return graphs    
    
def print_more_specific_elements(corpus, nbre_elements = 10):
    graphs = get_graphs(corpus)
    for category in graphs :
        g = graphs[category]
        weights = get_weights(g)
        cc = g.transitivity_local_undirected(weights=weights)
        words = g.vs["name"]
        scores = [(word,coeff) for word in words for coeff in cc]
        print("Top words in category: {}".format(category))
        sorted_words = sorted(scores, key=lambda x: x[1], reverse=True)
        for word, score in sorted_words[:nbre_elements]:
            print("\tWord: {}, Clustering Coefficient: {}".format(word.encode('utf-8'), round(score, 5)))
        print    
