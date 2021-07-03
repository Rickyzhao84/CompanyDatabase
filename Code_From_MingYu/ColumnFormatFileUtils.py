from io import TextIOWrapper
from typing import List
from flair.data import Sentence
from flair.datasets import ColumnDataset

def ToColumnFileFormat(ss : Sentence) -> str :
    columnStr = ''
    for token in ss.tokens :
        nerTag = token.get_tag('ner')
        columnStr += token.text + '\t' + (nerTag.value if (nerTag != None) else 'O')
        columnStr += '\n'
    return columnStr

def LoadColumnDataset(fileName : str, textColIdx : int = 0, nerColIdx : int = 1) -> ColumnDataset :
    columnNampMapping = {textColIdx: "text", nerColIdx: "ner"}
    return ColumnDataset(fileName, columnNampMapping, column_delimiter='\t', tag_to_bioes="ner")

def GetLabelForTokensOfSentence(sentence : Sentence, tag_type : str = "ner") :
    return list(map(lambda t: t.get_tag(tag_type).value, sentence.tokens))

def SaveSentenceToFile(writer : TextIOWrapper, sentence : Sentence) :
    writer.write(ToColumnFileFormat(sentence))
    writer.write('\n')
    return

def SaveSentencesToFile(writer : TextIOWrapper, sentences : List[Sentence]) :
    for sentence in sentences :
        SaveSentenceToFile(writer, sentence)
    return

def SaveSentencesToFile2(fileName : str, sentences : List[Sentence]) :
    writer = open(fileName, "w", encoding="utf-8")
    SaveSentencesToFile(writer, sentences)
    writer.close()
    return

