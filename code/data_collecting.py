# -*- coding: utf-8 -*-
"""
Spyder Editor

This file will download some articles from google news and wikipedia and other newspapers
 
"""
import re, string 
import nltk
import threading, Queue
#from eventregistry import *
from library_graph import clean_text_simple, hasNumbers
from stop_words import get_stop_words
import treetaggerwrapper
from gensim.models.phrases import Phrases
from news_paper_scrapper import get_lefigaro, get_lepoint, get_lesechos, get_lemonde, get_lexpress\
,get_google_news_query, read_article, get_wikipedia_titles, get_text_from_wikipedia


def get_corpus(categories, lang="fr", download = False):
    
    """Returns a dictionnary of corpuses (= a corpus is a long text) 

    Parameters
    ----------
    categories : dictionary
        key : string 
            category name
        value : list 
            list of keywords that are strongly related to this category 
        e.g: { "Santé" : ["santé", "médicament",...]}
        
    download : boolean 
        If False, that implies there are already some data present and we just have to exploit the texts
        If True , we download corpuses and save files in the directory /data
       
    Returns
    -------
    corpus : dictionnary 
        key = category 
        value = list of tokens obtained from the text in a given domain e.g ["Quick", "Fox",..]

    Examples
    --------
    >>> from data_collecting import get_corpus
    >>> categories = { 
            "Santé" : ["santé","médicament","médecin","soins","bien-être", \
            "centres de santé","prévention","maladie","guérison"]
        }    
    >>> corpus = get_corpus(categories, download=True) will create the files ../data/Santé.txt and ../data/Santé_cleaned.txt
    
    """
    categories_names = categories.keys()
    if download :
        """In this function, we concatenate the two corpus from wikipedia and from gnp"""
        #links = get_links(categories)
        print "Getting the texts from NewsPapers..."
        #orpus_gnp = get_corpus_from_gnp(categories, links)       
        #links_news_papers = get_links_from_newspapers(categories_names, lang)
        #save_corpus_from_newspapers(categories_names, links_news_papers)       
        print "Getting the texts from Wikipedia..."
        save_corpus_from_wikipedia(categories, lang) 
        save_corpus_cleaned(categories_names, lang)  
    corpus = {}
    for category in categories_names :
        print category
        #with open("../data/"+category+"_cleaned_and_stemmed.txt", "r") as f :
        with open("../data/"+category+"_cleaned.txt", "r") as f :
            content = f.read()
            corpus[category] = nltk.word_tokenize(content)
    return corpus 
               

def get_links_from_newspapers(categories, lang) :
    
    """Returns a dictionnary of lists of links to news articles (= a corpus is a long text) 

    Parameters
    ----------
    categories : list of string
        e.g :   ["Santé","Business","Immobilier","Séport", "Automobile"]
        
    lang : string 
        default : "fr" 
        
    Returns
    -------
    links : dictionnary 
        key = category 
        value = list of links to news articles e.g : ["http://lactualite.com", "http://www.lemonde.fr/police-justice/article/2017/04/11/le-camp-de-migrants-de-grande-synthe-ravage-par-un-incendie_5109126_1653578.html"]
    
    """
    links = {}  #'links' is a list of URLs pointing to the articles
    for category in categories :
        links[category] = get_google_news_query(category, lang)
        if lang == "fr":
            le_figaro_articles = get_lefigaro(category)       
            le_point_articles = get_lepoint(category)
            les_echos_articles = get_lesechos(category)
            le_monde_articles = get_lemonde(category)
            lexpress_articles = get_lexpress(category)
            links[category] += le_monde_articles + le_figaro_articles + le_point_articles + les_echos_articles + lexpress_articles  
    return links
        
def save_corpus_from_newspapers(categories, links):
    
    """Download articles given the links then save the corpus collected in different files in the directory ../data

    Parameters
    ----------
    categories : list of string
        e.g :   ["Santé","Business","Immobilier","Sport", "Automobile"]
        
    links : dictionary 
        key = category 
        value = list of links to news articles e.g : ["http://lactualite.com", "http://www.lemonde.fr/police-justice/article/2017/04/11/le-camp-de-migrants-de-grande-synthe-ravage-par-un-incendie_5109126_1653578.html"] 
         
    """
    for category in categories :
        print "Category: " + category           
        custom_links = links[category]
        filename = "../data/"+category+".txt"
        with open(filename, "a") as f:
            counter = 0
            for link in custom_links:
                q = Queue.Queue()
            	# will apply 'read_article' function to 'link' and store the result to the queue
                t = threading.Thread(target=lambda x, y: x.put(read_article(y)), args=(q, link))
            	# start thread (execute previous line)
                t.start()
            	# wait until the thread is done
                t.join()
            	# get result from queue
                text = q.get()
            	# store result
                if text :
                    text = text.replace("En poursuivant votre navigation sur ce site, vous acceptez nos CGV et l’utilisation de cookies pour vous proposer des contenus et services adaptés à vos centres d’intérêts et vous permettre l'utilisation de boutons de partages sociaux. En savoir plus et gérer ces paramètres édition abonné", "")
                    f.write(text.encode('utf8') + " ")
                counter += 1
                if counter % 100 == True:
                    print(counter, "articles processsed")
    print("Corpus collected from newspapers")      

