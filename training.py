from logging import currentframe
from flair.data import Sentence
from flair.models import SequenceTagger
from datetime import datetime
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

                    newFile.write(token.text)
                    newFile.write("\t")
                    token.add_tag("Organization", "B-Company")
                    newFile.write(token.get_tag("Organization").value)
                    newFile.write("\n")
                    #If company is one word, it is B
                    #If company is several, B-I-I-I until end of comp name
                else:

                    newFile.write(token.text)
                    newFile.write("\t")
                    newFile.write(token.get_tag('ner').value)
                    newFile.write("\n")

    if ("[QUERY]" in line.strip('\n')):
        companyName = line.split(":")[1]
        currentCompany = companyName
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(current_time + ": processing " + companyName)
        # newFile.write(companyName)
        # newFile.write("\n")
    if ("https://" in line.strip('\n')):
        textParagraphCount += 1


newFile.close()
bingQueryFile.close()


    