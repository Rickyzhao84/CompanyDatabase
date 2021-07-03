from typing import List
from io import TextIOWrapper
from warnings import showwarning
import warnings

def IsEmptyString(line : str) -> bool :
    return line == '' or line.isspace()

class QueryAndResult :
    def __init__(self, query : str):
        self.query = query
        self.results : List[str] = list() # list of string result

    def AddResult(self, result : str):
        self.results.append(result)

class QueryResultReader :
    maxLinesPerRecord = 402 #Max 100 result per query
    def LoadQueryResults(self, fileName : str) -> List[QueryAndResult]:
        with open(fileName, "r", encoding='utf-8') as reader:
            while True:
                linesForResult, endOfFileMet = self._read_next_result_item(reader)
                resultItem = self._convert_lines_to_QueryAndResults(linesForResult)
                if resultItem != None:
                    yield resultItem
                if endOfFileMet == True:
                    break
        reader.close

    def _read_next_result_item(self, file : TextIOWrapper):
        linesForResultItem = []
        continuosuEmptyLines = 0
        line = file.readline()
        while line and line != '':
            lineRemovedCrlf = line.strip()
            if not IsEmptyString(lineRemovedCrlf):
                linesForResultItem.append(lineRemovedCrlf)
                continuosuEmptyLines = 0
            else:
                continuosuEmptyLines += 1
                # if sentence ends, break
                if len(linesForResultItem) > 0 and continuosuEmptyLines >= 2:
                    break
                else:
                    linesForResultItem.append(lineRemovedCrlf)
            if len(linesForResultItem) > self.maxLinesPerRecord:
                break

            line = file.readline()

        return linesForResultItem, (line == None or line == '')# indicate if file is reaching END

    def _convert_lines_to_QueryAndResults(self, lines : List[str]) -> QueryAndResult:
        # empty input will yield nothing
        if lines == None or len(lines) == 0 :
            return None

        # skip leading empty lines
        index = 0
        for line in lines:
            if IsEmptyString(line):
                index += 1
            else:
                break

        # this line has to be [QUERY]:
        queryLineMarker = '[QUERY]:'
        if (line.startswith(queryLineMarker)):
            query = line[len(queryLineMarker) : ]
        else:
            warnings.warn("bad data format, expect {0} not found".format(queryLineMarker))
            return None
        index += 1

        # skip an empty line
        index += 1

        # this line should be [RESPONSE]:
        line = lines[index]
        responseMarker = '[RESPONSE]:'
        if (not line.startswith(responseMarker)):
            warnings.warn("bad data format, expect {0} not found".format(responseMarker))
            return None
        index += 1

        queryAndResults = QueryAndResult(query)
        while True:
            # four lines as a response
            # skip   url line
            index += 1
            # skip   title line
            index += 1
            # get   snippet line
            if (index < len(lines)):
                queryAndResults.results.append(lines[index])
                index += 1
            else:
                break

            # this line should be an blank line
            if index >= len(lines):
                break
            else:
                if not IsEmptyString(lines[index]):
                    warnings.warn("format error, expect blank line, but met {0}".format(lines[index]))
                    break

            # skip empty line
            index += 1

        return queryAndResults

