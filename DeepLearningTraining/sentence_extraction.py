from company_tagger import CompanyTagging
from logging import currentframe
from os import PathLike
from flair.data import Sentence
from flair.models import SequenceTagger
from datetime import datetime
from numpy.core.numeric import outer
import spacy

nlp = spacy.load('en_core_web_sm', exclude=["tok2vec", "tagger", "parser", "lemmatizer", "ner", "transformer"])
nlp.add_pipe("sentencizer")

class SentenceExtraction():

    def __init__(self, input_file: str, output_file: str):
        global company_tagger
        company_tagger = CompanyTagging(output_file)
        self.input_file = input_file
        self.output_file = output_file
    

    def get_sentence(self, input_file: str):
        bingQueryFile = open(input_file, 'r', encoding='UTF8')
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
                    if (currentCompany not in sent.text):
                        continue
                    company_tagger.tag_company_name(sent.text, currentCompany)

            if ("[QUERY]" in line.strip('\n')):
                companyName = line.split(":")[1]
                currentCompany = companyName.strip()
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print(current_time + ": processing " + companyName)

            if ("https://" in line.strip('\n')):
                textParagraphCount += 1
        bingQueryFile.close()
