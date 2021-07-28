import spacy
from spacy.training import Corpus, corpus
from flair.datasets import ColumnDataset

# nlp = spacy.load('en_core_web_sm', exclude=["tok2vec", "tagger", "parser", "lemmatizer", "ner", "transformer"])
# nlp.add_pipe("sentencizer")

inputFile = "CONLLData.txt"
newFile = open("spacyFormat.txt", "w", encoding='UTF8')

sentence = ""
currentWord = ""
currentEntity = ""

mydataset = ColumnDataset(inputFile, {0: "text", 1: "ner"})
newFile.write("[")
for ss in mydataset.sentences:
    entities = []
    for entity in ss.get_spans('ner'):
        startIndex = ss.to_original_text().find(entity.text)
        entities.append((startIndex, startIndex + len(entity.text), "\'" + entity.tag + "\'"))
    newFile.write("(\'" + ss.to_original_text().replace('\'', '') + "\', {\"entities\": " + str(entities) + "}),")
    newFile.write("\n")
newFile.write("]")




# newFile.write(ColumnDataset(inputFile, columns))



# for line in inputFile:
#     if line == "\n":
#         print(sentence)
#         startIndex = sentence.find(currentEntity.strip())
#         print(currentEntity)
#         print(startIndex)
#         entities.append((startIndex, startIndex + len(currentEntity), currentWord))
#         newFile.write("('" + sentence.strip() + ", {'entities': " + str(entities) + "}),")
#         # newFile.write((sentence.strip(), {'entities': entities}))
#         newFile.write("\n")
#         sentence = ""
#         currentEntity = ""
#         entities = []
#         break

#     else:
#         specificLine = line.split("\t")
#         sentence += specificLine[0]
#         sentence += " "
#         if (specificLine[1].strip() != "O"):
#             secondSplit = specificLine[1].strip().split("-")
#             if (secondSplit[0] == "I"):
#                 currentEntity += " "
#             currentEntity += specificLine[0]
#             currentWord = secondSplit[1]
#         # if (specificLine[1].strip() == "B-Company"):
#         #     currentCompany = specificLine[0]
#         # if (specificLine[1].strip() == "I-Company"):
#         #     currentCompany += " "
#         #     currentCompany += specificLine[0]

# newFile.close()
# inputFile.close()