def create_ngrams(category, lang):
    """Given a category, create n-grams for the text, clean the corpus and return the sentences cleaned

    Parameters
    ----------
    category : string 
        Name of the domain e.g :   "Santé","Business",etc.
        
    lang : string 
        default = "fr" 
    
    Returns
    -------
    sentences : list of string
            sentences[i] is a sentence in the corpus cleaned
    """
    tagger = treetaggerwrapper.TreeTagger(TAGLANG=lang) #to lemmatize words
    sentences = []
    bigrams_model = Phrases(min_count=100, threshold=10.0, delimiter="-") #to create bigrams
    filename = "../data/"+category+".txt"

    with open(filename, "r") as ins:      
        for line in ins:
            line = line.decode("utf8")
            lines = line.split('.')
            for l in lines :
                sentence = nltk.word_tokenize(l) 
                if sentence :
                    sentences.append(sentence)
                    #bigrams_model.add_vocab([sentence])         
    bigrams = list(bigrams_model[sentences])                
    #to create trigrams
    trigrams_model = Phrases(bigrams, min_count=50, threshold=10.0, delimiter="-")
    sentences = list(trigrams_model[bigrams]) 
           
    n = len(sentences) 
    for i in range(n):
        tags = tagger.tag_text(sentences[i])
        text =  [ tag.split('\t')[2] for tag in tags if tag.split('\t')[1] != "NUM" and tag.split('\t')[1] != "PUN"] 
        text = " ".join(text)
        text = clean_text_simple(text)
        sentences[i] = text
        if i % 10000 == True:
            print i, "sentences processsed"        
    sentences = [ sent for sent in sentences if len(sent) != 0]
    return sentences

def save_corpus_from_wikipedia(categories, lang):
    """Download articles given the titles then save the corpus collected in different files in the directory ../data

    Parameters
    ----------
    categories : dictionary
         key : string 
            category name
         value : list 
            list of keywords that are strongly related to this category 
         e.g: { "Santé" : ["santé", "médicament",...]}
        
    lang : string 
        default = "fr"
         
    """
 
    for category in categories :
        print "Category: " + category
        results = get_wikipedia_titles(categories[category],lang)       
        filename = "../data/"+category+".txt"
        with open(filename, "w") as f:  
            counter = 0
            for result in results:
                q = Queue.Queue()
            	# will apply 'get_text_from_wikipedia' function to 'link' and store the result to the queue
                t = threading.Thread(target=lambda x, y: x.put(get_text_from_wikipedia(y)), args=(q, result))
            	# start thread (execute previous line)
                t.start()
            	# wait until the thread is done
                t.join()
            	# get result from queue
                text = q.get()
            	# store result
                if text :
                    #text = text.replace(u"En poursuivant votre navigation sur ce site, vous acceptez nos CGV et l’utilisation de cookies pour vous proposer des contenus et services adaptés à vos centres d’intérêts et vous permettre l'utilisation de boutons de partages sociaux. En savoir plus et gérer ces paramètres édition abonné", "")
                    text = text.replace("Portail", "")
                    f.write(text.encode('utf8') + " ")
                counter += 1
                if counter % 100 == True:
                    print(counter, "article(s) processsed")       
    print("Corpus collected from Wikipedia")    
    
def save_corpus_cleaned(categories, lang): 
    
    """Save corpus cleaned in different files in the directory ../data

    Parameters
    ----------
    categories : list of string
        e.g :   ["Santé","Business","Immobilier","Sport", "Automobile"]
        
    lang : string
        default = "fr" 
         
    """
    print "Saving corpus cleaned..."
    for category in categories : 
        print "Category: " + category           
        sentences = create_ngrams(category, lang) 
        print "Created n-grams..." 
        filename = "../data/"+category+"_cleaned.txt"
        #filename = "../data/"+category+"_cleaned_and_stemmed.txt"
        with open(filename, "w") as f:
            for sentence in sentences :
                #sentence = re.sub(' +',' ',sentence)
                if sentence :
                    f.write(sentence.encode('utf8') + " ") 
    print "Corpus cleaned saved..."
    
    