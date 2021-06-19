from flair.data import Sentence
from flair.models import SequenceTagger

bingQueryFile = open('bingqueryresultx.txt', 'r', encoding='UTF8')

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
        print(sentence)
        for entity in sentence.get_spans('ner'):
            print(entity)

    if ("[QUERY]" in line.strip('\n')):
        print(line.split(":")[1])
    if ("https://" in line.strip('\n')):
        textParagraphCount += 1



bingQueryFile.close()


    