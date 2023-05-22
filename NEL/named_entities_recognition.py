from deeppavlov import build_model
import logging
from pymystem3 import Mystem

logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)
my_stem = Mystem()


def extractNamedEntities(sentence_list, ner_model_name, tags_list):
    tags = tags_list
    model = build_model(ner_model_name)
    named_entities_set = findTextNamedEntities(sentence_list, tags, model)
    full_entity_set = makeFullEntitySet(named_entities_set)
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
    lemmas = my_stem.lemmatize(named_entity)
    return "".join(lemmas).strip()


def entityCorrection(named_entitity):
    return named_entitity.replace(" .", ".").lower()


def clearNERTag(tag):
    return tag.split("-")[1]


def makeFullEntitySet(entities_set):
    new_entities_set = set()
    for entity_tuple in entities_set:
        corrected_entity = entityCorrection(entity_tuple[0])
        entity_lemma = lemmatizeEntity(corrected_entity).strip()
        new_entity_tuple = (corrected_entity, entity_tuple[1], entity_lemma)
        new_entities_set.add(new_entity_tuple)

    return new_entities_set
