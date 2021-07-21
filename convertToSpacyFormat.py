import spacy
from spacy.training import Corpus, corpus
nlp = spacy.load('en_core_web_sm')
gc = Corpus("backup_data_dev")
for doc, gold in gc.dev_docs(nlp, gold_preproc=True):
    doc.ents = spacy.training.spans_from_biluo_tags(doc, gold.ner)
    spacy.displacy.serve(doc, style='ent')