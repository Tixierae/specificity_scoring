#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 05:09:14 2017

@author: diop
"""
from corpus2pairs import corpus2pairs
from counts2pmi import counts2pmi
from counts2vocab import counts2vocab
import networkx as nx
from library_graph import csv_writer
from graph_creation import get_weights

def construct_pmi_graphs(categories, directory_name, thr=10):
    """Return the graphs of words given the corpus(=text)

    Parameters
    ----------
    categories : list of string
        e.g :   ["Santé","Business","Immobilier","Sport", "Automobile"]
    directory_name : "../data"
    thr : num    
        
    w : sliding_window size
       
    Returns
    -------
    graphs : dictionary of weigthed directed graphs 
   
    """
    graphs = {}
    for category in categories :
        print "Category : "+category
        # Extracts a collection of word-context pairs from the corpus and aggregates identical word-context pairs.
        corpus2pairs(category, directory_name)
        vectors_path = counts_path = directory_name+"/"+category+"2pairs" 
        #Creates vocabularies with the words' and contexts' unigram distributions.
        counts2vocab(counts_path)
        #Creates a PMI matrix (*scipy.sparse.csr_matrix*) from the counts.
        pmi, words, contexts = counts2pmi(counts_path, vectors_path) 
        ppmi_values = pmi.toarray()
        #Creates a weigthed undirected graph with as weigth ppmi value
        graph = create_graph_with_ppmi(ppmi_values, words, contexts)
        graphs[category] = graph
    return graphs   
                 
def create_graph_with_ppmi(ppmi_values, words, contexts) :
    """Helper Function 
    Return a directed weigthed graph of words given the ppmi_values
   
    """
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

     
def save_specificity_scores(corpus, nbre_elements = 10):
    """Print the nbre_elements most specific elements

    Parameters
    ----------
    corpus : dictionary 
        key = category 
        value = list of tokens obtained from the text in a given domain e.g ["Quick", "Fox",..]
        
    nbre_elements : num
   
    """
    categories = corpus.keys()
    graphs = construct_pmi_graphs(categories, "../data", 10)
    print "Constructed graphs..."
    """Takes a dictionnary in entry"""
    for key in graphs :
        print "Constructing ppmi graph for the category "+ key+ "..."
        g = graphs[key]
        cc = nx.clustering(g)
#        for w in cc :
#            if w in idf :
#                cc[w] = idf[w]/cc[w] #to take into account words that are even rare in their corpus 
        cc_sorted = sorted(cc.items(), key=lambda x:x[1], reverse=True)
        max_cc = cc_sorted[0][1]   
        cc_sorted = [(a,b/max_cc) for a,b in cc_sorted]           
        print("Top words in category: {}".format(key))
        top_words = cc_sorted[:nbre_elements]
        for word, score in top_words:
            print("\tWord: {}, Clustering Coefficient: {}".format(word, round(score, 5)))
        print  
        #path = "../results/ppmi_matrix/"+key+"_stemmed.csv"
        path = "../results/ppmi_matrix/"+key+".csv"
        csv_writer(cc_sorted, path) 
        