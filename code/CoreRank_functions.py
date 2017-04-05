import string
import re 
import itertools
import copy
import igraph
import nltk

from nltk.corpus import stopwords
# requires nltk 3.2.1
from nltk import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
import csv
import networkx as nx
from itertools import groupby
             
def clean_text_simple(text, remove_stopwords=True, pos_filtering=True, stemming=True, countries=None):
    
    punct = string.punctuation.replace('-', '')
    
    # convert to lower case
    text = text.lower()
    #remove countries
           
    # remove punctuation (preserving intra-word dashes)
    if countries :
        text = ''.join(l for l in text if l not in punct and l not in countries)
    #strip years, dates, ages
    pattern1 = re.compile(r'\d+-\d+')
    text = pattern1.sub("",text)    
    pattern2 = re.compile(r'\d+th')
    text = pattern2.sub("",text)   
    pattern3 = re.compile(r'\d+-year(s)*')
    text = pattern3.sub("",text)  
    pattern4 = re.compile(r'\d+-year(s)*-old')
    text = pattern4.sub("",text)
    pattern5 = re.compile(r'year\S+')
    text = pattern5.sub("",text)
    pattern6 = re.compile(r'month\S+')
    text = pattern6.sub("",text)
    pattern7 = re.compile(r'day\S+')
    text = pattern7.sub("",text)
    pattern8 = re.compile(r'day\S+')
    text = pattern8.sub("",text)
    # strip extra white space
    text = re.sub('\n',' ',text)
    text = re.sub(' +',' ',text)
    # strip leading and trailing white space
    text = text.strip()
    # tokenize (split based on whitespace)
    tokens = text.split(' ')
    if pos_filtering == True:
        # apply POS-tagging
        tagged_tokens = pos_tag(tokens)
        # retain only nouns and adjectives
        tokens_keep = []
        for i in range(len(tagged_tokens)):
            item = tagged_tokens[i]
            if (
            item[1] == 'NN' or
            item[1] == 'NNS' or
            item[1] == 'NNP' or
            item[1] == 'NNPS' or
            item[1] == 'JJ' or
            item[1] == 'JJS' or
            item[1] == 'JJR'
            ):
                tokens_keep.append(item[0])
        tokens = tokens_keep
    if remove_stopwords:
        stpwds = stopwords.words('english')
        # remove stopwords
        tokens = [token for token in tokens if token not in stpwds and token[0].isalpha() and len(token) > 3]
    if stemming:
        #lmtzr = WordNetLemmatizer()
        stemmer = nltk.stem.PorterStemmer()
        # apply Porter's stemmer
        tokens_stemmed = list()
        for token in tokens:
            tokens_stemmed.append(stemmer.stem(token))
        tokens = tokens_stemmed
    tokens = [x[0] for x in groupby(tokens)]    
    return(tokens)

def terms_to_graph(terms, w):
    # This function returns a directed, weighted igraph from a list of terms (the tokens from the pre-processed text) e.g., ['quick','brown','fox']
    # Edges are weighted based on term co-occurence within a sliding window of fixed size 'w'
    
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
    #g = igraph.Graph(directed=True)
    g = nx.Graph()
    
    # add vertices
    g.add_nodes_from(sorted(set(terms)))   
    
    # add edges, direction is preserved since the graph is directed
    weighted_edges = [(key[0], key[1], val) for key, val in from_to.iteritems()]
    g.add_weighted_edges_from(weighted_edges)
    
    # set edge and vertice weights
    #g.es['weight'] = from_to.values() # based on co-occurence within sliding window
    #g.vs['weight'] = g.strength(weights=from_to.values()) # weighted degree
    
    return(g)
