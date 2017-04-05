#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 23:36:22 2017

@author: diop
"""
import requests
from newspaper import Article
import wikipedia
from bs4 import BeautifulSoup

def read_article(link, lang='fr') :
    "This function downloads the text from an article given the link"
    try :
        a = Article(link, language=lang)
        a.download()  
        a.parse()
        s = a.text
        return s
    except :
        return 
        
def get_text_from_wikipedia(result):
    "This function returns the content of a wikipedia page given the title"
    try :
        article = wikipedia.page(result)
        content = article.content
        return content    
    except :
        return ''    
    
     
def get_lemonde(category):
    links_category = []
    category = category.lower()
    for i in range(1,201) :
        url = "http://www.lemonde.fr/recherche/?keywords="+category+"&page_num="+str(i)+"&operator=and&exclude_keywords=&qt=recherche_titre&author=&period=since_1944&start_day=01&start_month=01&start_year=1944&end_day=06&end_month=04&end_year=2017&sort=pertinence"
        r = requests.get(url)
        if r.status_code == 200 :
            soup = BeautifulSoup(r.text, "html.parser")
            letters = soup.find_all("h3", class_="txt4_120")
            for x in range(0, len(letters)):
                link = 'http://www.lemonde.fr'+letters[x].a["href"]
                links_category.append(link)   
    return list(set(links_category)) 
    
def get_lefigaro(category):
    links_category = []
    category = category.lower()
    for i in range(1,21) :
        url = "http://recherche.lefigaro.fr/recherche/"+category+"?motscles_slug="+category
        r = requests.get(url)
        if r.status_code == 200 :
            soup = BeautifulSoup(r.text, "html.parser")
            letters = soup.find_all("h2", class_="fig-profil-headline")
            for x in range(0, len(letters)):
                link = letters[x].a["href"]
                links_category.append(link)   
    return list(set(links_category)) 
    
def get_lepoint(category):
    links_category = []
    category = category.lower()
    for i in range(1,51) :
        url = "http://www.lepoint.fr/recherche/recherche.php?query="+category+"&page="+str(i)
        r = requests.get(url)
        if r.status_code == 200 :
            soup = BeautifulSoup(r.text, "html.parser")
            letters = soup.find_all("article", class_="art-small")
            for x in range(0, len(letters)):
                link = letters[x].div.div.a["href"]
                links_category.append(link)   
    return list(set(links_category))  
    
def get_lesechos(category):
    links_category = []
    category = category.lower()
    for i in range(1,21) :
        url = "http://recherche.lesechos.fr/recherche.php?exec=1&texte="+category+"&ob=globalrelevance"+"&page="+str(i)
        r = requests.get(url)
        if r.status_code == 200 :
            soup = BeautifulSoup(r.text, "html.parser")
            letters = soup.find_all("article", class_="liste-article")
            for x in range(0, len(letters)):
                link = letters[x].a["href"]
                links_category.append(link)   
    return list(set(links_category))  
    
def get_lexpress(category):
    links_category = []
    category = category.lower()
    for i in range(1,51) :
        url = "http://www.lexpress.fr/recherche?q="+category+"&p="+str(i)
        r = requests.get(url)
        if r.status_code == 200 :
            soup = BeautifulSoup(r.text, "html.parser")
            letters = soup.find_all("div", class_="group")
            for x in range(0, len(letters)):
                link = letters[x].a["href"]
                links_category.append(link)   
    return list(set(links_category))      

def get_google_news_query(category, lang="fr") :
    ##Doesn't work very well because Google blocks requests
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    links_category = []
    category = category.lower()
    for i in range(0, 100,10) :
        url = 'https://www.google.com/search?q=%22'+category+'%22&tbm=nws&start='+str(i)
        r = requests.get(url, headers=headers)
        if r.status_code == 200 :
            soup = BeautifulSoup(r.text, "html.parser")
            letters = soup.find_all("div", class_="_cnc")
            for x in range(0, len(letters)):
                link = letters[x].a["href"]
                links_category.append(link)
    return list(set(links_category))      