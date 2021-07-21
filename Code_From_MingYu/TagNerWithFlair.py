from io import TextIOWrapper
from typing import List, Sequence, Set, TextIO
from warnings import showwarning
import flair
from flair.models import SequenceTagger,TextClassifier
from flair.data import Sentence, Token
import json
import spacy
from spacy import tokens
from spacy.language import Language

from ColumnFormatFileUtils import ToColumnFileFormat
from KMP import KMP
from QueryResultReader import QueryResultReader, QueryAndResult


# declare global variables
_nerTagger : SequenceTagger = None
_spacyEnCoreModel : Language = None

def initialize():
    global _nerTagger
    global _spacyEnCoreModel

    print("initializing - load NER tagger")
    _nerTagger = SequenceTagger.load('flair/ner-english-ontonotes')
    print("initialization NER tagger - done")
    _spacyEnCoreModel = spacy.load('en_core_web_sm', exclude=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer", "ner"])
    _spacyEnCoreModel.add_pipe('sentencizer')

# find all the matched string, an set those tokens of mathced to new tag - tagOfMatch
def TagMatchedSubstring(ss : Sentence, nameToMatch: Sentence, tagOfMatch : str) :
    kmp = KMP()
    foundIndice = kmp.search(list(map(lambda t: t.text, ss.tokens)), list(map(lambda t: t.text, nameToMatch.tokens)))
    index = 0
    insideMatch = False
    currentMatchedTokens = 0
    for token in ss.tokens :
        if insideMatch:
            if currentMatchedTokens < len(nameToMatch.tokens) :
                token.set_label('ner', "I-"+tagOfMatch)
                currentMatchedTokens += 1
            else:
                insideMatch = False
                currentMatchedTokens = 0
        if not insideMatch:
            if index in foundIndice:
                insideMatch = True
                token.set_label('ner', "B-"+tagOfMatch)
                currentMatchedTokens = 1

        index += 1

# filter out not trustable tags
def FilterNerTags(ss : Sentence, nerTypesTrustbale : Set[str]):
    for token in ss.tokens :
        nerTag = token.get_tag('ner')
        if ((nerTag != None) and (nerTag != 'O') and (nerTag.value[2:] not in nerTypesTrustbale)):
            token.set_label('ner', 'O')

def ConvertFlairNerTagToBizQATag(flairNerTag : str) -> str:
    if len(flairNerTag) < 2:
        return flairNerTag

    prefix = flairNerTag[:2]
    tagStr = flairNerTag[2:]
    if prefix == "S-":
        prefix = "B-"
    else:
        if prefix == "E-":
            prefix = "I-"
    maptable = {
        'CARDINAL': 'Number',
        'DATE': 'DateTime',
        'GPE': 'Location',
        'LANGUAGE': 'Language',
        'MONEY': 'Currency',
        "ORDINAL": 'Number',
        "PERCENT": 'Number',
        "QUANTITY": 'Number',
        "TIME": 'DateTime',
    }
    if tagStr in maptable:
        tagStr = maptable[tagStr]
    
    return prefix+tagStr

def MapNerTags(sentence : Sentence) :
    for token in sentence.tokens:
        nerTag = token.get_tag('ner')
        if (nerTag != None and nerTag.value != None):
            newNerTag = ConvertFlairNerTagToBizQATag(nerTag.value)
            if (newNerTag != nerTag.value):
                token.set_label('ner', newNerTag)

def showmessage(msg : str) :
    print(msg)

def ProcessResultFile(inputFileName : str, resultFileName : str, nerTagForQuery : str):
    trustableFlairNerTypes : Set[str] = set(["CARDINAL", "DATE", "GPE", "LANGUAGE", "MONEY", "ORDINAL", "PERCENT", "QUANTITY", "TIME"])
    queryResultReader = QueryResultReader()
    writer = open(resultFileName, "w", encoding="utf-8")
    for queryResult in queryResultReader.LoadQueryResults(inputFileName):
        showmessage("processing query: " + queryResult.query)
        companyName = queryResult.query
        companyNameSentence = Sentence(companyName)
        resultSnippet : str
        for resultSnippet in queryResult.results:
            parsedSnippet = _spacyEnCoreModel(resultSnippet)
            sentenceText : str
            for sentenceText in list(parsedSnippet.sents):
                if companyName in sentenceText.sent.text:
                    sentence = Sentence(sentenceText.sent.text)
                    _nerTagger.predict(sentence)
                    FilterNerTags(sentence, trustableFlairNerTypes)
                    TagMatchedSubstring(sentence, companyNameSentence, nerTagForQuery)
                    MapNerTags(sentence)
                    taggedColumnStr = ToColumnFileFormat(sentence)
                    writer.write(taggedColumnStr)
                    writer.write("\n")
    writer.close()

if __name__ == "__main__":
    initialize()
    nerTag = 'Company'  #'Company'
    resultFile = r"largedatasetpart1.txt"
    taggedFile = "test.txt"
    ProcessResultFile(resultFile, taggedFile, nerTag)
