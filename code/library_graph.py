#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import string
import re 
import itertools
import csv
import nltk
#from nltk.corpus import stopwords
from stop_words import get_stop_words
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
# requires nltk 3.2.1
import igraph
 
def hasNumbers(inputString):
     return bool(re.search(r'\d', inputString))
               
def csv_writer(data, path):
    """
    Write data to a CSV file path
    """
    with open(path, "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(("Word","Specificity Score"))
        for line in data:
            writer.writerow(line)
             
def clean_text_simple(text, remove_stopwords=True, lang="fr"):
    
    """Returns a list of tokens 

    Parameters
    ----------
    text : string 
    remove_stopwords : boolean
    pos_filtering : boolean    
    lang : string
        default : "fr"
        
    Returns
    -------
    tokens : list of strings (tokens)

    Examples
    --------
    >>> from library_graph import clean_text_simple
    >>> text = "Je n'aime pas du tout aller à la plage"
    >>> tokens = clean_text_simple(text) => [u'aime', u'aller', u'plage']
    
    Warning !! L'encoding doit-être en utf-8
    
    """
    if not text :
        return []
    
    
    # apply POS-tagging and retain only nouns (not personal nouns), adjectives and verbs
    text = text.replace("|", " ")
    permitted_pos_tags = ['NN', 'NNS','VB', 'VBN', 'VBG', 'JJ', 'JJS', 'JJR']
    blob = TextBlob(text, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer())
    tags = blob.tags
    
    #lemmatizing verbs and singularizing words            
    tokens = [item[0].lower() for item in tags if item[1] in permitted_pos_tags] # there is also a conversion to lower case
    
    punct = string.punctuation.replace('-', '')
    
    #remove stopwords if there are remaining
    stpwds = get_stop_words(lang) #stopwords
    
    pattern_hours = re.compile('\d+h\d+')   
    pattern_figures = re.compile('\d+')
    first_component_bigram = re.compile("^([A-z]*)-")
    
    #remove hours and dates
    tokens = [pattern_hours.sub('', token) for token in tokens]
    tokens = [pattern_figures.sub('', token) for token in tokens] 
    #remove punctuation
    tokens = [token for token in tokens if token not in punct ]
    #remove bigrams and trigrams that start with a stopword
    tokens = [first_component_bigram.sub('', token) if (first_component_bigram.findall(token) and first_component_bigram.findall(token)[0] in stpwds) else token for token in tokens ]
    tokens = [first_component_bigram.sub('', token) if (first_component_bigram.findall(token) and first_component_bigram.findall(token)[0] in stpwds) else token for token in tokens ]
    tokens = [token for token in tokens if len(token) > 2]
    punct = string.punctuation
    tokens = [token.strip(punct) for token in tokens]
    tokens = [token for token in tokens if token not in stpwds ]
    #stemmer = nltk.stem.snowball.FrenchStemmer()
    #tokens = [stemmer.stem(token) for token in tokens]
    
 
    return( " ".join(tokens))

def terms_to_graph(terms, w):
    
    """Returns a weighted graph from a list of terms (the tokens from the pre-processed text) e.g., ['quick','brown','fox'] 
    Edges are weighted based on term co-occurence within a sliding window of fixed size 'w'
    
    Parameters
    ----------
    terms : list of strings
    w : sliding_window size    
    
    Returns
    -------
    g : directed weigthed graph
    
    """
  
    from_to = {}
    
    # create initial complete graph (first w terms)
    terms_temp = terms[0:w]
    indexes = list(itertools.combinations(range(w), r=2))
    
    new_edges = []
    
    for my_tuple in indexes:
        new_edges.append(tuple([terms_temp[i] for i in my_tuple]))
    
    for new_edge in new_edges:
        if new_edge in from_to:
            from_to[new_edge] += 1
        else:
            from_to[new_edge] = 1
    
    # then iterate over the remaining terms
    for i in xrange(w, len(terms)):
        # term to consider
        considered_term = terms[i]
        # all terms within sliding window
        terms_temp = terms[(i-w+1):(i+1)]
        
        # edges to try
        candidate_edges = []
        for p in xrange(w-1):
            candidate_edges.append((terms_temp[p],considered_term))
            
        for try_edge in candidate_edges:
        
            # if not self-edge
            if try_edge[1] != try_edge[0]:
                
                # if edge has already been seen, update its weight
                if try_edge in from_to:
                    from_to[try_edge] += 1
                
                # if edge has never been seen, create it and assign it a unit weight     
                else:
                    from_to[try_edge] = 1
    
    # create empty graph
    g = igraph.Graph(directed=True)
    
    # add vertices
    g.add_vertices(sorted(set(terms)))
    
    # add edges, direction is preserved since the graph is directed
    g.add_edges(from_to.keys())
    
    # set edge and vertice weights
    g.es['weight'] = from_to.values() # based on co-occurence within sliding window
    g.vs['weight'] = g.strength(weights=from_to.values()) # weighted degree
    
    return(g)

        
