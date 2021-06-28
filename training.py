from logging import currentframe
from flair.data import Sentence
from flair.models import SequenceTagger
import spacy

nlp = spacy.load('en_core_web_sm', exclude=["tok2vec", "tagger", "parser", "lemmatizer", "ner", "transformer"])
nlp.add_pipe("sentencizer")
bingQueryFile = open('bingqueryresultx.txt', 'r', encoding='UTF8')
newFile = open("split_sentence.txt", "w", encoding='utf-8')
tagger = SequenceTagger.load('ner')

count = 0
textParagraphCount = 0
currentCompany = ""

for line in bingQueryFile:
    count+=1
    if (textParagraphCount == 1):
        textParagraphCount += 1
        continue

    if (textParagraphCount == 2):
        textParagraphCount = 0
        doc = nlp(line)
        for sent in doc.sents:
            # print(sent.text)
            # newFile.write(sent.text)
            # newFile.write("\n")
            sent = Sentence(sent.text)
            tagger.predict(sent)
            for token in sent.tokens:
                if (token.text in currentCompany):
                    print(token.text + "\t")
                    newFile.write(token.text)
                    newFile.write("\n")
                    token.add_tag("Organization", "I-Company")
                    newFile.write(token.get_tag("Organization").value)
                    newFile.write("\n")
                
                    print(token.get_tag("Organization").value)
                else:
                    print(token.text + "\t")
                    print(token.get_tag('ner').value)
                    newFile.write(token.text + "\t")
                    newFile.write("\n")
                    newFile.write(token.get_tag('ner').value)
                    newFile.write("\n")

    if ("[QUERY]" in line.strip('\n')):
        companyName = line.split(":")[1]
        currentCompany = companyName
        # newFile.write(companyName)
        # newFile.write("\n")
    if ("https://" in line.strip('\n')):
        textParagraphCount += 1


newFile.close()
bingQueryFile.close()


    