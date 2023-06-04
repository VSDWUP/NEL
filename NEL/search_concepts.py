import time

import requests
from thefuzz import fuzz
from configs.search_config import loc_entities_id_weight_dict, per_filter_labels, entity_alias_ratio
import string
from concurrent.futures import ThreadPoolExecutor


def getNamedEntitiesLinks(named_entities_set):
    named_entities_list = list(named_entities_set)
    pool = ThreadPoolExecutor()
    result_list = pool.map(getNamedEntityLink, named_entities_list)
    result_set = set()
    for entity_info in result_list:
        result_set.add(entity_info)
    pool.shutdown()
    return result_set


def getNamedEntityLink(named_entity_info):
    lemmatized_entity = named_entity_info[2]
    entity_tag = named_entity_info[1]
    entity_initial_info_list = (lemmatized_entity, entity_tag)

    entity_search_result = getEntitySearchResult(entity_tag, lemmatized_entity)

    if entity_search_result == (None, None):
        raw_entity = named_entity_info[0]
        entity_initial_info_list = (raw_entity, entity_tag)
        entity_search_result = getEntitySearchResult(entity_tag, raw_entity)

    entity_full_info_list = entity_initial_info_list + entity_search_result
    return entity_full_info_list


def getEntitySearchResult(entity_tag, entity):
    entity_search_result = (None, None)
    if entity_tag == "PER":
        entity_search_result = getPEREntitySearchResult(entity, entity_search_result)
    elif entity_tag == "LOC":
        entity_search_result = getLOCEntitySearchResult(entity, entity_search_result)
    return entity_search_result


def getPEREntitySearchResult(query, initial_entity_search_result):
    search_entities_list = getEntitiesIdsFromSearchResult(query)

    if len(search_entities_list) > 0:
        filtered_entities_dict = filterPEREntitiesSearchResult(search_entities_list)

        if len(filtered_entities_dict) > 0:

            if len(filtered_entities_dict) > 1:
                getEntitiesAliases(filtered_entities_dict)
                entities_weight_dict = setWeightsForPEREntities(filtered_entities_dict, query)
                result_entity = findFirstDictMaxPriorityEntity(entities_weight_dict)
                return result_entity, createWikiDataLink(result_entity)
            else:
                result_entity = tuple(filtered_entities_dict.keys())[0]
                return result_entity, createWikiDataLink(result_entity)
        else:
            return initial_entity_search_result

    else:
        return initial_entity_search_result


def getLOCEntitySearchResult(query, initial_entity_search_result):
    search_entities_list = getEntitiesIdsFromSearchResult(query)

    if len(search_entities_list) > 0:
        filtered_entities_dict = filterLOCEntitiesSearchResult(search_entities_list)

        if len(filtered_entities_dict) > 0:

            if len(filtered_entities_dict) > 1:
                entities_instance_of_dict = getEntitiesInstanceOfDict(filtered_entities_dict)
                setWeightsForLOCEntities(entities_instance_of_dict, filtered_entities_dict)
                result_entity = findFirstDictMaxPriorityEntity(filtered_entities_dict)
                return result_entity, createWikiDataLink(result_entity)
            else:
                result_entity = tuple(filtered_entities_dict.keys())[0]
                return result_entity, createWikiDataLink(result_entity)
        else:
            return initial_entity_search_result
    else:
        return initial_entity_search_result


def getEntitiesIdsFromSearchResult(search_query):
    wbse_entity_id_list = getEntitiesListFromWbse(search_query)
    query_entity_id_list = getEntitiesListFromQuery(search_query)
    mergeSearchResults(wbse_entity_id_list, query_entity_id_list)
    return wbse_entity_id_list


def getEntitiesListFromWbse(search_query):
    search_url = "https://www.wikidata.org/w/api.php?action=wbsearchentities&search={}&format=json&language=ru&limit=10".format(
        search_query)
    response = requests.get(search_url)
    data = response.json()
    result = data['search']
    entity_id_list = []
    for entity in result:
        entity_id_list.append(entity['id'])
    return entity_id_list


def getEntitiesListFromQuery(search_query):
    search_url = "https://www.wikidata.org/w/api.php?action=query&format=json&list=search&srsearch={}".format(
        search_query)
    response = requests.get(search_url)
    data = response.json()
    result = data['query']['search']
    entity_id_list = []
    for entity in result:
        entity_id_list.append(entity['title'])
    return entity_id_list


