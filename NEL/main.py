from text_pre_processing import getSentenceList
from named_entity_recognition import extractNamedEntities
from configs.ner_model_config import ner_model_name
from search import getNamedEntitiesLinks
from db import upsertMethodResult
from configs.search_config import tags_list


def process(path_to_file, tag_list):
    ner_model = ner_model_name
    sentence_list = getSentenceList(path_to_file)
    named_entities_set = extractNamedEntities(sentence_list, ner_model, tag_list)
    named_entities_full_info_list = getNamedEntitiesLinks(named_entities_set)
    upsertMethodResult(named_entities_full_info_list, path_to_file)
    return named_entities_full_info_list


file_path = "../files/2.txt"
result = process(file_path, tags_list)
# print(result)

# for i in result:
#     print(i)
# result_set = process(file,tags_list)
# print(len(result_set))
