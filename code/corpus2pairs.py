#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 06:33:41 2017

@author: diop
"""
from collections import Counter
import numpy as np
from random import Random

def read_vocab(thr, category, directory_name) :
    """
    Options:
        --thr NUM    The minimal word count for being in the vocabulary [default: 10]
    """
    vocab = Counter()
    corpus_file = directory_name+"/"+category+".txt"
    with open(corpus_file) as f:
        for line in f:
            vocab.update(Counter(line.strip().split()))
    return dict([(token, count) for token, count in vocab.items() if count >= thr])
    
def corpus2pairs(category, directory_name, pos = False, dyn=True, delete = True, sub = 0, thr=10, win = 2):
    """
        Options:
        --category STRING category of the corpus    
        --thr NUM    The minimal word count for being in the vocabulary [default: 10]
        --win NUM    Window size [default: 2]
        --pos        Positional contexts
        --dyn        Dynamic context windows
        --sub NUM    Subsampling threshold [default: 0]
        --delete        Delete out-of-vocabulary and subsampled placeholders
    """
    subsample = sub
    sub = subsample != 0
    d3l = delete
    vocab = read_vocab(thr, category, directory_name)
    corpus_size = sum(vocab.values())
    
    subsample *= corpus_size
    subsampler = dict([(word, 1 - np.sqrt(subsample / count)) for word, count in vocab.items() if count > subsample])
    
    rnd = Random(17)
    corpus_file = directory_name+"/"+category+".txt"
    pairs = []  
    with open(corpus_file) as f: 
        for line in f:       
            tokens = [t if t in vocab else None for t in line.strip().split()]
            if sub:
                tokens = [t if t not in subsampler or rnd.random() > subsampler[t] else None for t in tokens]
            if d3l:
                tokens = [t for t in tokens if t is not None]
            
            len_tokens = len(tokens)
            
            for i, tok in enumerate(tokens):
                if tok is not None:
                    if dyn:
                        dynamic_window = rnd.randint(1, win)
                    else:
                        dynamic_window = win
                    start = i - dynamic_window
                    if start < 0:
                        start = 0
                    end = i + dynamic_window + 1
                    if end > len_tokens:
                        end = len_tokens
                    
                    if pos:
                        output = [row for row in [tok + ' ' + tokens[j] + '_' + str(j - i) for j in xrange(start, end) if j != i and tokens[j] is not None] if len(row) > 0]
                    else:
                        output = [row for row in [tok + ' ' + tokens[j] for j in xrange(start, end) if j != i and tokens[j] is not None] if len(row) > 0]
                    if len(output) > 0:
                        #new_f.write(output + '\n')
                        #print output
                        for pair in output :
                            pairs.append(pair)                         
    pairs_freq = Counter(pairs)              
    filename = directory_name+"/"+category+"2pairs"                        
    with open(filename, "w") as new_f:
        for key in pairs_freq:
            val = pairs_freq[key]
            line = key + " " + str(val)
            #print line
            new_f.write(line + '\n')        