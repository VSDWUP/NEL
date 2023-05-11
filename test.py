import random

import requests
from configs.search_config import per_filter_labels


# dict = {}
# dict[(1,2)] = "FirstAndSecond"
#
# for key, value in dict.items():
#     print(f"{key[0]} : {value}")
#
#
#
# def getSumAndElements(a,b):
#     return a+b, a, b
#
# print(getSumAndElements(7,3))
#
#
#
# a = set()
# a.add(("пушкин","PER"))
# a.add(("пушкин","LOC"))
# a.add(("пушкин","PER"))
# a.add(("пушкин","LOC"))
# for i in a:
#     print(i[0])

# dict1 = {'Q7200': 0}
#print(dict1.items())

# result_entity = list(dict1.keys())[0]
# print(result_entity)

# dict = {'Q78364': 0, 'Q4131539': 0}
# for i in dict:
#     print(i)

# def getEntityAliases(entity_id):
#     ru_aliases_list = []
#     search_url = "https://www.wikidata.org/wiki/Special:EntityData/{}.json".format(entity_id)
#     response = requests.get(search_url)
#     data = response.json()
#     try:
#         entity_aliases = data['entities'][entity_id]['aliases']
#         # for i in range(len(entity_aliases)):
#         #     ru_aliases_list.append(entity_aliases[i]['value'])
#         return entity_aliases
#     except KeyError:
#         return None
#
#
# print(getEntityAliases("Q7200"))

entities_aliases_dict = {"Q7243": ["Толстой, Лев Николаевич", "Лев Толстой", "Толстой, Лев", "Л. Н. Толстой"], "Q212575": ["Толстой А. К.", "Толстой Алексей Константинович", "А. К. Толстой", "Толстой, Алексей Константинович"]}

# def cleanEntity(entity):
#     return entity.replace(".","").replace(",","").replace(" ","").lower()

# def setWeightsForPEREntities(entities_aliases_dict, query):
#     entities_ratio_dict = {}
#     for i in entities_aliases_dict:
#         ratio = 0
#         for k in entities_aliases_dict[i]:
#             ratio += calculateRatio(query,k)
#         entities_ratio_dict[i] = ratio
#     return entities_ratio_dict
#
#
# def calculateRatio(query,entity):
#     fuzzy_ratio = fuzz.token_set_ratio(query,entity)
#     if fuzzy_ratio < 75:
#         return 0
#     else:
#         return 1

#print(setWeightsForPEREntities(entities_aliases_dict,"алексей толстой"))

# fuzzy_ratio = fuzz.token_set_ratio("Барак Обама","Барак Хуссеейн Обама")
# print(fuzzy_ratio)
# def findDictMaxPriorityEntity(prioritised_entites_dict):
#     for i in prioritised_entites_dict:
#         if prioritised_entites_dict[i] == max(prioritised_entites_dict.values()):
#             return i
#
# test_dict = {'Q7243': 4, 'Q212575': 4}
#
# print(findDictMaxPriorityEntity(test_dict))

# test_set = {('а . п . полторацкий', 'PER'), ('а . с . пушкин', 'PER'), ('с . г . голицын', 'PER'), ('а . а . оленина - младший', 'PER'), ('н . далее . киселёв', 'PER'), ('п . а . вяземский', 'PER')}
# print(test_set[0])
# print(len(test_set))

# def getNamedEntitiesLinks(named_entities_set):
#     for entity_element in named_entities_set:
#         entity = entity_element[0]
#         entity_tag = entity_element[1]
#         print(entity)
#         print(entity_tag + "\n")
#
# getNamedEntitiesLinks(test_set)
#
# list = []
# print(len(list))

#
# file_path = "../files/test1.txt"
# end = file_path.split("/")[-1]
# print(end)

# print('с . г . голицын'.replace(" .", "."))

# from natasha import (
#     Segmenter,
#     MorphVocab,
#
#     NewsEmbedding,
#     NewsMorphTagger,
#     NewsSyntaxParser,
#     NewsNERTagger,
#
#     NamesExtractor,
#
#     Doc
# )
#
# segmenter = Segmenter()
# morph_vocab = MorphVocab()
#
# emb = NewsEmbedding()
# morph_tagger = NewsMorphTagger(emb)
# syntax_parser = NewsSyntaxParser(emb)
# ner_tagger = NewsNERTagger(emb)
#
# names_extractor = NamesExtractor(morph_vocab)
# text = "соедененным штатам америки"
# doc = Doc(text)
# doc.segment(segmenter)
# doc.tag_morph(morph_tagger)
#
# for token in doc.tokens:
#     token.lemmatize(morph_vocab)
#
# for token in doc.tokens:
#     print(token.lemma)
#
# print(doc.tokens)


