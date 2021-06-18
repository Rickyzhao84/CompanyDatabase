from flair.models import SequenceTagger

tagger = SequenceTagger.load('ner')

sentence = Sentence('Ricky went to Seattle today')

tagger.predict(sentence)

print(sentence.to_tagged_string())

for entity in sentence.get_spans('ner'):
    print(entity)