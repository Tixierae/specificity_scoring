# Specificity Scoring
This code attibutes specificity scoring to words. i.e when given a corpus of documents it can extract the more specific words
For example german shepherd is more specific than dog

The main.py file in /code is in charge of collecting the corpus of documents from Wikipedia ( I tried to use EventRegistry(http://eventregistry.org/) and Google News Api(https://github.com/mPAND/gnp)
but these two API are very inconsistent so I only use Wikipedia API(https://github.com/goldsmith/Wikipedia)). 

Roles of every file :
/code 
To install newspaper : check the documentation here https://github.com/codelucas/newspaper
To install gnp : use pip 
To install WordLevelStatistics : pip install git+https://github.com/napsternxg/WordLevelStatistics.git



