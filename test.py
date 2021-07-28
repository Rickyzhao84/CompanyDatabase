import spacy
from spacy.training import Corpus, corpus
from flair.datasets import ColumnDataset

nlp = spacy.load('en_core_web_sm', exclude=["tok2vec", "tagger", "parser", "lemmatizer", "ner", "transformer"])
nlp.add_pipe("sentencizer")

inputFile = open("CONLLData.txt", 'r', encoding='UTF8')
newFile = open("spacyFormat.txt", "w", encoding='UTF8')

index = 0
sentence = ""
currentTaggedWord = ""
currentEntity = ""
entities = []

for line in inputFile:
    if line == "\n":
        newFile.write("('" + sentence.strip() + ", {'entities': " + str(entities) + "}),")
        newFile.write("\n")
        sentence = ""
        currentEntity = ""
        entities = []
        index = 0
    else:
        getWordAndTag = line.split("\t")
        word = getWordAndTag[0].strip()
        tag = getWordAndTag[1].strip()
        sentence += word
        sentence += " "
        endIndex = index + len(word)
        if (tag.strip() != "O"):
            getEntity = tag.strip().split("-")
            if (getEntity[0] == "I"):
                currentTaggedWord += " "
                continue
            currentEntity = getEntity[1]
            currentTaggedWord += word
            entities.append((index, endIndex, currentEntity))
        index = endIndex
