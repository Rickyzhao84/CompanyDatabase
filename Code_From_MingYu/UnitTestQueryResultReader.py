from typing import List
from QueryResultReader import QueryAndResult, QueryResultReader

def Test():
    reader = QueryResultReader()

    textLines : List[str] = list()
    textLines.append("[QUERY]:hello world")
    textLines.append("[RESPONSE]:")
    textLines.append("http://www.helloworld.com")
    textLines.append("title of hello world")
    textLines.append("snippit #1 of hello world: cool!")
    textLines.append("")
    textLines.append("http://www.helloworld2.com")
    textLines.append("title of hello world #2")
    textLines.append("snippit #2 of hello world: cool!")
    textLines.append("")
    resultItem = reader._convert_lines_to_QueryAndResults(textLines)
    assert(resultItem.query == "hello world")
    assert(len(resultItem.results) == 2)
    assert(resultItem.results[0] == "snippit #1 of hello world: cool!")
    assert(resultItem.results[1] == "snippit #2 of hello world: cool!")

    # insert empty line ahead not change the result
    textLines.insert(0, "")
    textLines.insert(0, "")
    resultItem2 = reader._convert_lines_to_QueryAndResults(textLines)
    assert(resultItem2.query == "hello world")
    assert(len(resultItem2.results) == 2)
    assert(resultItem2.results[0] == "snippit #1 of hello world: cool!")
    assert(resultItem2.results[1] == "snippit #2 of hello world: cool!")

    # format error: no marker of [QUERY]:
    textLines.clear()
    textLines.append("hello world")
    textLines.append("[RESPONSE]:")
    resultItem = reader._convert_lines_to_QueryAndResults(textLines)
    assert(resultItem == None)

    # format error: no marker of [RESPONSE]:
    textLines.clear()
    textLines.append("[QUERY]:hello world")
    textLines.append("data:")
    resultItem = reader._convert_lines_to_QueryAndResults(textLines)
    assert(resultItem == None)

# invoke testing
Test()
