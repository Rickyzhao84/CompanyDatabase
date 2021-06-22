from flair.data import Sentence
from flair.models import SequenceTagger

split_file = open('split_sentence.txt', 'r', encoding='UTF8')
newFile = open('data.txt', 'w', encoding='utf-8')

for line in split_file:
    sentence = Sentence(line)
    tagger = SequenceTagger.load('ner')
    tagger.predict(sentence)
    newFile.write(sentence.to_tagged_string())
    newFile.write("\n")