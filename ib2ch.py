import sys
import htmlparser
from htmldocument import THTMLNode, THTMLDocument
from abstractparser import TPost, TAbstractParser

if len(sys.argv) <= 1:
    print("no args!")
    sys.exit(0)

print("Parsing file ", sys.argv[1])

f = open(sys.argv[1], "r", encoding="utf8")
lRawData = f.read()
lProcessedData = lRawData
f.close()

Doc = THTMLDocument()
htmlparser.Parse(lRawData, Doc, {})

def PrintRec(Node):
    S = "|"
    for i in range(Node.fDepth):
        S += "    "

    S += '[' + Node.fNodeType + ']'

    for a in Node.fAttributes:
        S += a + ':"' + Node.fAttributes[a] + '", '
    #print (Node.fAttributes)
    #for an, av in Node.fAttributes:
    #    SA = an + '"' + av + '"'
        #S += an + '"' + av + '"' + ', '

    S += 'Text:"' + Node.fText + '"'

    print(S)

    for N in Node.fChildNodes:
        PrintRec(N)
        
PrintRec(Doc.fRootNode)
