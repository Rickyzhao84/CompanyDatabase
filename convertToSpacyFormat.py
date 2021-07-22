import spacy
from spacy.training import Corpus, corpus
nlp = spacy.load('en_core_web_sm', exclude=["tok2vec", "tagger", "parser", "lemmatizer", "ner", "transformer"])
nlp.add_pipe("sentencizer")

inputFile = open("MingYusTagging.txt", 'r', encoding='UTF8')
newFile = open("spacyFormat.txt", "w", encoding='UTF8')

sentence = ""
TRAIN_DATA = []
currentCompany = ""

for line in inputFile:
    if line == "\n":
        entities = []
        startIndex = sentence.find(currentCompany.strip())
        entities.append((startIndex - 1, startIndex + len(currentCompany) - 1, 'Company'))
        TRAIN_DATA.append((sentence.strip(), {'entities': entities}))
        sentence = ""
        currentCompany = ""

    else:
        specificLine = line.split("\t")
        sentence += " "
        sentence += specificLine[0]
        if (specificLine[1].strip() == "B-Company"):
            currentCompany = specificLine[0]
        if (specificLine[1].strip() == "I-Company"):
            currentCompany += " "
            currentCompany += specificLine[0]

newFile.write(str(TRAIN_DATA))