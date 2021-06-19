from flair.data import Sentence
from flair.models import SequenceTagger

bingQueryFile = open('bingqueryresultx.txt', 'r')

count = 0

for line in bingQueryFile:
    count+=1
    if (line[0:7] == "[Query]"):
        print(line.split(":")[1])


bingQueryFile.close()


    