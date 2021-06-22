from flair.data import Sentence
from flair.models import SequenceTagger
import spacy

nlp = spacy.load('en_core_web_sm')
bingQueryFile = open('bingqueryresultx.txt', 'r', encoding='UTF8')
newFile = open("data.txt", "w", encoding='utf-8')

count = 0
textParagraphCount = 0

for line in bingQueryFile:
    count+=1
    if (textParagraphCount == 1):
        textParagraphCount += 1
        continue

    if (textParagraphCount == 2):
        textParagraphCount = 0
        doc = nlp(line)
        for sent in doc.sents:
            # tagger = SequenceTagger.load('ner')
            # tagger.predict(sent)
            newFile.write(sent.text)
            newFile.write("\n")
        # sentence = Sentence(line)
        # tagger = SequenceTagger.load('ner')
        # tagger.predict(sentence)
        # for entity in sentence.get_spans('ner'):
        #     doc = nlp(str(entity))
        #     for sent in doc.sents:
        #         print(sent.text)
        

    if ("[QUERY]" in line.strip('\n')):
        newFile.write(line.split(":")[1])
        newFile.write("\n")
    if ("https://" in line.strip('\n')):
        textParagraphCount += 1


newFile.close()
bingQueryFile.close()


    