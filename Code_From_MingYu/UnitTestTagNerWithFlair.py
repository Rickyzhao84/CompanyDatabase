from typing import Set
import flair
from flair.data import Sentence, Token
from spacy import tokens
from TagNerWithFlair import TagMatchedSubstring, FilterNerTags, ConvertFlairNerTagToBizQATag
from ColumnFormatFileUtils import ToColumnFileFormat

def PrepareTestSentence() -> Sentence:
    sentence = Sentence("Microsoft headquater is at Redmond, WA, founded at 1975.")
    sentence.tokens[0].set_label('ner', 'O')
    sentence.tokens[1].set_label('ner', 'O')
    sentence.tokens[2].set_label('ner', 'O')
    sentence.tokens[3].set_label('ner', 'O')
    sentence.tokens[4].set_label('ner', 'B-GPE')
    sentence.tokens[5].set_label('ner', 'O')
    sentence.tokens[6].set_label('ner', 'B-GPE')
    sentence.tokens[7].set_label('ner', 'O')
    sentence.tokens[8].set_label('ner', 'O')
    sentence.tokens[9].set_label('ner', 'O')
    sentence.tokens[10].set_label('ner', 'B-TIME')
    sentence.tokens[11].set_label('ner', 'O')
    return sentence

def TestTagMatchedSubstring():
    sentence = PrepareTestSentence()
    company = Sentence("Microsoft")
    trustableFlairNerTypes : Set[str]= set(["CARDINAL", "DATE", "LANGUAGE", "MONEY", "ORDINAL", "PERCENT", "QUANTITY", "TIME"])
    TagMatchedSubstring(sentence, company, "Company")
    assert(sentence.tokens[0].get_tag('ner').value == 'B-Company')
    assert(sentence.tokens[1].get_tag('ner').value == 'O')
    FilterNerTags(sentence, trustableFlairNerTypes)
    assert(sentence.tokens[1].get_tag('ner').value == 'O') # no change
    assert(sentence.tokens[5].get_tag('ner').value == 'O') # no change
    assert(sentence.tokens[6].get_tag('ner').value == 'O') # change to 'O'
    assert(sentence.tokens[10].get_tag('ner').value == 'B-TIME') # no change
    
    # change sentence to: Microsoft Corp headquater is at Redmond, WA, founded at 1975.
    # change company to: Microsoft Corp
    sentence.tokens.insert(1, Token("Corp"))  # token 1
    sentence.tokens[1].set_label('ner', 'O')
    company.tokens.append(Token('Corp'))
    TagMatchedSubstring(sentence, company, "COMPANY")
    assert(sentence.tokens[0].get_tag('ner').value == 'B-COMPANY')
    assert(sentence.tokens[1].get_tag('ner').value == 'I-COMPANY')

    # multiple match of company name
    sentence.tokens.append(Token("The"))  #token 13
    sentence.tokens.append(Token("great")) # token 14
    sentence.tokens.append(Token("Microsoft"))
    sentence.tokens.append(Token("Corp"))
    sentence.tokens.append(Token("rocks"))
    sentence.tokens.append(Token("."))
    TagMatchedSubstring(sentence, company, "COM")
    assert(sentence.tokens[0].get_tag('ner').value == 'B-COM')
    assert(sentence.tokens[1].get_tag('ner').value == 'I-COM')
    assert(sentence.tokens[15].get_tag('ner').value == 'B-COM')
    assert(sentence.tokens[16].get_tag('ner').value == 'I-COM')

def TestColumnStrFormater():
    ss = PrepareTestSentence()
    str = ToColumnFileFormat(ss)
    lines = str.split('\n')
    assert(len(lines) == len(ss.tokens) + 1) # work around for the trailing empty line
    assert(lines[0] == "Microsoft\tO")
    assert(lines[1] == "headquater\tO")

def TestTagConversion():
    flairTag = 'O'
    assert("O" == ConvertFlairNerTagToBizQATag(flairTag))

    flairTag = 'S-GPE'
    assert("B-Location" == ConvertFlairNerTagToBizQATag(flairTag))

    flairTag = 'E-DATE'
    assert("I-DateTime" == ConvertFlairNerTagToBizQATag(flairTag))

    flairTag = 'B-QUANTITY'
    assert("B-Number" == ConvertFlairNerTagToBizQATag(flairTag))

    flairTag = 'I-PERCENT'
    assert("I-Number" == ConvertFlairNerTagToBizQATag(flairTag))

    flairTag = 'B-Company'
    assert("B-Company" == ConvertFlairNerTagToBizQATag(flairTag))

    flairTag = 'I-Company'
    assert("I-Company" == ConvertFlairNerTagToBizQATag(flairTag))

runtest = True

if  runtest :
    TestTagConversion()
    TestColumnStrFormater()
    TestTagMatchedSubstring()
