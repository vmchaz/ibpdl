import sys
import htmlparser
from htmldocument import THTMLNode, THTMLDocument
from abstractparser import TPost, TAbstractParser
from httpclient import execute_http_request

if len(sys.argv) <= 2:
    print("not enough args!")
    sys.exit(0)
    
    
print("Saving URL ", sys.argv[1], "to file", sys.argv[2])
lRawData = execute_http_request(sys.argv[1], "utf-8")
    
f = open(sys.argv[2], "w", encoding="utf8")
f.write(lRawData)
f.close()

