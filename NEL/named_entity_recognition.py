import pymorphy2
from deeppavlov import build_model
import logging

logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)


def extractNamedEntities(sentence_list, ner_model_name, tags_list):
    tags = tags_list
    model = build_model(ner_model_name)
    named_entities_set = findTextNamedEntities(sentence_list, tags, model)
    corrected_entities_set = tokenCorrection(named_entities_set)
    full_entity_set = addEntitiesLemmas(corrected_entities_set)
    return full_entity_set


def findTextNamedEntities(sentence_list, required_tag_list, ner_model):
    found_entities_set = set()
    tags_start_mark_list = makeTagsStartMarkList(required_tag_list)
    tags_inside_mark_list = makeTagsInsideMarkList(required_tag_list)
    for sentence in sentence_list:
        sentence_ner_result = ner_model([sentence])
        token_list = sentence_ner_result[0][0]
        tag_list = sentence_ner_result[1][0]
        findSentenceNamedEntities(token_list, tag_list, tags_start_mark_list, tags_inside_mark_list, found_entities_set)

    return found_entities_set


def makeTagsStartMarkList(tag_list):
    tags_start_mark_list = []
    for tag in tag_list:
        tags_start_mark_list.append("B-" + tag)

    return tags_start_mark_list


def makeTagsInsideMarkList(tag_list):
    tags_inside_mark_list = []
    for tag in tag_list:
        tags_inside_mark_list.append("I-" + tag)

    return tags_inside_mark_list


def findSentenceNamedEntities(token_list, tag_list, start_mark_list, inside_mark_list, result_set):
    named_entity = ""

    for token in reversed(range(len(token_list))):
        if tag_list[token] == "O":
            continue

        elif tag_list[token] in start_mark_list:
            if named_entity == "":
                result_set.add((token_list[token], clearNERTag(tag_list[token])))
            elif named_entity != "":
                result_set.add((token_list[token] + " " + named_entity, clearNERTag(tag_list[token])))
                named_entity = ""

        elif tag_list[token] in inside_mark_list:
            if named_entity == "":
                named_entity += token_list[token]
            elif named_entity != "":
                named_entity = token_list[token] + " " + named_entity

        else:
            continue


def lemmatizeEntity(named_entity):
    morph = pymorphy2.MorphAnalyzer()
    word_list = named_entity.split()
    lemmatized_entity = ""
    for word in word_list:
        word_lemma = morph.parse(word)[0].normal_form
        lemmatized_entity = lemmatized_entity + word_lemma + " "
    lemmatized_entity.strip()

    return lemmatized_entity


def tokenCorrection(named_entities_set):
    new_set = set()
    for element in named_entities_set:
        new_set.add((element[0].replace(" .", ".").lower(), element[1]))
    return new_set


def clearNERTag(tag):
    return tag.split("-")[1]


def addEntitiesLemmas(entities_set):
    new_entities_set = set()
    for entity_info in entities_set:
        entity_tuple = entity_info
        entity_lemma = lemmatizeEntity(entity_tuple[0]).strip()
        new_entity_tuple = (entity_tuple[0], entity_tuple[1], entity_lemma)
        new_entities_set.add(new_entity_tuple)

    return new_entities_set
