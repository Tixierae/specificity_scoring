#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  2 01:03:49 2017

@author: diop
"""

from newspaper import Article
    
categories = ["International", "Économie", "Science", "Technologie", "Sport", "Culture", "Santé", "Politique", "Société", "Business", "Automobile", "Start-up", "Alimentation"]

for category in categories :
    filename = 'Categories/'+category+'.txt'    
    f = open(filename, 'r', encoding="utf-8")
    lines = f.readlines()
    f.close()
    n = len(lines)
    for i in range(0,n,3):
        title = lines[i]
        link = lines[i+1]
        print(title)
        print(link)
    print('')    


#these are the following steps I would like to do in my loop
filename = 'Categories/International.txt'

f = open(filename, 'r', encoding="utf-8")
lines = f.readlines()
f.close()
n = len(lines)
for i in range(0,n,3):
    title = lines[i]
    link = lines[i+1]
    print(link)
    if "rfi" not in link :
        a = Article(link, language='fr')
        a.download() #this is asynchronous and so my next line is None
        a.parse()   #the text is not parsed         
        s = a.text
        print(title)
        print(a.text)
        print('')
