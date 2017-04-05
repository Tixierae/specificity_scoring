#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 05:09:14 2017

@author: diop
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from corpus2pairs import corpus2pairs
from counts2pmi import counts2pmi
from counts2vocab import counts2vocab
import networkx as nx
import numpy as np
import pandas as pd
from tfidf import get_vector_and_features

def construct_counts(categories, directory_name, thr=10) :
    for category in categories :   
        #print "Category : "+category
        corpus2pairs(category, directory_name)
        counts_path = directory_name+"/"+category+"2pairs" 
        counts2vocab(counts_path)
        
def construct_pmi_graphs(categories, directory_name, thr=10):
    """this function create a dictionnary of graphs with as key the category and as value a graph on the category"""
    graphs = {}
    for category in categories :
        print "Category : "+category
        #corpus2pairs(category, directory_name)
        vectors_path = counts_path = directory_name+"/"+category+"2pairs" 
        #counts2vocab(counts_path)
        pmi, words, contexts = counts2pmi(counts_path, vectors_path)
        ppmi_values = pmi.toarray()
        graph = create_graph_with_ppmi(ppmi_values, words, contexts)
        graphs[category] = graph
    return graphs   
                 
def create_graph_with_ppmi(ppmi_values, words, contexts) :
    g = nx.Graph() 
    num_words = len(words)
    num_contexts = len(contexts)
    for row in range(num_words):
        word = words[row]
        g.add_node(word)
        for col in range(num_contexts):
            pmi = ppmi_values[row, col] 
            context = contexts[col]
            if word != context and  pmi != 0 :
                g.add_edge(word, context, weight=pmi)
    return g

     
def print_more_specific_elements(corpus, categories, nbre_elements = 10):
    #get idf values
    X, feature_names, vectorizer = get_vector_and_features(corpus)
    idf = vectorizer.idf_
    print "Constructed vectorizer..."
    #construct_counts(categories,  "../data")
    graphs = construct_pmi_graphs(categories, "../data", 10)
    print "Constructed graphs..."
    """Takes a dictionnary in entry"""
    for key in graphs :
        print "Constructing ppmi graph for the category "+ key+ "..."
        g = graphs[key]
        cc = nx.clustering(g)
        for w in cc :
            if w in idf :
                cc[w] = idf[w]/cc[w] #to take into account words that are even rare in their corpus 
        cc_sorted = sorted(cc.items(), key=lambda x:x[1], reverse=True)
        max_cc = cc_sorted[0][1]   
        cc_sorted = [(a,b/max_cc) for a,b in cc_sorted]           
        print("Top words in category: {}".format(key))
        top_words = cc_sorted[:nbre_elements]
        for word, score in top_words:
            print("\tWord: {}, Clustering Coefficient: {}".format(word, round(score, 5)))
        print    
            