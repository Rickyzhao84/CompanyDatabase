from logging import currentframe
import spacy
from spacy.training import Corpus, corpus
from flair.datasets import ColumnDataset

nlp = spacy.load('en_core_web_sm', exclude=["tok2vec", "tagger", "parser", "lemmatizer", "ner", "transformer"])
nlp.add_pipe("sentencizer")

inputFile = open("CONLLData.txt", 'r', encoding='UTF8')
newFile = open("spacyFormat.txt", "w", encoding='UTF8')

sentence = ""
currentWord = ""
currentEntity = ""

# newFile.write(ColumnDataset(inputFile, ["word","label"]))

for line in inputFile:
    if line == "\n":
        entities = []
        print(sentence)
        startIndex = sentence.find(currentEntity.strip())
        print(currentEntity)
        print(startIndex)
        entities.append((startIndex, startIndex + len(currentEntity), currentWord))
        newFile.write("('" + sentence.strip() + ", {'entities': " + str(entities) + "}),")
        # newFile.write((sentence.strip(), {'entities': entities}))
        newFile.write("\n")
        sentence = ""
        currentEntity = ""

    else:
        specificLine = line.split("\t")
        sentence += specificLine[0]
        sentence += " "
        if (specificLine[1].strip() != "O"):
            secondSplit = specificLine[1].strip().split("-")
            if (secondSplit[0] == "I"):
                currentEntity += " "
            currentEntity += specificLine[0]
            currentWord = secondSplit[1]
        # if (specificLine[1].strip() == "B-Company"):
        #     currentCompany = specificLine[0]
        # if (specificLine[1].strip() == "I-Company"):
        #     currentCompany += " "
        #     currentCompany += specificLine[0]

newFile.close()
inputFile.close()