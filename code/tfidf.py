#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 01:03:30 2017

@author: diop
"""

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from library_graph import csv_writer
#import pandas as pd

def get_matrix_and_features(corpus):
    """Return the sparse matrix X, the names of the features

    Parameters
    ----------
    corpus : dictionary 
        key = category 
        value = list of tokens obtained from the text in a given domain e.g ["Quick", "Fox",..]
    
    Returns
    -------
    X : sparse matrix
    feature_names : words in the corpus
   
    """
    documents_cleaned = [' '.join(words) for words in corpus.values()]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(documents_cleaned)
    feature_names = np.array(vectorizer.get_feature_names())
    return X, feature_names

def save_specificity_scores(corpus, nbre_elements = 20):
    """Print the nbre_elements most specific elements

    Parameters
    ----------
    corpus : dictionary 
        key = category 
        value = list of tokens obtained from the text in a given domain e.g ["Quick", "Fox",..]
        
    nbre_elements : num
   
    """
    X, feature_names = get_matrix_and_features(corpus)
    categories = corpus.keys()  
    for i in range(len(corpus)):
     category = categories[i]   
     print("Top words in category: {}".format(category))
     scores = {feature_names[col].encode("utf8") : X[i, col] for col in X.nonzero()[1]}
     sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
     for word, score in sorted_words[:nbre_elements]:
         print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))
     print
     #path = "../results/tf-idf/"+category+"_stemmed.csv"  
     path = "../results/tf-idf/"+category+".csv" 
     csv_writer(sorted_words, path)
     
