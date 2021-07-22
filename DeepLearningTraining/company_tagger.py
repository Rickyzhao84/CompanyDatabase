from flair.data import Sentence
from flair.models import SequenceTagger

class CompanyTagging():

    def __init__(self, output_file):
        global tagger
        global newFile
        newFile = open(output_file, "w", encoding='utf-8')
        tagger = SequenceTagger.load('ner')
        
    
    def tag_company_name(self, sent: str, currentCompany: str):
        sent = Sentence(sent)
        tagger.predict(sent)
            
        for token in sent.tokens:
            if (token.text in currentCompany):
                partsOfCurrentCompany = currentCompany.split(" ")
                newFile.write(token.text)
                newFile.write("\t")
                if (token.text == partsOfCurrentCompany[0]):
                    token.add_tag("Organization", "B-Company")
                else:
                    for eachWord in partsOfCurrentCompany:
                        if (token.text == eachWord):
                            token.add_tag("Organization", "I-Company")
                newFile.write(token.get_tag("Organization").value)
                newFile.write("\n")
            else:
                newFile.write(token.text)
                newFile.write("\t")
                newFile.write(token.get_tag('ner').value)
                newFile.write("\n")
        newFile.write("\n")
