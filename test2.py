# import requests
#
# def getEntitiesIdsFromSearchResult(search_query):
#     wbse_entity_id_list = getEntitiesListFromWbse(search_query)
#     query_entity_id_list = getEntitiesListFromQuery(search_query)
#     mergeSearchResults(wbse_entity_id_list,query_entity_id_list)
#     return wbse_entity_id_list
#
# def getEntitiesListFromWbse(search_query):
#     search_url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search={}&format=json&language=ru".format(search_query)
#     response = requests.get(search_url)
#     data = response.json()
#     result = data['search']
#     entity_id_list = []
#     for entity in result:
#         entity_id_list.append(entity['id'])
#     return entity_id_list
#
# def getEntitiesListFromQuery(search_query):
#     search_url = "https://www.wikidata.org/w/api.php?action=query&format=json&list=search&srsearch={}".format(search_query)
#     response = requests.get(search_url)
#     data = response.json()
#     result = data['query']['search']
#     entity_id_list = []
#     for entity in result:
#         entity_id_list.append(entity['title'])
#     return entity_id_list
#
# def mergeSearchResults(wbse_entitiy_id_list, query_entity_id_list):
#     for id in query_entity_id_list:
#         if id in wbse_entitiy_id_list:
#             pass
#         else:
#             if len(query_entity_id_list) < 20:
#                 wbse_entitiy_id_list.append(id)
#             else:
#                 pass
#
# print(getEntitiesIdsFromSearchResult("поттер"))


# entity_rep_search_result = [None, None]
# if entity_rep_search_result == [None,None]:
#     print("True")
#
# a = ""
# b = "1"
#
# c = a + b + " "
# print(c)


set1 = {('лондоне', 'LOC'), ('петербург', 'LOC'), ('соединенные штаты америки', 'LOC'), ('россия', 'LOC')}
for element in set1:
    element_list = list(element)
    element_list.append("Q")
    print(element_list)

# print(set1)