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
# l1=[]
# l2=[]
#make class 
for line in bingQueryFile:
    count+=1
    if (textParagraphCount == 1):
        textParagraphCount += 1
        continue

    if (textParagraphCount == 2):
        textParagraphCount = 0
        doc = nlp(line)
        for sent in doc.sents:
            if (currentCompany not in sent.text):
                continue
         
            sent = Sentence(sent.text)
            tagger.predict(sent)
            # l1.append(sent)
            
            for token in sent.tokens:
                if (token.text in currentCompany):
                    partsOfCurrentCompany = currentCompany.split(" ")
                    newFile.write(token.text)
                    newFile.write("\t")
                    if (token.text != partsOfCurrentCompany[0]):
                        token.add_tag("Organization", "I-Company")
                    else: 
                        token.add_tag("Organization", "B-Company")
                    newFile.write(token.get_tag("Organization").value)
                    # l2.append(token.get_tag("Organization").value)
                    newFile.write("\n")
                else:
                    newFile.write(token.text)
                    newFile.write("\t")
                    newFile.write(token.get_tag('ner').value)
                    # l2.append(token.get_tag('ner').value)
                    newFile.write("\n")
            train_data = list(zip(l1, l2))
            print(train_data)

    if ("[QUERY]" in line.strip('\n')):
        companyName = line.split(":")[1]
        currentCompany = companyName.strip()
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(current_time + ": processing " + companyName)

    if ("https://" in line.strip('\n')):
        textParagraphCount += 1


newFile.close()
bingQueryFile.close()