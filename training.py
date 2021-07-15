from typing import Sequence
from flair.data import Corpus
from flair.datasets import UD_ENGLISH
from flair.datasets import ColumnCorpus
from flair.data import Sentence
from flair.embeddings import CharacterEmbeddings, FlairEmbeddings, TokenEmbeddings, WordEmbeddings, StackedEmbeddings

#get corpus
# corpus: Corpus = UD_ENGLISH().downsample(0.1)
columnFormat = {0 : 'test', 1: 'ner'}
corpus: ColumnCorpus = ColumnCorpus('datasets', columnFormat)
print(corpus)

tag_type = 'ner'

tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)
print(tag_dictionary)

embedding_types = [

    WordEmbeddings('glove'),

    # comment in this line to use character embeddings
    CharacterEmbeddings(),

    # comment in these lines to use flair embeddings
    FlairEmbeddings('news-forward', chars_per_chunk = 128),
    FlairEmbeddings('news-backward', chars_per_chunk= 128),
]

embeddings: StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)

#initialize sequence tagger
from flair.models import SequenceTagger

tagger: SequenceTagger = SequenceTagger(hidden_size=128,
                                        embeddings=embeddings,
                                        tag_dictionary=tag_dictionary,
                                        tag_type=tag_type,
                                        use_crf=True)

#initialize trainer
from flair.trainers import ModelTrainer

trainer: ModelTrainer = ModelTrainer(tagger, corpus)

#start training
trainer.train('resources/taggers/example-pos',
              learning_rate=0.1,
              mini_batch_size=32,
              max_epochs= 5)

# load model trained
model = SequenceTagger.load('resources/taggers/example-pos/final-model.pt')

# sentence = Sentence('Starbucks in a big company located in Seattle Washington')

# # predict tags and print
# model.predict(sentence)

# print(sentence.to_tagged_string())