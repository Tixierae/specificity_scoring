# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#This file will download some articles from google news with the title and the link to the full article
#The title and the links anre then registered in a file Categories/category_name 
#where category_name is the name of the category
#I wll then use python3 with newspapers for parsing

categories = ["International", "Économie", "Science", "Technologie", "Sport", "Culture", "Santé", "Politique", "Société", "Business", "Automobile", "Start-up", "Alimentation"]

import gnp #google news paper
import json

for category in categories :
    print category
    news = gnp.get_google_news_query(category)
    news_to_json = json.loads(json.dumps(news, indent=4))
    filename = 'Categories/'+category+'.txt'
    with open(filename, 'w+') as f: 
        for story in news_to_json['stories'] :
            link = story['link']
            content_snippet = story['content_snippet']
            title = story['title']
            f.write(title.encode('utf8') + '\n')
            f.write(link.encode('utf8') + '\n')
            f.write(''.encode('utf8') + '\n')
