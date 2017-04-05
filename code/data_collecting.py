# -*- coding: utf-8 -*-
"""
Spyder Editor

This file will download some articles from google news and wikipedia

"""
#import gnp
import re 
import nltk
import gnp
import json
import threading, Queue
from newspaper import Article
#from eventregistry import *
from library_graph import clean_text_simple
import os
import wikipedia
import treetaggerwrapper
from gensim.models.phrases import Phraser, Phrases
from news_paper_scrapper import *


def get_corpus(categories, lang="fr", download = False):
    
    if download :
        """In this function, we concatenate the two corpus from wikipedia and from gnp"""
        #links = get_links(categories)
        print "Getting the texts from NewsPapers..."
        #corpus_gnp = get_corpus_from_gnp(categories, links)
        if lang == "fr":
            links_french_news_papers = get_links_from_french_newspapers(categories)
            get_corpus_from_newspapers(categories, links_french_news_papers)       
        print "Getting the texts from Wikipedia..."
        get_corpus_from_wikipedia(categories, lang) 
        clean_corpus(categories, lang)  
    corpus = {}
    filenames = os.listdir("../data")
    filenames = [ f for f in filenames if f.endswith("_cleaned.txt")]
    for filename in filenames :
        category = filename[:-12] 
        with open("../data/"+filename, "r") as f :
            content = f.read()
            corpus[category] = content.split(" ")
    return corpus 
               

def get_links_from_french_newspapers(categories) :  
    links = {}  #'links' is a list of URLs pointing to the articles
    for category in categories :
        print category
        le_figaro_articles = get_lefigaro(category)       
        le_point_articles = get_lepoint(category)
        les_echos_articles = get_lesechos(category)
        le_monde_articles = get_lemonde(category)
        lexpress_articles = get_lexpress(category)
        google_news_articles = get_google_news_query(category)
        links[category] = le_monde_articles + le_figaro_articles + le_point_articles + les_echos_articles + google_news_articles
        print("Corpus collected from Le Point, LesEchos, Le Figaro, Le Monde, Google Actualités for the category : "+category)
    return links
        
def get_corpus_from_newspapers(categories, links):
    """this dictionnary returns a dictionnary of corpus : each element is a a text belonging to a certain category
     categories is a list of categories
     links is a dictionnary of corpus with each value being a list of links
     key = category
     value = list of texts in this category
    """
    for category in categories :
              
        custom_links = links[category]
        print category
        filename = "../data/"+category+".txt"
        with open(filename, "a") as f:
            counter = 0
            for link in custom_links:
                q = Queue.Queue()
            	# will apply 'get_text_from_link' function to 'link' and store the result to the queue
                t = threading.Thread(target=lambda x, y: x.put(read_article(y)), args=(q, link))
            	# start thread (execute previous line)
                t.start()
            	# wait until the thread is done
                t.join()
            	# get result from queue
                text = q.get()
            	# store result
                if text :
                    f.write(text.encode('utf8') + " ")
                counter += 1
                if counter % 100 == True:
                    print(counter, "articles processsed")
    print("Corpus collected from newspapers")      

def create_ngrams(category, lang):
    #stemmer = nltk.stem.snowball.FrenchStemmer()
    tagger = treetaggerwrapper.TreeTagger(TAGLANG=lang)
    sentences = []
    bigrams_model = Phrases(min_count=10, threshold=10.0)
    with open("../data/"+category+".txt", "r") as ins:
        for line in ins:
            lines = line.decode('utf8').split('.')
            for l in lines :
                sentence = nltk.word_tokenize(l) 
                if sentence :
                    sentences.append(sentence)
                    bigrams_model.add_vocab([sentence])  
    bigrams = list(bigrams_model[sentences])                
    
    trigrams_model = Phrases(bigrams, min_count=10, threshold=10.0)
    trigrams = list(trigrams_model[bigrams])
    
    fourgrams_model = Phrases(trigrams, min_count=10, threshold=10.0)
    fourgrams = list(fourgrams_model[trigrams])
    
    fivegrams_model = Phrases(fourgrams, min_count=10, threshold=10.0)
    sentences = list(fivegrams_model[fourgrams])             
    n = len(sentences) 
    for i in range(n):
        text = " ".join(sentences[i])
        text = clean_text_simple(text)
        text = " ".join(text)
        text = text.strip()
        if len(text) != 0:
            tags = tagger.tag_text(text)
            sentences[i] = [ tag.split('\t')[2] for tag in tags]
    sentences = [ " ".join(sent) for sent in sentences if len(sent) != 0]
    return sentences

def get_corpus_from_wikipedia(categories, lang):
    """this dictionnary returns a dictionnary of corpus : each element is a a text belonging to a certain category
     categories is a list of categories
     links is a dictionnary of corpus with each value being a list of links
     key = category
     value = list of texts in this category
    """
    wikipedia.set_lang(lang)    
    for category in categories :
        #results = wiki.find(category)
        results = wikipedia.search(category, 500)
        print category
        filename = "../data/"+category+".txt"
        with open(filename, "a") as f:  
            counter = 0
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
                #text = clean_text_simple(text)
                #text = " ".join(text)
            	# store result
                if text :
                    f.write(text.encode('utf8') + " ")
                counter += 1
                if counter % 100 == True:
                    print(counter, "articles processsed")       
    print("Corpus collected from Wikipedia")    
    
def clean_corpus(categories, lang):  
    for category in categories :
        print "Creating bi-grams..."        
        sentences = create_ngrams(category, lang) 
        print "Created bi-grams..." 
        filename = "../data/"+category+"_cleaned.txt"
        with open(filename, "w") as f:
            for sentence in sentences :
                sentence = re.sub(' +',' ',sentence)
                f.write(sentence.encode('utf8') + " ") 
    
#def get_links(categories) :
#    """this function returns links to articles that belong to categories specified
#    
#    input : categories = list of categories names
#    output : 
#    the result is a dictionnary with as keys the category and 
#    as value a list of all links of articles in this category
#    categories : 
#    """
##    er = EventRegistry(apiKey = "dd57c2f0-2ac7-4b0b-9b1a-01d3322c99d5")
#    links = {}  #'links' is a list of URLs pointing to the articles
#    for category in categories :
#        print "Getting links for "+category+"..."
#        links[category] = []
#        filename = "../data/"+category+"_links_from_google_news_paper.txt"
#        with open(filename, "w") as f: 
##        q = QueryArticlesIter(lang="eng")
##        q.addConcept(er.getConceptUri(category))
##        q.addRequestedResult(RequestArticlesInfo(count = 30, returnInfo = ReturnInfo()))
##        for article in q.execQuery(er, articleBatchSize = 50):
##            if "url" in article :
##                links[category].append(article["url"]) 
#        #this was the code for Google News Paper but the API doesn't work very well        
#            news = gnp.get_google_news_query(category)
#            news_to_json = json.loads(json.dumps(news, indent=4))
#            for story in news_to_json['stories'] :
#                    links.append(story['link'])
#                    f.write(story['link'].encode('utf8') + "\n")
#    return links    
    
                                
