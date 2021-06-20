from flair.data import Sentence
from flair.models import SequenceTagger
import spacy

nlp = spacy.load('en_core_web_sm')
bingQueryFile = open('bingqueryresultx.txt', 'r', encoding='UTF8')
newFile = open("data.txt", "w")

count = 0
textParagraphCount = 0

for line in bingQueryFile:
    count+=1
    if (textParagraphCount == 1):
        textParagraphCount += 1
        continue

    if (textParagraphCount == 2):
        textParagraphCount = 0
        sentence = Sentence(line)
        tagger = SequenceTagger.load('ner')
        tagger.predict(sentence)
        for entity in sentence.get_spans('ner'):
            doc = nlp(str(entity))
            for sent in doc.sents:
                newFile.write(str(sent))
        

    if ("[QUERY]" in line.strip('\n')):
        print(line.split(":")[1])
    if ("https://" in line.strip('\n')):
        textParagraphCount += 1


newFile.close()
bingQueryFile.close()


    