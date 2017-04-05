#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 19:36:25 2017

@author: diop
"""
# Copyright 2014 Shubhanshu Mishra. All rights reserved.
# 
# This library is free software; you can redistribute it and/or
# modify it under the same terms as Python itself.

"""
This package is a port of the perl module Algorithm::WordLevelStatistics by
Francesco Nidito which can be found at:
    http://search.cpan.org/~nids/Algorithm-WordLevelStatistics-0.03/

The code is an implementation of the spatial statistics described in the
following paper:
@article{carpena2009level,
  title={Level statistics of words: Finding keywords in literary texts and symbolic sequences},
  author={Carpena, P and Bernaola-Galv{\'a}n, P and Hackenberg, M and Coronado, AV and Oliver, JL},
  journal={Physical Review E},
  volume={79},
  number={3},
  pages={035102},
  year={2009},
  publisher={APS}
}

Author: Shubhanshu Mishra
Published: December 29, 2014
License: GPL3

"""

import re, os, nltk
__version__ = "0.0.1"


# Module class create an object of this class to get the WordLevel Staticics.
class WordLevelStatistics():
    def __init__(self,word_pos=None,corpus_file=None):
        if word_pos is not None:
            self.word_pos = word_pos
        elif corpus_file is not None:
            self.word_pos = dict()
            self.pos_counter = 0
            if isinstance(corpus_file,list):
                for c in corpus_file:
                    self.gen_word_pos(c)
            else:
                self.gen_word_pos(corpus_file)

    def gen_word_pos(self,corpus_file):
        with open(corpus_file, ) as fp:
            text = fp.read()
            tokens = nltk.word_tokenize(text)
            tokens = [token for token in tokens if len(token)>2]
            for t in tokens:
                if t not in self.word_pos:
                    self.word_pos[t] = []
                self.word_pos[t].append(self.pos_counter)
                self.pos_counter += 1

    def compute_spectra(self):
        if self.word_pos is None or len(self.word_pos.keys()) < 1:
            return None
        # Count total words in the text.
        self.tot_words = sum([len(self.word_pos[k]) for k in self.word_pos.keys()])

        # Compute level statistics of all temrs
        self.level_stat = dict()
        for k in self.word_pos.keys():
            self.level_stat[k] = \
                    self.compute_spectrum(k)
        return self.level_stat

    def compute_spectrum(self,word):
        positions = self.word_pos[word]
        n = len(positions)
        ls = { 'count': n, 'C': 0, 'sigma_nor': 0 }
        if n > 3:
            # position -> distance from preceding element in text
            tmp = [positions[i+1] - positions[i] for i in range(n-1)]
            # len(tmp) = n-1
            avg = sum(tmp)*1.0/(n-1)
            sigma = sum([(k-avg)**2 for k in tmp])*1.0/(n-1)
            sigma = (sigma**(0.5))/avg

            p = n*1.0/self.tot_words
            ls['sigma_nor'] = sigma/((1.0-p)**.5)

            ls['C'] = (ls['sigma_nor'] - (2.0*n-1.0)/(2.0*n+2.0))\
                        * ((n**0.5) * (1.0+2.8*n**-0.865))
        return ls

if __name__ == "__main__":
    obj = WordLevelStatistics(corpus_file=["../data/Santé_cleaned.txt"])
    lvls = obj.compute_spectra()
    lvls = sorted(lvls.items(), key=lambda x: x[1]['C'], reverse=True)
    with open("Relativity.out","wb+") as fp:
        print >> fp, "word\tC\tcount\tsigma_nor"
        for k,v in lvls:
            print >> fp, "%s\t%s\t%s\t%s" % (k,v['C'],v['count'],v['sigma_nor'])
    print "Done computing"
