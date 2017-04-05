#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 23:36:22 2017

@author: diop
"""
import requests
from bs4 import BeautifulSoup


##Doesn't work because Google blocks requests
def get_google_news_query(category, lang="fr") :
    
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
    links_category = []
    category = category.lower()
    for i in range(0,50,10) :
        r = requests.get('https://www.google.com/search?q=%22'+category+'%22&tbm=nws&start='+str(i), headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        letters = soup.find_all("div", class_="_cnc")
        for x in range(0, len(letters)):
            link = letters[x].a["href"]
            links_category.append(link)
    return list(set(links_category))  

     
def get_lemonde_query(category, lang="fr"):
    links_category = []
    category = category.lower()
    for i in range(1,11) :
        url = "http://www.lemonde.fr/recherche/?keywords="+category+"&page_num="+str(i)+"&operator=and&exclude_keywords=&qt=recherche_titre&author=&period=since_1944&start_day=01&start_month=01&start_year=1944&end_day=05&end_month=04&end_year=2017&sort=desc"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        letters = soup.find_all("h3", class_="txt4_120")
        for x in range(0, len(letters)):
            link = 'http://www.lemonde.fr'+letters[x].a["href"]
            links_category.append(link)   
    return list(set(links_category)) 
    
def get_lefigaro_query(category, lang="fr"):
    links_category = []
    category = category.lower()
    for i in range(1,11) :
        url = "http://recherche.lefigaro.fr/recherche/"+category
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        letters = soup.find_all("h2", class_="fig-profil-headline")
        for x in range(0, len(letters)):
            link = letters[x].a["href"]
            links_category.append(link)   
    return list(set(links_category))    