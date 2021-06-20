import spacy

nlp = spacy.load('en_core_web_sm')

string1 = "This is the first sentence. This is the second sentence. This is the third sentence."

doc = nlp(string1)

for sent in doc.sents:
    print(sent)