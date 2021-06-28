from flair.data import Sentence
from flair.models import SequenceTagger

split_file = open('split_sentence.txt', 'r', encoding='UTF8')
newFile = open('data.txt', 'w', encoding='utf-8')

tagger = SequenceTagger.load('ner')

for line in split_file:
    sentence = Sentence(line)
    tagger.predict(sentence)
    for token in sentence.tokens:
        print(token.text + "\t")
        print(token.get_tag('ner').value)
    # for entity in sentence.get_spans('ner'):
    #     print(entity.text + " " + entity.tag)
    #     newFile.write(entity.text + " " + entity.tag)
    #     newFile.write("\n")