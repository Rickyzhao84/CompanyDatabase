from flair.data import Sentence
from flair.models import SequenceTagger

split_file = open('split_sentence.txt', 'r', encoding='UTF8')
newFile = open('data.txt', 'w', encoding='utf-8')

tagger = SequenceTagger.load('ner')

for line in split_file:
    sentence = Sentence(line)
    tagger.predict(sentence)
    for entity in sentence.get_spans('ner'):
        print(entity)
    newFile.write(sentence.to_tagged_string())

    newFile.write("\n")