from razdel import sentenize
import os


def readFile(input_file):
    if os.path.getsize(input_file) != 0:
        with open(input_file, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    else:
        raise OSError("Empty file")


def segmentText(full_text):
    sentence_list = []
    raw_sentence_list = list(sentenize(full_text))
    for sentence in raw_sentence_list:
        sentence_list.append(sentence.text)
    return sentence_list


def getSentenceList(input_file):
    try:
        full_text = readFile(input_file)
        sentence_list = segmentText(full_text)
        return sentence_list
    except OSError:
        print("Empty file")
