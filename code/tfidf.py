#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 01:03:30 2017

@author: diop
"""

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd

def get_vector_and_features(corpus):
    """
    this function returns the sparse matrix X and the names of the features
    corpus is a list of documents
    """
    documents_cleaned = [' '.join(words) for words in corpus.values()]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(documents_cleaned)
    feature_names = np.array(vectorizer.get_feature_names())
    return X, feature_names, vectorizer

def print_more_specific_elements(corpus, nbre_elements = 10):
    """
    this function returns the nbre_elements more specific words in the corpus given
    corpus is a dict with as key the category name and as value the text
    """
    X, feature_names, vectorizer = get_vector_and_features(corpus)
    categories = corpus.keys()  
    for i in range(len(corpus)):
     print("Top words in category: {}".format(categories[i]))
     scores = {feature_names[col] : X[i, col] for col in X.nonzero()[1]}
     sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
     for word, score in sorted_words[:nbre_elements]:
         print("\tWord: {}, TF-IDF: {}".format(word.encode('utf-8'), round(score, 5)))
     print 
     
