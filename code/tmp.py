#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 00:21:01 2017

@author: diop
"""
import bs4
import requests

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}


#just add to this list for each new player
#player name : url
queries = {"bledsoe":"https://www.google.com/search?q=%22eric+bledsoe%22&tbm=nws&tbs=qdr:d",
           "james":"https://www.google.com/search?q=%22lebron+james%22&tbm=nws&tbs=qdr:y"}


total = []

for player in queries: #keys

    #request the google query url of each player
    req  = requests.get(queries[player], headers=headers)
    print re.stats
    soup = bs4.BeautifulSoup(req.text, "html.parser")

    #look for the main container
    for each in soup.find_all("div"):
        results = {player: { \
            "link": None,    \
            "title": None,   \
            "source": None,  \
            "time": None}    \
        }

        try:
          #if <div> doesn't have class="anything"
          #it will throw a keyerror, just ignore

          if "_cnc" in each.attrs["class"]: #mainstories
            results[player]["link"] = each.find("a")["href"]
            results[player]["title"] = each.find("a").get_text()
            sourceAndTime = each.contents[1].get_text().split("-")
            results[player]["source"], results[player]["time"] = sourceAndTime
            total.append(results)

          elif "card-section" in each.attrs["class"]: #buckets
            results[player]["link"] = each.find("a")["href"]
            results[player]["title"] = each.find("a").get_text()
            results[player]["source"] = each.contents[1].contents[0].get_text()
            results[player]["time"] = each.contents[1].get_text()
            total.append(results)

        except KeyError:
            pass    