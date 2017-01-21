#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 01:37:44 2017

@author: diop
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This file will download some articles from google news with the title and the link to the full article
The title and the links anre then registered in a file Categories/category_name
where category_name is the name of the category and we get the current article thanks to newspaper

"""

import gnp
import json
import threading, Queue
from newspaper import Article
from wikiapi import WikiApi

wiki = WikiApi({ 'locale' : 'en'})

def get_corpus(categories):
    """In this function, we concatenate the two corpus from wikipedia and from gnp"""
    links = get_links(categories)
    print "Getting the texts from Google News Paper..."
    corpus_gnp = get_corpus_from_gnp(categories, links)
    print "Getting the texts from Wikipedia..."
    corpus_wikipedia = get_corpus_from_wikipedia(categories)
    for key in corpus_gnp :
        corpus_gnp[key] = [corpus_gnp[key]]
        corpus_gnp[key].append(corpus_wikipedia[key])
        corpus_gnp[key] = "".join(text for text in corpus_gnp[key])
    return corpus_gnp
    
def get_text_from_gnp(link):
	a = Article(link, language='en')
	a.download()
	a.parse()
	s = a.text
	return s
 
def get_text_from_wikipedia(result):
	a = wiki.get_article(result)
	return a.content 

def get_links(categories) :
    """this function returns links to articles that belong to categories specified
    the result is a dictionnary with as keys the category and as value a list of all links of articles in this category
    categories is a list of categories
    """
    links = {}  #'links' is a list of URLs pointing to the articles
    for category in categories :
        links[category] = []
        news = gnp.get_google_news_query(category)
        news_to_json = json.loads(json.dumps(news, indent=4))
        for story in news_to_json['stories'] :
                links[category].append(story['link'])
    return links

def get_corpus_from_gnp(categories, links):
    """this dictionnary returns a dictionnary of corpus : each element is a a text belonging to a certain category
     categories is a list of categories
     links is a dictionnary of corpus with each value being a list of links
     key = category
     value = list of texts in this category
    """
    corpus = {}
    for category in categories :
        corpus[category] = []
        custom_links = links[category]
        #print category
        for link in custom_links:
            q = Queue.Queue()
        	# will apply 'get_text_from_link' function to 'link' and store the result to the queue
            t = threading.Thread(target=lambda x, y: x.put(get_text_from_gnp(y)), args=(q, link))
        	# start thread (execute previous line)
            t.start()
        	# wait until the thread is done
            t.join()
        	# get result from queue
            text = q.get()
        	# store result
            corpus[category].append(text)
        corpus[category] = "".join([txt for txt in corpus[category]]) #this line is to concatenate texts of the category into one
    return corpus
    
def get_corpus_from_wikipedia(categories):
    """this dictionnary returns a dictionnary of corpus : each element is a a text belonging to a certain category
     categories is a list of categories
     links is a dictionnary of corpus with each value being a list of links
     key = category
     value = list of texts in this category
    """
    corpus = {}
    for category in categories :
        corpus[category] = []
        results = wiki.find(category)
        #print category
        for result in results:
            q = Queue.Queue()
        	# will apply 'get_text_from_link' function to 'link' and store the result to the queue
            t = threading.Thread(target=lambda x, y: x.put(get_text_from_wikipedia(y)), args=(q, result))
        	# start thread (execute previous line)
            t.start()
        	# wait until the thread is done
            t.join()
        	# get result from queue
            text = q.get()
        	# store result
            corpus[category].append(text)
        corpus[category] = "".join([txt for txt in corpus[category]]) #this line is to concatenate texts
    return corpus    

