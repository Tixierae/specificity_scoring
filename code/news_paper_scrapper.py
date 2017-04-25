#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 23:36:22 2017

@author: diop
"""
import sys
import requests
from newspaper import Article
import wikipedia
from bs4 import BeautifulSoup

sys.tracebacklimit = 0

def read_article(link, lang='fr') :
    """Returns the content of a web article given the link to this article.


    Parameters
    ----------
    link : string
    lang : string 
    The default lang is French ("fr") 
    but the list of all languages is accessible through "newspaper.languages()" after importing newspaper

    Returns
    -------
    article_content : string

    Examples
    --------
    >>> from news_paper_scrapper import read_article
    >>> link = "http://edition.cnn.com/2017/04/10/politics/syria-russia-iran-missile-strikes/"
    >>> article_content = read_article(link, lang="en")
    
    """
    try :
        a = Article(link, language=lang)
        a.download()  
        a.parse()
        s = a.text
        return s
    except :
        return ''
        
def get_text_from_wikipedia(title):
    """Returns the content of a wikipedia article given the title of the article.

    Parameters
    ----------
    title : string
    
    Returns
    -------
    article_content : string

    Examples
    --------
    >>> from news_paper_scrapper import get_text_from_wikipedia
    >>> title = "Barack Obama"
    >>> article_content = get_text_from_wikipedia(title)
    
    """
    try :
        article = wikipedia.page(title)
        content = article.content
        return content    
    except :
        return ''    
    
     
def get_lemonde(keyword, num_pages=41):
    """Returns a list of links to articles in "Le Monde" related to a certain keyword
    Articles are in french but they are sometimes very short because we must have a subscription to read some articles

    Parameters
    ----------
    keyword : string e.g : Santé, Médecine, etc.
    num_pages : num 
        In general, num_pages < 50 but this can be checked in the website
       
    Returns
    -------
    list_of_links : list
        A list of links to articles related to our keyword

    Examples
    --------
    >>> from news_paper_scrapper import get_lemonde
    >>> keyword = "Santé"
    >>> links = get_lemonde(keyword)
    
    """
    links_keyword = []
    keyword = keyword.lower()
    for i in range(1,num_pages) : #the search results are in many pages : we use the first 200 pages
        url = "http://www.lemonde.fr/recherche/?keywords="+keyword+"&page_num="+str(i)+"&operator=and&exclude_keywords=&qt=recherche_titre&author=&period=since_1944&start_day=01&start_month=01&start_year=1944&end_day=06&end_month=04&end_year=2017&sort=pertinence"
        r = requests.get(url)
        if r.status_code == 200 :
            soup = BeautifulSoup(r.text, "html.parser")
            letters = soup.find_all("h3", class_="txt4_120")
            for x in range(0, len(letters)):
                link = 'http://www.lemonde.fr'+letters[x].a["href"]
                links_keyword.append(link)   
    return list(set(links_keyword)) 
    
def get_lefigaro(keyword):
    """Returns a list of links to articles in "Le Figaro" related to a certain keyword
    Articles are in french but they are sometimes very short because we must have a subscription to read some articles

    Parameters
    ----------
    keyword : string e.g : Santé, Médecine, etc.
    
    Returns
    -------
    list_of_links : list
        A list of links to articles related to our keyword - about 20 links
 
    Examples
    --------
    >>> from news_paper_scrapper import get_lefigaro
    >>> keyword = "Santé"
    >>> links = get_lefigaro(keyword)
    
    """
    links_keyword = []
    keyword = keyword.lower()
    url = "http://recherche.lefigaro.fr/recherche/"+keyword
    r = requests.get(url)
    if r.status_code == 200 :
        soup = BeautifulSoup(r.text, "html.parser")
        letters = soup.find_all("h2", class_="fig-profil-headline")
        for x in range(0, len(letters)):
            link = letters[x].a["href"]
            links_keyword.append(link)   
    return list(set(links_keyword)) 
    
def get_lepoint(keyword, num_pages=21):
    """Returns a list of links to articles in "Le Point" related to a certain keyword
    Articles are in french but they are sometimes very short because we must have a subscription to read some articles

    Parameters
    ----------
    keyword : string e.g : Santé, Médecine, etc.
    num_pages : num 
        
    Returns
    -------
    list_of_links : list
        A list of links to articles related to our keyword

    Examples
    --------
    >>> from news_paper_scrapper import get_lepoint
    >>> keyword = "Santé"
    >>> links = get_lepoint(keyword)
    
    """
    links_keyword = []
    keyword = keyword.lower()
    for i in range(1,num_pages) :
        url = "http://www.lepoint.fr/recherche/recherche.php?query="+keyword+"&sort=pertinence&page="+str(i)
        r = requests.get(url)
        if r.status_code == 200 :
            soup = BeautifulSoup(r.text, "html.parser")
            letters = soup.find_all("article", class_="art-small")
            for x in range(0, len(letters)):
                link = letters[x].div.div.a["href"]
                links_keyword.append(link)   
    return list(set(links_keyword))  
    
def get_lesechos(keyword, num_pages=21):
    """Returns a list of links to articles in "Les Echos" related to a certain keyword
    Articles are in french but they are sometimes very short because we must have a subscription to read some articles

    Parameters
    ----------
    keyword : string e.g : Santé, Médecine, etc.
    num_pages : num 
     
    Returns
    -------
    list_of_links : list
        A list of links to articles related to our keyword

    Examples
    --------
    >>> from news_paper_scrapper import get_lesechos
    >>> keyword = "Santé"
    >>> links = get_lesechos(keyword)
    
    """
    links_keyword = []
    keyword = keyword.lower()
    for i in range(1,num_pages) :
        url = "http://recherche.lesechos.fr/recherche.php?exec=1&texte="+keyword+"&ob=globalrelevance"+"&page="+str(i)
        r = requests.get(url)
        if r.status_code == 200 :
            soup = BeautifulSoup(r.text, "html.parser")
            letters = soup.find_all("article", class_="liste-article")
            for x in range(0, len(letters)):
                link = letters[x].a["href"]
                links_keyword.append(link)   
    return list(set(links_keyword))  
    
def get_lexpress(keyword, num_pages=21):
    """Returns a list of links to articles in "L'Express" related to a certain keyword
    Articles are in french but they are sometimes very short because we must have a subscription to read some articles

    Parameters
    ----------
    keyword : string e.g : Santé, Médecine, etc.
    num_pages : num
        
    Returns
    -------
    list_of_links : list
        A list of links to articles related to our keyword

    Examples
    --------
    >>> from news_paper_scrapper import get_lexpress
    >>> keyword = "Santé"
    >>> links = get_lesechos(keyword)
    
    """
    links_keyword = []
    keyword = keyword.lower()
    for i in range(1,num_pages) :
        url = "http://www.lexpress.fr/recherche?q="+keyword+"&p="+str(i)
        r = requests.get(url)
        if r.status_code == 200 :
            soup = BeautifulSoup(r.text, "html.parser")
            letters = soup.find_all("div", class_="group")
            for x in range(0, len(letters)):
                link = letters[x].a["href"]
                links_keyword.append(link)   
    return list(set(links_keyword))      

def get_google_news_query(keyword, lang="fr") :
    
    """Returns a list of links to articles referenced by Google related to a certain keyword
    Articles are sometimes very short because we must have a subscription to read some articles

    Parameters
    ----------
    keyword : string e.g : Santé, Médecine, etc.
    num_pages : num
        
    Returns
    -------
    list_of_links : list
        A list of links to articles related to our keyword: (about 100 links)

    Examples
    --------
    >>> from news_paper_scrapper import get_google_news_query
    >>> keyword = "Santé"
    >>> links = get_google_news_query(keyword)
    
    Warning !! May not work very well because Google may block requests
    
    """
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    links_keyword = []
    keyword = keyword.lower()
    for i in range(0, 100,10) :
        url = 'https://www.google.com/search?q=%22'+keyword+'%22&tbm=nws&start='+str(i)
        r = requests.get(url, headers=headers)
        if r.status_code == 200 :
            soup = BeautifulSoup(r.text, "html.parser")
            letters = soup.find_all("div", class_="_cnc")
            for x in range(0, len(letters)):
                link = letters[x].a["href"]
                links_keyword.append(link)
    return list(set(links_keyword))  

def get_wikipedia_titles(keywords,lang, num_titles = 400):
    """Returns a list of links to articles in Wikipedia related to a certain keyword

    Parameters
    ----------
    keywords : list of string
        A list of keywords related to a category e.g : [Santé, Médecine, etc.] for the category "Santé"
    num_titles : num
        It is the num of titles that will be collected. The max is 500
    lang : default "fr"
        
    Returns
    -------
    list_of_links : list
        A list of links to articles related to our keyword: (about 100 links)

    Examples
    --------
    >>> from news_paper_scrapper import get_wikipedia_titles
    >>> keywords = ["santé","médicament","médecin","soins","bien-être", \
            "centres de santé","prévention","maladie","guérison"]
    >>> titles = get_wikipedia_titles(keywords)
   
    """
    wikipedia.set_lang(lang)
    titles = []
    for key in keywords :
        tmp =  wikipedia.search(key, num_titles) 
        titles+=tmp
    return titles
    
    