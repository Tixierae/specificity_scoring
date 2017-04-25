# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


from data_collecting import get_corpus
import tfidf 
import graph_creation
import pmi_matrix
import wordlevelstatistics
#list of categories
categories = {
        "Santé": ["santé", "médicament","médecin", "soins de santé","centres de santé", "chirurgien", "maladie", "guérison","dépistage", "allergies", "cancer","assurance santé","infections", "vaccins"],
        "Economie": ["économie","concurrence économique","monnaie","économie collaborative","commerce","emplois","pme","entreprises","chômage","impôts","investissements","bourse","microéconomie","macroéconomie"],
        "Immobilier": ["immobilier","location","bail","dépôt de garantie","hypothèque","lotissement","immeuble","colocation","nantissement","revenus fonciers","résidence","taxe d'habitation","état des lieux", "appartement","studio"],
        "Sport": ["sport","athlétisme","sports collectifs", "gymnastique", "épreuves combinées","sports mécaniques","sports de raquette","sports avec animaux","cyclisme","arts martiaux","sports de combat", "sports de force","sports nautiques", "sports de cible", "sports de glisse"],
        "Automobile": ["automobile","voiture","véhicule","voitures compactes", "cabriolets","voitures familiales", "voitures citadines", "4x4"]             
}
    
print "Getting corpus..."
corpus = get_corpus(categories, lang="fr", download=False) #dic of lists
print "Corpus collected...."
for category in corpus:
    print("Size of the corpus  {} = {} words".format(category, len(corpus[category])))
    
print ""    
print "Using tf-idf..."   
tfidf.save_specificity_scores(corpus) #using tf-idf
#print ""
#print "Using clustering coefficient..."  
graph_creation.save_specificity_scores(corpus) #using clustering coefficient
#print "PMI Matrix..."  
pmi_matrix.save_specificity_scores(corpus) #using clustering coefficient
wordlevelstatistics.save_specificity_scores(corpus) #using clustering coefficient

    