def mergeSearchResults(wbse_entitiy_id_list, query_entity_id_list):
    for entity_id in query_entity_id_list:
        if entity_id in wbse_entitiy_id_list:
            pass
        else:
            if len(query_entity_id_list) < 20:
                wbse_entitiy_id_list.append(entity_id)
            else:
                pass


def filterPEREntitiesSearchResult(search_entity_list):
    filtered_entities_dict = {}
    for entity in search_entity_list:
        claim = getEntityClaim(entity)
        filterPerEntity(claim, filtered_entities_dict, entity)
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


def filterLOCEntitiesSearchResult(search_entity_list):
    filtered_entities_dict = {}
    for entity in search_entity_list:
        claim = getEntityClaim(entity)

        if 'P625' in claim:
            mainsnak = claim['P625'][0]['mainsnak']

            if mainsnak['datatype'] == 'globe-coordinate':
                filtered_entities_dict[entity] = 0
    return filtered_entities_dict


def getEntitiesAliases(filtered_entities_dict):
    for entity_id in filtered_entities_dict:

        ru_aliases_list = []
        search_url = "https://www.wikidata.org/wiki/Special:EntityData/{}.json".format(entity_id)
        response = requests.get(search_url)
        data = response.json()

        try:
            entity_aliases = data['entities'][entity_id]['aliases']['ru']
            for i in range(len(entity_aliases)):
                ru_aliases_list.append(cleanAlias(entity_aliases[i]['value']))
            filtered_entities_dict[entity_id] = ru_aliases_list
        except KeyError:
            pass
    return filtered_entities_dict


def setWeightsForPEREntities(entities_aliases_dict, query):
    entities_ratio_dict = {}
    for i in entities_aliases_dict:
        ratio = 0

        for k in entities_aliases_dict[i]:
            ratio += calculateRatio(query, k)

        entities_ratio_dict[i] = ratio
    return entities_ratio_dict


def calculateRatio(query, entity):
    fuzzy_ratio = fuzz.token_set_ratio(query, entity)
    if fuzzy_ratio <= entity_alias_ratio:
        return 0
    else:
        return 1


def findFirstDictMaxPriorityEntity(prioritised_entities_dict):
    for i in prioritised_entities_dict:
        if prioritised_entities_dict[i] == max(prioritised_entities_dict.values()):
            return i


def createWikiDataLink(entity_id):
    if entity_id is not None:
        return "https://www.wikidata.org/wiki/{}".format(entity_id)
    else:
        return None


def getEntityInfo(entity_id):
    search_url = "https://www.wikidata.org/wiki/Special:EntityData/{}.json".format(entity_id)
    response = requests.get(search_url)
    return response


def getEntityClaim(entity_id):
    try:
        entity_info = getEntityInfo(entity_id)
    except requests.exceptions.SSLError:
        time.sleep(1)
        entity_info = getEntityInfo(entity_id)
    data = entity_info.json()
    claims = data['entities'][entity_id]['claims']
    return claims


def getEntitiesInstanceOfDict(filtered_entities_list):
    instance_of_dict = {}
    for entity in filtered_entities_list:
        pageClaims = getEntityClaim(entity)
        instance_of_entity_list = []

        if 'P31' in pageClaims:
            claimLen = len(pageClaims['P31'])

            for i in range(claimLen):
                mainsnak = pageClaims['P31'][i]['mainsnak']

                if mainsnak['datatype'] == 'wikibase-item':
                    property_entity_id = mainsnak['datavalue']['value']['id']
                    instance_of_entity_list.append(property_entity_id)

        instance_of_dict[entity] = instance_of_entity_list
    return instance_of_dict


def setWeightsForLOCEntities(instance_of_dict, filtered_entities_dict):
    for i in instance_of_dict:
        iterateList = instance_of_dict[i]
        for k in loc_entities_id_weight_dict:
            if k in iterateList:
                filtered_entities_dict[i] = loc_entities_id_weight_dict[k]
                break


def cleanAlias(alias):
    clean_alias = ""
    for char in alias:
        if char.isalpha() or char.isspace() or char in string.punctuation:
            clean_alias += char
    return clean_alias
