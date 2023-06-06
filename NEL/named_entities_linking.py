from text_pre_processing import getSentenceList
from named_entities_recognition import extractNamedEntities
from configs.ner_model_config import ner_model_name
from search_concepts import getNamedEntitiesLinks
from db import upsertMethodResult
from configs.search_config import tags_list
import time


def linkNamedEntities(path_to_file, tag_list):
    ner_model = ner_model_name
    sentence_list = getSentenceList(path_to_file)
    named_entities_set = extractNamedEntities(sentence_list, ner_model, tag_list)
    named_entities_full_info_list = getNamedEntitiesLinks(named_entities_set)
    upsertMethodResult(named_entities_full_info_list, path_to_file)
    return named_entities_full_info_list


def printResult(method_result):
    for entity in method_result:
        print(entity)


def runWithTimeCalculation(path, tags):
    start = time.time()
    file_path = path
    result = linkNamedEntities(file_path, tags)
    printResult(result)
    end = time.time() - start
    print(end)


runWithTimeCalculation("../files/target_sample004.txt", tags_list)
