.. _l-README:

Specificity Scoring
==================

This code attibutes specificity scoring to words. 
i.e when given a corpus of documents it can extract the most specific words in the corpus
For example, given the corpus "dog" or "animal", german shepherd is more specific than dog

We have two main directories : /code that contains all algorithms and /data that contains the corpuses

The /code directory
===================

* main.py : downloads corpuses (or just reads them if there are already present). At the end, specificity scores are assigned to words using different methods
* data_collecting.py : collects articles links from newspapers, or pages titles from Wikipedia then downloads contents, cleans and saves them in the directory /data  
* news_scrapper.py : collects links to articles or pages titles from "Le Figaro", "Le Monde", "L'Express", "Le Point", "Les Echos", Google News and Wikipedia                                        
* tf_idf.py : implements tf-idf for domains specified
* graph_creation.py : uses clustering coefficent on a graph of words
* pmi_matrix.py : uses clustering coefficent with a graph of words created with a ppmi matrix
* wordlevelstatistics.py : implements the spatial statistics described in the following `paper <http://bioinfo2.ugr.es/Publicaciones/PRE09.pdf>`_

The /data directory
===================

It contains the corpus collected (I only used Wikipedia to collect them)

Results
=======

They can be found in the /results directory


Problems encountered
====================

- * Data collecting

At first, I used `gnp api <https://github.com/mPAND/gnp>`_ but the API was very inconsistent and could only collect 20 links. 
I also implemented a Google News Scrapper directly but the problem is that Google restricts the number of requests that can be made and can block the url.
I also used `Event Registry API <http://eventregistry.org/>`_ that could download more than 2000 articles but they blocked the number of requests a free user could perform
Finally, I used mainly Wikipedia with several keywords to collect a lot of texts (I also implemented some scrappers to use with french NewsPapers websites like Le Monde)

- * Data preprocessing

For the preprocesing steps, I had mainly issues with the French Language. So, I used some librairies like blob or treetaggerwrapper to lemmatize texts, do pos-tagging, remove stopwords, dates...
Specially, in the case of newspapers when we have a lot of garbage, it was relevant. 
I also created n-grams (for n=1,2..5) with gensim before cleaning the texts

- * Algorithms

Gaph_creation and ppmi matrix don't seem to work. I would recommend WordLevelStatistics