# def getIdsFromSearch(searchQuery):
#     search_url = "https://www.wikidata.org/w/api.php?action=query&format=json&list=search&srsearch={}".format(searchQuery)
#     response = requests.get(search_url)
#     data = response.json()
#     entity_id_list = []
#     results = data['query']['search']
#     for search_result in results:
#         entity_id_list.append(search_result['title'])
#     return entity_id_list

# print(getEntitiesIdsFromSearchResult("с. г. голицын"))
# print(getIdsFromSearch("с. г. голицын"))

# print(getEntitiesIdsFromSearchResult("пушкин"))
# print(getIdsFromSearch("пушкин"))

# ['н. далее. киселёв', 'PER', None, None]
# ['с. г. голицын', 'PER', None, None]
# ['а. а. оленина - младший', 'PER', None, None]
# ['а. п. полторацкий', 'PER', None, None]
# ['п. а. вяземский', 'PER', None, None]
# ['а. с. пушкин', 'PER', 'Q7200', 'https://www.wikidata.org/wiki/Q7200']



#list100 = ['Q3244512']
list100 = ['Q501340', 'Q113293', 'Q495191', 'Q2106585', 'Q355406', 'Q3244512', 'Q214565', 'Q8337', 'Q5410773', 'Q43361', 'Q102438', 'Q754837']


def getEntityClaim(entity_id):
    search_url = "https://www.wikidata.org/wiki/Special:EntityData/{}.json".format(entity_id)
    response = requests.get(search_url)
    data = response.json()
    claims = data['entities'][entity_id]['claims']
    return claims


# def getEntityInstanceOfList(entity):
#     instance_of_list = []
#     pageClaims = getEntityClaim(entity)
#     if 'P31' in pageClaims:
#         claimLen = len(pageClaims['P31'])
#
#         for i in range(claimLen):
#             mainsnak = pageClaims['P31'][i]['mainsnak']
#
#             if mainsnak['datatype'] == 'wikibase-item':
#                 property_entity_id = mainsnak['datavalue']['value']['id']
#                 instance_of_list.append(property_entity_id)
#
#     return instance_of_list

def filterPEREntitiesSearchResult(search_entity_list):
    filtered_entities_dict = {}
    for entity in search_entity_list:
        claim = getEntityClaim(entity)
        filterPerEntity(claim,filtered_entities_dict,entity)
    return filtered_entities_dict

def filterPerEntity(entity_claim, filtered_entities_dict, entity):
    if 'P31' in entity_claim:
        full_list = entity_claim['P31']
        for i in range(len(full_list)):
            mainsnak = full_list[i]['mainsnak']

            if mainsnak['datatype'] == 'wikibase-item':
                property_entity_id = mainsnak['datavalue']['value']['id']
                label = getEntityLabel(property_entity_id)
                label_last_word = getLabelLastWord(label)

                if label_last_word in per_filter_labels:
                    filtered_entities_dict[entity] = []
                    return

def getEntityLabel(entity_id):
    search_url = "https://www.wikidata.org/wiki/Special:EntityData/{}.json".format(entity_id)
    response = requests.get(search_url)
    data = response.json()
    label = data['entities'][entity_id]['labels']['en']['value']
    return label

def getLabelLastWord(label):
    return label.split(" ")[-1]

dict_filtered = filterPEREntitiesSearchResult(list100)
print(dict_filtered)

#print(filterPEREntitiesSearchResult(list100))
#filterPEREntitiesSearchResult(list100)
# result100 = getEntityInstanceOfList("Q3244512")
# for i in result100:
#     label = getEntityLabel(i)
#     print(getLabelLastWord(label))

# print(getEntityInstanceOfList("Q3244512"))

#
#
# search_query = "буш"
# url1 = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search={}&format=json&language=ru&limit=10".format(search_query)
# url2 = "https://www.wikidata.org/w/api.php?action=query&format=json&list=search&srsearch={}".format(search_query)
#
# response1 = requests.get(url1)
# response2 = requests.get(url2)
#
# data1 = response1.json()
# print(data1)
# data2 = response2.json()
#
# wbsearch_results = data1['search']
# wbsearch_entity_id_list = []
# for entity in wbsearch_results:
#     wbsearch_entity_id_list.append(entity['id'])
# print(wbsearch_entity_id_list)
#
# query_entity_id_list = []
# query_results = data2['query']['search']
# for search_result in query_results:
#     query_entity_id_list.append(search_result['title'])
#
# print(query_entity_id_list)
#
# for i in query_entity_id_list:
#     if i in wbsearch_entity_id_list:
#         pass
#     else:
#         if len(query_entity_id_list) < 20:
#             wbsearch_entity_id_list.append(i)
#         else:
#             pass
#
# print(wbsearch_entity_id_list)

# set = set()
#
# for i in wbsearch_entity_id_list:
#     print(i)
#     set.add(i)
# # for k in query_entity_id_list:
# #     set.add(k)
#
# print(set)